// src/App.tsx

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import VideoListPage from "./pages/VideoListPage";
import VideoPlayerPage from "./pages/VideoPlayerPage";
import CameraPage from "./pages/CameraPage"; // <-- Import the new page

function App() {
  return (
    <Router>
      <Routes>
        {/* Home page with the video list */}
        <Route path="/" element={<VideoListPage />} />

        {/* Video player page for a specific video */}
        <Route path="/videos/:videoName" element={<VideoPlayerPage />} />

        {/* Live camera feed page */}
        <Route path="/camera" element={<CameraPage />} />
      </Routes>
    </Router>
  );
}

export default App;
