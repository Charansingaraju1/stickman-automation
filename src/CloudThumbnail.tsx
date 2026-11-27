import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Stickman } from "./components/Stickman";

export interface CloudThumbnailProps {
  topBadge: string;
  headline: string;
  accentHex: string;
  primaryImgPath?: string;
  secondaryImgPath?: string;
}

export const CloudThumbnail: React.FC<CloudThumbnailProps> = ({
  topBadge,
  headline,
  accentHex,
  primaryImgPath,
  secondaryImgPath,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#FFFFFF", fontFamily: "Impact, Arial Black, sans-serif" }}>
      {/* Upper comedic action panel */}
      <div style={{ position: "relative", height: "54%", width: "100%", overflow: "hidden" }}>
        {primaryImgPath ? (
          <Img src={staticFile(primaryImgPath)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <svg width={1080} height={1040} viewBox="0 0 1080 1040" style={{ backgroundColor: "#FFF7ED" }}>
            <circle cx={540} cy={560} r={340} fill={accentHex} opacity={0.22} />
            <Stickman x={520} y={920} pose="charge" facing="right" sweat scale={1.85} />
          </svg>
        )}
      </div>

      {/* Lower magnified aftermath / high-contrast light slate panel */}
      <div
        style={{
          position: "relative",
          height: "46%",
          width: "100%",
          borderTop: `12px solid ${accentHex}`,
          overflow: "hidden",
        }}
      >
        {secondaryImgPath ? (
          <Img src={staticFile(secondaryImgPath)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <svg width={1080} height={880} viewBox="0 0 1080 880" style={{ backgroundColor: "#F1F5F9" }}>
            <circle cx={540} cy={470} r={260} fill="#FEE2E2" stroke="#EF4444" strokeWidth={18} />
            <Stickman x={540} y={760} pose="kneel" facing="left" dizzy scale={1.5} />
          </svg>
        )}
      </div>

      {/* Center high-CTR hook banner */}
      <div
        style={{
          position: "absolute",
          top: "51%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: accentHex,
          color: "#FFFFFF",
          padding: "16px 38px",
          borderRadius: 16,
          border: "8px solid #FFFFFF",
          fontSize: 64,
          letterSpacing: 1.5,
          whiteSpace: "nowrap",
          boxShadow: "0 18px 40px rgba(0,0,0,0.45)",
        }}
      >
        {headline}
      </div>

      <div
        style={{
          position: "absolute",
          top: 90,
          left: "50%",
          transform: "translateX(-50%)",
          backgroundColor: "#EF4444",
          color: "#FFFFFF",
          padding: "10px 28px",
          borderRadius: 12,
          fontSize: 42,
          letterSpacing: 1,
          whiteSpace: "nowrap",
          boxShadow: "0 10px 24px rgba(0,0,0,0.28)",
        }}
      >
        {topBadge}
      </div>
    </AbsoluteFill>
  );
};
