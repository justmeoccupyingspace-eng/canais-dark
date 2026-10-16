import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, delayRender, continueRender} from 'remotion';
import {THEMES} from './themes.js';
import {ArtScene, ChartScene, StatScene} from './scenes.jsx';

const FPS = 30;

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const ff = new FontFace('Anton', `url(${staticFile('fonts/anton.woff2')})`);
    ff.load().then((f) => { document.fonts.add(f); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

const Paper = ({theme}) => (
  <AbsoluteFill style={{background: theme.paper}}>
    <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(20,22,31,.10) 3px, transparent 3.5px)', backgroundSize: '54px 54px'}} />
  </AbsoluteFill>
);

const Top = ({theme, total}) => {
  const f = useCurrentFrame();
  const p = Math.min(f / total, 1);
  return (
    <>
      <div style={{position: 'absolute', top: 64, left: 50, right: 50, height: 14, borderRadius: 7, background: 'rgba(20,22,31,.15)', border: '3px solid #14161f'}}>
        <div style={{width: `${p * 100}%`, height: '100%', background: theme.acc2}} />
      </div>
      <div style={{position: 'absolute', top: 92, width: '100%', textAlign: 'center', fontSize: 30, letterSpacing: 10, color: '#14161f', fontWeight: 900, opacity: 0.75, fontFamily: 'Inter, Arial'}}>{theme.tag}</div>
    </>
  );
};

export const Video = ({spec}) => {
  useFonts();
  const theme = THEMES[spec.channel] || THEMES.chartbound;
  let from = 0;
  const seqs = spec.scenes.map((sc, i) => {
    const dur = Math.ceil((sc.duration || 4) * FPS);
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <Scene sc={sc} theme={theme} spec={spec} />
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
        <Audio src={staticFile('audio/fx/whoosh.wav')} volume={0.45} />
        {sc.type === 'stat' ? <Audio src={staticFile('audio/fx/pop.wav')} volume={0.6} /> : null}
      </Sequence>
    );
    from += dur;
    return el;
  });
  return (
    <AbsoluteFill style={{fontFamily: theme.font, color: theme.ink}}>
      <Paper theme={theme} />
      {seqs}
      <Top theme={theme} total={from} />
      <Audio src={staticFile(`audio/fx/music_${spec.channel}.wav`)} volume={0.11} loop />
    </AbsoluteFill>
  );
};

const Scene = ({sc, theme, spec}) => {
  switch (sc.type) {
    case 'chart': return <ChartScene sc={sc} theme={theme} />;
    case 'stat': return <StatScene sc={sc} theme={theme} />;
    default: return <ArtScene sc={sc} theme={theme} spec={spec} />;
  }
};
