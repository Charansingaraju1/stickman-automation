import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface DoorProps {
  x?: number;
  groundY?: number;
}

export const Door: React.FC<DoorProps> = ({ x = 700, groundY = 1450 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Door opening animation at frame 415 (Scene 5)
  // Note: Only Door #1 opens at frame 415. For Door #2 (x >= 1400), it stays firmly closed!
  const isDoor2 = x >= 1400;

  const openSpring = spring({
    frame: frame - 415,
    fps,
    config: { damping: 14, stiffness: 80, mass: 1 },
  });
  const openProgress = isDoor2 || frame < 415 ? 0 : openSpring;

  // Impact vibration on battering ram hit (frame 150) and shoulder ram (frame 110)
  let shakeX = 0;
  if (!isDoor2) {
    if (frame >= 110 && frame < 135) {
      const f = frame - 110;
      shakeX = Math.sin(f * 2.5) * Math.exp(-f * 0.15) * 8;
    } else if (frame >= 150 && frame < 190) {
      const f = frame - 150;
      shakeX = Math.sin(f * 3.0) * Math.exp(-f * 0.12) * 22;
    }
  }

  // Giant PULL sign highlight during Scene 6 (frames 450 - 540: "My bad.")
  const isScene6 = !isDoor2 && frame >= 450 && frame < 540;
  const highlightSpring = spring({
    frame: frame - 450,
    fps,
    config: { damping: 11, stiffness: 200 },
  });

  const doorWidth = 230;
  const doorHeight = 750;
  const doorTop = groundY - doorHeight;
  const hingeX = doorWidth + 10; // Right post

  // 3D Perspective angle as door opens towards camera (0 to 65 degrees)
  const angleDeg = interpolate(openProgress, [0, 1], [0, 65]);
  const angleRad = (angleDeg * Math.PI) / 180;

  // Quad coordinates for the swinging door leaf
  const edgeX = hingeX - doorWidth * Math.cos(angleRad);
  const persOffset = Math.sin(angleRad) * 40;
  const topLeftY = doorTop - persOffset;
  const bottomLeftY = groundY + persOffset * 0.4;
  const topRightY = doorTop;
  const bottomRightY = groundY;

  // Center of the PULL sign on the perspective leaf
  const signX = (edgeX + hingeX) / 2;
  const signY = doorTop + 220;

  return (
    <g transform={`translate(${x + shakeX}, 0)`}>
      {/* Doorway Interior Opening (revealed as door swings open) */}
      {openProgress > 0.05 && (
        <g opacity={Math.min(1, openProgress * 1.5)}>
          <rect
            x={10}
            y={doorTop}
            width={doorWidth}
            height={doorHeight}
            fill="#F6F6F6"
          />
          {/* Depth / floor perspective lines */}
          <line
            x1={10}
            y1={groundY}
            x2={60}
            y2={groundY - 50}
            stroke="#CCCCCC"
            strokeWidth={5}
          />
          <line
            x1={10 + doorWidth}
            y1={groundY}
            x2={10 + doorWidth - 50}
            y2={groundY - 50}
            stroke="#CCCCCC"
            strokeWidth={5}
          />
          <line
            x1={60}
            y1={groundY - 50}
            x2={10 + doorWidth - 50}
            y2={groundY - 50}
            stroke="#CCCCCC"
            strokeWidth={5}
          />
        </g>
      )}

      {/* Door Leaf (Perspective Quad) */}
      <polygon
        points={`${edgeX},${topLeftY} ${hingeX},${topRightY} ${hingeX},${bottomRightY} ${edgeX},${bottomLeftY}`}
        fill="#FFFFFF"
        stroke="#000000"
        strokeWidth={10}
        strokeLinejoin="round"
      />

      {/* Door Inner Mouldings / Panels */}
      {openProgress < 0.8 && (
        <>
          {/* Top moulding */}
          <polygon
            points={`${edgeX + 20},${topLeftY + 30} ${hingeX - 20},${topRightY + 30} ${hingeX - 20},${topRightY + 320} ${edgeX + 20},${topLeftY + 320}`}
            fill="none"
            stroke="#000000"
            strokeWidth={5}
          />
          {/* Bottom moulding */}
          <polygon
            points={`${edgeX + 20},${topLeftY + 370} ${hingeX - 20},${topRightY + 370} ${hingeX - 20},${bottomRightY - 30} ${edgeX + 20},${bottomLeftY - 30}`}
            fill="none"
            stroke="#000000"
            strokeWidth={5}
          />
        </>
      )}

      {/* Door Handle */}
      <g transform={`translate(${edgeX + 18}, ${doorTop + 410})`}>
        <rect
          x={-8}
          y={-28}
          width={16}
          height={56}
          rx={6}
          fill="#000000"
        />
        <circle cx={0} cy={0} r={8} fill="#000000" />
      </g>

      {/* THE PROMINENT "PULL" SIGN */}
      <g transform={`translate(${signX}, ${signY})`}>
        <rect
          x={-85}
          y={-42}
          width={170}
          height={84}
          rx={10}
          fill="#FFFFFF"
          stroke="#000000"
          strokeWidth={9}
        />
        <text
          x={0}
          y={16}
          textAnchor="middle"
          fill="#000000"
          fontFamily="'Arial Black', Impact, sans-serif"
          fontSize={46}
          fontWeight={900}
          letterSpacing={4}
        >
          PULL
        </text>
      </g>

      {/* Scene 6 Highlight: Giant comedic pulsing red box and top-down pointer arrow */}
      {isScene6 && (
        <g
          transform={`translate(${signX}, ${signY}) scale(${highlightSpring})`}
        >
          {/* Dashed Red Comic Box around PULL sign */}
          <rect
            x={-102}
            y={-56}
            width={204}
            height={112}
            rx={16}
            fill="none"
            stroke="#FF1111"
            strokeWidth={11}
            strokeDasharray="16 10"
          />

          {/* Animated Comic Arrow pointing DOWN directly at the PULL sign */}
          <g
            transform={`translate(0, -75 + ${Math.sin(frame * 0.8) * 10})`}
          >
            <path
              d="M 0 -45 L 0 -12 M -16 -28 L 0 -10 L 16 -28"
              fill="none"
              stroke="#FF1111"
              strokeWidth={12}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>
        </g>
      )}

      {/* Outer Door Frame (drawn on top of the door aperture) */}
      <rect
        x={0}
        y={doorTop - 15}
        width={doorWidth + 20}
        height={doorHeight + 15}
        fill="none"
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Ground Threshold */}
      <line
        x1={-10}
        y1={groundY}
        x2={doorWidth + 30}
        y2={groundY}
        stroke="#000000"
        strokeWidth={16}
        strokeLinecap="round"
      />
    </g>
  );
};
