import { logDOM } from "@testing-library/dom";
import { log } from "console";
import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

const SimpleMjpeg: React.FC = () => {
  return (
    <div>
      <h2>Simple MJPEG Stream</h2>
      <img
        style={{
          width: "100%",
          maxWidth: "800px",
          marginTop: "1rem",
          border: "1px solid #ccc",
        }}
        src="http://localhost:8000/video_feed"
        alt="MJPEG Stream"
      />
      <Link to="/">Back</Link>
    </div>
  );
};

export default SimpleMjpeg;
