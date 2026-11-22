import React from "react";
import { Composition } from "remotion";
import { StickmanDoor } from "./StickmanDoor";
import { PhonePanicShort } from "./PhonePanicShort";
import { ZackBatteryShort } from "./ZackBatteryShort";
import { GravityShortTest } from "./GravityShortTest";

export const Root: React.FC = () => {
  return (
    <>
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
    </>
  );
};
