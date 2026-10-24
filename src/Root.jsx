import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video.jsx';
import {Lab} from './three/Lab.jsx';

const FPS = 30;

export const Root = () => (
  <>
  <Composition id="Lab" component={Lab} width={1080} height={1920} fps={FPS} durationInFrames={120} defaultProps={{m: {bg: '#0b0d0a', color: '#ffb000', belly: '#ffe6a3', acc: 'antenna', accent: '#ff5d73', pose: 'wave', title: 'How It Ticks'}}} />
  <Composition
    id="Short"
    component={Video}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={FPS * 30}
    defaultProps={{spec: {channel: 'chartbound', title: 'Demo', scenes: []}}}
    calculateMetadata={({props}) => {
      const total = props.spec.scenes.reduce((s, sc) => s + Math.ceil((sc.duration || 4) * FPS), 0);
      return {durationInFrames: Math.max(total, FPS)};
    }}
  />

  </>
);
