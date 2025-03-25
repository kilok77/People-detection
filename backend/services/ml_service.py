import cv2
import asyncio
import time
import os
import csv
from ultralytics import YOLO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

# -------------------------------
# Setup Functions
# -------------------------------

def setup_model(model_path="yolo11m.pt", imgsz=320):
    model = YOLO(model_path)
    model.fuse()
    model.overrides["imgsz"] = imgsz
    return model

def setup_video_capture(video_path):
    cap = cv2.VideoCapture(0 if video_path == "0" else video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video source: {video_path}")
    cv2.setNumThreads(4)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    return cap, fps

# -------------------------------
# Global Setup
# -------------------------------

model = setup_model()
# video_path = "video1.mp4"
video_path = "0"
cap, video_fps = setup_video_capture(video_path)
router = APIRouter()

CSV_DIR = "./csv"
CSV_FILE = os.path.join(CSV_DIR, "detections.csv")
os.makedirs(CSV_DIR, exist_ok=True)
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp","video_id", "frame_number", "x1", "y1", "x2", "y2"])

# -------------------------------
# Processing Functions
# -------------------------------

def get_detections(results):
    detections = []
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            if int(cls) == 0:
                x1, y1, x2, y2 = map(int, box[:4])
                detections.append((x1, y1, x2, y2))
    return detections

def draw_boxes(frame, detections):
    for x1, y1, x2, y2 in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def save_detections_to_csv(timestamp, video_id,  frame_number, detections):
    rows = [[timestamp, video_id, frame_number, x1, y1, x2, y2] for x1, y1, x2, y2 in detections]
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

async def process_frame(frame, model, timestamp, frame_number, video_id):
    results = await asyncio.to_thread(model, frame)
    detections = get_detections(results)
    if detections:
        save_detections_to_csv(timestamp, video_id, frame_number, detections)
    frame = draw_boxes(frame, detections)
    return frame

# -------------------------------
# Frame Generator
# -------------------------------

async def generate_frames():
    global current_video_id
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    current_video_id = f"video_{int(time.time())}"
    output_video_path = f"./videos/{current_video_id}.mp4"
    video_writer = cv2.VideoWriter(output_video_path, fourcc, video_fps, (frame_width, frame_height))

    frame_number = 0
    try:
        while True:
            success, frame = cap.read()
            if not success:
                if video_path != "0":
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frame_number = 0
                    continue
                else:
                    break

            timestamp = int(time.time())
            processed_frame = await process_frame(frame, model, timestamp, frame_number, current_video_id)

            video_writer.write(processed_frame)

            success_enc, buffer = cv2.imencode('.jpg', processed_frame)
            if not success_enc:
                continue
            frame_bytes = buffer.tobytes()

            frame_number += 1

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
            )
    finally:
        video_writer.release()


# -------------------------------
# FastAPI Endpoint
# -------------------------------

@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )