import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, delayRender, continueRender} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {Mascot, Shadow, Lights, Toon, useToon} from '../three/Mascot.jsx';

// Formato v3: mascote 3D persistente (narrador) + visual por cena + legenda grande.
// Layout 1080x1920: título 170-560 · visual 560-1150 · legenda ~1240 · mascote embaixo.
const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const FONT = 'InterX, Inter, "Helvetica Neue", Arial, sans-serif';
const EMOJI = '"Noto Color Emoji", "Apple Color Emoji", sans-serif';
const PPU = 256; // pixels por unidade em z=0 (câmera fov 30 a z 14)
const R3W = 720, R3H = 1280; // canvas 3D renderizado menor e ampliado (WebGL em software é caro)
const wx = (px) => (px - 540) / PPU;
const wy = (py) => (960 - py) / PPU;

export const PAL = {
  chartbound: {bg1: '#1b2b5c', bg2: '#060a1a', acc: '#ffc233', acc2: '#3ee0b5', warm: '#ff5c6c', colA: '#7f93ff', colB: '#ffc233', tag: 'CHARTBOUND', mascot: {color: '#33d6aa', belly: '#e6fff6', acc: 'glasses', accent: '#ff7a8a'}, music: 'music_chartbound.wav'},
  howitticks: {bg1: '#3a2606', bg2: '#0b0803', acc: '#ffb000', acc2: '#41d3ff', warm: '#ff4d6d', colA: '#6f7a8a', colB: '#ffb000', tag: 'HOW IT TICKS', mascot: {color: '#ffb000', belly: '#fff1c9', acc: 'antenna', accent: '#ff5d73'}, music: 'music_howitticks.wav'},
  gabarito: {bg1: '#26386a', bg2: '#0d1530', acc: '#ffc83d', acc2: '#7fd1ff', warm: '#ff6b6b', colA: '#7f93ff', colB: '#ffc83d', tag: 'GABARITO DO DIA', mascot: {color: '#ffc83d', belly: '#fff4d1', acc: 'cap', accent: '#ff7a7a'}, music: 'music_loja.wav'},
};

const DEF = {
  hook: {pose: 'shock', pos: 'bottom'},
  bars: {pose: 'pointUpL', pos: 'right'},
  big: {pose: 'cheer', pos: 'bottom'},
  text: {pose: 'idle', pos: 'bottom'},
  screen: {pose: 'pointUpL', pos: 'right'},
  quiz: {pose: 'think', pos: 'right'},
  answer: {pose: 'cheer', pos: 'bottom'},
  end: {pose: 'wave', pos: 'center'},
};
const POS = {bottom: [0, -2.62, 0, 0.76], right: [1.22, -2.8, 0.6, 0.56], left: [-1.22, -2.8, 0.6, 0.56], center: [0, -0.9, 0, 1.1]};

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all([['800', 'fonts/inter800.woff2'], ['900', 'fonts/inter900.woff2']].map(([w, u]) => {
      const ff = new FontFace('InterX', `url(${staticFile(u)})`, {weight: w});
      return ff.load().then((f) => document.fonts.add(f));
    })).then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

// ---------- tempo ----------
const useTimeline = (spec) => useMemo(() => {
  let from = 0;
  return spec.scenes.map((sc) => {
    const d = Math.max(1, Math.ceil((sc.duration || 4) * FPS));
    const r = {from, d};
    from += d;
    return r;
  });
}, [spec]);

const sceneAt = (tl, f) => {
  for (let i = tl.length - 1; i >= 0; i--) if (f >= tl[i].from) return i;
  return 0;
};

// ---------- fundo ----------
const Bg = ({p}) => {
  const f = useCurrentFrame();
  const blobs = [[160, 380, 520, p.acc], [900, 900, 600, p.acc2], [420, 1500, 700, p.warm]];
  return (
    <AbsoluteFill style={{background: `radial-gradient(1400px 1500px at 50% 40%, ${p.bg1}, ${p.bg2})`}}>
      {blobs.map(([x, y, r, c], i) => (
        <div key={i} style={{position: 'absolute', left: x - r + Math.sin(f / (70 + i * 13) + i) * 60, top: y - r + Math.cos(f / (80 + i * 9) + i) * 50, width: r * 2, height: r * 2, background: `radial-gradient(circle, ${c}2e 0%, ${c}00 60%)`}} />
      ))}
      <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(255,255,255,.07) 2px, transparent 2.5px)', backgroundSize: '46px 46px', backgroundPosition: `${f * 0.3}px ${f * 0.5}px`, opacity: 0.7}} />
    </AbsoluteFill>
  );
};

