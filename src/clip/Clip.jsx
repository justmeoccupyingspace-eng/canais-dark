// Corte vertical (Short) de um vídeo longo: gancho no topo, o trecho 16:9 no meio, legenda palavra a palavra e chamada pro vídeo completo.
import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';
import {PAL} from '../v3/V3.jsx';
import {SANS, useFonts} from '../long/L1.jsx';

const chunks = (words, n = 3) => {
  const out = [];
  let cur = [];
  for (const w of words) {
    cur.push(w);
    const end = /[.,!?;:]$/.test(w.w);
    if (cur.length >= n || end) { out.push(cur); cur = []; }
  }
  if (cur.length) out.push(cur);
  return out;
};

export const Clip = ({c}) => {
  useFonts();
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const p = PAL[c.channel] || PAL.chartbound;
  const T = c.t0 + f / fps;  // tempo no vídeo-fonte
  const groups = chunks(c.words || []);
  const g = groups.find((q) => T >= q[0].t0 - 0.05 && T <= q[q.length - 1].t1 + 0.25) || null;
  const inS = spring({frame: f, fps, config: {damping: 14, stiffness: 120}});
  const hookParts = String(c.hook || '').split(/(\*[^*]+\*)/);
  const prog = f / durationInFrames;
  const W = 1080, VH = Math.round((W * 9) / 16);
  const vy = 560;
  return (
    <AbsoluteFill style={{background: `radial-gradient(1200px 1500px at 50% 40%, ${p.bg1}, ${p.bg2})`, fontFamily: SANS}}>
      <div style={{position: 'absolute', left: 70, top: 120, display: 'flex', alignItems: 'center', gap: 14, opacity: 0.85}}>
        <div style={{width: 22, height: 22, borderRadius: '50%', background: p.mascot.color}} />
        <div style={{fontWeight: 900, fontSize: 30, letterSpacing: 7, color: '#fff'}}>{p.tag}</div>
      </div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 200, fontWeight: 900, fontSize: c.hook && c.hook.length > 60 ? 70 : 84, lineHeight: 1.08, color: '#fff',
        letterSpacing: -1.5, transform: `translateY(${(1 - inS) * 40}px)`, opacity: inS, textShadow: '0 8px 30px rgba(0,0,0,.45)'}}>
        {hookParts.map((h, i) => (h.startsWith('*') ? <span key={i} style={{color: p.acc}}>{h.slice(1, -1)}</span> : <span key={i}>{h}</span>))}
      </div>
      <div style={{position: 'absolute', left: 0, top: vy, width: W, height: VH, overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,.55)'}}>
        <OffthreadVideo src={staticFile(c.src)} startFrom={Math.round(c.t0 * fps)} style={{width: W, height: VH}} />
      </div>
      {g ? (
        <div style={{position: 'absolute', left: 50, right: 50, top: vy + VH + 80, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: 22, rowGap: 4,
          fontWeight: 900, fontSize: 78, lineHeight: 1.1, color: '#fff', textShadow: '0 6px 0 rgba(0,0,0,.55)'}}>
          {g.map((w, i) => {
            const on = T >= w.t0 - 0.03;
            return <span key={i} style={{color: on ? (T <= w.t1 + 0.08 ? p.acc : '#fff') : '#ffffff55'}}>{w.w.replace(/[.,;:]$/, '')}</span>;
          })}
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 210, display: 'flex', justifyContent: 'center'}}>
        <div style={{background: p.acc, color: '#0d1020', fontWeight: 900, fontSize: 40, padding: '18px 38px', borderRadius: 60, boxShadow: '0 12px 30px rgba(0,0,0,.4)',
          transform: `scale(${1 + 0.03 * Math.sin(f / 9)})`}}>▶ {c.cta || 'Full video on the channel'}</div>
      </div>
      {c.longTitle ? <div style={{position: 'absolute', left: 80, right: 80, bottom: 140, textAlign: 'center', fontWeight: 700, fontSize: 30, color: '#ffffffb0'}}>“{c.longTitle}”</div> : null}
      <div style={{position: 'absolute', left: 0, bottom: 0, height: 12, width: `${prog * 100}%`, background: p.acc}} />
    </AbsoluteFill>
  );
};
