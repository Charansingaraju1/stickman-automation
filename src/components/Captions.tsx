import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

export interface CaptionSegment {
  text: string;
  from: number;
  to: number;
  isPunchline?: boolean;
}

export const CAPTIONS: CaptionSegment[] = [
  { text: "Push", from: 0, to: 60 },
  { text: "Still stuck", from: 60, to: 150 },
  { text: "OPEN!", from: 150, to: 240, isPunchline: true },
  { text: "I give up.", from: 240, to: 360 },
  { text: "Oh.", from: 360, to: 450 },
  { text: "My bad.", from: 450, to: 540 },
  { text: "Next door.", from: 540, to: 600 },
];

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Find active segment
  const activeSegment = CAPTIONS.find(
    (seg) => frame >= seg.from && frame < seg.to
  );

  if (!activeSegment) {
    return null;
  }

  const relativeFrame = frame - activeSegment.from;
  const popSpring = spring({
    frame: relativeFrame,
    fps,
    config: {
      damping: activeSegment.isPunchline ? 10 : 13,
      stiffness: activeSegment.isPunchline ? 240 : 190,
      mass: 0.8,
    },
  });

  // Small punchline shake on impact
  const punchlineShake = activeSegment.isPunchline
    ? Math.sin(relativeFrame * 1.5) *
      interpolate(relativeFrame, [0, 15], [8, 0], {
        extrapolateRight: "clamp",
      })
    : 0;

  return (
    <div
      style={{
        position: "absolute",
        top: 260,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 50,
      }}
    >
      <span
        style={{
          fontFamily: "'Montserrat', 'Arial Black', Impact, sans-serif",
          fontSize: activeSegment.isPunchline ? 110 : 92,
          fontWeight: 900,
          textTransform: "uppercase",
          letterSpacing: "3px",
          color: "#FFFFFF",
          WebkitTextStroke: "7px #000000",
          paintOrder: "stroke fill",
          filter: "drop-shadow(0px 8px 20px rgba(0,0,0,0.4))",
          transform: `scale(${popSpring}) translateY(${punchlineShake}px)`,
          display: "inline-block",
        }}
      >
        {activeSegment.text}
      </span>
    </div>
  );
};
