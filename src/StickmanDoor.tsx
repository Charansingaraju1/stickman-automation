import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Door } from "./components/Door";
import { Stickman } from "./components/Stickman";
import { Ground } from "./components/Ground";
import { Captions } from "./components/Captions";
import { BatteringRam } from "./components/BatteringRam";

export const StickmanDoor: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Screen shake on major impacts (shoulder ram at frame 110, battering ram at frame 150)
  let screenShakeY = 0;
  let screenShakeX = 0;
  if (frame >= 110 && frame < 135) {
    const f = frame - 110;
    screenShakeY = Math.sin(f * 2.8) * Math.exp(-f * 0.2) * 12;
    screenShakeX = Math.cos(f * 2.8) * Math.exp(-f * 0.2) * 8;
  } else if (frame >= 150 && frame < 190) {
    const f = frame - 150;
    screenShakeY = Math.sin(f * 3.2) * Math.exp(-f * 0.12) * 28;
    screenShakeX = Math.cos(f * 3.2) * Math.exp(-f * 0.12) * 18;
  }

  // Camera horizontal shift for the seamless loop in Scene 7 (frames 545 to 599)
  // Shifts world by exactly -1100px so Door #1 exits completely and Door #2 (x = 1800) lands at 700!
  const loopPanX = interpolate(frame, [545, 599], [0, -1100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // --- STICKMAN 1 CHOREOGRAPHY ---
  let s1X = 350;
  let s1Pose:
    | "walk"
    | "push"
    | "charge"
    | "ram_hold"
    | "kneel"
    | "look_up"
    | "casual_walk"
    | "casual_stand"
    | "pull_door" = "walk";
  let s1WalkCycle = 0;
  let s1Sweat = false;
  let s1Dizzy = false;
  let s1Facing: "left" | "right" = "right";

  if (frame < 60) {
    // [0-2s] Scene 1: Approach door & push hard
    if (frame < 25) {
      s1X = interpolate(frame, [0, 25], [350, 560], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      s1Pose = "walk";
      s1WalkCycle = frame * 0.35;
    } else {
      s1X = 560;
      s1Pose = "push";
      s1Sweat = frame % 15 < 8;
    }
  } else if (frame < 150) {
    // [2-5s] Scene 2: Back up, charge & shoulder ram
    if (frame < 85) {
      // Backing up
      s1X = interpolate(frame, [60, 85], [560, 360], {
        extrapolateRight: "clamp",
      });
      s1Pose = "walk";
      s1Facing = "left";
      s1WalkCycle = (frame - 60) * 0.3;
    } else if (frame < 110) {
      // Charging forward
      s1X = interpolate(frame, [85, 110], [360, 640], {
        extrapolateRight: "clamp",
      });
      s1Pose = "charge";
      s1Facing = "right";
      s1WalkCycle = (frame - 85) * 0.5;
    } else {
      // Rebound & dazed wobble
      s1X = interpolate(frame, [110, 120, 150], [640, 590, 590], {
        extrapolateRight: "clamp",
      });
      s1Pose = "walk";
      s1Facing = "right";
      s1Dizzy = true;
    }
  } else if (frame < 240) {
    // [5-8s] Scene 3: Battering Ram (PUNCHLINE)
    s1Pose = "ram_hold";
    s1Facing = "right";
    const recoil =
      Math.sin((frame - 150) * 1.2) *
      Math.exp(-(frame - 150) * 0.07) *
      interpolate(frame - 150, [0, 40], [-60, 0], {
        extrapolateRight: "clamp",
      });
    s1X = 570 + recoil;
  } else if (frame < 360) {
    // [8-12s] Scene 4: Exhausted, drops to knees
    s1X = 430;
    s1Facing = "right";
    s1Pose = "kneel";
    s1Sweat = frame % 25 < 12;
  } else if (frame < 450) {
    // [12-15s] Scene 5: Second guy walks up & opens door
    s1X = 430;
    s1Facing = "right";
    s1Pose = "kneel";
  } else if (frame < 540) {
    // [15-18s] Scene 6: Staring blankly at PULL sign ("My bad.")
    s1X = 430;
    s1Facing = "right";
    s1Pose = "look_up";
  } else {
    // [18-20s] Scene 7: Walks through, reaches second door (SEAMLESS LOOP)
    if (frame < 555) {
      s1X = 430;
      s1Facing = "right";
      s1Pose = "kneel";
    } else {
      // Walks towards Door #2 (world x = 1800)
      // At frame 599: s1X = 1450. With loopPanX = -1100, on-screen x is 350!
      // Exactly matching frame 0 screen position (s1X = 350)!
      const walkProgress = (frame - 555) / (599 - 555);
      s1X = interpolate(walkProgress, [0, 1], [430, 1450]);
      s1Facing = "right";
      s1Pose = "walk";
      // Walk cycle completes 2 full cycles (4 * PI) so at frame 599 walkCycle % 2PI = 0
      s1WalkCycle = (frame - 555) * ((Math.PI * 4) / (599 - 555));
    }
  }

  // --- STICKMAN 2 CHOREOGRAPHY (Scenes 5 & 6, frames 360 - 540) ---
  const isS2Active = frame >= 360 && frame < 550;
  let s2X = 0;
  let s2Pose: "casual_walk" | "casual_stand" | "pull_door" = "casual_walk";
  let s2WalkCycle = 0;

  if (isS2Active) {
    if (frame < 410) {
      // Casual stroll from left
      s2X = interpolate(frame, [360, 410], [50, 620], {
        extrapolateRight: "clamp",
      });
      s2Pose = "casual_walk";
      s2WalkCycle = (frame - 360) * 0.35;
    } else if (frame < 445) {
      // Pulling door open
      s2X = interpolate(frame, [410, 425], [620, 590], {
        extrapolateRight: "clamp",
      });
      s2Pose = "pull_door";
    } else {
      // Standing chilled, holding door open
      s2X = 590;
      s2Pose = "casual_stand";
    }
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#FFFFFF",
        width: 1080,
        height: 1920,
        overflow: "hidden",
      }}
    >
      {/* Punchline Sound Effect at exactly Second 5 (Frame 150) */}
      <Sequence from={150} durationInFrames={30}>
        <Audio src={staticFile("punchline_sfx.wav")} />
      </Sequence>

      {/* Captions Overlay at upper third of screen */}
      <Captions />

      {/* Main Vector Animation Stage */}
      <svg
        width={1080}
        height={1920}
        viewBox="0 0 1080 1920"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translate(${screenShakeX}px, ${screenShakeY}px)`,
        }}
      >
        <g transform={`translate(${loopPanX}, 0)`}>
          {/* Continuous Ground Plane across both rooms */}
          <Ground groundY={1450} />

          {/* Door #1 (Main Door at world x = 700) */}
          <Door x={700} groundY={1450} />

          {/* Door #2 (Loop Door at world x = 1800) */}
          <Door x={1800} groundY={1450} />

          {/* Battering Ram Prop for Scene 3 */}
          <BatteringRam x={s1X + 50} y={1270} />

          {/* Stickman 1 */}
          <Stickman
            x={s1X}
            y={1450}
            pose={s1Pose}
            walkCycle={s1WalkCycle}
            facing={s1Facing}
            sweat={s1Sweat}
            dizzy={s1Dizzy}
          />

          {/* Stickman 2 */}
          {isS2Active && (
            <Stickman
              x={s2X}
              y={1450}
              pose={s2Pose}
              walkCycle={s2WalkCycle}
              facing="right"
              scale={0.98}
            />
          )}
        </g>
      </svg>
    </AbsoluteFill>
  );
};
