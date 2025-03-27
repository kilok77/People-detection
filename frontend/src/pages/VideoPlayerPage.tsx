import React from "react";
import { useParams, Link } from "react-router-dom";
import { getVideoUrl } from "../services/api";
import VideoPlayer from "../components/VideoPlayer";

function VideoPlayerPage() {
  const { videoName } = useParams();

  if (!videoName) {
    return (
      <div style={{ padding: "2rem" }}>
        <h2>No video specified.</h2>
        <Link to="/">Go Back</Link>
      </div>
    );
  }

  const videoSrc = getVideoUrl(videoName);

  return (
    <div style={{ padding: "2rem" }}>
      <Link to="/">← Back to List</Link>
      <h1>Now Playing: {videoName}</h1>
      <VideoPlayer videoSrc={videoSrc} />
    </div>
  );
}

export default VideoPlayerPage;
