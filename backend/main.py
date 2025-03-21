from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import root, logs, iot
from core.mqtt_client import MQTTManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(root.router)
app.include_router(logs.router, prefix="/api")
# app.include_router(iot.router)

# Create a global MQTTManager instance and start it
mqtt_manager = MQTTManager()
mqtt_manager.start()




@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}