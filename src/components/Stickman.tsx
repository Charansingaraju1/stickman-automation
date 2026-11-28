import React from "react";

export type StickmanPose =
  | "walk"
  | "run"
  | "push"
  | "charge"
  | "ram_hold"
  | "kneel"
  | "look_up"
  | "fall"
  | "jump"
  | "point"
  | "think"
  | "casual_walk"
  | "casual_stand"
  | "pull_door";

export type StickmanExpression = "neutral" | "shock" | "curious" | "panic" | "pain";

export interface StickmanProps {
  x: number;
  y?: number; // Ground y coordinate (default 1450)
  pose: StickmanPose;
  walkCycle?: number;
  facing?: "left" | "right";
  expression?: StickmanExpression;
  sweat?: boolean;
  dizzy?: boolean;
  scale?: number;
}

export const Stickman: React.FC<StickmanProps> = ({
  x,
  y = 1450,
  pose,
  walkCycle = 0,
  facing = "right",
  expression = "neutral",
  sweat = false,
  dizzy = false,
  scale = 1,
}) => {
  const dir = facing === "right" ? 1 : -1;
  const headRadius = 38;

  // Joints relative to ground (0,0)
  let headY = -340;
  let headX = 0;
  let hipX = 0;
  let hipY = -180;
  let neckX = 0;
  let neckY = -270;

  // Natural standing limbs
  let leftArm = { elbowX: -28 * dir, elbowY: -210, handX: -36 * dir, handY: -150 };
  let rightArm = { elbowX: 28 * dir, elbowY: -210, handX: 36 * dir, handY: -150 };
  let leftLeg = { kneeX: -20 * dir, kneeY: -90, footX: -35 * dir, footY: 0 };
  let rightLeg = { kneeX: 20 * dir, kneeY: -90, footX: 35 * dir, footY: 0 };

  switch (pose) {
    case "walk":
    case "casual_walk": {
      const stride = pose === "casual_walk" ? 0.8 : 1.1;
      const legAngle = Math.sin(walkCycle) * 36 * stride;
      const armAngle = -Math.sin(walkCycle) * 30 * stride;
      const bob = Math.abs(Math.sin(walkCycle * 2)) * 8;

      headY = -340 + bob;
      neckY = -270 + bob;
      hipY = -180 + bob;

      // Ensure base separation so legs never collapse into a single line
      const baseStance = 28;
      const leg1X = (-baseStance * 0.5 + Math.sin((legAngle * Math.PI) / 180) * 80) * dir;
      const leg2X = (baseStance * 0.5 - Math.sin((legAngle * Math.PI) / 180) * 80) * dir;
      const lift = Math.max(0, -Math.cos((legAngle * Math.PI) / 180) * 22);

      leftLeg = {
        kneeX: leg1X * 0.6,
        kneeY: -90 + bob * 0.5,
        footX: leg1X,
        footY: 0,
      };
      rightLeg = {
        kneeX: leg2X * 0.6,
        kneeY: -90 + bob * 0.5 - lift * 0.5,
        footX: leg2X,
        footY: -lift,
      };

      // Arms swinging naturally with offset
      leftArm = {
        elbowX: (-20 + Math.sin((armAngle * Math.PI) / 180) * 45) * dir,
        elbowY: neckY + 45,
        handX: (-30 + Math.sin((armAngle * Math.PI) / 180) * 85) * dir,
        handY: neckY + 95,
      };
      rightArm = {
        elbowX: (20 - Math.sin((armAngle * Math.PI) / 180) * 45) * dir,
        elbowY: neckY + 45,
        handX: (30 - Math.sin((armAngle * Math.PI) / 180) * 85) * dir,
        handY: neckY + 95,
      };
      break;
    }

    case "push": {
      // Aggressive forward lean against door
      headX = 75 * dir;
      headY = -315;
      neckX = 55 * dir;
      neckY = -260;
      hipX = -35 * dir;
      hipY = -175;

      leftLeg = { kneeX: 10 * dir, kneeY: -80, footX: 25 * dir, footY: 0 };
      rightLeg = { kneeX: -65 * dir, kneeY: -75, footX: -110 * dir, footY: 0 };

      leftArm = {
        elbowX: 95 * dir,
        elbowY: -250,
        handX: 145 * dir,
        handY: -260,
      };
      rightArm = {
        elbowX: 90 * dir,
        elbowY: -225,
        handX: 145 * dir,
        handY: -220,
      };
      break;
    }

    case "charge": {
      headX = 90 * dir;
      headY = -280;
      neckX = 70 * dir;
      neckY = -230;
      hipX = -50 * dir;
      hipY = -170;

      leftLeg = { kneeX: 30 * dir, kneeY: -70, footX: 60 * dir, footY: 0 };
      rightLeg = {
        kneeX: -90 * dir,
        kneeY: -80,
        footX: -140 * dir,
        footY: -20,
      };

      leftArm = {
        elbowX: 95 * dir,
        elbowY: -200,
        handX: 115 * dir,
        handY: -180,
      };
      rightArm = {
        elbowX: 75 * dir,
        elbowY: -180,
        handX: 85 * dir,
        handY: -140,
      };
      break;
    }

    case "ram_hold": {
      headX = 40 * dir;
      headY = -320;
      neckX = 25 * dir;
      neckY = -260;
      hipX = -20 * dir;
      hipY = -180;

      leftLeg = { kneeX: 10 * dir, kneeY: -90, footX: 20 * dir, footY: 0 };
      rightLeg = { kneeX: -50 * dir, kneeY: -85, footX: -85 * dir, footY: 0 };

      leftArm = {
        elbowX: 45 * dir,
        elbowY: -200,
        handX: 70 * dir,
        handY: -160,
      };
      rightArm = {
        elbowX: 15 * dir,
        elbowY: -190,
        handX: 30 * dir,
        handY: -155,
      };
      break;
    }

    case "kneel": {
      headX = 25 * dir;
      headY = -190;
      neckX = 15 * dir;
      neckY = -150;
      hipX = -25 * dir;
      hipY = -95;

      leftLeg = { kneeX: 25 * dir, kneeY: 0, footX: -40 * dir, footY: 0 };
      rightLeg = { kneeX: 15 * dir, kneeY: 0, footX: -50 * dir, footY: 0 };

      leftArm = {
        elbowX: 25 * dir,
        elbowY: -90,
        handX: 35 * dir,
        handY: -10,
      };
      rightArm = {
        elbowX: 5 * dir,
        elbowY: -85,
        handX: 10 * dir,
        handY: -10,
      };
      break;
    }

    case "look_up": {
      headX = 25 * dir;
      headY = -210;
      neckX = 15 * dir;
      neckY = -150;
      hipX = -25 * dir;
      hipY = -95;

      leftLeg = { kneeX: 25 * dir, kneeY: 0, footX: -40 * dir, footY: 0 };
      rightLeg = { kneeX: 15 * dir, kneeY: 0, footX: -50 * dir, footY: 0 };

      leftArm = {
        elbowX: 25 * dir,
        elbowY: -90,
        handX: 35 * dir,
        handY: -10,
      };
      rightArm = {
        elbowX: 45 * dir,
        elbowY: -190,
        handX: 20 * dir,
        handY: -225,
      };
      break;
    }

    case "casual_stand": {
      headX = 0;
      headY = -340;
      neckX = 0;
      neckY = -270;
      hipX = 0;
      hipY = -180;

      leftLeg = { kneeX: -18 * dir, kneeY: -90, footX: -26 * dir, footY: 0 };
      rightLeg = { kneeX: 18 * dir, kneeY: -90, footX: 26 * dir, footY: 0 };

      leftArm = { elbowX: -32 * dir, elbowY: -200, handX: -25 * dir, handY: -140 };
      rightArm = { elbowX: 32 * dir, elbowY: -200, handX: 25 * dir, handY: -140 };
      break;
    }

    case "pull_door": {
      headX = -10 * dir;
      headY = -335;
      neckX = -10 * dir;
      neckY = -265;
      hipX = -25 * dir;
      hipY = -180;

      leftLeg = { kneeX: -40 * dir, kneeY: -90, footX: -55 * dir, footY: 0 };
      rightLeg = { kneeX: 5 * dir, kneeY: -90, footX: 10 * dir, footY: 0 };

      leftArm = {
        elbowX: -45 * dir,
        elbowY: -220,
        handX: -30 * dir,
        handY: -180,
      };
      rightArm = {
        elbowX: 35 * dir,
        elbowY: -230,
        handX: 65 * dir,
        handY: -210,
      };
      break;
    }

    case "run": {
      const a = Math.sin(walkCycle * 1.6);
      headX = 28 * dir;
      headY = -325 + Math.abs(a) * 12;
      neckX = 18 * dir;
      neckY = -260 + Math.abs(a) * 10;
      hipX = -15 * dir;
      hipY = -175 + Math.abs(a) * 8;
      leftLeg = { kneeX: (a * 65) * dir, kneeY: -90, footX: (a * 95 - 20) * dir, footY: Math.min(0, -a * 28) };
      rightLeg = { kneeX: (-a * 65) * dir, kneeY: -90, footX: (-a * 95 - 20) * dir, footY: Math.min(0, a * 28) };
      leftArm = { elbowX: (-a * 50) * dir, elbowY: neckY + 40, handX: (-a * 80 + 25) * dir, handY: neckY + 15 };
      rightArm = { elbowX: (a * 50) * dir, elbowY: neckY + 40, handX: (a * 80 + 25) * dir, handY: neckY + 15 };
      break;
    }

    case "jump": {
      headY = -395;
      neckY = -325;
      hipY = -235;
      leftLeg = { kneeX: -35 * dir, kneeY: -135, footX: -20 * dir, footY: -65 };
      rightLeg = { kneeX: 35 * dir, kneeY: -145, footX: 45 * dir, footY: -75 };
      leftArm = { elbowX: -55 * dir, elbowY: -355, handX: -75 * dir, handY: -415 };
      rightArm = { elbowX: 55 * dir, elbowY: -355, handX: 75 * dir, handY: -415 };
      break;
    }

    case "fall": {
      headX = -65 * dir;
      headY = -260;
      neckX = -35 * dir;
      neckY = -215;
      hipX = 25 * dir;
      hipY = -145;
      leftLeg = { kneeX: 75 * dir, kneeY: -125, footX: 115 * dir, footY: -80 };
      rightLeg = { kneeX: 60 * dir, kneeY: -85, footX: 105 * dir, footY: -20 };
      leftArm = { elbowX: -75 * dir, elbowY: -275, handX: -115 * dir, handY: -315 };
      rightArm = { elbowX: -15 * dir, elbowY: -290, handX: 20 * dir, handY: -345 };
      break;
    }

    case "point": {
      leftArm = { elbowX: -30 * dir, elbowY: -210, handX: -25 * dir, handY: -150 };
      rightArm = { elbowX: 65 * dir, elbowY: -265, handX: 135 * dir, handY: -275 };
      break;
    }

    case "think": {
      headX = 8 * dir;
      leftArm = { elbowX: -28 * dir, elbowY: -205, handX: -12 * dir, handY: -155 };
      rightArm = { elbowX: 48 * dir, elbowY: -225, handX: 18 * dir, handY: -305 };
      break;
    }
  }

  return (
    <g transform={`translate(${x}, ${y}) scale(${scale})`}>
      {/* Torso / Spine */}
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
      <circle
        cx={headX}
        cy={headY}
        r={headRadius}
        fill="#000000"
      />

      {/* Minimal expressive eyes/mouth strictly when expression != neutral */}
      {expression !== "neutral" && (
        <g transform={`translate(${headX + 8 * dir}, ${headY - 4})`}>
          <ellipse
            cx={-10}
            cy={-2}
            rx={7}
            ry={expression === "shock" || expression === "panic" ? 10 : 7}
            fill="#FFFFFF"
          />
          <ellipse
            cx={10}
            cy={-2}
            rx={7}
            ry={expression === "shock" || expression === "panic" ? 10 : 7}
            fill="#FFFFFF"
          />
          <circle cx={-9} cy={-2} r={3} fill="#000000" />
          <circle cx={11} cy={-2} r={3} fill="#000000" />
          {expression === "shock" || expression === "panic" ? (
            <ellipse cx={0} cy={17} rx={8} ry={6} fill="#FFFFFF" />
          ) : expression === "pain" ? (
            <path d="M-9 18 Q0 12 9 18" fill="none" stroke="#FFFFFF" strokeWidth={3} strokeLinecap="round" />
          ) : (
            <line x1={-6} y1={16} x2={8} y2={15} stroke="#FFFFFF" strokeWidth={3} strokeLinecap="round" />
          )}
        </g>
      )}

      {/* Dizzy stars / wobble lines if dizzy */}
      {dizzy && (
        <g transform={`translate(${headX}, ${headY - 55})`}>
          <text
            x={-30}
            y={0}
            fontSize={24}
            fontWeight="bold"
            fill="#000000"
          >
            ★
          </text>
          <text
            x={0}
            y={-10}
            fontSize={28}
            fontWeight="bold"
            fill="#000000"
          >
            ★
          </text>
          <text
            x={25}
            y={0}
            fontSize={24}
            fontWeight="bold"
            fill="#000000"
          >
            ★
          </text>
        </g>
      )}

      {/* Sweat drops when exhausted or pushing hard */}
      {sweat && (
        <g transform={`translate(${headX + 35 * dir}, ${headY - 15})`}>
          <path
            d="M 0 0 C 12 -8 18 8 0 16 C -6 8 0 0 0 0 Z"
            fill="#00AAFF"
            stroke="#000000"
            strokeWidth={3}
          />
        </g>
      )}
    </g>
  );
};
