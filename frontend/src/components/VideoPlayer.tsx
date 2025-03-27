import React, { useRef, useEffect } from "react";

interface VideoPlayerProps {
  videoSrc: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoSrc }) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  return (
    <video
      ref={videoRef}
      src={videoSrc}
      controls
      style={{
        width: "100%",
        maxWidth: "800px",
        marginTop: "1rem",
        border: "1px solid #ccc",
      }}
    />
  );
};

export default VideoPlayer;
