import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video.jsx';

const FPS = 30;

export const Root = () => (
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
);
