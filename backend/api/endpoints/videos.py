import os
import re
import subprocess
from fastapi import APIRouter, HTTPException, Request
from pathlib import Path
from fastapi import FastAPI, Request, Response, Header, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

router = APIRouter()

VIDEO_DIR = "./videos"
THUMBNAIL_DIR = "./thumbnails"

# Ensure the thumbnails directory exists
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

def generate_thumbnail(video_path: str, thumbnail_path: str):
    """
    Generate a thumbnail from the first frame of a video using ffmpeg.
    This command grabs a frame at 1 second into the video.
    """

    print("generating thumbnail")
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ss", "00:00:00.000",
        "-vframes", "1",
        thumbnail_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail for {video_path}: {e}")

@router.get("/video-list")
async def list_videos():
    """
    Returns a JSON list of videos with their names and thumbnail URLs.
    Each video object contains:
      - name: the file name of the video
      - thumbnail: the URL endpoint to fetch the video’s thumbnail image
    """
    if not os.path.exists(VIDEO_DIR):
        return JSONResponse(content={"videos": []}, status_code=200)

    videos = []
    for filename in os.listdir(VIDEO_DIR):
        if filename.lower().endswith((".mp4", ".mov")):
            video_path = os.path.join(VIDEO_DIR, filename)
            # Thumbnail filename uses the same basename but with a .jpg extension
            thumbnail_filename = os.path.splitext(filename)[0] + ".jpg"
            thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
            # Generate thumbnail if it doesn't exist
            if not os.path.exists(thumbnail_path):
                generate_thumbnail(video_path, thumbnail_path)
            videos.append({
                "name": filename,
                "thumbnail": f"/thumbnail/{filename}"
            })

    return {"videos": videos}


CHUNK_SIZE = 1024 * 1024  # 1 MB chunk size

CHUNK_SIZE = 1024 * 1024  # 1 MB chunks

@router.get("/video/{video_name}")
async def stream_video(video_name: str, request: Request):
    video_path = os.path.join("videos", video_name)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_size = os.path.getsize(video_path)
    range_header = request.headers.get("range")
    
    if range_header is None:
        # No Range header; return the full content
        def iterfile():
            with open(video_path, "rb") as video:
                yield from video
        return StreamingResponse(iterfile(), media_type="video/mp4")
    
    # Parse the Range header (e.g., "bytes=0-1023")
    range_match = re.search(r"bytes=(\d+)-(\d*)", range_header)
    if range_match:
        byte1, byte2 = range_match.groups()
        byte1 = int(byte1)
        byte2 = int(byte2) if byte2 else file_size - 1
    else:
        # If the Range header is invalid, send the full file
        def iterfile():
            with open(video_path, "rb") as video:
                yield from video
        return StreamingResponse(iterfile(), media_type="video/mp4")
    
    # Ensure byte2 doesn't exceed the file size
    byte2 = min(byte2, file_size - 1)
    length = byte2 - byte1 + 1
    
    def iterfile():
        with open(video_path, "rb") as video:
            video.seek(byte1)
            remaining = length
            while remaining > 0:
                chunk_size = min(4096, remaining)
                data = video.read(chunk_size)
                if not data:
                    break
                yield data
                remaining -= len(data)
    
    headers = {
        "Content-Range": f"bytes {byte1}-{byte2}/{file_size}",
        "Accept-Ranges": "bytes",
    }
    
    return StreamingResponse(iterfile(), status_code=206, headers=headers, media_type="video/mp4")


@router.get("/thumbnail/{video_name}")
async def get_thumbnail(video_name: str):
    """
    Returns the thumbnail image corresponding to the given video name.
    """
    thumbnail_filename = os.path.splitext(video_name)[0] + ".jpg"
    thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
    if not os.path.exists(thumbnail_path):
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(thumbnail_path, media_type="image/jpeg")