// ---------- texto ----------
const Words = ({text = '', hl, size: want = 110, color = '#fff', hlColor = '#ffc233', instant = false, delay = 0, weight = 900, maxW = 960, align = 'center'}) => {
  const f = useCurrentFrame();
  const longest = Math.max(...text.split(' ').map((w) => w.length), 1);
  const size = Math.min(want, maxW / (longest * 0.62));
  const toks = [];
  const hit = hl && text.includes(hl) ? hl : null;
  const parts = hit ? text.split(hit) : [text];
  parts.forEach((part, i) => {
    part.split(' ').filter(Boolean).forEach((w) => toks.push({w, h: false}));
    if (hit && i < parts.length - 1) toks.push({w: hit, h: true});
  });
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: align === 'left' ? 'flex-start' : 'center', gap: `0 ${size * 0.26}px`, fontFamily: FONT, fontWeight: weight, fontSize: size, lineHeight: 1.04, letterSpacing: -size * 0.02, textAlign: align, textShadow: '0 6px 24px rgba(0,0,0,.35)'}}>
      {toks.map((t, i) => {
        const s = instant ? 1 : spring({frame: f - delay - i * 2, fps: FPS, config: {damping: 15, stiffness: 260}});
        const pulse = t.h ? 1 + 0.04 * Math.sin(f / 6) : 1;
        return (
          <span key={i} style={{display: 'inline-block', color: t.h ? '#14121f' : color, background: t.h ? hlColor : 'transparent', borderRadius: size * 0.14, padding: t.h ? `0 ${size * 0.12}px` : 0, opacity: interpolate(s, [0, 0.4], [0, 1], C), transform: `translateY(${(1 - s) * 50}px) scale(${(0.9 + 0.1 * s) * pulse}) rotate(${t.h ? -1.5 : 0}deg)`}}>{t.w}</span>
        );
      })}
    </div>
  );
};

const Kicker = ({text, p, instant}) => {
  const f = useCurrentFrame();
  const s = instant ? 1 : spring({frame: f, fps: FPS, config: {damping: 14, stiffness: 200}});
  if (!text) return null;
  return (
    <div style={{display: 'flex', justifyContent: 'center', marginBottom: 26, opacity: s, transform: `scale(${0.8 + 0.2 * s})`}}>
      <span style={{fontFamily: FONT, fontWeight: 900, fontSize: 38, letterSpacing: 4, color: '#14121f', background: p.acc2, padding: '10px 26px', borderRadius: 40, textTransform: 'uppercase'}}>{text}</span>
    </div>
  );
};

const fmtNum = (v, sc) => {
  const d = sc.dec || 0;
  const loc = sc.pt ? 'pt-BR' : 'en-US';
  return `${sc.prefix || ''}${Number(v).toLocaleString(loc, {minimumFractionDigits: d, maximumFractionDigits: d})}${sc.suffix || ''}`;
};

// ---------- cenas (camada 2D) ----------
const Hook = ({sc, p, first}) => {
  const f = useCurrentFrame();
  const vs = sc.vs || null;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 175, left: 50, right: 50}}>
        <Kicker text={sc.kicker} p={p} instant={first} />
        <Words text={sc.text} hl={sc.hl} size={sc.size || (vs ? 92 : 118)} hlColor={p.acc} instant={first} />
      </div>
      {vs ? (
        <div style={{position: 'absolute', top: 700, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 40}}>
          {vs.map((v, i) => {
            const s = first ? 1 : spring({frame: f - i * 5, fps: FPS, config: {damping: 11, stiffness: 180}});
            return (
              <React.Fragment key={i}>
                {i === 1 ? <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 90, color: p.warm, transform: `scale(${1 + 0.08 * Math.sin(f / 5)})`}}>VS</div> : null}
                <div style={{textAlign: 'center', transform: `scale(${0.6 + 0.4 * s}) translateY(${Math.sin(f / 12 + i * 2) * 8}px)`, opacity: s}}>
                  <div style={{fontFamily: EMOJI, fontSize: 210, lineHeight: 1}}>{v.flag}</div>
                  <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 52, color: '#fff', marginTop: 8}}>{v.name}</div>
                </div>
              </React.Fragment>
            );
          })}
        </div>
      ) : null}
      {!vs && sc.icon ? <Icon icon={sc.icon} first={first} /> : null}
    </AbsoluteFill>
  );
};

