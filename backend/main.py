from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import root
from services import ml_service  # Import the service
from services import camera  # Import the service
from fastapi.staticfiles import StaticFiles
from api.endpoints.videos import router as videos_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(root.router)

# Include the ML service endpoints
app.include_router(ml_service.router)

app.include_router(camera.router)

app.include_router(videos_router, prefix="/api", tags=["Videos"])


# Mount the static directory
# app.mount("/api/video", StaticFiles(directory="videos"), name="videos")


@app.get("/")
def root():
    return {"message": "MJPEG Streaming with FastAPI"}