import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Stickman } from "./components/Stickman";

export interface SceneBeat {
  startSec: number;
  endSec: number;
  label: string;
  labelColor?: string;
  pose:
    | "walk"
    | "push"
    | "charge"
    | "ram_hold"
    | "kneel"
    | "look_up"
    | "casual_walk"
    | "casual_stand"
    | "pull_door";
  motion: "hook_punch" | "punch4" | "pan" | "zoom" | "shake" | "push";
  imgPath?: string; // relative to public/
  fx: "crack" | "xray" | "gel" | "bubble" | "steam" | "toxic" | "fire" | "seed" | "chill" | "sleep";
  callout?: string;
}

export interface WordTiming {
  word: string;
  start: number;
  end: number;
  mode: string;
  scene_id: string;
}

export interface CloudShortProps {
  title: string;
  bgHex: string;
  accentHex: string;
  propKind: SceneBeat["fx"];
  durationSec?: number;
  scenes: SceneBeat[];
  words: WordTiming[];
  loopBackStartSec?: number;
}

const MODE_COLOR: Record<string, string> = {
  alert: "#FF3B30",
  panic: "#FF453A",
  doc: "#00D4FF",
  loop: "#FFD60A",
};

const AnimatedOverlayFx: React.FC<{ fx: SceneBeat["fx"]; frame: number }> = ({ fx, frame }) => {
  if (fx === "xray") {
    const scanY = (frame * 26) % 1920;
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        <rect x={0} y={scanY} width={1080} height={14} fill="#00E5FF" opacity={0.45} />
        <circle
          cx={540}
          cy={940}
          r={120 + (frame % 20) * 14}
          fill="none"
          stroke="#00E5FF"
          strokeWidth={6}
          opacity={Math.max(0, 1 - (frame % 20) / 20)}
        />
      </svg>
    );
  }
  if (fx === "bubble" || fx === "seed" || fx === "toxic") {
    const col = fx === "toxic" ? "#C0FF33" : fx === "seed" ? "#34D399" : "#FFFFFF";
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        {[0, 1, 2, 3, 4, 5].map((i) => {
          const t = (frame * 1.6 + i * 11) % 36;
          const r = 20 + t * 9;
          const cy = 980 - i * 38 + Math.sin(frame * 0.25 + i) * 28;
          const cx = 360 + ((i * 113) % 360);
          return (
            <circle
              key={i}
              cx={cx}
              cy={cy}
              r={r}
              fill="none"
              stroke={col}
              strokeWidth={5}
              opacity={Math.max(0, 0.7 - t / 36)}
            />
          );
        })}
      </svg>
    );
  }
  if (fx === "crack" || fx === "fire" || fx === "steam") {
    const col = fx === "fire" ? "#FF6B00" : fx === "steam" ? "#E2E8F0" : "#FF3B30";
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        {[0, 1, 2, 3].map((i) => {
          const ang = (i * 90 + 35 + frame * 2) * (Math.PI / 180);
          const d0 = 90 + (frame % 12) * 10;
          const d1 = d0 + 60;
          return (
            <line
              key={i}
              x1={540 + Math.cos(ang) * d0}
              y1={760 + Math.sin(ang) * d0}
              x2={540 + Math.cos(ang) * d1}
              y2={760 + Math.sin(ang) * d1}
              stroke={col}
              strokeWidth={10}
              strokeLinecap="round"
              opacity={0.75}
            />
          );
        })}
      </svg>
    );
  }
  return null;
};