const BarsLabels = ({sc, p, layout}) => {
  const f = useCurrentFrame();
  const g = layout.grow(f);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 180, left: 50, right: 50}}>
        <Kicker text={sc.kicker} p={p} />
        <Words text={sc.text} hl={sc.hl} size={sc.size || 86} hlColor={p.acc} />
      </div>
      {layout.cols.map((c, i) => {
        const shown = c.v0 + (c.v - c.v0) * g[i];
        const top = layout.basePy - c.hPx * g[i] - 104;
        return (
          <React.Fragment key={i}>
            <div style={{position: 'absolute', left: c.px - 210, width: 420, top, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: i === layout.cols.length - 1 ? 92 : 76, color: i === layout.cols.length - 1 ? p.acc : '#fff', opacity: Math.min(1, g[i] * 3), textShadow: '0 6px 20px rgba(0,0,0,.4)'}}>{fmtNum(shown, sc)}</div>
            <div style={{position: 'absolute', left: c.px - 210, width: 420, top: layout.basePy + 14, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 40, color: '#ffffffd9', letterSpacing: 1}}>
              {c.flag ? <span style={{fontFamily: EMOJI, marginRight: 10}}>{c.flag}</span> : null}{c.label}
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

const Big = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f - 2, fps: FPS, config: {damping: 9, stiffness: 160}});
  const shown = sc.value != null ? interpolate(f, [2, 26], [sc.value0 || 0, sc.value], {...C, easing: Easing.out(Easing.cubic)}) : null;
  const str = sc.big || (shown != null ? fmtNum(shown, sc) : '');
  const size = Math.min(sc.bigSize || 300, Math.floor(940 / (Math.max(String(sc.big || fmtNum(sc.value || 0, sc)).length, 1) * 0.72)));
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 180, left: 50, right: 50}}>
        <Kicker text={sc.kicker} p={p} />
        <Words text={sc.text} hl={sc.hl} size={sc.size || 84} hlColor={p.acc} />
      </div>
      <div style={{position: 'absolute', left: 540 - 520, top: 820 - 520, width: 1040, height: 1040, borderRadius: '50%', background: `repeating-conic-gradient(from ${f * 1.2}deg, ${p.acc}22 0deg 12deg, transparent 12deg 24deg)`, opacity: s * 0.9, WebkitMaskImage: 'radial-gradient(circle, black 30%, transparent 70%)'}} />
      <div style={{position: 'absolute', top: 820 - size * 0.62, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1, color: p.acc, whiteSpace: 'nowrap', letterSpacing: -size * 0.03, transform: `scale(${0.5 + 0.5 * s}) rotate(${(1 - s) * -8}deg)`, textShadow: `0 10px 0 ${p.bg2}, 0 20px 50px rgba(0,0,0,.45)`}}>{str}</div>
      <Burst p={p} at={4} y={820} />
      {sc.label ? <div style={{position: 'absolute', top: 820 + size * 0.5 + 10, left: 70, right: 70, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 50, color: '#fff', opacity: interpolate(f, [10, 20], [0, 1], C)}}>{sc.label}</div> : null}
    </AbsoluteFill>
  );
};

const Burst = ({p, at = 0, y = 800, n = 26}) => {
  const f = useCurrentFrame() - at;
  if (f < 0 || f > 40) return null;
  const cols = [p.acc, p.acc2, p.warm, '#ffffff'];
  return (
    <>
      {Array.from({length: n}, (_, i) => {
        const a = (i / n) * Math.PI * 2 + i * 0.37;
        const sp = 18 + (i % 5) * 6;
        const d = sp * f * (1 - f / 80);
        return <div key={i} style={{position: 'absolute', left: 540 + Math.cos(a) * d - 9, top: y + Math.sin(a) * d + f * f * 0.12 - 9, width: 18, height: i % 3 ? 18 : 30, borderRadius: i % 2 ? '50%' : 4, background: cols[i % 4], opacity: interpolate(f, [26, 40], [1, 0], C), transform: `rotate(${f * 12 + i * 30}deg)`}} />;
      })}
    </>
  );
};

