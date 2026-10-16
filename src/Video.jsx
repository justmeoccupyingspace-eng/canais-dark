import React from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {THEMES} from './themes.js';
import {TitleScene, ChartScene, StatScene, TextScene} from './scenes.jsx';

const FPS = 30;

export const Video = ({spec}) => {
  const theme = THEMES[spec.channel] || THEMES.chartbound;
  let from = 0;
  const seqs = spec.scenes.map((sc, i) => {
    const dur = Math.ceil((sc.duration || 4) * FPS);
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <Scene sc={sc} theme={theme} spec={spec} />
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
      </Sequence>
    );
    from += dur;
    return el;
  });
  return (
    <AbsoluteFill style={{background: theme.bg, fontFamily: theme.font, color: theme.ink}}>
      {seqs}
      <Footer theme={theme} />
      {spec.music ? <Audio src={staticFile(spec.music)} volume={0.08} loop /> : null}
    </AbsoluteFill>
  );
};

const Scene = ({sc, theme, spec}) => {
  switch (sc.type) {
    case 'title': return <TitleScene sc={sc} theme={theme} spec={spec} />;
    case 'chart': return <ChartScene sc={sc} theme={theme} />;
    case 'stat': return <StatScene sc={sc} theme={theme} />;
    default: return <TextScene sc={sc} theme={theme} />;
  }
};

const Footer = ({theme}) => (
  <div style={{position: 'absolute', bottom: 70, width: '100%', textAlign: 'center', fontSize: 34, letterSpacing: 8, color: theme.acc, opacity: 0.9, fontWeight: 700}}>
    {theme.tag}
  </div>
);
