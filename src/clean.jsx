import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, delayRender, continueRender} from 'remotion';

const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const FONT = 'InterX, Inter, "Helvetica Neue", Arial, sans-serif';
const PAL = {
  valeopreco: {bg: '#0a0f1c', acc: '#2ee59d', warm: '#ffb020', ink: '#0a0f1c', tag: 'VALE O PREÇO?'},
  howitticks: {bg: '#0a0f1c', acc: '#22d3ee', warm: '#ff5c8a', ink: '#06222a', tag: 'HOW IT TICKS'},
  chartbound: {bg: '#0a0f1c', acc: '#ffc233', warm: '#ff5c5c', ink: '#201700', tag: 'CHARTBOUND'},
};

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all([['800', 'fonts/inter800.woff2'], ['900', 'fonts/inter900.woff2']].map(([w, u]) => {
      const ff = new FontFace('InterX', `url(${staticFile(u)})`, {weight: w});
      return ff.load().then((f) => document.fonts.add(f));
    })).then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

const Bg = ({p, block}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: block ? p.acc : p.bg}}>
      {!block && (
        <>
          <AbsoluteFill style={{background: `radial-gradient(900px 900px at ${50 + Math.sin(f / 90) * 12}% ${42 + Math.cos(f / 110) * 8}%, ${p.acc}22, transparent 70%)`}} />
          <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,.045) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.045) 2px, transparent 2px)', backgroundSize: '90px 90px', backgroundPosition: `0 ${f * 0.5}px`}} />
        </>
      )}
    </AbsoluteFill>
  );
};

const Hud = ({p, total, block}) => {
  const f = useCurrentFrame();
  const ink = block ? p.ink : '#ffffff';
  return (
    <>
      <div style={{position: 'absolute', top: 70, left: 64, fontFamily: FONT, fontWeight: 800, fontSize: 28, letterSpacing: 6, color: ink, opacity: 0.7}}>{p.tag}</div>
      <div style={{position: 'absolute', bottom: 0, left: 0, height: 8, width: `${Math.min(f / total, 1) * 100}%`, background: block ? p.ink : p.acc}} />
    </>
  );
};

// legenda palavra por palavra, discreta, no terço inferior
const Caps = ({sc, p, block}) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const words = sc.words || [];
  if (!words.length) return null;
  const chunks = [];
  let cur = [];
  words.forEach((w) => {
    const len = cur.reduce((n, x) => n + x.w.length + 1, 0) + w.w.length;
    if (cur.length && (cur.length >= 4 || len > 22)) { chunks.push(cur); cur = []; }
    cur.push(w);
  });
  if (cur.length) chunks.push(cur);
  const active = chunks.find((c) => t >= c[0].t0 && t < c[c.length - 1].t1 + 0.12) || null;
  if (!active) return null;
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 1380, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 70, lineHeight: 1.15, color: block ? p.ink : '#fff', textShadow: block ? 'none' : '0 4px 24px rgba(0,0,0,.6)'}}>
      {active.map((w, i) => {
        const on = t >= w.t0 && t < w.t1;
        return <span key={i} style={{color: on ? (block ? '#fff' : p.acc) : undefined, marginRight: 16, display: 'inline-block'}}>{w.w}</span>;
      })}
    </div>
  );
};

const Words = ({text, hl, size: want, color, hlColor, delay = 0}) => {
  const f = useCurrentFrame();
  const longest = Math.max(...text.split(' ').map((w) => w.length));
  const size = Math.min(want, 940 / (longest * 0.66));
  const toks = [];
  const hit = hl && text.includes(hl) ? hl : null;
  const parts = hit ? text.split(hit) : [text];
  parts.forEach((part, i) => {
    part.split(' ').filter(Boolean).forEach((w) => toks.push({w, h: false}));
    if (hit && i < parts.length - 1) toks.push({w: hit, h: true});
  });
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `0 ${size * 0.28}px`, fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1.02, letterSpacing: -size * 0.02, textAlign: 'center'}}>
      {toks.map((t, i) => {
        const s = spring({frame: f - delay - i * 3, fps: FPS, config: {damping: 16, stiffness: 240}});
        return <span key={i} style={{display: 'inline-block', color: t.h ? hlColor : color, opacity: interpolate(s, [0, 0.5], [0, 1], C), transform: `translateY(${(1 - s) * 60}px) scale(${0.92 + 0.08 * s})`}}>{t.w}</span>;
      })}
    </div>
  );
};

