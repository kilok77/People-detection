import cv2
import asyncio
from ultralytics import YOLO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Or "yolov8s.pt" for better accuracy

# Open video or webcam (0 for webcam, or replace with a file path)
video_path = "./face_recogniction_video.mov"
cap = cv2.VideoCapture(video_path)

async def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLOv8 detection
        results = model(frame)

        # Draw bounding boxes
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        await asyncio.sleep(0.03)  # Prevents CPU overload (adjust as needed)

@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
