from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import root
from services import ml_service  # Import the service
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(root.router)
# app.include_router(iot.router)

# Include the ML service endpoints
app.include_router(ml_service.router)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "MJPEG Streaming with FastAPI"}