const fmt = (v) => Math.round(v).toLocaleString('pt-BR');

const Kin = ({sc, p}) => (
  <AbsoluteFill style={{justifyContent: 'center', padding: '0 70px', top: -120}}>
    <Words text={sc.text} hl={sc.hl} size={sc.size || 150} color="#fff" hlColor={p.acc} />
  </AbsoluteFill>
);

// duas barras comparando valores; a segunda cresce com contagem
const Num = ({sc, p}) => {
  const f = useCurrentFrame();
  const a = sc.a, b = sc.b, max = Math.max(a, b);
  const g1 = interpolate(f, [4, 26], [0, 1], {...C, easing: Easing.out(Easing.cubic)});
  const g2 = interpolate(f, [30, 80], [0, 1], {...C, easing: Easing.out(Easing.cubic)});
  const H = 640;
  const bar = (x, v, g, col, label, shown) => {
    const h = (v / max) * H * g;
    return (
      <div style={{position: 'absolute', left: x, bottom: 0, width: 400, textAlign: 'center'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 84, color: '#fff', marginBottom: 18, opacity: g}}>{sc.prefix}{fmt(shown)}</div>
        <div style={{height: h, background: col, borderRadius: '18px 18px 0 0'}} />
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 38, letterSpacing: 2, color: '#ffffffaa', marginTop: 18, textTransform: 'uppercase'}}>{label}</div>
      </div>
    );
  };
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 210, left: 60, right: 60}}>
        <Words text={sc.text} hl={sc.hl} size={92} color="#fff" hlColor={p.acc} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 480, height: 800}}>
        {bar(110, a, g1, '#ffffff33', sc.l1, a * g1)}
        {bar(570, b, g2, p.acc, sc.l2, a + (b - a) * g2)}
      </div>
    </AbsoluteFill>
  );
};

const Stat = ({sc, p}) => {
  const f = useCurrentFrame();
  const v = interpolate(f, [4, 38], [0, sc.value], {...C, easing: Easing.out(Easing.cubic)});
  const s = spring({frame: f, fps: FPS, config: {damping: 14, stiffness: 160}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', top: -140}}>
      <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 330, letterSpacing: -12, color: p.ink, lineHeight: 1, transform: `scale(${0.85 + 0.15 * s})`}}>{sc.prefix}{Math.round(v)}{sc.suffix}</div>
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 56, color: p.ink, opacity: 0.8, textAlign: 'center', padding: '0 90px', marginTop: 10}}>{sc.label}</div>
    </AbsoluteFill>
  );
};

const SceneWrap = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const x = interpolate(f, [0, 8], [60, 0], {...C, easing: Easing.out(Easing.cubic)});
  return <AbsoluteFill style={{opacity: interpolate(f, [0, 3, d - 3, d], [0, 1, 1, 0], C), transform: `translateX(${x}px)`}}>{children}</AbsoluteFill>;
};

export const CleanVideo = ({spec}) => {
  useFonts();
  const p = PAL[spec.channel] || PAL.chartbound;
  let from = 0;
  const parts = spec.scenes.map((sc, i) => {
    const dur = Math.ceil((sc.duration || 4) * FPS);
    const block = sc.type === 'stat';
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <Bg p={p} block={block} />
        <SceneWrap>
          {sc.type === 'num' ? <Num sc={sc} p={p} /> : sc.type === 'stat' ? <Stat sc={sc} p={p} /> : <Kin sc={sc} p={p} />}
          <Caps sc={sc} p={p} block={block} />
        </SceneWrap>
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
        <Audio src={staticFile(i === 0 ? 'audio/fx/hit.wav' : 'audio/fx/whoosh.wav')} volume={i === 0 ? 0.7 : 0.35} />
        {block ? <Audio src={staticFile('audio/fx/pop.wav')} volume={0.5} /> : null}
      </Sequence>
    );
    from += dur;
    return el;
  });
  const total = from;
  return (
    <AbsoluteFill style={{background: p.bg}}>
      {parts}
      <Hud p={p} total={total} block={false} />
      <Audio src={staticFile(`audio/fx/music_${spec.channel}.wav`)} volume={0.09} loop />
    </AbsoluteFill>
  );
};
