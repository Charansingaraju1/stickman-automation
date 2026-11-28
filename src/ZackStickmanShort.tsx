import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Ground } from "./components/Ground";
import { Stickman, StickmanExpression, StickmanPose } from "./components/Stickman";
import { PhysicsModuleKind, StickmanPhysicsStage } from "./components/StickmanPhysicsStage";

export interface VectorSceneBeat {
  startSec: number;
  endSec: number;
  label: string;
  pose: StickmanPose;
  expression: StickmanExpression;
  module: PhysicsModuleKind;
  callout?: string;
  accentHex?: string;
  cameraZoom?: number;
  cameraPanY?: number;
}

export interface VectorWordTiming {
  word: string;
  start: number;
  end: number;
}

export type ZackStickmanShortProps = {
  title: string;
  durationSec: number;
  scenes: VectorSceneBeat[];
  words: VectorWordTiming[];
};

export const ZackStickmanShort: React.FC<ZackStickmanShortProps> = ({
  scenes,
  words,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  // Seamless return to Frame-0 state in last 0.45s for organic loop retention
  const loopCut = Math.max(0, durationInFrames / fps - 0.45);
  let activeIdx = scenes.findIndex((s) => t >= s.startSec && t < s.endSec);
  if (activeIdx < 0) activeIdx = Math.max(0, scenes.length - 1);
  if (t >= loopCut && scenes.length > 0) activeIdx = 0;

  const scene = scenes[activeIdx];
  const localFrame = Math.max(0, Math.round((t - scene.startSec) * fps));
  const pop = spring({ frame: localFrame, fps, config: { damping: 14, stiffness: 220 } });
  const zoom = interpolate(pop, [0, 1], [1.0, scene.cameraZoom ?? 1.08]);
  const panY = scene.cameraPanY ?? 0;

  const activeWords = React.useMemo(() => {
    const out: VectorWordTiming[][] = [];
    let cur: VectorWordTiming[] = [];
    for (const w of words) {
      cur.push(w);
      if (cur.length >= 3) {
        out.push(cur);
        cur = [];
      }
    }
    if (cur.length) out.push(cur);
    return out.find((c) => t >= c[0].start && t <= c[c.length - 1].end + 0.25) || [];
  }, [words, t]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#FAFAFA", overflow: "hidden" }}>
      <svg
        width={1080}
        height={1920}
        viewBox="0 0 1080 1920"
        style={{
          transform: `translateY(${panY}px) scale(${zoom})`,
          transformOrigin: "540px 1080px",
        }}
      >
        <Ground groundY={1450} />
        <Stickman
          x={380}
          y={1450}
          pose={scene.pose}
          expression={scene.expression}
          walkCycle={localFrame * 0.24}
          scale={1.35}
          sweat={scene.expression === "panic"}
        />
        <StickmanPhysicsStage
          kind={scene.module}
          frame={localFrame}
          accentHex={scene.accentHex || "#FF3B30"}
          callout={scene.callout}
        />
      </svg>

      {scene.label && (
        <div
          style={{
            position: "absolute",
            top: 135,
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "#000000",
            color: scene.accentHex || "#FFFFFF",
            padding: "10px 24px",
            borderRadius: 6,
            fontFamily: "Arial Black, Impact, sans-serif",
            fontSize: 34,
            fontWeight: 900,
            letterSpacing: 1.5,
          }}
        >
          {scene.label}
        </div>
      )}

      {activeWords.length > 0 && (
        <div
          style={{
            position: "absolute",
            bottom: 430,
            left: 56,
            right: 110,
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 14,
          }}
        >
          {activeWords.map((w, idx) => {
            const isNow = t >= w.start && t <= w.end + 0.1;
            return (
              <span
                key={`${w.start}-${idx}`}
                style={{
                  fontFamily: "Impact, Arial Black, sans-serif",
                  fontSize: isNow ? 92 : 82,
                  color: isNow ? (scene.accentHex || "#FF3B30") : "#000000",
                  WebkitTextStroke: "3px #FAFAFA",
                  lineHeight: 1.05,
                }}
              >
                {w.word.toUpperCase()}
              </span>
            );
          })}
        </div>
      )}
    </AbsoluteFill>
  );
};
