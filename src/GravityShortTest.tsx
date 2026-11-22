import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";

export const GravityShortTest: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#FFFFFF" }}>
      <OffthreadVideo src={staticFile("gravity_raw.mp4")} />
    </AbsoluteFill>
  );
};
