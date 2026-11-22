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
import { ZackCaptions } from "./components/ZackCaptions";
import { AnatomyDiagram } from "./components/AnatomyDiagram";
import { Ground } from "./components/Ground";

export const ZackBatteryShort: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Camera zoom choreography into the esophagus cross-section
  const cameraZoom = interpolate(
    frame,
    [70, 95, 710, 740],
    [1.0, 1.35, 1.35, 1.0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const cameraTranslateY = interpolate(
    frame,
    [70, 95, 710, 740],
    [0, 40, 40, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Subtle heartbeat pulse shake during danger phase (frames 510 to 680)
  let dangerShakeY = 0;
  if (frame >= 510 && frame < 680) {
    dangerShakeY = Math.sin(frame * 0.4) * 5;
  }

  // Full body stickman coordinates (for wide shot frames 0 - 75 and 740 - 900)
  const isFullBody = frame < 85 || frame >= 730;

  // Swallowing animation at frame 45-60
  const isSwallowing = frame >= 45 && frame < 75;

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
      {/* 1. Gulp / Swallow */}
      <Sequence from={48} durationInFrames={20}>
        <Audio src={staticFile("gulp_sfx.wav")} volume={1.0} />
      </Sequence>

      {/* 2. Zoom Whoosh */}
      <Sequence from={72} durationInFrames={25}>
        <Audio src={staticFile("whoosh_sfx.wav")} volume={0.85} />
      </Sequence>

      {/* 3. Electric Zap */}
      <Sequence from={175} durationInFrames={30}>
        <Audio src={staticFile("zap_sfx.wav")} volume={0.9} />
      </Sequence>

      {/* 4. Chemical Fizz */}
      <Sequence from={340} durationInFrames={40}>
        <Audio src={staticFile("fizz_sfx.wav")} volume={0.8} />
      </Sequence>

      {/* 5. Heartbeat / Danger Warning */}
      <Sequence from={520} durationInFrames={45}>
        <Audio src={staticFile("heartbeat_sfx.wav")} volume={1.0} />
      </Sequence>

      {/* 6. Medical Honey Chime */}
      <Sequence from={710} durationInFrames={35}>
        <Audio src={staticFile("chime_sfx.wav")} volume={0.95} />
      </Sequence>

      {/* --- ZACK D FILMS SCIENTIFIC VOICEOVER --- */}
      {/* Segment 1: "If you accidentally swallow a button battery..." */}
      <Sequence from={10} durationInFrames={150}>
        <Audio src={staticFile("zack_vo1.mp3")} volume={1.0} />
      </Sequence>

      {/* Segment 2: "Inside your throat, the moisture completes an electric circuit..." */}
      <Sequence from={170} durationInFrames={155}>
        <Audio src={staticFile("zack_vo2.mp3")} volume={1.0} />
      </Sequence>

      {/* Segment 3: "This current creates sodium hydroxide..." */}
      <Sequence from={335} durationInFrames={170}>
        <Audio src={staticFile("zack_vo3.mp3")} volume={1.0} />
      </Sequence>

      {/* Segment 4: "In less than two hours, this chemical dissolves right through..." */}
      <Sequence from={515} durationInFrames={190}>
        <Audio src={staticFile("zack_vo4.mp3")} volume={1.0} />
      </Sequence>

      {/* Segment 5: "This is why doctors say: swallow two spoonfuls of honey..." */}
      <Sequence from={705} durationInFrames={192}>
        <Audio src={staticFile("zack_vo5.mp3")} volume={1.0} />
      </Sequence>

      {/* Upper-Third Captions Overlay */}
      <ZackCaptions />

      {/* Main SVG Visual Scene */}
      <svg
        width={1080}
        height={1920}
        viewBox="0 0 1080 1920"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translate(0px, ${cameraTranslateY + dangerShakeY}px) scale(${cameraZoom})`,
          transformOrigin: "540px 980px",
        }}
      >
        {/* Ground Line */}
        <Ground groundY={1450} />

        {/* ANATOMICAL CROSS-SECTION (Visible during zoom frames 75 to 740) */}
        <AnatomyDiagram frame={frame} />

        {/* FULL BODY STICKMAN (Intro 0-80 and Outro 730-900) */}
        {isFullBody && (
          <g transform="translate(540, 1450)">
            {/* Torso */}
            <line
              x1={0}
              y1={-270}
              x2={0}
              y2={-180}
              stroke="#000000"
              strokeWidth={16}
              strokeLinecap="round"
            />

            {/* Legs */}
            <path
              d="M 0 -180 L -25 -90 L -35 0"
              fill="none"
              stroke="#000000"
              strokeWidth={14}
              strokeLinecap="round"
            />
            <path
              d="M 0 -180 L 25 -90 L 35 0"
              fill="none"
              stroke="#000000"
              strokeWidth={14}
              strokeLinecap="round"
            />

            {/* Arms & Hands */}
            {frame < 75 ? (
              // Intro: Holding battery up to mouth
              <g>
                <path
                  d="M 0 -270 L -35 -200 L -25 -140"
                  fill="none"
                  stroke="#000000"
                  strokeWidth={14}
                  strokeLinecap="round"
                />
                <path
                  d={`M 0 -270 L 45 -220 L ${isSwallowing ? 15 : 45} ${isSwallowing ? -310 : -270}`}
                  fill="none"
                  stroke="#000000"
                  strokeWidth={14}
                  strokeLinecap="round"
                />
                {!isSwallowing && (
                  <circle
                    cx={50}
                    cy={-285}
                    r={18}
                    fill="#BDC3C7"
                    stroke="#000000"
                    strokeWidth={5}
                  />
                )}
              </g>
            ) : (
              // Outro: Holding honey jar and spoon with ER hospital symbol
              <g>
                <path
                  d="M 0 -270 L -45 -210 L -45 -160"
                  fill="none"
                  stroke="#000000"
                  strokeWidth={14}
                  strokeLinecap="round"
                />
                <g transform="translate(-75, -190)">
                  <rect
                    x={-30}
                    y={-40}
                    width={60}
                    height={75}
                    rx={12}
                    fill="#F39C12"
                    stroke="#000000"
                    strokeWidth={8}
                  />
                  <rect
                    x={-20}
                    y={-50}
                    width={40}
                    height={14}
                    rx={4}
                    fill="#F1C40F"
                    stroke="#000000"
                    strokeWidth={6}
                  />
                  <text
                    x={0}
                    y={5}
                    textAnchor="middle"
                    fill="#FFFFFF"
                    fontFamily="'Arial Black', Impact, sans-serif"
                    fontSize={18}
                    fontWeight={900}
                  >
                    HONEY
                  </text>
                </g>

                <path
                  d="M 0 -270 L 45 -210 L 55 -210"
                  fill="none"
                  stroke="#000000"
                  strokeWidth={14}
                  strokeLinecap="round"
                />
                <circle cx={62} cy={-215} r={8} fill="#000000" />
              </g>
            )}

            {/* Head */}
            <circle
              cx={isSwallowing ? 15 : 0}
              cy={isSwallowing ? -330 : -340}
              r={38}
              fill="#000000"
            />

            {/* Throat swallow bulge */}
            {isSwallowing && (
              <circle cx={10} cy={-280} r={16} fill="#BDC3C7" stroke="#000000" strokeWidth={4} />
            )}

            {/* Outro ER Hospital Cross Badge */}
            {frame >= 730 && (
              <g transform="translate(180, -220)">
                <circle cx={0} cy={0} r={65} fill="#E74C3C" stroke="#000000" strokeWidth={10} />
                <rect x={-14} y={-40} width={28} height={80} rx={6} fill="#FFFFFF" />
                <rect x={-40} y={-14} width={80} height={28} rx={6} fill="#FFFFFF" />
                <text
                  x={0}
                  y={95}
                  textAnchor="middle"
                  fill="#C0392B"
                  fontFamily="'Arial Black', Impact, sans-serif"
                  fontSize={26}
                  fontWeight={900}
                  letterSpacing={2}
                >
                  RUSH TO ER
                </text>
              </g>
            )}
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};
