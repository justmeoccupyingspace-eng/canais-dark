import React from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {THEMES} from './themes.js';
import {TitleScene, ChartScene, StatScene, TextScene} from './scenes.jsx';

const FPS = 30;

const Background = ({theme}) => {
  const f = useCurrentFrame();
  const a = 160 + Math.sin(f / 120) * 40;
  const orb = (x, y, r, c, sp, ph) => (
    <div style={{
      position: 'absolute', width: r, height: r, borderRadius: '50%', background: c, filter: 'blur(120px)', opacity: 0.55,
      left: x + Math.sin(f / sp + ph) * 140, top: y + Math.cos(f / (sp * 1.3) + ph) * 180,
    }} />
  );
  return (
    <AbsoluteFill style={{background: `linear-gradient(${a}deg, ${theme.bg1}, ${theme.bg2} 55%, ${theme.bg3})`}}>
      {orb(-200, 100, 800, theme.acc2, 90, 0)}
      {orb(500, 900, 900, theme.acc, 110, 2)}
      {orb(-100, 1400, 700, theme.bg3, 100, 4)}
      <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,.04) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.04) 2px, transparent 2px)', backgroundSize: '90px 90px'}} />
    </AbsoluteFill>
  );
};

const Top = ({theme, total}) => {
  const f = useCurrentFrame();
  const p = Math.min(f / total, 1);
  return (
    <>
      <div style={{position: 'absolute', top: 70, left: 60, right: 60, height: 10, borderRadius: 5, background: 'rgba(255,255,255,.18)'}}>
        <div style={{width: `${p * 100}%`, height: '100%', borderRadius: 5, background: `linear-gradient(90deg, ${theme.acc}, ${theme.acc2})`}} />
      </div>
      <div style={{position: 'absolute', top: 105, width: '100%', textAlign: 'center', fontSize: 36, letterSpacing: 10, color: '#fff', fontWeight: 800, opacity: 0.9, textShadow: '0 2px 10px rgba(0,0,0,.6)'}}>
        {theme.tag}
      </div>
    </>
  );
};

export const Video = ({spec}) => {
  const theme = THEMES[spec.channel] || THEMES.chartbound;
  let from = 0;
  const seqs = spec.scenes.map((sc, i) => {
    const dur = Math.ceil((sc.duration || 4) * FPS);
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <Scene sc={sc} theme={theme} spec={spec} />
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
        <Audio src={staticFile('audio/fx/whoosh.wav')} volume={0.5} />
        {sc.type === 'stat' ? <Audio src={staticFile('audio/fx/pop.wav')} volume={0.6} startFrom={0} /> : null}
      </Sequence>
    );
    from += dur;
    return el;
  });
  return (
    <AbsoluteFill style={{fontFamily: theme.font, color: theme.ink}}>
      <Background theme={theme} />
      {seqs}
      <Top theme={theme} total={from} />
      <Audio src={staticFile(`audio/fx/music_${spec.channel}.wav`)} volume={0.13} loop />
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
