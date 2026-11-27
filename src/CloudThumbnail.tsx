import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

export interface CloudThumbnailProps {
  topBadge: string;
  headline: string;
  accentHex: string;
  primaryImgPath?: string;
  secondaryImgPath?: string;
}

// Unified full-bleed StickNation signature thumbnail (matches Mentos "DO NOT MIX!" bold yellow/white house style)
export const CloudThumbnail: React.FC<CloudThumbnailProps> = ({
  topBadge,
  headline,
  primaryImgPath,
  secondaryImgPath,
}) => {
  const heroImg = primaryImgPath || secondaryImgPath;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0B1120",
        fontFamily: "Impact, Arial Black, sans-serif",
        overflow: "hidden",
      }}
    >
      {heroImg ? (
        <Img
          src={staticFile(heroImg)}
          style={{ width: "100%", height: "100%", objectFit: "cover", filter: "contrast(1.08) saturate(1.12)" }}
        />
      ) : (
        <svg width={1080} height={1920} viewBox="0 0 1080 1920">
          <defs>
            <radialGradient id="thumbBg" cx="50%" cy="55%" r="60%">
              <stop offset="0%" stopColor="#1E293B" />
              <stop offset="100%" stopColor="#050811" />
            </radialGradient>
            <radialGradient id="thumbHead" cx="38%" cy="32%" r="68%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="70%" stopColor="#E2E8F0" />
              <stop offset="100%" stopColor="#94A3B8" />
            </radialGradient>
          </defs>
          <rect width={1080} height={1920} fill="url(#thumbBg)" />
          <circle cx={540} cy={1250} r={340} fill="none" stroke="#FF3B30" strokeWidth={18} opacity={0.85} />
          <g transform="translate(540, 1280) scale(1.45)">
            <rect x={-46} y={-240} width={92} height={210} rx={46} fill="url(#thumbHead)" />
            <path d="M-40 -210 L-105 -120 L-65 -40" fill="none" stroke="#CBD5E1" strokeWidth={30} strokeLinecap="round" />
            <path d="M40 -210 L105 -120 L65 -40" fill="none" stroke="#CBD5E1" strokeWidth={30} strokeLinecap="round" />
            <circle cx={0} cy={-345} r={115} fill="url(#thumbHead)" />
            <ellipse cx={-38} cy={-352} rx={26} ry={30} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={4} />
            <ellipse cx={38} cy={-352} rx={26} ry={30} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={4} />
            <circle cx={-32} cy={-350} r={10} fill="#0F172A" />
            <circle cx={44} cy={-350} r={10} fill="#0F172A" />
            <ellipse cx={0} cy={-284} rx={30} ry={26} fill="#1E293B" />
          </g>
        </svg>
      )}

      {/* Subtle inset circular X-ray / macro zoom bubble when secondary cutout differs from primary */}
      {primaryImgPath && secondaryImgPath && primaryImgPath !== secondaryImgPath && (
        <div
          style={{
            position: "absolute",
            bottom: 130,
            right: 65,
            width: 390,
            height: 390,
            borderRadius: "50%",
            overflow: "hidden",
            border: "12px solid #FF3B30",
            boxShadow: "0 18px 44px rgba(0,0,0,0.85)",
          }}
        >
          <Img src={staticFile(secondaryImgPath)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </div>
      )}

      {/* Dark top gradient scrim for instant mobile-feed readability */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 540,
          background: "linear-gradient(180deg, rgba(5,8,16,0.92) 0%, rgba(5,8,16,0.55) 65%, transparent 100%)",
        }}
      />

      {/* Signature 2-line Impact header (matches DO NOT MIX! aesthetic) */}
      <div
        style={{
          position: "absolute",
          top: 90,
          left: 40,
          right: 40,
          textAlign: "center",
          lineHeight: 0.96,
        }}
      >
        <div
          style={{
            fontSize: 132,
            color: "#FFFFFF",
            WebkitTextStroke: "8px #000000",
            textShadow: "0 12px 24px rgba(0,0,0,0.95)",
            letterSpacing: 2,
          }}
        >
          {topBadge}
        </div>
        <div
          style={{
            fontSize: 146,
            color: "#FFD60A",
            WebkitTextStroke: "8px #000000",
            textShadow: "0 12px 24px rgba(0,0,0,0.95)",
            letterSpacing: 2,
            marginTop: 6,
          }}
        >
          {headline}
        </div>
      </div>
    </AbsoluteFill>
  );
};
