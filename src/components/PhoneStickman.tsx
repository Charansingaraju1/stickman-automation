import React from "react";

export interface PhoneStickmanProps {
  x: number;
  y?: number; // ground level (1450)
  pose:
    | "sit_scroll"
    | "panic_pat"
    | "run_frantic"
    | "search_low"
    | "stare_hand"
    | "facepalm";
  frame: number;
  flashlightOn?: boolean;
  facing?: "left" | "right";
  scale?: number;
}

export const PhoneStickman: React.FC<PhoneStickmanProps> = ({
  x,
  y = 1450,
  pose,
  frame,
  flashlightOn = false,
  facing = "right",
  scale = 1,
}) => {
  const dir = facing === "right" ? 1 : -1;
  const headRadius = 38;

  // Joints relative to ground (0,0)
  let headX = 0;
  let headY = -340;
  let neckX = 0;
  let neckY = -270;
  let hipX = 0;
  let hipY = -180;

  // Limbs
  let leftArm = { elbowX: -25 * dir, elbowY: -210, handX: -35 * dir, handY: -150 };
  let rightArm = { elbowX: 25 * dir, elbowY: -210, handX: 35 * dir, handY: -150 };
  let leftLeg = { kneeX: -18 * dir, kneeY: -90, footX: -28 * dir, footY: 0 };
  let rightLeg = { kneeX: 18 * dir, kneeY: -90, footX: 28 * dir, footY: 0 };

  // Phone position and orientation
  let phoneX = 0;
  let phoneY = 0;
  let phoneAngle = 0;
  let showPhone = true;
  let eyeType: "normal" | "wide_panic" | "deadpan" | "closed" = "normal";
  let thumbCycle = 0;

  switch (pose) {
    case "sit_scroll": {
      // Sitting comfortably on the couch
      headX = -10 * dir;
      headY = -290;
      neckX = -10 * dir;
      neckY = -230;
      hipX = -25 * dir;
      hipY = -130;

      // Knees bent over edge of couch seat
      leftLeg = { kneeX: 35 * dir, kneeY: -125, footX: 35 * dir, footY: 0 };
      rightLeg = { kneeX: 55 * dir, kneeY: -125, footX: 55 * dir, footY: 0 };

      // Left arm relaxed on lap
      leftArm = {
        elbowX: -5 * dir,
        elbowY: -180,
        handX: 15 * dir,
        handY: -140,
      };

      // Right arm holding phone in front of face
      rightArm = {
        elbowX: 35 * dir,
        elbowY: -200,
        handX: 55 * dir,
        handY: -225,
      };

      phoneX = 65 * dir;
      phoneY = -235;
      phoneAngle = -15 * dir;
      thumbCycle = frame;
      eyeType = "normal";
      break;
    }

    case "panic_pat": {
      // Sitting bolt upright, frantic patting
      headX = 5 * dir;
      headY = -310;
      neckX = 0;
      neckY = -245;
      hipX = -20 * dir;
      hipY = -130;

      leftLeg = { kneeX: 35 * dir, kneeY: -125, footX: 35 * dir, footY: 0 };
      rightLeg = { kneeX: 55 * dir, kneeY: -125, footX: 55 * dir, footY: 0 };

      // Right arm is STILL holding the phone out!
      rightArm = {
        elbowX: 45 * dir,
        elbowY: -210,
        handX: 70 * dir,
        handY: -220,
      };
      phoneX = 80 * dir;
      phoneY = -225;
      phoneAngle = -10 * dir;

      // Left hand rapidly patting chest, hoodie pocket, and hip
      const patSin = Math.sin(frame * 0.9);
      const patCos = Math.cos(frame * 0.9);
      leftArm = {
        elbowX: (-40 + patCos * 15) * dir,
        elbowY: -200 + patSin * 20,
        handX: (-10 + patCos * 20) * dir,
        handY: -160 + patSin * 35,
      };

      eyeType = "wide_panic";
      break;
    }

    case "run_frantic": {
      // Sprinting across the room searching
      const stride = Math.sin(frame * 0.6) * 45;
      const leg1X = Math.sin((stride * Math.PI) / 180) * 90 * dir;
      const leg2X = -Math.sin((stride * Math.PI) / 180) * 90 * dir;
      const lift = Math.max(0, -Math.cos((stride * Math.PI) / 180) * 25);
      const bob = Math.abs(Math.sin(frame * 0.6)) * 12;

      headX = 25 * dir;
      headY = -330 + bob;
      neckX = 15 * dir;
      neckY = -265 + bob;
      hipX = -10 * dir;
      hipY = -175 + bob;

      leftLeg = { kneeX: leg1X * 0.5, kneeY: -85 + bob * 0.5, footX: leg1X, footY: 0 };
      rightLeg = {
        kneeX: leg2X * 0.5,
        kneeY: -85 + bob * 0.5 - lift * 0.5,
        footX: leg2X,
        footY: -lift,
      };

      leftArm = {
        elbowX: -35 * dir,
        elbowY: -210 + bob,
        handX: (-20 - Math.sin((stride * Math.PI) / 180) * 50) * dir,
        handY: -170 + bob,
      };

      rightArm = {
        elbowX: 45 * dir,
        elbowY: -210 + bob,
        handX: 80 * dir,
        handY: -200 + bob + Math.sin(frame * 0.4) * 20,
      };
      phoneX = 92 * dir;
      phoneY = -205 + bob + Math.sin(frame * 0.4) * 20;
      phoneAngle = 25 * dir;
      eyeType = "wide_panic";
      break;
    }

    case "search_low": {
      // Crawling on all fours, peeking under couch with flashlight
      headX = 85 * dir;
      headY = -120;
      neckX = 60 * dir;
      neckY = -110;
      hipX = -35 * dir;
      hipY = -95;

      leftLeg = { kneeX: -20 * dir, kneeY: 0, footX: -70 * dir, footY: 0 };
      rightLeg = { kneeX: -30 * dir, kneeY: 0, footX: -80 * dir, footY: 0 };

      // Left arm on ground for support
      leftArm = { elbowX: 25 * dir, elbowY: -50, handX: 25 * dir, handY: 0 };

      // Right arm pointing phone directly under the couch!
      const sweep = Math.sin(frame * 0.3) * 12;
      rightArm = {
        elbowX: 80 * dir,
        elbowY: -90,
        handX: (125 + sweep) * dir,
        handY: -40,
      };
      phoneX = (140 + sweep) * dir;
      phoneY = -40;
      phoneAngle = (85 + sweep * 0.4) * dir;
      eyeType = "wide_panic";
      break;
    }

    case "stare_hand": {
      // Standing upright, looking in complete disbelief at phone in hand
      headX = 0;
      headY = -340;
      neckX = 0;
      neckY = -270;
      hipX = 0;
      hipY = -180;

      leftLeg = { kneeX: -18 * dir, kneeY: -90, footX: -26 * dir, footY: 0 };
      rightLeg = { kneeX: 18 * dir, kneeY: -90, footX: 26 * dir, footY: 0 };

      leftArm = { elbowX: -28 * dir, elbowY: -200, handX: -25 * dir, handY: -130 };

      // Right hand holding phone directly in front of face
      rightArm = {
        elbowX: 35 * dir,
        elbowY: -225,
        handX: 45 * dir,
        handY: -265,
      };
      phoneX = 55 * dir;
      phoneY = -275;
      phoneAngle = -10 * dir;

      eyeType = frame % 70 < 6 ? "closed" : "deadpan";
      break;
    }

    case "facepalm": {
      headX = 10 * dir;
      headY = -325;
      neckX = 5 * dir;
      neckY = -260;
      hipX = -10 * dir;
      hipY = -175;

      leftLeg = { kneeX: -18 * dir, kneeY: -90, footX: -26 * dir, footY: 0 };
      rightLeg = { kneeX: 18 * dir, kneeY: -90, footX: 26 * dir, footY: 0 };

      rightArm = {
        elbowX: 25 * dir,
        elbowY: -190,
        handX: 35 * dir,
        handY: -130,
      };
      phoneX = 40 * dir;
      phoneY = -125;
      phoneAngle = 80 * dir;

      // Left hand on forehead (facepalm!)
      leftArm = {
        elbowX: -55 * dir,
        elbowY: -290,
        handX: 0,
        handY: -325,
      };
      eyeType = "closed";
      break;
    }
  }

  return (
    <g transform={`translate(${x}, ${y}) scale(${scale})`}>
      {/* Torso */}
      <line
        x1={neckX}
        y1={neckY}
        x2={hipX}
        y2={hipY}
        stroke="#000000"
        strokeWidth={16}
        strokeLinecap="round"
      />

      {/* Left Leg */}
      <path
        d={`M ${hipX} ${hipY} L ${leftLeg.kneeX} ${leftLeg.kneeY} L ${leftLeg.footX} ${leftLeg.footY}`}
        fill="none"
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Right Leg */}
      <path
        d={`M ${hipX} ${hipY} L ${rightLeg.kneeX} ${rightLeg.kneeY} L ${rightLeg.footX} ${rightLeg.footY}`}
        fill="none"
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Left Arm */}
      <path
        d={`M ${neckX} ${neckY} L ${leftArm.elbowX} ${leftArm.elbowY} L ${leftArm.handX} ${leftArm.handY}`}
        fill="none"
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Right Arm */}
      <path
        d={`M ${neckX} ${neckY} L ${rightArm.elbowX} ${rightArm.elbowY} L ${rightArm.handX} ${rightArm.handY}`}
        fill="none"
        stroke="#000000"
        strokeWidth={14}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Head */}
      <circle cx={headX} cy={headY} r={headRadius} fill="#000000" />

      {/* Eyes / Face Expression */}
      {eyeType === "normal" && (
        <g transform={`translate(${headX + 16 * dir}, ${headY - 5})`}>
          <circle cx={0} cy={0} r={5} fill="#FFFFFF" />
        </g>
      )}

      {eyeType === "wide_panic" && (
        <g transform={`translate(${headX + 14 * dir}, ${headY - 6})`}>
          <ellipse cx={0} cy={0} rx={11} ry={13} fill="#FFFFFF" />
          <circle cx={2 * dir} cy={0} r={4} fill="#000000" />
          <text
            x={16 * dir}
            y={-12}
            fontFamily="'Arial Black', Impact, sans-serif"
            fontSize={26}
            fontWeight="bold"
            fill="#FF2222"
          >
            !
          </text>
        </g>
      )}

      {eyeType === "deadpan" && (
        <g transform={`translate(${headX + 14 * dir}, ${headY - 4})`}>
          <ellipse cx={0} cy={0} rx={10} ry={12} fill="#FFFFFF" />
          <circle cx={2 * dir} cy={0} r={3} fill="#000000" />
          <ellipse cx={-4 * dir} cy={16} rx={7} ry={10} fill="#000000" />
        </g>
      )}

      {eyeType === "closed" && (
        <g transform={`translate(${headX + 12 * dir}, ${headY - 5})`}>
          <path
            d="M -6 0 Q 0 -6 6 0"
            fill="none"
            stroke="#FFFFFF"
            strokeWidth={4}
            strokeLinecap="round"
          />
          <path
            d="M -15 0 C -10 -6 -6 4 -15 10 Z"
            fill="#00AAFF"
            stroke="#000000"
            strokeWidth={2}
          />
        </g>
      )}

      {/* THE PHONE IN HAND */}
      {showPhone && (
        <g
          transform={`translate(${phoneX}, ${phoneY}) rotate(${phoneAngle})`}
        >
          {/* Phone body */}
          <rect
            x={-16}
            y={-30}
            width={32}
            height={60}
            rx={8}
            fill="#1A1A1A"
            stroke="#000000"
            strokeWidth={5}
          />

          {/* Screen */}
          <rect
            x={-12}
            y={-25}
            width={24}
            height={50}
            rx={4}
            fill={flashlightOn ? "#FFFFFF" : "#00D2FF"}
          />

          {/* Thumb scrolling animation */}
          {pose === "sit_scroll" && (
            <ellipse
              cx={-3 * dir}
              cy={Math.sin(thumbCycle * 0.4) * 8}
              rx={6}
              ry={4}
              fill="#000000"
            />
          )}

          {/* FLASHLIGHT CONE OF LIGHT (When flashlight is active) */}
          {flashlightOn && (
            <g transform="translate(0, -32)">
              <circle cx={0} cy={0} r={5} fill="#FFFF00" />
              <polygon
                points="-15,0 -160,-480 160,-480 15,0"
                fill="url(#lightGradient)"
                opacity={0.7}
              />
            </g>
          )}

          {/* Subtle Screen Glow when scrolling */}
          {!flashlightOn && (
            <ellipse
              cx={0}
              cy={0}
              rx={35}
              ry={45}
              fill="#00D2FF"
              opacity={0.25}
            />
          )}
        </g>
      )}

      {/* Comic Callout Arrow for the Punchline ("YOUR PHONE") */}
      {pose === "stare_hand" && (
        <g transform={`translate(${phoneX + 25 * dir}, ${phoneY - 70})`}>
          <rect
            x={-10}
            y={-28}
            width={185}
            height={54}
            rx={12}
            fill="#FF1111"
            stroke="#000000"
            strokeWidth={6}
          />
          <text
            x={82}
            y={8}
            textAnchor="middle"
            fill="#FFFFFF"
            fontFamily="'Arial Black', Impact, sans-serif"
            fontSize={23}
            fontWeight={900}
            letterSpacing={2}
          >
            YOUR PHONE
          </text>
          {/* Arrow pointing down-left at the phone */}
          <path
            d="M -10 10 L -30 35 M -30 20 L -30 35 L -15 35"
            fill="none"
            stroke="#FF1111"
            strokeWidth={8}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </g>
      )}
    </g>
  );
};
