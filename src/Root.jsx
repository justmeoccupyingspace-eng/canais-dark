import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video.jsx';
import {Lab} from './three/Lab.jsx';
import {Long, longDuration, Thumb} from './long/L1.jsx';

const FPS = 30;

export const Root = () => (
  <>
  <Composition id="Long" component={Long} width={1920} height={1080} fps={FPS} durationInFrames={FPS * 60}
    defaultProps={{spec: {channel: 'chartbound', shots: [], acts: [], total: 60}}}
    calculateMetadata={({props}) => ({durationInFrames: longDuration(props.spec)})} />
  <Composition id="Thumb" component={Thumb} width={1280} height={720} fps={FPS} durationInFrames={1} defaultProps={{spec: {channel: 'chartbound', data: {}}}} />
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
