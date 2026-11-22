import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

export interface ZackCaptionCue {
  text: string;
  subText?: string;
  from: number;
  to: number;
  isAlert?: boolean;
}

export const ZACK_CAPTIONS: ZackCaptionCue[] = [
  {
    text: "SWALLOWED A BATTERY?",
    subText: "WHAT ACTUALLY HAPPENS INSIDE",
    from: 0,
    to: 165,
  },
  {
    text: "COMPLETES A CIRCUIT",
    subText: "MOISTURE CONDUCTS CURRENT",
    from: 165,
    to: 330,
    isAlert: true,
  },
  {
    text: "CREATES DRAIN CLEANER",
    subText: "SODIUM HYDROXIDE (pH 13+)",
    from: 330,
    to: 510,
    isAlert: true,
  },
  {
    text: "BURNS THROUGH IN 2 HOURS",
    subText: "RISK OF INTERNAL BLEEDING",
    from: 510,
    to: 700,
    isAlert: true,
  },
  {
    text: "SWALLOW HONEY & CALL 911",
    subText: "COATS TISSUE TO SLOW BURN",
    from: 700,
    to: 900,
  },
];

export const ZackCaptions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const activeCue = ZACK_CAPTIONS.find(
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
      damping: activeCue.isAlert ? 10 : 13,
      stiffness: activeCue.isAlert ? 240 : 190,
      mass: 0.8,
    },
  });

  const shake = activeCue.isAlert
    ? Math.sin(relFrame * 1.8) *
      interpolate(relFrame, [0, 15], [5, 0], {
        extrapolateRight: "clamp",
      })
    : 0;

  return (
    <div
      style={{
        position: "absolute",
        top: 150,
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 50,
      }}
    >
      <span
        style={{
          fontFamily: "'Montserrat', 'Arial Black', Impact, sans-serif",
          fontSize: activeCue.isAlert ? 86 : 80,
          fontWeight: 900,
          textTransform: "uppercase",
          letterSpacing: "3px",
          color: activeCue.isAlert ? "#FFE600" : "#FFFFFF",
          WebkitTextStroke: "7px #000000",
          paintOrder: "stroke fill",
          filter: "drop-shadow(0px 8px 24px rgba(0,0,0,0.55))",
          transform: `scale(${popSpring}) translateY(${shake}px)`,
          display: "inline-block",
          textAlign: "center",
          maxWidth: "960px",
          lineHeight: 1.1,
        }}
      >
        {activeCue.text}
      </span>

      {activeCue.subText && (
        <span
          style={{
            fontFamily: "'Montserrat', 'Arial Black', sans-serif",
            fontSize: 34,
            fontWeight: 800,
            textTransform: "uppercase",
            letterSpacing: "3px",
            color: "#FFFFFF",
            WebkitTextStroke: "4px #000000",
            paintOrder: "stroke fill",
            marginTop: 12,
            filter: "drop-shadow(0px 4px 12px rgba(0,0,0,0.4))",
          }}
        >
          {activeCue.subText}
        </span>
      )}
    </div>
  );
};
