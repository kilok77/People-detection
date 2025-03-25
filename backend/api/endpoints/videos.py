import os
import subprocess
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

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
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ss", "00:00:01.000",
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

@router.get("/video/{video_name}")
async def get_video(video_name: str):
    """
    Returns the video file for a given video name.
    """
    video_path = os.path.join(VIDEO_DIR, video_name)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    # Adjust media_type if necessary (e.g. "video/quicktime" for .mov files)
    return FileResponse(video_path, media_type="video/mp4")

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
