import React from "react";

interface GroundProps {
  groundY?: number;
}

export const Ground: React.FC<GroundProps> = ({ groundY = 1450 }) => {
  return (
    <g>
      {/* Main Ground Line */}
      <line
        x1={-200}
        y1={groundY}
        x2={2000}
        y2={groundY}
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
      />

      {/* Decorative Ground Texture Hatches */}
      {[
        100, 220, 360, 480, 600, 750, 880, 1020, 1180, 1320, 1480, 1600,
      ].map((gx, i) => (
        <line
          key={i}
          x1={gx}
          y1={groundY + 12}
          x2={gx + 30}
          y2={groundY + 28}
          stroke="#000000"
          strokeWidth={6}
          strokeLinecap="round"
        />
      ))}
    </g>
  );
};
