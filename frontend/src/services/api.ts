// src/services/api.ts

import axios from "axios";
import { VideoItem } from "../types/videoTypes";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export const fetchVideoList = async (): Promise<VideoItem[]> => {
  try {
    const response = await axios.get<{ videos: VideoItem[] }>(
      `${API_URL}/video-list`
    );
    return response.data.videos;
  } catch (error) {
    console.error("Error fetching video list:", error);
    throw error;
  }
};

export const getVideoUrl = (videoName: string): string => {
  return `${API_URL}/video/${videoName}`;
};

export const getThumbnailUrl = (videoName: string): string => {
  return `${API_URL}/thumbnail/${videoName}`;
};
