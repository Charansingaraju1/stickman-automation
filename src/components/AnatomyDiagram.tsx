import React from "react";
import { interpolate } from "remotion";

interface AnatomyDiagramProps {
  frame: number;
}

export const AnatomyDiagram: React.FC<AnatomyDiagramProps> = ({ frame }) => {
  // Active during anatomical zoom (frames 80 to 740)
  if (frame < 75 || frame > 740) {
    return null;
  }

  const centerX = 540;
  const batteryY = 980;
  const batteryRadius = 125;

  const isCircuitActive = frame >= 165 && frame < 330;
  const isChemicalActive = frame >= 330 && frame < 520;
  const isNecrosisActive = frame >= 510 && frame < 740;
  const isHoneyActive = frame >= 700;

  // Tissue wall burn depth (0 to 45px erosion)
  const burnDepth = interpolate(frame, [510, 620], [0, 50], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <g>
      {/* Background shadow for throat interior */}
      <rect
        x={280}
        y={300}
        width={520}
        height={1300}
        fill="#FDF2E9"
        opacity={0.9}
      />


      {/* AORTA (Major Blood Vessel) pulsing behind left esophagus wall */}
      <g>
        <path
          d="M 230 300 Q 210 980 230 1600"
          fill="none"
          stroke="#C0392B"
          strokeWidth={48 + (isNecrosisActive ? Math.sin(frame * 0.4) * 8 : 0)}
          strokeLinecap="round"
          opacity={0.85}
        />
        <path
          d="M 230 300 Q 210 980 230 1600"
          fill="none"
          stroke="#E74C3C"
          strokeWidth={22}
          opacity={0.65}
        />
        {isNecrosisActive && (
          <text
            x={150}
            y={840}
            fill="#C0392B"
            fontFamily="'Arial Black', Impact, sans-serif"
            fontSize={26}
            fontWeight={900}
            letterSpacing={2}
          >
            AORTA
          </text>
        )}
      </g>

      {/* LEFT ESOPHAGUS WALL */}
      <path
        d={`M 310 300 Q ${330 + (isNecrosisActive ? burnDepth : 0)} 980 310 1600`}
        fill="none"
        stroke={isNecrosisActive ? "#641E16" : "#E67E73"}
        strokeWidth={34}
        strokeLinecap="round"
      />
      <path
        d={`M 310 300 Q ${330 + (isNecrosisActive ? burnDepth : 0)} 980 310 1600`}
        fill="none"
        stroke="#000000"
        strokeWidth={8}
      />

      {/* RIGHT ESOPHAGUS WALL */}
      <path
        d={`M 770 300 Q ${750 - (isNecrosisActive ? burnDepth * 0.7 : 0)} 980 770 1600`}
        fill="none"
        stroke={isNecrosisActive ? "#78281F" : "#E67E73"}
        strokeWidth={34}
        strokeLinecap="round"
      />
      <path
        d={`M 770 300 Q ${750 - (isNecrosisActive ? burnDepth * 0.7 : 0)} 980 770 1600`}
        fill="none"
        stroke="#000000"
        strokeWidth={8}
      />

      {/* TISSUE BURN / NECROSIS ZONE (Crimson & Charred Black) */}
      {isNecrosisActive && (
        <g>
          <ellipse
            cx={centerX - 160}
            cy={batteryY}
            rx={50 + burnDepth * 0.5}
            ry={90}
            fill="#17202A"
            opacity={0.92}
          />
          <ellipse
            cx={centerX - 160}
            cy={batteryY}
            rx={32 + burnDepth * 0.3}
            ry={65}
            fill="#78281F"
            opacity={0.85}
          />

          {/* Sizzling smoke particles */}
          {[0, 1, 2, 3].map((i) => {
            const smokeY = batteryY - 40 - ((frame * 3 + i * 40) % 130);
            const smokeX = centerX - 165 + Math.sin(frame * 0.2 + i) * 22;
            return (
              <circle
                key={i}
                cx={smokeX}
                cy={smokeY}
                r={9 + i * 3}
                fill="#666666"
                opacity={0.4}
              />
            );
          })}
        </g>
      )}

      {/* THE BUTTON BATTERY (LODGED IN ESOPHAGUS) */}
      <g transform={`translate(${centerX}, ${batteryY})`}>
        {/* Battery Outer Metallic Casing (Positive Pole +) */}
        <circle
          cx={0}
          cy={0}
          r={batteryRadius}
          fill="#BDC3C7"
          stroke="#000000"
          strokeWidth={12}
        />
        {/* Metal Sheen Highlight */}
        <ellipse
          cx={-35}
          cy={-35}
          rx={70}
          ry={50}
          fill="#ECF0F1"
          opacity={0.7}
        />

        {/* Negative Terminal Inner Disk (-) */}
        <circle
          cx={0}
          cy={0}
          r={batteryRadius * 0.72}
          fill="#95A5A6"
          stroke="#000000"
          strokeWidth={8}
        />

        {/* Insulating Gasket Ring */}
        <circle
          cx={0}
          cy={0}
          r={batteryRadius * 0.72}
          fill="none"
          stroke="#E67E22"
          strokeWidth={10}
        />

        {/* Polarity Markings - Cleanly sized */}
        <text
          x={0}
          y={-75}
          textAnchor="middle"
          fill="#000000"
          fontFamily="'Arial Black', Impact, sans-serif"
          fontSize={24}
          fontWeight={900}
          letterSpacing={2}
        >
          + POSITIVE
        </text>
        <text
          x={0}
          y={10}
          textAnchor="middle"
          fill="#000000"
          fontFamily="'Arial Black', Impact, sans-serif"
          fontSize={32}
          fontWeight={900}
          letterSpacing={2}
        >
          - NEGATIVE
        </text>
        <text
          x={0}
          y={50}
          textAnchor="middle"
          fill="#2C3E50"
          fontFamily="'Montserrat', sans-serif"
          fontSize={18}
          fontWeight={800}
          letterSpacing={2}
        >
          3V COIN CELL
        </text>
      </g>

      {/* ELECTRICAL CIRCUIT ARCS (Stage 2: Frames 165 - 330) */}
      {isCircuitActive && (
        <g>
          {[-1, 1].map((side, i) => {
            const jitter = Math.sin(frame * 4.0 + i) * 16;
            return (
              <g key={i}>
                <path
                  d={`M ${centerX + side * 90} ${batteryY - 25} Q ${centerX + side * 185 + jitter} ${batteryY} ${centerX + side * 90} ${batteryY + 25}`}
                  fill="none"
                  stroke="#00F0FF"
                  strokeWidth={14}
                  strokeLinecap="round"
                />
                <path
                  d={`M ${centerX + side * 90} ${batteryY - 25} Q ${centerX + side * 185 + jitter} ${batteryY} ${centerX + side * 90} ${batteryY + 25}`}
                  fill="none"
                  stroke="#FFE600"
                  strokeWidth={7}
                  strokeLinecap="round"
                />
              </g>
            );
          })}

          {/* Electric Current Flash Callout */}
          <g transform={`translate(${centerX}, ${batteryY + 185})`}>
            <rect
              x={-200}
              y={-30}
              width={400}
              height={60}
              rx={12}
              fill="#002244"
              stroke="#00F0FF"
              strokeWidth={5}
            />
            <text
              x={0}
              y={10}
              textAnchor="middle"
              fill="#00F0FF"
              fontFamily="'Arial Black', Impact, sans-serif"
              fontSize={24}
              fontWeight={900}
              letterSpacing={3}
            >
              ⚡ CLOSED CIRCUIT ACTIVE
            </text>
          </g>
        </g>
      )}

      {/* CAUSTIC CHEMICAL BUBBLES: SODIUM HYDROXIDE (Stage 3: Frames 330 - 510) */}
      {isChemicalActive && (
        <g>
          {[-1, 1].map((side, i) => (
            <g key={i} transform={`translate(${centerX + side * 125}, ${batteryY})`}>
              <ellipse
                cx={0}
                cy={0}
                rx={45 + Math.sin(frame * 0.5 + i) * 8}
                ry={60 + Math.cos(frame * 0.5 + i) * 10}
                fill="#2ECC71"
                opacity={0.75}
              />
              {[0, 1, 2, 3, 4].map((b) => (
                <circle
                  key={b}
                  cx={Math.sin(frame * 0.4 + b * 2) * 24}
                  cy={-25 - ((frame * 2 + b * 15) % 70)}
                  r={8 + (b % 3) * 3}
                  fill="#E8F8F5"
                  stroke="#27AE60"
                  strokeWidth={3}
                />
              ))}
            </g>
          ))}

          {/* Chemical Callout Tag */}
          <g transform={`translate(${centerX}, ${batteryY + 185})`}>
            <rect
              x={-240}
              y={-32}
              width={480}
              height={64}
              rx={14}
              fill="#196F3D"
              stroke="#2ECC71"
              strokeWidth={6}
            />
            <text
              x={0}
              y={12}
              textAnchor="middle"
              fill="#FFFFFF"
              fontFamily="'Arial Black', Impact, sans-serif"
              fontSize={26}
              fontWeight={900}
              letterSpacing={2}
            >
              ☠️ SODIUM HYDROXIDE (NaOH)
            </text>
          </g>
        </g>
      )}

      {/* DANGER RUPTURE CALLOUT (Stage 4: Frames 510 - 700) */}
      {isNecrosisActive && !isHoneyActive && (
        <g transform={`translate(${centerX}, ${batteryY + 185})`}>
          <rect
            x={-240}
            y={-32}
            width={480}
            height={64}
            rx={14}
            fill="#78281F"
            stroke="#E74C3C"
            strokeWidth={6}
          />
          <text
            x={0}
            y={12}
            textAnchor="middle"
            fill="#FFFFFF"
            fontFamily="'Arial Black', Impact, sans-serif"
            fontSize={26}
            fontWeight={900}
            letterSpacing={2}
          >
            ⚠️ PERFORATION & RUPTURE RISK
          </text>
        </g>
      )}

      {/* HONEY COATING BARRIER (Stage 5: Frames 700 - 740) */}
      {isHoneyActive && (
        <g>
          {/* Thick golden amber honey layer covering esophagus and battery */}
          <path
            d={`M 315 300 Q 340 980 340 1500 L 740 1500 Q 740 980 765 300 Z`}
            fill="#F39C12"
            opacity={0.85}
          />
          <path
            d={`M 345 500 Q 365 980 365 1400 L 715 1400 Q 715 980 735 500 Z`}
            fill="#F1C40F"
            opacity={0.7}
          />
          <ellipse cx={centerX} cy={batteryY - 140} rx={100} ry={30} fill="#D68910" />
          <ellipse cx={centerX} cy={batteryY + 140} rx={100} ry={30} fill="#D68910" />

          {/* Protective Honey Callout */}
          <g transform={`translate(${centerX}, ${batteryY + 185})`}>
            <rect
              x={-240}
              y={-32}
              width={480}
              height={64}
              rx={14}
              fill="#B7950B"
              stroke="#F1C40F"
              strokeWidth={6}
            />
            <text
              x={0}
              y={12}
              textAnchor="middle"
              fill="#FFFFFF"
              fontFamily="'Arial Black', Impact, sans-serif"
              fontSize={26}
              fontWeight={900}
              letterSpacing={2}
            >
              🍯 HONEY STOPS CURRENT
            </text>
          </g>
        </g>
      )}
    </g>
  );
};