const ScenarioPropSvg: React.FC<{ fx: SceneBeat["fx"]; localFrame: number }> = ({ fx, localFrame }) => {
  const pulse = 1 + 0.08 * Math.sin(localFrame * 0.45);
  const propsMap: Partial<Record<SceneBeat["fx"], React.ReactNode>> = {
    crack: (
      <g transform={`translate(560, 1080) scale(${pulse})`}>
        <path d="M-24 20 L0 -65 L28 -10 L62 -72" fill="none" stroke="#FF3B30" strokeWidth={12} strokeLinecap="round" />
        <circle cx={0} cy={0} r={34} fill="none" stroke="#111827" strokeWidth={8} />
      </g>
    ),
    steam: (
      <g transform="translate(565, 1140)">
        <rect x={-48} y={-55} width={96} height={110} rx={16} fill="#334155" stroke="#0F172A" strokeWidth={6} />
        <rect x={-30} y={-20} width={60} height={60} rx={8} fill="#86EFAC" />
        <path d={`M-15 -70 Q${-35 + Math.sin(localFrame * 0.3) * 14} -115 -10 -150`} fill="none" stroke="#94A3B8" strokeWidth={8} strokeLinecap="round" />
        <path d={`M18 -70 Q${35 - Math.sin(localFrame * 0.3) * 14} -115 15 -150`} fill="none" stroke="#94A3B8" strokeWidth={8} strokeLinecap="round" />
      </g>
    ),
    seed: (
      <g transform={`translate(570, 1120) scale(${pulse})`}>
        <path d="M-65 30 A70 70 0 0 0 65 30 Z" fill="#EF4444" stroke="#15803D" strokeWidth={12} />
        <ellipse cx={0} cy={-40 + ((localFrame * 8) % 60)} rx={9} ry={15} fill="#111827" />
      </g>
    ),
    toxic: (
      <g transform="translate(575, 1135)">
        <rect x={-55} y={-40} width={44} height={90} rx={8} fill="#38BDF8" stroke="#0F172A" strokeWidth={5} />
        <rect x={12} y={-40} width={44} height={90} rx={8} fill="#FACC15" stroke="#0F172A" strokeWidth={5} />
        <circle cx={0} cy={-85 - (localFrame % 16) * 4} r={24 + (localFrame % 16) * 2} fill="#BEF264" opacity={0.75} />
      </g>
    ),
    fire: (
      <g transform={`translate(565, 1140) scale(${pulse})`}>
        <ellipse cx={0} cy={45} rx={72} ry={18} fill="#1F2937" />
        <path d="M-32 40 Q-50 -45 0 -105 Q50 -45 32 40 Z" fill="#F97316" />
        <path d="M-16 40 Q-25 -15 0 -62 Q25 -15 16 40 Z" fill="#FACC15" />
      </g>
    ),
    chill: (
      <g transform={`translate(570, 1130) scale(${pulse})`}>
        <path d="M-12 -55 C25 -45 42 5 22 55 C5 20 -25 5 -12 -55 Z" fill="#DC2626" />
        <circle cx={40} cy={-35 + (localFrame % 18) * 3} r={12} fill="#38BDF8" />
      </g>
    ),
    sleep: (
      <g transform="translate(565, 1135)">
        <rect x={-55} y={-20} width={40} height={60} rx={6} fill="#78350F" stroke="#111827" strokeWidth={5} />
        <rect x={0} y={-20} width={40} height={60} rx={6} fill="#78350F" stroke="#111827" strokeWidth={5} />
        <text x={-10} y={-55 - (localFrame % 20)} fill="#EF4444" fontSize={42} fontWeight={900}>Zzz</text>
      </g>
    ),
  };
  return <>{propsMap[fx] || null}</>;
};

