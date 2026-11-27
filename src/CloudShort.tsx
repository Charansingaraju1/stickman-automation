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
  panic: "#FF3B30",
  doc: "#00E5FF",
  loop: "#FFD60A",
};

const AnimatedOverlayFx: React.FC<{ fx: SceneBeat["fx"]; frame: number }> = ({ fx, frame }) => {
  if (fx === "xray") {
    const scanY = (frame * 26) % 1920;
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        <rect x={0} y={scanY} width={1080} height={12} fill="#00E5FF" opacity={0.42} />
        <circle
          cx={540}
          cy={940}
          r={120 + (frame % 20) * 14}
          fill="none"
          stroke="#00E5FF"
          strokeWidth={5}
          opacity={Math.max(0, 1 - (frame % 20) / 20)}
        />
      </svg>
    );
  }
  if (fx === "bubble" || fx === "seed" || fx === "toxic") {
    const col = fx === "toxic" ? "#C0FF33" : fx === "seed" ? "#34D399" : "#FFFFFF";
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        {[0, 1, 2, 3, 4].map((i) => {
          const t = (frame * 1.6 + i * 11) % 36;
          const r = 18 + t * 8;
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
              strokeWidth={4}
              opacity={Math.max(0, 0.55 - t / 36)}
            />
          );
        })}
      </svg>
    );
  }
  if (fx === "fire" || fx === "steam") {
    const col = fx === "fire" ? "#FF6B00" : "#94A3B8";
    return (
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        {[0, 1, 2, 3].map((i) => {
          const drift = ((frame * 5 + i * 35) % 140);
          return (
            <circle
              key={i}
              cx={480 + Math.sin(frame * 0.15 + i) * 65}
              cy={880 - drift}
              r={18 + drift * 0.15}
              fill={col}
              opacity={Math.max(0, 0.32 - drift / 350)}
            />
          );
        })}
      </svg>
    );
  }
  return null;
};

// Matte-white 3D-shaded Stickman figure matching StickNation's cinema house look
const Matte3DStickman: React.FC<{
  pose: SceneBeat["pose"];
  localFrame: number;
  shock?: boolean;
}> = ({ pose, localFrame, shock = false }) => {
  const headBob = Math.sin(localFrame * 0.35) * 10;
  const lean = pose === "charge" || pose === "kneel" ? 14 : 0;
  const armUp = pose === "pull_door" || pose === "look_up" || shock;

  return (
    <g transform={`translate(540, ${1140 + headBob}) rotate(${lean})`}>
      <defs>
        <radialGradient id="stick3dHead" cx="38%" cy="32%" r="68%">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="68%" stopColor="#E2E8F0" />
          <stop offset="100%" stopColor="#94A3B8" />
        </radialGradient>
        <linearGradient id="stick3dLimb" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="60%" stopColor="#CBD5E1" />
          <stop offset="100%" stopColor="#64748B" />
        </linearGradient>
      </defs>

      {/* Legs */}
      <path d="M-24 -160 L-58 -60 L-75 40" fill="none" stroke="url(#stick3dLimb)" strokeWidth={34} strokeLinecap="round" strokeLinejoin="round" />
      <path d="M24 -160 L58 -60 L75 40" fill="none" stroke="url(#stick3dLimb)" strokeWidth={34} strokeLinecap="round" strokeLinejoin="round" />

      {/* Torso */}
      <rect x={-44} y={-340} width={88} height={195} rx={44} fill="url(#stick3dHead)" />

      {/* Arms */}
      <path
        d={armUp ? "M-38 -310 L-105 -250 L-85 -190" : "M-38 -310 L-82 -215 L-65 -140"}
        fill="none"
        stroke="url(#stick3dLimb)"
        strokeWidth={30}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d={armUp ? "M38 -310 L118 -275 L92 -215" : "M38 -310 L82 -215 L65 -140"}
        fill="none"
        stroke="url(#stick3dLimb)"
        strokeWidth={30}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Rounded 3D Head + Expressive Eyes */}
      <circle cx={0} cy={-445} r={108} fill="url(#stick3dHead)" />
      {/* Brows */}
      <path d="M-54 -488 Q-32 -504 -12 -486" fill="none" stroke="#1E293B" strokeWidth={10} strokeLinecap="round" />
      <path d="M12 -486 Q34 -504 54 -488" fill="none" stroke="#1E293B" strokeWidth={10} strokeLinecap="round" />
      {/* Eyes */}
      <ellipse cx={-34} cy={-452} rx={22} ry={shock ? 28 : 24} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={3} />
      <ellipse cx={34} cy={-452} rx={22} ry={shock ? 28 : 24} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={3} />
      <circle cx={-30} cy={-450} r={9} fill="#0F172A" />
      <circle cx={38} cy={-450} r={9} fill="#0F172A" />
      {/* Mouth */}
      {shock ? (
        <ellipse cx={0} cy={-392} rx={26} ry={22} fill="#1E293B" />
      ) : (
        <path d="M-26 -394 Q0 -380 26 -396" fill="none" stroke="#1E293B" strokeWidth={9} strokeLinecap="round" />
      )}
    </g>
  );
};

