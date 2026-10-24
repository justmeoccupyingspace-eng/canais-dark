import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {Mascot, Shadow, Lights} from './Mascot.jsx';

export const Lab = ({m}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: m.bg}}>
      <ThreeCanvas width={1080} height={1920} camera={{fov: 30, position: [0, 0.6, 14]}} gl={{antialias: true, alpha: true}}>
        <Lights />
        <Shadow position={[0, -1.62 * 1.5 - 0.5, 0]} scale={2.2} />
        <Mascot color={m.color} belly={m.belly} acc={m.acc} accent={m.accent} pose={m.pose} talk={m.talk ? (Math.sin(f / 2.2) + 1) / 2 : 0} look={m.look || [0, 0]} scale={1.5} position={[0, -0.5, 0]} />
      </ThreeCanvas>
      <div style={{position: 'absolute', top: 170, width: '100%', textAlign: 'center', fontFamily: 'Inter, Arial', fontWeight: 900, fontSize: 90, color: m.ink || '#fff'}}>{m.title}</div>
    </AbsoluteFill>
  );
};