const StickmanComedyStage: React.FC<{
  scene: SceneBeat;
  localFrame: number;
  bgHex: string;
  accentHex: string;
}> = ({ scene, localFrame, bgHex, accentHex }) => {
  const popScale = spring({ frame: localFrame, fps: 30, config: { damping: 12, stiffness: 220 } });
  const bounceY = Math.sin(localFrame * 0.35) * 12;
  const friendDropY = Math.min(180, localFrame * 12);
  const friendRot = Math.min(68, localFrame * 3.6);
  const showCallout = Boolean(scene.callout && scene.callout.toUpperCase() !== (scene.label || "").toUpperCase());

  return (
    <AbsoluteFill style={{ backgroundColor: bgHex }}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920">
        {/* Elevated stage horizon so bottom safe-zone captions NEVER collide with characters */}
        <rect x={0} y={1160} width={1080} height={760} fill="#F1F5F9" />
        <line x1={0} y1={1160} x2={1080} y2={1160} stroke="#CBD5E1" strokeWidth={6} />

        {/* Dynamic background accent halo */}
        <circle cx={540} cy={780} r={330 + Math.sin(localFrame * 0.25) * 18} fill={accentHex} opacity={0.14} />

        {/* Fainting buddy stickman in background */}
        <g transform={`translate(790, ${1160 + friendDropY * 0.22}) rotate(${friendRot}, 0, -180)`}>
          <Stickman x={0} y={0} pose="kneel" facing="left" dizzy scale={0.95} />
        </g>

        {/* Lead Stickman center-left stage cleanly above captions */}
        <g transform={`translate(390, ${1180 + bounceY}) scale(${1.12 + 0.14 * popScale})`}>
          <Stickman
            x={0}
            y={0}
            pose={scene.pose}
            walkCycle={localFrame * 0.45}
            facing="right"
            sweat={scene.motion === "shake" || scene.fx === "fire"}
            dizzy={scene.fx === "sleep"}
            scale={1.12}
          />
        </g>

        <g transform="translate(0, -190)">
          <ScenarioPropSvg fx={scene.fx} localFrame={localFrame} />
        </g>

        {showCallout && (
          <g transform={`translate(540, ${380 - popScale * 16})`}>
            <rect x={-280} y={-50} width={560} height={100} rx={22} fill="#111827" />
            <text
              x={0}
              y={14}
              textAnchor="middle"
              fill={accentHex}
              fontFamily="Arial Black, Impact, sans-serif"
              fontSize={44}
              fontWeight={900}
            >
              {scene.callout}
            </text>
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};

export const CloudShort: React.FC<CloudShortProps> = ({
  bgHex,
  accentHex,
  scenes,
  words,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  // Determine current active scene beat (cut cleanly back to Scene 0 on final 0.45s for seamless feed loop!)
  const loopCutoff = Math.max(0, durationInFrames / fps - 0.45);
  let activeIdx = scenes.findIndex((s) => t >= s.startSec && t < s.endSec);
  if (activeIdx < 0) activeIdx = Math.max(0, scenes.length - 1);
  if (t >= loopCutoff && scenes.length > 0) activeIdx = 0;

  const scene = scenes[activeIdx];
  const localFrame = Math.max(0, Math.round((t - scene.startSec) * fps));

  // Punchy Frame-0 / cut motion curves
  let scale = 1.0;
  let tx = 0;
  let ty = 0;
  if (scene.motion === "hook_punch" || scene.motion === "punch4") {
    scale = Math.min(1.22, 1.0 + 0.16 * Math.min(1, localFrame / 4) + localFrame * 0.0012);
  } else if (scene.motion === "shake") {
    scale = 1.12;
    tx = Math.sin(localFrame * 2.1) * 14;
    ty = Math.cos(localFrame * 2.4) * 10;
  } else if (scene.motion === "zoom") {
    scale = Math.min(1.24, 1.02 + localFrame * 0.003);
  } else {
    scale = interpolate(localFrame, [0, 90], [1.14, 1.0], { extrapolateRight: "clamp" });
  }

  // Group word timings into 3-word punch chunks matching ASS safe zone
  const activeChunk = React.useMemo(() => {
    const chunks: WordTiming[][] = [];
    let cur: WordTiming[] = [];
    for (const w of words) {
      if (cur.length && (w.scene_id !== cur[cur.length - 1].scene_id || cur.length >= 3)) {
        chunks.push(cur);
        cur = [];
      }
      cur.push(w);
    }
    if (cur.length) chunks.push(cur);
    return chunks.find((c) => t >= c[0].start && t <= c[c.length - 1].end + 0.28) || [];
  }, [words, t]);

  return (
    <AbsoluteFill style={{ backgroundColor: bgHex, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transform: `translate(${tx}px, ${ty}px) scale(${scale})`,
          transformOrigin: "center center",
        }}
      >
        {scene.imgPath ? (
          <Img
            src={staticFile(scene.imgPath)}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <StickmanComedyStage scene={scene} localFrame={localFrame} bgHex={bgHex} accentHex={accentHex} />
        )}
      </AbsoluteFill>

      <AnimatedOverlayFx fx={scene.fx} frame={localFrame} />

      {/* Crisp top diagnostic pill */}
      {scene.label && (
        <div
          style={{
            position: "absolute",
            top: 120,
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "rgba(17, 24, 39, 0.86)",
            border: `4px solid ${scene.labelColor || accentHex}`,
            color: scene.labelColor || "#FFFFFF",
            padding: "10px 26px",
            borderRadius: 12,
            fontFamily: "Arial Black, Impact, sans-serif",
            fontSize: 34,
            fontWeight: 900,
            letterSpacing: 1.2,
            whiteSpace: "nowrap",
          }}
        >
          {scene.label}
        </div>
      )}

      {/* Word-by-word safe-zone kinetic captions */}
      {activeChunk.length > 0 && (
        <div
          style={{
            position: "absolute",
            bottom: 360,
            left: 56,
            right: 110,
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 14,
          }}
        >
          {activeChunk.map((w, idx) => {
            const isNow = t >= w.start && t <= w.end + 0.1;
            const col = isNow ? MODE_COLOR[w.mode] || accentHex : t > w.end ? "#FFFFFF" : "#D1D5DB";
            return (
              <span
                key={`${w.start}-${idx}`}
                style={{
                  fontFamily: "Impact, Arial Black, sans-serif",
                  fontSize: isNow ? 88 : 78,
                  color: col,
                  WebkitTextStroke: "5px #000000",
                  textShadow: "0 8px 18px rgba(0,0,0,0.85)",
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
