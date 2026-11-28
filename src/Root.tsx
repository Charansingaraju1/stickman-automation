import React from "react";
import { Composition, Still } from "remotion";
import { StickmanDoor } from "./StickmanDoor";
import { PhonePanicShort } from "./PhonePanicShort";
import { ZackBatteryShort } from "./ZackBatteryShort";
import { GravityShortTest } from "./GravityShortTest";
import { CloudShort, CloudShortProps } from "./CloudShort";
import { CloudLongThumbnail, CloudThumbnail, CloudThumbnailProps } from "./CloudThumbnail";
import { ZackStickmanShort, ZackStickmanShortProps } from "./ZackStickmanShort";

const DEFAULT_CLOUD_SHORT: CloudShortProps = {
  title: "StickNation Cloud Short",
  bgHex: "#FFF8F1",
  accentHex: "#F38020",
  propKind: "crack",
  durationSec: 20,
  scenes: [
    { startSec: 0, endSec: 4, label: "TOO CRUNCHY", pose: "pull_door", motion: "hook_punch", fx: "crack", callout: "CRACK!" },
  ],
  words: [],
};

const DEFAULT_THUMB: CloudThumbnailProps = {
  topBadge: "DON'T DO THIS",
  headline: "100% SHOCK",
  accentHex: "#F38020",
};

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="CloudShort"
        component={CloudShort}
        durationInFrames={600}
        calculateMetadata={({ props }: { props: CloudShortProps }) => ({
          durationInFrames: Math.max(90, Math.round((props.durationSec || 20) * 30)),
        })}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={DEFAULT_CLOUD_SHORT}
      />
      <Still
        id="CloudThumbnail"
        component={CloudThumbnail}
        width={1080}
        height={1920}
        defaultProps={DEFAULT_THUMB}
      />
      <Still
        id="CloudLongThumbnail"
        component={CloudLongThumbnail}
        width={1280}
        height={720}
        defaultProps={{
          topBadge: "7 TRAPS",
          headline: "DON'T BLINK!",
          accentHex: "#FFD60A",
          primaryImgPath: "scenes/mentos_cola/scene_3_eruption.jpg",
          secondaryImgPath: "scenes/knuckle_cracking/scene_2_xray_bones.jpg",
        }}
      />
      <Composition
        id="GravityShortTest"
        component={GravityShortTest}
        durationInFrames={944}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="ZackBatteryExplainer"
        component={ZackBatteryShort}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="PhonePanic"
        component={PhonePanicShort}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="StickmanDoor"
        component={StickmanDoor}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="ZackStickmanShort"
        component={ZackStickmanShort}
        durationInFrames={600}
        calculateMetadata={({ props }: { props: ZackStickmanShortProps }) => ({
          durationInFrames: Math.max(90, Math.round((props.durationSec || 20) * 30)),
        })}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "B&W Vector Stickman Pilot",
          durationSec: 18,
          scenes: [
            {
              startSec: 0,
              endSec: 4,
              label: "400F GREASE TRAP",
              pose: "point",
              expression: "shock",
              module: "explosion_safe",
              callout: "1700x STEAM",
              accentHex: "#FF3B30",
              cameraZoom: 1.08,
            },
          ],
          words: [],
        }}
      />
    </>
  );
};
