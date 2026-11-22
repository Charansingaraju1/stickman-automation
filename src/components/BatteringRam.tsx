import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface BatteringRamProps {
  x: number;
  y: number;
}

export const BatteringRam: React.FC<BatteringRamProps> = ({ x, y }) => {
  const frame = useCurrentFrame();

  // Active during Scene 3 (frames 150 to 240)
  if (frame < 150 || frame >= 240) {
    return null;
  }

  const relFrame = frame - 150;

  // Impact recoil oscillation
  const recoil =
    Math.sin(relFrame * 1.2) *
    Math.exp(-relFrame * 0.07) *
    interpolate(relFrame, [0, 40], [-60, 0], {
      extrapolateRight: "clamp",
    });

  // Shockwave expansion on strike (frame 150-175)
  const shockwaveRadius = interpolate(relFrame, [0, 25], [10, 180], {
    extrapolateRight: "clamp",
  });
  const shockwaveOpacity = interpolate(relFrame, [0, 25], [1, 0], {
    extrapolateRight: "clamp",
  });

  const ramX = x + recoil;
  const ramY = y + Math.sin(relFrame * 0.8) * 3;

  return (
    <g>
      {/* Impact Shockwaves at the door boundary */}
      {relFrame < 25 && (
        <g transform={`translate(${700}, ${y})`}>
          <circle
            cx={0}
            cy={0}
            r={shockwaveRadius}
            fill="none"
            stroke="#000000"
            strokeWidth={12}
            opacity={shockwaveOpacity}
          />
          <circle
            cx={0}
            cy={0}
            r={shockwaveRadius * 0.6}
            fill="none"
            stroke="#000000"
            strokeWidth={8}
            opacity={shockwaveOpacity}
          />
          {/* Starburst impact sparks */}
          {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
            const rad = (angle * Math.PI) / 180;
            const r1 = shockwaveRadius * 0.7;
            const r2 = shockwaveRadius * 1.2;
            return (
              <line
                key={i}
                x1={Math.cos(rad) * r1}
                y1={Math.sin(rad) * r1}
                x2={Math.cos(rad) * r2}
                y2={Math.sin(rad) * r2}
                stroke="#000000"
                strokeWidth={8}
                strokeLinecap="round"
                opacity={shockwaveOpacity}
              />
            );
          })}
        </g>
      )}

      {/* The Heavy Battering Ram */}
      <g transform={`translate(${ramX}, ${ramY})`}>
        {/* Main Log Body */}
        <rect
          x={-280}
          y={-35}
          width={280}
          height={70}
          rx={18}
          fill="#1A1A1A"
          stroke="#000000"
          strokeWidth={8}
        />

        {/* Steel Bands around log */}
        <rect x={-230} y={-38} width={22} height={76} rx={4} fill="#888888" stroke="#000000" strokeWidth={5} />
        <rect x={-140} y={-38} width={22} height={76} rx={4} fill="#888888" stroke="#000000" strokeWidth={5} />
        <rect x={-50} y={-38} width={22} height={76} rx={4} fill="#888888" stroke="#000000" strokeWidth={5} />

        {/* Heavy Iron Ram Head (Front Strike Face) */}
        <path
          d="M 0 -42 L 35 -20 L 45 0 L 35 20 L 0 42 Z"
          fill="#444444"
          stroke="#000000"
          strokeWidth={8}
          strokeLinejoin="round"
        />

        {/* Iron Ram Horn Details */}
        <path
          d="M 15 -18 Q 30 -35 15 -50 Q 5 -35 10 -20"
          fill="#333333"
          stroke="#000000"
          strokeWidth={6}
        />
        <path
          d="M 15 18 Q 30 35 15 50 Q 5 35 10 20"
          fill="#333333"
          stroke="#000000"
          strokeWidth={6}
        />

        {/* Heavy Handle Straps */}
        <path
          d="M -200 35 Q -175 75 -150 35"
          fill="none"
          stroke="#555555"
          strokeWidth={10}
          strokeLinecap="round"
        />
        <path
          d="M -110 35 Q -85 75 -60 35"
          fill="none"
          stroke="#555555"
          strokeWidth={10}
          strokeLinecap="round"
        />
      </g>
    </g>
  );
};
