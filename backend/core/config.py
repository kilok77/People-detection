import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    CV_MODE = os.getenv("CV_MODE", 0)
    