import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

export interface CaptionCue {
  text: string;
  from: number;
  to: number;
  isPunchline?: boolean;
}

export const PHONE_CAPTIONS: CaptionCue[] = [
  { text: "WHERE IS IT?!", from: 40, to: 100 },
  { text: "I JUST HAD IT!", from: 100, to: 230 },
  { text: "WAIT A SECOND...", from: 230, to: 320 },
  { text: "USING THE FLASHLIGHT...", from: 320, to: 380, isPunchline: true },
  { text: "TO FIND THE PHONE?!", from: 380, to: 460, isPunchline: true },
  { text: "BRAIN CELL: 404", from: 460, to: 540 },
  { text: "BACK TO SCROLLING", from: 540, to: 600 },
];

export const PhoneCaptions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const activeCue = PHONE_CAPTIONS.find(
    (c) => frame >= c.from && frame < c.to
  );

  if (!activeCue) {
    return null;
  }

  const relFrame = frame - activeCue.from;
  const popSpring = spring({
    frame: relFrame,
    fps,
    config: {
      damping: activeCue.isPunchline ? 10 : 13,
      stiffness: activeCue.isPunchline ? 240 : 190,
      mass: 0.8,
    },
  });

  const punchlineShake = activeCue.isPunchline
    ? Math.sin(relFrame * 1.5) *
      interpolate(relFrame, [0, 15], [8, 0], {
        extrapolateRight: "clamp",
      })
    : 0;

  return (
    <div
      style={{
        position: "absolute",
        top: 250,
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
          fontSize: activeCue.isPunchline ? 105 : 90,
          fontWeight: 900,
          textTransform: "uppercase",
          letterSpacing: "3px",
          color: "#FFFFFF",
          WebkitTextStroke: "7px #000000",
          paintOrder: "stroke fill",
          filter: "drop-shadow(0px 8px 24px rgba(0,0,0,0.45))",
          transform: `scale(${popSpring}) translateY(${punchlineShake}px)`,
          display: "inline-block",
          textAlign: "center",
          maxWidth: "920px",
          lineHeight: 1.1,
        }}
      >
        {activeCue.text}
      </span>
    </div>
  );
};
