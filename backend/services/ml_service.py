import cv2
import asyncio
import time
from ultralytics import YOLO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter()

# -------------------------------
# Setup Functions
# -------------------------------

def setup_model(model_path="yolov8s.pt", imgsz=320):
    """
    Load the YOLO model, fuse layers, and override the input image size.
    """
    model = YOLO(model_path)
    model.fuse()  # Fuse layers for faster inference
    model.overrides["imgsz"] = imgsz  # Set a smaller input size for faster processing
    return model

def setup_video_capture(video_path):
    """
    Initialize video capture and configure OpenCV parameters.
    Returns the capture object and video FPS.
    """
    if video_path == "0":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open video source: {video_path}")
        raise ValueError(f"Video source {video_path} is not available.")
    cv2.setNumThreads(4)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if not available
    return cap, fps

# -------------------------------
# Processing Functions
# -------------------------------

def draw_detections(frame, results):
    """
    Draw bounding boxes on the frame for 'person' detections (class id 0).
    """
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            if int(cls) == 0:
                x1, y1, x2, y2 = map(int, box[:4])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def overlay_fps(frame, fps_value):
    """
    Overlay the FPS counter on the frame (top-left corner).
    """
    cv2.putText(
        frame,
        f"FPS: {fps_value:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    return frame

async def process_frame(frame, model):
    """
    Run the model inference asynchronously and draw detections.
    """
    results = await asyncio.to_thread(model, frame)
    frame = draw_detections(frame, results)
    return frame

# -------------------------------
# Global Setup
# -------------------------------

model = setup_model()
# video_path = "./face_recogniction_video.mov"
# video_path = "0"
video_path = "video1.mp4"
cap, video_fps = setup_video_capture(video_path)
frame_duration = 1 / video_fps  # Duration per frame in seconds

# -------------------------------
# Frame Generator
# -------------------------------

async def generate_frames():
    prev_time = time.time()
    
    while True:
        success, frame = cap.read()
        if not success:
            # If the source is a video file, restart from the beginning.
            if video_path != "0":
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break
        
        start_time = time.monotonic()
       
        # Process frame (inference + drawing detections)
        processed_frame = await process_frame(frame, model)
        
        # Calculate FPS based on time between frames
        current_time = time.time()
        calculated_fps = 1.0 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        
        # Overlay FPS counter on the frame
        processed_frame = overlay_fps(processed_frame, calculated_fps)
        
        # Encode frame as JPEG
        success_enc, buffer = cv2.imencode('.jpg', processed_frame)
        if not success_enc:
            continue
        frame_bytes = buffer.tobytes()
        
        elapsed = time.monotonic() - start_time
        delay = frame_duration - elapsed
        if delay > 0:
            await asyncio.sleep(delay)
        
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
