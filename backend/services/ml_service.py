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
video_path = "video1.mp4"
video_path = "0"
cap, video_fps = setup_video_capture(video_path)
router = APIRouter()

print("Video FPS:", video_fps)

DETECTION_DIR = "detections"
os.makedirs(DETECTION_DIR, exist_ok=True)
CSV_FILE = "detections.csv"

if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "image_path", "x1", "y1", "x2", "y2"])


# -------------------------------
# Processing Functions
# -------------------------------

def draw_detections(frame, results, timestamp):
    detections_exist = False
    rows_to_save = []
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            if int(cls) == 0:
                detections_exist = True
                x1, y1, x2, y2 = map(int, box[:4])
                rows_to_save.append([timestamp, "", x1, y1, x2, y2])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if detections_exist:
        image_filename = f"frame_{timestamp}.jpg"
        image_path = os.path.join(DETECTION_DIR, image_filename)
        cv2.imwrite(image_path, frame)
        # Update CSV rows with correct image paths
        for row in rows_to_save:
            row[1] = image_path

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows_to_save)

    return frame


async def process_frame(frame, model, timestamp):
    results = await asyncio.to_thread(model, frame)
    frame = draw_detections(frame, results, timestamp)
    return frame

# -------------------------------
# Frame Generator
# -------------------------------

async def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            if video_path != "0":
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break

        timestamp = int(time.time())
        processed_frame = await process_frame(frame, model, timestamp)

        success_enc, buffer = cv2.imencode('.jpg', processed_frame)
        if not success_enc:
            continue
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )

# -------------------------------
# FastAPI Endpoint
# -------------------------------

@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