const TextScene = ({sc, p, first}) => (
  <AbsoluteFill>
    <div style={{position: 'absolute', top: sc.sub ? 260 : 330, left: 60, right: 60}}>
      <Kicker text={sc.kicker} p={p} instant={first} />
      <Words text={sc.text} hl={sc.hl} size={sc.size || 104} hlColor={p.acc} instant={first} />
      {sc.sub ? <div style={{marginTop: 40, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 50, color: '#ffffffcc'}}>{sc.sub}</div> : null}
    </div>
    {sc.icon ? <Icon icon={sc.icon} first={first} /> : null}
  </AbsoluteFill>
);

const Icon = ({icon, first}) => {
  const f = useCurrentFrame();
  const s = first ? 1 : spring({frame: f - 4, fps: FPS, config: {damping: 9, stiffness: 150}});
  return <div style={{position: 'absolute', top: 690, left: 0, right: 0, textAlign: 'center', fontFamily: EMOJI, fontSize: 250, lineHeight: 1, transform: `scale(${0.4 + 0.6 * s}) translateY(${Math.sin(f / 10) * 12}px) rotate(${Math.sin(f / 14) * 6}deg)`, textShadow: '0 18px 30px rgba(0,0,0,.4)'}}>{icon}</div>;
};

const ScreenTitle = ({sc, p}) => (
  <AbsoluteFill>
    <div style={{position: 'absolute', top: 180, left: 50, right: 50}}>
      <Kicker text={sc.kicker} p={p} />
      <Words text={sc.text} hl={sc.hl} size={sc.size || 86} hlColor={p.acc} />
    </div>
  </AbsoluteFill>
);