const DarkScenarioProp: React.FC<{ fx: SceneBeat["fx"]; localFrame: number }> = ({ fx, localFrame }) => {
  const pulse = 1 + 0.08 * Math.sin(localFrame * 0.45);
  if (fx === "seed") {
    return (
      <g transform={`translate(760, 860) scale(${pulse})`}>
        <ellipse cx={0} cy={0} rx={82} ry={108} fill="none" stroke="#FF6B6B" strokeWidth={14} opacity={0.88} />
        <ellipse cx={0} cy={35} rx={64} ry={58} fill="#84CC16" opacity={0.55} />
        <ellipse cx={0} cy={-20 + (localFrame * 4) % 55} rx={12} ry={20} fill="#111827" stroke="#FFFFFF" strokeWidth={3} />
      </g>
    );
  }
  if (fx === "steam") {
    return (
      <g transform={`translate(765, 870) scale(${pulse})`}>
        <rect x={-64} y={-70} width={128} height={140} rx={20} fill="#1E293B" stroke="#00E5FF" strokeWidth={6} />
        <rect x={-42} y={-32} width={84} height={80} rx={10} fill="#22C55E" opacity={0.8} />
      </g>
    );
  }
  if (fx === "toxic") {
    return (
      <g transform={`translate(765, 870) scale(${pulse})`}>
        <circle cx={0} cy={0} r={85} fill="#84CC16" opacity={0.25} />
        <rect x={-52} y={-40} width={44} height={92} rx={8} fill="#38BDF8" />
        <rect x={10} y={-40} width={44} height={92} rx={8} fill="#FACC15" />
      </g>
    );
  }
  return null;
};

const StickmanCinemaStage: React.FC<{
  scene: SceneBeat;
  localFrame: number;
  accentHex: string;
}> = ({ scene, localFrame, accentHex }) => {
  const popScale = spring({ frame: localFrame, fps: 30, config: { damping: 14, stiffness: 210 } });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0B1120" }}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920">
        <defs>
          <radialGradient id="cinemaSpotlight" cx="50%" cy="46%" r="58%">
            <stop offset="0%" stopColor="#1E293B" />
            <stop offset="65%" stopColor="#0F172A" />
            <stop offset="100%" stopColor="#050811" />
          </radialGradient>
        </defs>
        <rect x={0} y={0} width={1080} height={1920} fill="url(#cinemaSpotlight)" />
        <ellipse cx={540} cy={1210} rx={360} ry={48} fill={accentHex} opacity={0.18} />
        <g transform={`scale(${0.96 + 0.08 * popScale})`} style={{ transformOrigin: "540px 960px" }}>
          <Matte3DStickman pose={scene.pose} localFrame={localFrame} shock={scene.motion === "shake" || scene.motion === "hook_punch"} />
        </g>
        <DarkScenarioProp fx={scene.fx} localFrame={localFrame} />
      </svg>
    </AbsoluteFill>
  );
};

export const CloudShort: React.FC<CloudShortProps> = ({
  accentHex,
  scenes,
  words,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  // Seamless feed loop: cut back cleanly to Frame 0 scene right before end
  const loopCutoff = Math.max(0, durationInFrames / fps - 0.45);
  let activeIdx = scenes.findIndex((s) => t >= s.startSec && t < s.endSec);
  if (activeIdx < 0) activeIdx = Math.max(0, scenes.length - 1);
  if (t >= loopCutoff && scenes.length > 0) activeIdx = 0;

  const scene = scenes[activeIdx];
  const localFrame = Math.max(0, Math.round((t - scene.startSec) * fps));

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
    <AbsoluteFill style={{ backgroundColor: "#090D16", overflow: "hidden" }}>
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
          <StickmanCinemaStage scene={scene} localFrame={localFrame} accentHex={accentHex} />
        )}
      </AbsoluteFill>

      {/* Cinema dark radial vignette to match Mentos / Q-Tips / Fish Bone */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle at 50% 45%, transparent 48%, rgba(5,8,16,0.55) 100%)",
          pointerEvents: "none",
        }}
      />

      <AnimatedOverlayFx fx={scene.fx} frame={localFrame} />

      {/* Clean signature RefTag matching short_builder.py style */}
      {scene.label && (
        <div
          style={{
            position: "absolute",
            top: 135,
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "rgba(0, 0, 0, 0.72)",
            color: scene.labelColor || "#00E5FF",
            padding: "8px 22px",
            borderRadius: 6,
            fontFamily: "Arial Black, Impact, sans-serif",
            fontSize: 34,
            fontWeight: 900,
            letterSpacing: 1.5,
            whiteSpace: "nowrap",
          }}
        >
          {scene.label}
        </div>
      )}

      {/* Unified Impact safe-zone word captions */}
      {activeChunk.length > 0 && (
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
          {activeChunk.map((w, idx) => {
            const isNow = t >= w.start && t <= w.end + 0.1;
            const col = isNow ? MODE_COLOR[w.mode] || "#FFD60A" : t > w.end ? "#FFFFFF" : "#A1A1AA";
            return (
              <span
                key={`${w.start}-${idx}`}
                style={{
                  fontFamily: "Impact, Arial Black, sans-serif",
                  fontSize: isNow ? 94 : 84,
                  color: col,
                  WebkitTextStroke: "5px #000000",
                  textShadow: "0 8px 18px rgba(0,0,0,0.92)",
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
