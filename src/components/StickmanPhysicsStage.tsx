import React from "react";

export type PhysicsModuleKind =
  | "neutral"
  | "gravity"
  | "explosion_safe"
  | "space"
  | "anatomy"
  | "diagram";

interface StageProps {
  kind: PhysicsModuleKind;
  frame: number;
  accentHex?: string;
  callout?: string;
}

/** Deterministic B&W + selective-color scientific props & diagrams for Stickman explainers ($0). */
export const StickmanPhysicsStage: React.FC<StageProps> = ({
  kind,
  frame,
  accentHex = "#FF3B30",
  callout = "",
}) => {
  if (kind === "gravity") {
    const dropY = 760 + Math.min(640, (frame * frame * 0.42) % 660);
    return (
      <g>
        <path
          d="M 730 760 Q 790 980 790 1420"
          fill="none"
          stroke="#000000"
          strokeWidth={5}
          strokeDasharray="16 14"
        />
        <line x1={825} y1={820} x2={825} y2={1320} stroke={accentHex} strokeWidth={8} strokeLinecap="round" />
        <polygon points="825,1360 806,1310 844,1310" fill={accentHex} />
        <circle cx={730} cy={dropY} r={34} fill={accentHex} stroke="#000000" strokeWidth={7} />
        {callout && (
          <text x={790} y={715} textAnchor="middle" fill="#000000" fontFamily="Arial Black, sans-serif" fontSize={32} fontWeight={900}>
            {callout}
          </text>
        )}
      </g>
    );
  }

  if (kind === "explosion_safe") {
    const t = frame % 36;
    return (
      <g transform="translate(755, 1140)">
        {[0, 1, 2].map((i) => {
          const r = 35 + ((t * 9 + i * 55) % 210);
          return (
            <circle
              key={i}
              cx={0}
              cy={0}
              r={r}
              fill="none"
              stroke={i === 0 ? accentHex : "#000000"}
              strokeWidth={7}
              strokeDasharray={i === 2 ? "18 14" : undefined}
              opacity={Math.max(0.08, 1 - r / 230)}
            />
          );
        })}
        <circle cx={0} cy={0} r={26} fill={accentHex} stroke="#000000" strokeWidth={6} />
        {callout && (
          <text x={0} y={-240} textAnchor="middle" fill={accentHex} fontFamily="Arial Black, sans-serif" fontSize={32} fontWeight={900}>
            {callout}
          </text>
        )}
      </g>
    );
  }

  if (kind === "space") {
    const angle = (frame * 0.09) % (Math.PI * 2);
    const ox = Math.cos(angle) * 165;
    const oy = Math.sin(angle) * 95;
    return (
      <g transform="translate(740, 880)">
        <ellipse cx={0} cy={0} rx={165} ry={95} fill="none" stroke="#000000" strokeWidth={4} strokeDasharray="10 10" />
        <circle cx={0} cy={0} r={54} fill="#000000" />
        <circle cx={-16} cy={-16} r={14} fill="#FFFFFF" opacity={0.25} />
        <circle cx={ox} cy={oy} r={18} fill={accentHex} stroke="#000000" strokeWidth={5} />
        {callout && (
          <text x={0} y={-135} textAnchor="middle" fill="#000000" fontFamily="Arial Black, sans-serif" fontSize={30} fontWeight={900}>
            {callout}
          </text>
        )}
      </g>
    );
  }

  if (kind === "anatomy") {
    const pulse = 1 + Math.sin(frame * 0.32) * 0.08;
    return (
      <g transform="translate(765, 960)">
        <rect x={-145} y={-190} width={290} height={380} rx={36} fill="#FFFFFF" stroke="#000000" strokeWidth={8} />
        <path d="M 0 -150 L 0 40" fill="none" stroke="#000000" strokeWidth={18} strokeLinecap="round" />
        <ellipse cx={-55} cy={35} rx={44 * pulse} ry={85 * pulse} fill="none" stroke="#000000" strokeWidth={8} />
        <ellipse cx={55} cy={35} rx={44 * pulse} ry={85 * pulse} fill={accentHex} fillOpacity={0.28} stroke={accentHex} strokeWidth={8} />
        {callout && (
          <text x={0} y={160} textAnchor="middle" fill={accentHex} fontFamily="Arial Black, sans-serif" fontSize={28} fontWeight={900}>
            {callout}
          </text>
        )}
      </g>
    );
  }

  if (kind === "diagram" && callout) {
    return (
      <g transform="translate(755, 860)">
        <rect x={-165} y={-65} width={330} height={130} rx={16} fill="#FFFFFF" stroke="#000000" strokeWidth={7} />
        <line x1={-165} y1={0} x2={-235} y2={60} stroke={accentHex} strokeWidth={8} strokeLinecap="round" />
        <text x={0} y={12} textAnchor="middle" fill={accentHex} fontFamily="Arial Black, sans-serif" fontSize={32} fontWeight={900}>
          {callout}
        </text>
      </g>
    );
  }

  return null;
};
