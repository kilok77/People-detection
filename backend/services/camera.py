import cv2
import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

def mjpeg_generator():
    
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Encode the frame in JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            print("generating")
            # Prepare the MJPEG frame. The boundary "frame" is arbitrary.
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                jpeg.tobytes() +
                b'\r\n'
            )
    except GeneratorExit:
        # This exception is raised when the client disconnects.
        print("Client disconnected.")
    finally:
        cap.release()

@router.get("/mjpeg")
async def mjpeg_stream():
    # Set the media type to 'multipart/x-mixed-replace' with a boundary.
    return StreamingResponse(
        mjpeg_generator(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
