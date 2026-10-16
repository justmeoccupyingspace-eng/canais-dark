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

const MONO = '"DejaVu Sans Mono", Menlo, Consolas, monospace';

const HexLines = ({hex, other, x, y, size, p, reveal = 1}) => {
  const lines = [hex.slice(0, 32), hex.slice(32)];
  let n = 0;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: size, lineHeight: 1.35, letterSpacing: 1}}>
      {lines.map((ln, li) => (
        <div key={li}>
          {ln.split('').map((c, i) => {
            const idx = li * 32 + i;
            const diff = other && other[idx] !== c;
            const shown = idx < reveal * 64;
            return <span key={i} style={{opacity: shown ? 1 : 0.0, color: diff && shown ? p.ink : '#ffffffcc', background: diff && shown ? p.warm : 'transparent', borderRadius: 6}}>{c}</span>;
          })}
        </div>
      ))}
    </div>
  );
};

const Chip = ({text, y, p, hlIndex = -1}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: y, textAlign: 'center', fontFamily: MONO, fontWeight: 800, fontSize: 96}}>
    <span style={{border: '4px solid #ffffff55', borderRadius: 22, padding: '8px 36px', color: '#fff', background: '#ffffff0d'}}>
      {text.split('').map((c, i) => <span key={i} style={{color: i === hlIndex ? p.warm : '#fff'}}>{c}</span>)}
    </span>
  </div>
);

const firstDiff = (a, b) => { for (let i = 0; i < Math.max(a.length, b.length); i++) if (a[i] !== b[i]) return i; return -1; };

const HashCmp = ({sc, p}) => {
  const f = useCurrentFrame();
  const h = sc.hashdata;
  const t = f / FPS;
  const a = interpolate(f, [0, 10], [0, 1], C), b = interpolate(f, [14, 24], [0, 1], C);
  const rv = interpolate(t, [1.6, 3.2], [0, 1], C);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 190, left: 60, right: 60}}><Words text={sc.text} hl={sc.hl} size={86} color="#fff" hlColor={p.acc} /></div>
      <div style={{opacity: a}}><Chip text={h.a} y={450} p={p} /><HexLines hex={h.ha} y={600} size={40} p={p} /></div>
      <div style={{opacity: b}}><Chip text={h.b} y={800} p={p} hlIndex={firstDiff(h.a, h.b)} /><HexLines hex={h.hb} other={h.ha} y={950} size={40} p={p} reveal={1} /></div>
    </AbsoluteFill>
  );
};

const HashBox = ({sc, p}) => {
  const f = useCurrentFrame();
  const h = sc.hashdata;
  const type = interpolate(f, [30, 75], [0, 1], C);
  const g = interpolate(f, [0, 12], [0, 1], C);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 190, left: 60, right: 60}}><Words text={sc.text} hl={sc.hl} size={86} color="#fff" hlColor={p.acc} /></div>
      <div style={{opacity: g}}>
        <Chip text={h.a} y={470} p={p} />
        <div style={{position: 'absolute', top: 640, left: 0, right: 0, textAlign: 'center', fontSize: 70, color: p.acc, fontFamily: FONT, fontWeight: 900}}>▼ SHA-256 ▼</div>
      </div>
      <HexLines hex={h.ha} y={800} size={44} p={p} reveal={type} />
    </AbsoluteFill>
  );
};

const Grid = ({sc, p}) => {
  const f = useCurrentFrame();
  const flips = sc.hashdata.flips;
  const rows = interpolate(f, [10, 90], [0, 16], C);
  const cell = 52, gap = 6, ox = (1080 - 16 * (cell + gap) + gap) / 2, oy = 470;
  const count = flips.reduce((n, b, i) => n + (b && Math.floor(i / 16) < rows ? 1 : 0), 0);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 190, left: 60, right: 60}}><Words text={sc.text} hl={sc.hl} size={86} color="#fff" hlColor={p.acc} /></div>
      {flips.map((b, i) => {
        const r = Math.floor(i / 16), c = i % 16;
        const v = interpolate(rows - r, [0, 1], [0, 1], C);
        return <div key={i} style={{position: 'absolute', left: ox + c * (cell + gap), top: oy + r * (cell + gap), width: cell, height: cell, borderRadius: 10, background: b ? p.warm : '#ffffff1f', opacity: v, transform: `scale(${0.6 + 0.4 * v})`}} />;
      })}
      <div style={{position: 'absolute', top: 470 + 16 * (cell + gap) + 30, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 70, color: '#fff'}}><span style={{color: p.warm}}>{count}</span> / 256 flipped</div>
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
          {sc.type === 'num' ? <Num sc={sc} p={p} /> : sc.type === 'hashcmp' ? <HashCmp sc={sc} p={p} /> : sc.type === 'hashbox' ? <HashBox sc={sc} p={p} /> : sc.type === 'grid' ? <Grid sc={sc} p={p} /> : sc.type === 'stat' ? <Stat sc={sc} p={p} /> : <Kin sc={sc} p={p} />}
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
