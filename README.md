# People Detection

This project uses computer vision techniques to locate and track people in video streams. The FastAPI backend handles detection with OpenCV and YOLOv11, while a simple React frontend displays the results. The application is containerized with Docker for easy setup and deployment.

## Installation

### Prerequisites

- Python
- Node.js
- Docker

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
     nginx -g "daemon off;"
     ```

4. **Access the application:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

### Notes

- Ensure Docker is running before executing the Docker commands.
