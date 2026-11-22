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
import { Ground } from "./components/Ground";
import { Couch } from "./components/Couch";
import { PhoneStickman } from "./components/PhoneStickman";
import { PhoneCaptions } from "./components/PhoneCaptions";

export const PhonePanicShort: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Camera zoom during punchline realization (frames 240 to 450)
  const cameraZoom = interpolate(
    frame,
    [240, 310, 440, 480],
    [1.0, 1.25, 1.25, 1.0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const cameraTranslateY = interpolate(
    frame,
    [240, 310, 440, 480],
    [0, 140, 140, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Subtle camera shake on alert and facepalm
  let shakeY = 0;
  if (frame >= 40 && frame < 55) {
    const f = frame - 40;
    shakeY = Math.sin(f * 2.5) * Math.exp(-f * 0.2) * 8;
  } else if (frame >= 460 && frame < 480) {
    const f = frame - 460;
    shakeY = Math.sin(f * 3.0) * Math.exp(-f * 0.25) * 14;
  }

  // --- STICKMAN CHOREOGRAPHY ---
  let stickmanX = 540;
  let stickmanPose:
    | "sit_scroll"
    | "panic_pat"
    | "run_frantic"
    | "search_low"
    | "stare_hand"
    | "facepalm" = "sit_scroll";
  let facing: "left" | "right" = "right";
  let flashlightOn = false;

  if (frame < 40) {
    // [0-1.3s] Casual scrolling
    stickmanX = 540;
    stickmanPose = "sit_scroll";
    facing = "right";
    flashlightOn = false;
  } else if (frame < 100) {
    // [1.3s-3.3s] Panic patting pockets while still sitting
    stickmanX = 540;
    stickmanPose = "panic_pat";
    facing = "right";
    flashlightOn = false;
  } else if (frame < 180) {
    // [3.3s-6.0s] Jumps up, sprints back and forth, turns on flashlight!
    flashlightOn = frame >= 135;
    if (frame < 140) {
      // Sprint left towards couch edge
      stickmanX = interpolate(frame, [100, 140], [540, 260], {
        extrapolateRight: "clamp",
      });
      facing = "left";
    } else {
      // Sprint right searching room
      stickmanX = interpolate(frame, [140, 180], [260, 750], {
        extrapolateRight: "clamp",
      });
      facing = "right";
    }
    stickmanPose = "run_frantic";
  } else if (frame < 235) {
    // [6.0s-7.8s] Drops to hands and knees, shining flashlight directly under the couch!
    stickmanX = 260;
    stickmanPose = "search_low";
    facing = "right";
    flashlightOn = true;
  } else if (frame < 460) {
    // [7.8s-15.3s] Stands up, notices glowing hand, stares deadpan at phone
    stickmanX = 540;
    stickmanPose = "stare_hand";
    facing = "right";
    flashlightOn = true;
  } else if (frame < 540) {
    // [15.3s-18.0s] Slaps forehead in defeat (Facepalm!)
    stickmanX = 540;
    stickmanPose = "facepalm";
    facing = "right";
    flashlightOn = false;
  } else {
    // [18.0s-20.0s] Sits back down on couch, resumes scrolling (SEAMLESS 100% LOOP)
    stickmanX = 540;
    stickmanPose = "sit_scroll";
    facing = "right";
    flashlightOn = false;
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
      {/* --- SOUND EFFECTS --- */}
      {/* Frame 40: Panic alert chime */}
      <Sequence from={40} durationInFrames={20}>
        <Audio src={staticFile("alert_sfx.wav")} />
      </Sequence>

      {/* Frame 135: Flashlight Click ON */}
      <Sequence from={135} durationInFrames={15}>
        <Audio src={staticFile("click_sfx.wav")} />
      </Sequence>

      {/* Frame 460: Facepalm SLAP */}
      <Sequence from={460} durationInFrames={25}>
        <Audio src={staticFile("slap_sfx.wav")} />
      </Sequence>

      {/* Frame 545: Flashlight Click OFF */}
      <Sequence from={545} durationInFrames={15}>
        <Audio src={staticFile("click_sfx.wav")} />
      </Sequence>

      {/* --- FUNNY VOICEOVER SEQUENCE --- */}
      {/* 0.0s - 3.4s: "Wait. Wait, where is my phone?" */}
      <Sequence from={15} durationInFrames={100}>
        <Audio src={staticFile("vo_setup.mp3")} volume={1.0} />
      </Sequence>

      {/* 3.5s - 6.5s: "Where did it go?! I literally just had it!" */}
      <Sequence from={105} durationInFrames={90}>
        <Audio src={staticFile("vo_panic.mp3")} volume={1.0} />
      </Sequence>

      {/* 7.7s - 11.5s: "Wait... Why is my hand glowing?" */}
      <Sequence from={230} durationInFrames={110}>
        <Audio src={staticFile("vo_glow.mp3")} volume={1.0} />
      </Sequence>

      {/* 11.5s - 15.5s: "I am using my phone flashlight... to look for my phone." */}
      <Sequence from={345} durationInFrames={125}>
        <Audio src={staticFile("vo_punchline.mp3")} volume={1.0} />
      </Sequence>

      {/* 16.0s - 19.0s: "I need to be studied by scientists." */}
      <Sequence from={480} durationInFrames={90}>
        <Audio src={staticFile("vo_defeat.mp3")} volume={1.0} />
      </Sequence>

      {/* 19.1s - 20.0s: "Whatever." */}
      <Sequence from={575} durationInFrames={25}>
        <Audio src={staticFile("vo_loop.mp3")} volume={1.0} />
      </Sequence>

      {/* Upper-third captions */}
      <PhoneCaptions />

      {/* Main SVG Animation World */}
      <svg
        width={1080}
        height={1920}
        viewBox="0 0 1080 1920"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translate(0px, ${shakeY + cameraTranslateY}px) scale(${cameraZoom})`,
          transformOrigin: "540px 1300px",
        }}
      >
        <defs>
          {/* Flashlight Beam Gradient */}
          <linearGradient
            id="lightGradient"
            x1="0%"
            y1="100%"
            x2="0%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#FFEE44" stopOpacity="0.85" />
            <stop offset="60%" stopColor="#FFF275" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0.05" />
          </linearGradient>
        </defs>

        {/* Ground Line */}
        <Ground groundY={1450} />

        {/* Minimalist Living Room Couch */}
        <Couch x={380} groundY={1450} />

        {/* Stickman Character */}
        <PhoneStickman
          x={stickmanX}
          y={1450}
          pose={stickmanPose}
          frame={frame}
          flashlightOn={flashlightOn}
          facing={facing}
        />
      </svg>
    </AbsoluteFill>
  );
};
