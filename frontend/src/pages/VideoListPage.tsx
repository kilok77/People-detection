// src/pages/VideoListPage.tsx

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchVideoList, getThumbnailUrl } from "../services/api";
import { VideoItem } from "../types/videoTypes";

function VideoListPage() {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchVideoList()
      .then((fetchedVideos) => {
        setVideos(fetchedVideos);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Available Videos</h1>
      <Link to="/camera">View Live Camera</Link>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          marginTop: "1rem",
        }}
      >
        {videos.map((video) => (
          <div
            key={video.name}
            style={{
              border: "1px solid #ccc",
              borderRadius: "8px",
              width: "200px",
              padding: "1rem",
              textAlign: "center",
            }}
          >
            <img
              src={getThumbnailUrl(video.name)}
              alt={video.name}
              style={{
                width: "100%",
                height: "auto",
                marginBottom: "0.5rem",
                borderRadius: "4px",
              }}
            />
            <div style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>
              {video.name}
            </div>
            <Link to={`/videos/${video.name}`}>Play Video</Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default VideoListPage;
