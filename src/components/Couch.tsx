import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface CouchProps {
  x: number;
  groundY?: number;
}

export const Couch: React.FC<CouchProps> = ({ x, groundY = 1450 }) => {
  const frame = useCurrentFrame();

  const couchWidth = 360;
  const seatHeight = 130;
  const backHeight = 270;
  const seatY = groundY - seatHeight;
  const backY = groundY - backHeight;

  // Cushion flip animation during panic search (frames 110 to 180)
  let cushionAngle = 0;
  let cushionLiftY = 0;
  if (frame >= 110 && frame < 180) {
    cushionAngle = interpolate(frame, [110, 125, 160, 180], [0, -45, -45, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    cushionLiftY = interpolate(frame, [110, 125, 160, 180], [0, -40, -40, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  }

  return (
    <g transform={`translate(${x}, 0)`}>
      {/* Dark shadow underneath couch where lost items hide */}
      <rect
        x={25}
        y={groundY - 35}
        width={couchWidth - 50}
        height={35}
        fill="#EEEEEE"
      />

      {/* Couch Backrest */}
      <rect
        x={0}
        y={backY}
        width={90}
        height={backHeight}
        rx={16}
        fill="#FFFFFF"
        stroke="#000000"
        strokeWidth={12}
        strokeLinejoin="round"
      />

      {/* Main Seat Base */}
      <rect
        x={20}
        y={seatY}
        width={couchWidth - 40}
        height={seatHeight - 35}
        rx={14}
        fill="#FFFFFF"
        stroke="#000000"
        strokeWidth={12}
        strokeLinejoin="round"
      />

      {/* Removable / Flipping Cushion */}
      <g
        transform={`translate(60, ${seatY}) rotate(${cushionAngle}) translate(-60, ${cushionLiftY})`}
      >
        <rect
          x={40}
          y={seatY - 35}
          width={couchWidth - 70}
          height={40}
          rx={10}
          fill="#FFFFFF"
          stroke="#000000"
          strokeWidth={10}
          strokeLinejoin="round"
        />
        {/* Cushion tuft lines */}
        <line
          x1={120}
          y1={seatY - 20}
          x2={140}
          y2={seatY - 20}
          stroke="#000000"
          strokeWidth={6}
          strokeLinecap="round"
        />
        <line
          x1={220}
          y1={seatY - 20}
          x2={240}
          y2={seatY - 20}
          stroke="#000000"
          strokeWidth={6}
          strokeLinecap="round"
        />
      </g>

      {/* Right Armrest */}
      <rect
        x={couchWidth - 65}
        y={seatY - 50}
        width={65}
        height={seatHeight + 15}
        rx={16}
        fill="#FFFFFF"
        stroke="#000000"
        strokeWidth={12}
        strokeLinejoin="round"
      />

      {/* Couch Legs */}
      <line
        x1={35}
        y1={groundY - 35}
        x2={35}
        y2={groundY}
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
      />
      <line
        x1={couchWidth - 35}
        y1={groundY - 35}
        x2={couchWidth - 35}
        y2={groundY}
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
      />
    </g>
  );
};