const Quiz = ({sc, p}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const rv = d - Math.round((sc.revealFromEnd || 1.6) * FPS);
  const revealed = f >= rv;
  const k = revealed ? spring({frame: f - rv, fps: FPS, config: {damping: 11, stiffness: 170}}) : 0;
  const left = Math.max(0, Math.ceil((rv - f) / FPS));
  const inCd = f >= rv - (sc.countdown || 3) * FPS && f < rv;
  const card = spring({frame: f, fps: FPS, config: {damping: 15, stiffness: 160}});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 150, left: 50, right: 50, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <span style={{fontFamily: FONT, fontWeight: 900, fontSize: 30, letterSpacing: 3, color: '#14121f', background: p.acc2, borderRadius: 30, padding: '10px 24px'}}>{sc.label || 'QUESTÃO'}</span>
        {inCd ? <span style={{fontFamily: FONT, fontWeight: 900, fontSize: 64, color: p.warm, width: 96, height: 96, borderRadius: '50%', border: `8px solid ${p.warm}`, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 + 0.15 * (1 - ((f % FPS) / FPS))})`}}>{left}</span> : null}
      </div>
      <div style={{position: 'absolute', top: 270, left: 44, right: 44, background: '#ffffff', borderRadius: 34, padding: '36px 36px 26px', boxShadow: '0 30px 70px rgba(0,0,0,.35)', transform: `translateY(${(1 - card) * 80}px)`, opacity: card}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: sc.qsize || 56, lineHeight: 1.16, color: '#14121f', marginBottom: 26}}>{sc.q}</div>
        {(sc.alts || []).map((a, i) => {
          const ok = i === sc.correct;
          const s = spring({frame: f - 8 - i * 4, fps: FPS, config: {damping: 15, stiffness: 220}});
          const bg = revealed ? (ok ? '#2bd47d' : '#f1f1f4') : '#f3f4f8';
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 20, background: bg, borderRadius: 22, padding: '20px 20px', marginBottom: 14, opacity: revealed && !ok ? 0.45 : s, transform: `translateX(${(1 - s) * 60}px) scale(${ok ? 1 + 0.05 * k : 1})`}}>
              <span style={{flex: '0 0 auto', width: 66, height: 66, borderRadius: '50%', background: revealed && ok ? '#ffffff' : p.bg1, color: revealed && ok ? '#1d8f52' : '#fff', fontFamily: FONT, fontWeight: 900, fontSize: 36, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{'ABCDE'[i]}</span>
              <span style={{fontFamily: FONT, fontWeight: 800, fontSize: sc.asize || 48, lineHeight: 1.15, color: '#14121f'}}>{a}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const End = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 12, stiffness: 160}});
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 230, left: 60, right: 60, opacity: s, transform: `scale(${0.85 + 0.15 * s})`}}>
        <Words text={sc.text || 'Follow for more'} hl={sc.hl} size={sc.size || 96} hlColor={p.acc} />
        {sc.sub ? <div style={{marginTop: 30, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 48, color: '#ffffffcc'}}>{sc.sub}</div> : null}
      </div>
      <div style={{position: 'absolute', bottom: 120, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 44, letterSpacing: 6, color: '#ffffffb0'}}>{sc.brand || p.tag}</div>
    </AbsoluteFill>
  );
};

// ---------- legenda ----------
const Caps = ({spec, tl, p}) => {
  const f = useCurrentFrame();
  const i = sceneAt(tl, f);
  const sc = spec.scenes[i];
  if (!sc || sc.nocaps || sc.type === 'quiz') return null;
  const t = (f - tl[i].from) / FPS;
  const words = sc.words || [];
  const chunks = [];
  let cur = [];
  words.forEach((w) => {
    const len = cur.reduce((n, x) => n + x.w.length + 1, 0) + w.w.length;
    if (cur.length && (cur.length >= 3 || len > 18)) { chunks.push(cur); cur = []; }
    cur.push(w);
  });
  if (cur.length) chunks.push(cur);
  const active = chunks.find((c) => t >= c[0].t0 - 0.05 && t < c[c.length - 1].t1 + 0.1);
  if (!active) return null;
  const s = spring({frame: Math.round((t - active[0].t0) * FPS), fps: FPS, config: {damping: 14, stiffness: 300}});
  const y = sc.capsY || (DEF[sc.type]?.pos === 'center' ? 1500 : 1180);
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: y, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 78, lineHeight: 1.08, transform: `scale(${0.9 + 0.1 * s})`}}>
      {active.map((w, j) => {
        const on = t >= w.t0 && t < w.t1 + 0.05;
        return <span key={j} style={{display: 'inline-block', margin: '0 12px', color: on ? p.acc : '#ffffff', WebkitTextStroke: '3px #0a0a12', paintOrder: 'stroke fill', textShadow: '0 6px 0 #0a0a12, 0 10px 30px rgba(0,0,0,.5)', transform: on ? 'translateY(-4px) scale(1.06)' : 'none'}}>{w.w}</span>;
      })}
    </div>
  );
};

// ---------- 3D ----------
const barsLayout = (sc, p) => {
  const vals = sc.vals || [sc.a, sc.b];
  const labels = sc.labels || [sc.l1, sc.l2];
  const flags = sc.flags || [];
  const n = vals.length;
  const max = Math.max(...vals.map(Math.abs), 1e-9);
  const basePy = 1110, maxH = 520;
  const span = n === 2 ? [270, 610] : n === 3 ? [200, 460, 720] : vals.map((_, i) => 160 + i * (600 / Math.max(1, n - 1)));
  const cols = vals.map((v, i) => ({v, v0: 0, hPx: Math.max(14, (v / max) * maxH), px: span[i], label: labels[i] || '', flag: flags[i] || null, color: i === n - 1 ? p.colB : p.colA}));
  const grow = (f) => cols.map((_, i) => interpolate(f, [6 + i * 22, 30 + i * 22 + (i === n - 1 ? 14 : 0)], [0, 1], {...C, easing: Easing.out(Easing.cubic)}));
  return {cols, basePy, grow, coins: sc.style === 'coins'};
};

const Columns3D = ({layout, f}) => {
  const toon = useToon();
  const geo = useMemo(() => ({col: new THREE.CylinderGeometry(0.52, 0.52, 1, 48), coin: new THREE.CylinderGeometry(0.5, 0.5, 0.085, 40), cap: new THREE.SphereGeometry(0.52, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2)}), []);
  const g = layout.grow(f);
  return (
    <group>
      {layout.cols.map((c, i) => {
        const h = Math.max(0.001, (c.hPx / PPU) * g[i]);
        const x = wx(c.px), y0 = wy(layout.basePy);
        if (layout.coins) {
          const n = Math.max(1, Math.round(h / 0.095));
          return (
            <group key={i}>
              {Array.from({length: n}, (_, k) => (
                <mesh key={k} geometry={geo.coin} position={[x + Math.sin(k * 1.7 + i) * 0.025, y0 + 0.045 + k * 0.095, 0]}>
                  <meshStandardMaterial color={i === layout.cols.length - 1 ? '#ffc233' : '#d9dee8'} metalness={0.55} roughness={0.3} />
                </mesh>
              ))}
            </group>
          );
        }
        return (
          <group key={i}>
            <mesh geometry={geo.col} position={[x, y0 + h / 2, 0]} scale={[1, h, 1]}><meshStandardMaterial color={c.color} roughness={0.35} /></mesh>
            <mesh geometry={geo.cap} position={[x, y0 + h, 0]} scale={[1, 0.35, 1]}><meshStandardMaterial color={c.color} roughness={0.35} /></mesh>
          </group>
        );
      })}
      <mesh position={[0, wy(layout.basePy) - 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[2.6, 64]} />
        <meshBasicMaterial color="#000000" transparent opacity={0.18} />
      </mesh>
    </group>
  );
};

const useCodeTex = (lines, p) => useMemo(() => {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 640;
  const x = c.getContext('2d');
  x.fillStyle = '#0d1117'; x.fillRect(0, 0, 1024, 640);
  x.fillStyle = '#1f2937'; x.fillRect(0, 0, 1024, 70);
  ['#ff5f57', '#febc2e', '#28c840'].forEach((col, i) => { x.fillStyle = col; x.beginPath(); x.arc(44 + i * 40, 35, 13, 0, Math.PI * 2); x.fill(); });
  x.font = `bold ${Math.min(84, Math.floor(930 / (Math.max(...(lines || ['']).map((l) => l.length), 1) * 0.6)))}px "DejaVu Sans Mono", monospace`;
  (lines || []).forEach((ln, i) => { x.fillStyle = i === (lines.length - 1) ? p.acc : '#e5e7eb'; x.fillText(ln, 50, 190 + i * 120); });
  const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t;
}, [JSON.stringify(lines), p.acc]);

const Screen3D = ({sc, p, f}) => {
  const tex = useCodeTex(sc.code, p);
  const s = spring({frame: f, fps: FPS, config: {damping: 13, stiffness: 120}});
  const geo = useMemo(() => new THREE.BoxGeometry(3.4, 2.2, 0.18), []);
  return (
    <group position={[wx(500), wy(800), 0]} rotation={[0.05, 0.28 * (1 - s) + 0.1, 0]} scale={(0.6 + 0.4 * s) * 1.12}>
      <mesh geometry={geo}><meshStandardMaterial color="#2b2f3a" roughness={0.5} /></mesh>
      <mesh position={[0, 0.02, 0.095]}><planeGeometry args={[3.2, 2.0]} /><meshBasicMaterial map={tex} /></mesh>
      <mesh position={[0, -1.35, -0.1]}><cylinderGeometry args={[0.12, 0.12, 0.5, 20]} /><meshStandardMaterial color="#2b2f3a" /></mesh>
      <mesh position={[0, -1.6, -0.1]}><boxGeometry args={[1.2, 0.08, 0.6]} /><meshStandardMaterial color="#2b2f3a" /></mesh>
    </group>
  );
};

const Stage = ({spec, tl, p}) => {
  const f = useCurrentFrame();
  const i = sceneAt(tl, f);
  const sc = spec.scenes[i];
  const lf = f - tl[i].from;
  const prev = spec.scenes[i - 1];
  const def = DEF[sc.type] || DEF.text;
  const pdef = prev ? (DEF[prev.type] || DEF.text) : def;
  const posA = POS[(prev && (prev.mpos || pdef.pos)) || (sc.mpos || def.pos)];
  const posB = POS[sc.mpos || def.pos];
  const k = i === 0 ? 1 : spring({frame: lf, fps: FPS, config: {damping: 16, stiffness: 110}});
  const pos = posA.map((v, j) => v + (posB[j] - v) * k);
  // pose: segue a cena; no quiz vira "cheer" na revelação
  let pose = sc.pose || def.pose;
  if (sc.type === 'quiz' && lf >= tl[i].d - Math.round((sc.revealFromEnd || 1.6) * FPS)) pose = 'cheer';
  const prevPose = prev ? (prev.pose || pdef.pose) : pose;
  // boca: fala quando há palavra ativa
  const t = lf / FPS;
  let talk = 0;
  if (sc.env && sc.env.length) talk = Math.min(1, (sc.env[lf] || 0) * 1.25);
  else if ((sc.words || []).some((w) => t >= w.t0 && t < w.t1)) talk = 0.35 + 0.65 * Math.abs(Math.sin(f * 0.95));
  const look = pos[0] > 0.5 ? [-0.9, 0.5] : pos[0] < -0.5 ? [0.9, 0.5] : [0, 0];
  const bars = sc.type === 'bars' ? barsLayout(sc, p) : null;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: R3W, height: R3H, transform: `scale(${1080 / R3W})`, transformOrigin: '0 0'}}>
    <ThreeCanvas width={R3W} height={R3H} camera={{fov: 30, position: [0, 0, 14]}} gl={{antialias: true, alpha: true}}>
      <Lights />
      {bars ? <Columns3D layout={bars} f={lf} /> : null}
      {sc.type === 'screen' ? <Screen3D sc={sc} p={p} f={lf} /> : null}
      <Shadow position={[pos[0], pos[1] - 1.12 * pos[3] - 0.08, pos[2]]} scale={1.3 * pos[3]} opacity={0.35} />
      <Mascot {...p.mascot} pose={pose} prevPose={prevPose} poseAt={tl[i].from} talk={talk} look={look} enter={-30} scale={pos[3]} position={[pos[0], pos[1], pos[2]]} />
    </ThreeCanvas>
    </div>
  );
};

const Hud = ({p, total}) => {
  const f = useCurrentFrame();
  return (
    <>
      <div style={{position: 'absolute', top: 64, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 28, letterSpacing: 8, color: '#ffffff', opacity: 0.6}}>{p.tag}</div>
      <div style={{position: 'absolute', top: 0, left: 0, height: 10, width: `${Math.min(f / total, 1) * 100}%`, background: p.acc}} />
    </>
  );
};

const Layer2D = ({sc, p, first, tl, i}) => {
  switch (sc.type) {
    case 'hook': return <Hook sc={sc} p={p} first={first} />;
    case 'bars': return <BarsLabels sc={sc} p={p} layout={barsLayout(sc, p)} />;
    case 'big': return <Big sc={sc} p={p} />;
    case 'screen': return <ScreenTitle sc={sc} p={p} />;
    case 'quiz': return <Quiz sc={sc} p={p} />;
    case 'end': return <End sc={sc} p={p} />;
    default: return <TextScene sc={sc} p={p} first={first} />;
  }
};

const SFX = {hook: 'hit', bars: 'whoosh', big: 'ding', text: 'softwhoosh', screen: 'click', quiz: 'whoosh', answer: 'ding', end: 'sparkle'};

export const V3Video = ({spec}) => {
  useFonts();
  const p = PAL[spec.channel] || PAL.howitticks;
  const tl = useTimeline(spec);
  const total = tl.length ? tl[tl.length - 1].from + tl[tl.length - 1].d : 1;
  return (
    <AbsoluteFill style={{background: p.bg2}}>
      <Bg p={p} />
      <Stage spec={spec} tl={tl} p={p} />
      {spec.scenes.map((sc, i) => (
        <Sequence key={i} from={tl[i].from} durationInFrames={tl[i].d}>
          <Layer2D sc={sc} p={p} first={i === 0} tl={tl} i={i} />
          {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
          <Audio src={staticFile(`audio/fx/${sc.sfx || SFX[sc.type] || 'whoosh'}.wav`)} volume={i === 0 ? 0.55 : 0.32} />
          {sc.type === 'bars' ? <Sequence from={30 + (((sc.vals || [0, 0]).length) - 1) * 22}><Audio src={staticFile('audio/fx/pop.wav')} volume={0.5} /></Sequence> : null}
          {sc.type === 'quiz' ? <Sequence from={Math.max(0, tl[i].d - Math.round((sc.revealFromEnd || 1.6) * FPS))}><Audio src={staticFile('audio/fx/ding.wav')} volume={0.6} /></Sequence> : null}
        </Sequence>
      ))}
      <Caps spec={spec} tl={tl} p={p} />
      <Hud p={p} total={total} />
      <Audio src={staticFile(`audio/fx/${p.music}`)} volume={0.08} loop />
    </AbsoluteFill>
  );
};
