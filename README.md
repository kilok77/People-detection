# People Detection

This project uses computer vision techniques to locate and track people in video streams. The FastAPI backend handles detection with OpenCV and YOLOv11, while a simple React frontend displays the results. The application is containerized with Docker for easy setup and deployment.

## Current State

Currently, Docker is running, but it’s not as fast as I’d like, and I’m having trouble optimizing it for machine learning tasks. The people detection algorithm is functioning, yet it sometimes creates two bounding boxes around a single person when there’s a lot of movement. Also frames are saved to a video but the framerate is not in sync. Additionally, in the provided video, the second person is not always detected, resulting in gaps, which could be addressed using SORT algorithms. The backend produces an MJPEG stream accessible through the React page, but when switching routes from the live view to the video list view, the HTTP connection does not stop. I’ve tried for a while to fix and stop it, but I’m currently unsure how to proceed.

- **Configurable Source**: Easily switch between live camera feeds or file-based inputs via environment variables.
- **CSV Metadata**: All detection data is recorded in CSV files for easy analysis.
- **MP4 Recordings**: Videos are saved as MP4 files, enabling straightforward playback and sharing.
- **Video Library**: The React interface shows a list of recorded videos, allowing users to browse and select specific files.
- **Live Feed Support**: Users can view a live camera (or file-based) feed directly in the React application.

## Installation

### Prerequisites

- Python
- Node.js
- Docker

### System-Level Dependencies

To ensure the project runs smoothly, the following system-level dependencies must be installed:

1. **FFmpeg**: Required for generating video thumbnails in the backend.

   - **macOS**: Install using Homebrew:
     ```sh
     brew install ffmpeg
     ```
   - **Ubuntu**: Install using APT:
     ```sh
     sudo apt update && sudo apt install ffmpeg
     ```
   - **Windows**: Download and install from [ffmpeg.org](https://ffmpeg.org/).

2. **OpenCV System Libraries**: Required for video processing and camera feed handling.
   - **macOS**: Install using Homebrew:
     ```sh
     brew install opencv
     ```
   - **Ubuntu**: Install using APT:
     ```sh
     sudo apt update && sudo apt install libopencv-dev
     ```
   - **Windows**: OpenCV is typically bundled with the Python package `opencv-python`, but additional setup may be required for advanced features.

## Running the Project

### With Docker

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kilok77/People-detection.git
   cd People-detection
   ```

2. **Create and start containers:**

   ```sh
   docker-compose up -d
   ```

3. **Access the application:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

### Additional Commands

- **Stop containers:**

  ```sh
  docker-compose down
  ```

- **View logs:**

  ```sh
  docker-compose logs
  ```

- **Rebuild containers:**

  ```sh
  docker-compose up --build
  ```

### Without Docker

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kilok77/People-detection.git
   cd People-detection
   ```

2. **Backend Setup:**

   - Navigate to the backend directory:

     ```sh
     cd backend
     ```

   - Create a virtual environment:

     ```sh
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

   - Install dependencies:

     ```sh
     pip install -r requirements.txt
     ```

   - Run the backend server:

     ```sh
     uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```

3. **Frontend Setup:**

   - Navigate to the frontend directory:

     ```sh
     cd ../frontend
     ```

   - Install dependencies:

     ```sh
     npm install
     ```

   - Run the frontend server:

     ```sh
     npm start
     ```

4. **Access the application:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

### Notes

- Ensure Docker is running before executing the Docker commands.
