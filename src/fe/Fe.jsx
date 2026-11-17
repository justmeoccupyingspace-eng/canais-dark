// Vídeos de oração / histórias bíblicas (canal B em espanhol, canal A em inglês).
// Cenas procedurais (noite, amanhecer, vela, céu) ou pintura em domínio público com movimento lento (Ken Burns),
// texto da frase atual sincronizado com a narração, cartão de título no começo e chamada no fim.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, delayRender, continueRender} from 'remotion';

const SERIF = 'LoraI, Georgia, serif';
const SANS = 'PoppinsX, "Helvetica Neue", Arial, sans-serif';

const useFonts = () => {
  const [h] = useState(() => delayRender('fontes'));
  useEffect(() => {
    const L = [['LoraI', '400 700', 'fonts/Lora-Italic-Variable.ttf', 'italic'], ['PoppinsX', '400', 'fonts/Poppins-Regular.ttf', 'normal'], ['PoppinsX', '500', 'fonts/Poppins-Medium.ttf', 'normal'], ['PoppinsX', '700', 'fonts/Poppins-Bold.ttf', 'normal']];
    Promise.all(L.map(([fam, w, u, st]) => new FontFace(fam, `url(${staticFile(u)})`, {weight: w, style: st}).load().then((f) => document.fonts.add(f)).catch(() => null)))
      .then(() => continueRender(h));
  }, [h]);
};

// gerador pseudoaleatório determinístico (mesma cena em todos os pedaços do render)
const rng = (seed) => {
  let s = seed >>> 0 || 1;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
};

const PAL = {
  night: {top: '#05070f', mid: '#141a3a', low: '#3a2a55', glow: '#cfd8ff', hill: '#03040a', text: '#ffffff', acc: '#e8c27a'},
  dawn: {top: '#1b2a55', mid: '#c46a6a', low: '#f4b26a', glow: '#ffe2a8', hill: '#1a1220', text: '#ffffff', acc: '#ffd88a'},
  candle: {top: '#0a0604', mid: '#1c0f07', low: '#2e1a0c', glow: '#ffb45a', hill: '#000000', text: '#fff6e6', acc: '#ffcf7a'},
  sky: {top: '#3d74b8', mid: '#86b6e3', low: '#f2e6c9', glow: '#fff6d8', hill: '#2c3d52', text: '#ffffff', acc: '#fff1b8'},
};

const Stars = ({W, H, t, seed, n = 140}) => {
  const r = rng(seed);
  const S = Array.from({length: n}, () => [r() * W, r() * H * 0.72, 0.6 + r() * 1.8, r() * 6.28, 0.4 + r() * 1.4]);
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      {S.map(([x, y, s, ph, sp], i) => <circle key={i} cx={x} cy={y} r={s} fill="#fff" opacity={0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * sp + ph))} />)}
    </svg>
  );
};

// pessoa de braços erguidos (silhueta), centrada em (x, y = pés), altura h
const Person = ({x, y, h, color}) => {
  const k = h / 110;
  const P = [[-10, 0], [-8, -46], [-7, -52], [-10, -74], [-11, -77], [-27, -105], [-25, -109], [-21, -107], [-7, -81], [-3, -82], [3, -82], [7, -81], [21, -107], [25, -109], [27, -105], [11, -77], [10, -74], [7, -52], [8, -46], [10, 0], [3, 0], [1, -40], [-1, -40], [-3, 0]];
  const d = 'M' + P.map(([a, b]) => `${x + a * k},${y + b * k}`).join(' L') + ' Z';
  return <g><path d={d} fill={color} strokeLinejoin="round" stroke={color} strokeWidth={1.5 * k} /><ellipse cx={x} cy={y - 89 * k} rx={6 * k} ry={7 * k} fill={color} /></g>;
};

const Grass = ({W, H, color, seed}) => {
  const r = rng(seed + 11), y0 = H * 0.86;
  const blades = Array.from({length: 220}, () => [r() * W, 8 + r() * 46, (r() - 0.5) * 14]);
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <rect x={0} y={y0} width={W} height={H - y0} fill={color} />
      {blades.map(([x, h, lean], i) => <path key={i} d={`M${x - 2},${y0 + 2} Q${x + lean * 0.5},${y0 - h * 0.6} ${x + lean},${y0 - h} Q${x + lean * 0.4},${y0 - h * 0.5} ${x + 2},${y0 + 2} Z`} fill={color} />)}
    </svg>
  );
};

const Moon = ({W, H, x = 0.72, y = 0.3, r = 0.035}) => {
  const R = Math.min(W, H) * r * 2.2;
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <defs><radialGradient id="mg" cx="50%" cy="50%" r="50%"><stop offset="0%" stopColor="#dfe8ff" stopOpacity="0.55" /><stop offset="100%" stopColor="#dfe8ff" stopOpacity="0" /></radialGradient></defs>
      <circle cx={W * x} cy={H * y} r={R * 3} fill="url(#mg)" />
      <path d={`M${W * x + R * 0.2},${H * y - R} A${R},${R} 0 1,0 ${W * x + R * 0.2},${H * y + R} A${R * 0.78},${R * 0.86} 0 1,1 ${W * x + R * 0.2},${H * y - R} Z`} fill="#f4f1e6" />
    </svg>
  );
};

const Hills = ({W, H, color, cross, t}) => {
  const y0 = H * 0.78;
  const d = `M0,${H} L0,${y0 + 40} C${W * 0.18},${y0 - 30} ${W * 0.32},${y0 + 10} ${W * 0.5},${y0 - 40} C${W * 0.66},${y0 - 80} ${W * 0.82},${y0 + 20} ${W},${y0 - 10} L${W},${H} Z`;
  const cx = W * 0.5, cy = y0 - 40, ch = H * 0.2, cw = ch * 0.08;
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <path d={d} fill={color} />
      {cross ? (
        <g opacity={0.95}>
          <rect x={cx - cw / 2} y={cy - ch} width={cw} height={ch} fill={color} />
          <rect x={cx - ch * 0.32} y={cy - ch * 0.74} width={ch * 0.64} height={cw} fill={color} />
        </g>
      ) : null}
    </svg>
  );
};

const Rays = ({W, H, t, color, x = 0.5, y = 0.62, op = 0.18}) => (
  <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, mixBlendMode: 'screen'}}>
    <defs>
      <radialGradient id="rg" cx="50%" cy="50%" r="50%"><stop offset="0%" stopColor={color} stopOpacity="0.9" /><stop offset="100%" stopColor={color} stopOpacity="0" /></radialGradient>
    </defs>
    <g transform={`translate(${W * x},${H * y}) rotate(${t * 2})`}>
      {Array.from({length: 14}, (_, i) => <path key={i} d={`M0,0 L${-W * 0.05},${-H * 1.4} L${W * 0.05},${-H * 1.4} Z`} fill={color} opacity={op * (0.5 + 0.5 * Math.sin(i * 1.7 + t * 0.6))} transform={`rotate(${i * (360 / 14)})`} />)}
    </g>
    <circle cx={W * x} cy={H * y} r={Math.min(W, H) * 0.32} fill="url(#rg)" opacity={0.75} />
  </svg>
);

const Clouds = ({W, H, t, seed, color = '#ffffff', n = 9}) => {
  const r = rng(seed + 7);
  const C = Array.from({length: n}, () => [r() * W, H * (0.1 + r() * 0.45), W * (0.18 + r() * 0.22), H * (0.05 + r() * 0.06), 4 + r() * 10, 0.25 + r() * 0.4]);
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <defs><filter id="blur"><feGaussianBlur stdDeviation="28" /></filter></defs>
      {C.map(([x, y, rx, ry, sp, op], i) => <ellipse key={i} cx={((x + t * sp) % (W + rx * 2)) - rx} cy={y} rx={rx} ry={ry} fill={color} opacity={op} filter="url(#blur)" />)}
    </svg>
  );
};

const Candle = ({W, H, t}) => {
  const cx = W / 2, base = H * 0.86, bw = Math.min(W, H) * 0.09, bh = H * 0.22;
  const fl = 1 + 0.06 * Math.sin(t * 9) + 0.04 * Math.sin(t * 23 + 1);
  const fx = 3 * Math.sin(t * 5);
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <radialGradient id="cg" cx="50%" cy="50%" r="50%"><stop offset="0%" stopColor="#ffcf7a" stopOpacity="0.55" /><stop offset="100%" stopColor="#ffcf7a" stopOpacity="0" /></radialGradient>
        <linearGradient id="wax" x1="0" x2="1"><stop offset="0%" stopColor="#d9c3a0" /><stop offset="50%" stopColor="#f5e6cc" /><stop offset="100%" stopColor="#c7ad86" /></linearGradient>
        <radialGradient id="fl" cx="50%" cy="70%" r="60%"><stop offset="0%" stopColor="#fff8e0" /><stop offset="45%" stopColor="#ffc35a" /><stop offset="100%" stopColor="#ff7a1a" stopOpacity="0" /></radialGradient>
      </defs>
      <circle cx={cx} cy={base - bh - 40} r={Math.min(W, H) * 0.42 * fl} fill="url(#cg)" />
      <rect x={cx - bw / 2} y={base - bh} width={bw} height={bh} rx={8} fill="url(#wax)" />
      <line x1={cx} y1={base - bh} x2={cx} y2={base - bh - 14} stroke="#2a1a0a" strokeWidth={3} />
      <ellipse cx={cx + fx} cy={base - bh - 44 * fl} rx={16 * fl} ry={40 * fl} fill="url(#fl)" />
    </svg>
  );
};

const Slides = ({imgs, W, H, T, total, seed}) => {
  const n = imgs.length, seg = total / n, X = 2.2;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {imgs.map((src, i) => {
        const a = i * seg, b = (i + 1) * seg;
        const op = i === 0 ? Math.min(1, (b + X - T) / X) : Math.max(0, Math.min(1, (T - a) / X, (b + X - T) / X));
        if (op <= 0) return null;
        const p = Math.max(0, Math.min(1, (T - a) / (seg + X)));
        const dir = (i + seed) % 2 ? 1 : -1;
        return <Img key={i} src={staticFile(src)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', opacity: op,
          transform: `scale(${1.06 + 0.1 * p}) translate(${dir * (-1.5 + 3 * p)}%, ${(-0.8 + 1.6 * p)}%)`, filter: 'saturate(0.92) contrast(1.04)'}} />;
      })}
    </AbsoluteFill>
  );
};

const Painting = ({src, W, H, T, total, seed}) => {
  const r = rng(seed);
  const dir = r() > 0.5 ? 1 : -1;
  const p = Math.min(1, T / Math.max(1, total));
  const sc = 1.08 + 0.12 * p;
  const tx = dir * (-2 + 4 * p) * 1.5, ty = (-1 + 2 * p) * 1.2;
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
      <Img src={staticFile(src)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${sc}) translate(${tx}%, ${ty}%)`, filter: 'saturate(0.9) contrast(1.05)'}} />
    </AbsoluteFill>
  );
};

const Background = ({fe, W, H, T}) => {
  const P = PAL[fe.scene] || PAL.night;
  if (fe.imgs && fe.imgs.length) return <Slides imgs={fe.imgs} W={W} H={H} T={T} total={fe.total} seed={fe.seed || 1} />;
  if (fe.img) return <Painting src={fe.img} W={W} H={H} T={T} total={fe.total} seed={fe.seed || 1} />;
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${P.top} 0%, ${P.mid} 58%, ${P.low} 100%)`}}>
      {fe.scene === 'night' || !fe.scene ? <Stars W={W} H={H} t={T} seed={fe.seed || 3} /> : null}
      {fe.scene === 'night' || !fe.scene ? <Rays W={W} H={H} t={T} color={P.glow} x={0.72} y={0.2} op={0.05} /> : null}
      {fe.scene === 'dawn' ? <Rays W={W} H={H} t={T} color={P.glow} y={0.76 - Math.min(0.08, T / 600)} op={0.14} /> : null}
      {fe.scene === 'sky' ? <><Rays W={W} H={H} t={T} color={P.glow} y={-0.05} op={0.16} /><Clouds W={W} H={H} t={T} seed={fe.seed || 5} /></> : null}
      {fe.scene === 'dawn' ? <Clouds W={W} H={H} t={T} seed={fe.seed || 5} color="#ffd2b0" n={6} /> : null}
      {fe.scene === 'night' && fe.person ? <Moon W={W} H={H} x={0.5} y={H > W ? 0.6 : 0.47} /> : null}
      {fe.scene === 'candle' ? <Candle W={W} H={H} t={T} /> : fe.person ? (
        <>
          <Grass W={W} H={H} color={P.hill} seed={fe.seed || 3} />
          <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}><Person x={W * 0.5} y={H * 0.875} h={H * (H > W ? 0.16 : 0.26)} color={P.hill} /></svg>
        </>
      ) : <Hills W={W} H={H} color={P.hill} cross={fe.cross !== false} t={T} />}
    </AbsoluteFill>
  );
};

const fadeIO = (T, a, b, d = 0.45) => Math.max(0, Math.min(1, (T - a) / d, (b - T) / d));

export const Fe = ({fe}) => {
  useFonts();
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const T = f / fps;
  const P = PAL[fe.scene] || PAL.night;
  const vert = H > W;
  const lines = fe.lines || [];
  const cur = lines.find((l) => T >= l.t0 - 0.15 && T < l.t1 + 0.35);
  const titleOp = fe.title ? fadeIO(T, 0, (fe.title_end || 3.2), 0.6) : 0;
  const outroAt = fe.outro_at || fe.total - 4;
  const outroOp = fe.outro ? fadeIO(T, outroAt, fe.total + 1, 0.6) : 0;
  const len = cur ? cur.text.length : 0;
  const fs = vert ? (len > 140 ? 54 : len > 90 ? 62 : 72) : (len > 160 ? 52 : len > 100 ? 60 : 70);
  const shade = fe.img ? 0.55 : 0.18;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Background fe={fe} W={W} H={H} T={T} />
      <AbsoluteFill style={{background: `radial-gradient(${vert ? '90% 60%' : '70% 70%'} at 50% ${vert ? '45%' : '50%'}, rgba(0,0,0,${shade}) 0%, rgba(0,0,0,${shade * 0.4}) 70%, rgba(0,0,0,0) 100%)`}} />
      {fe.kicker ? (
        <div style={{position: 'absolute', top: vert ? 150 : 60, width: '100%', textAlign: 'center', fontFamily: SANS, fontWeight: 500, letterSpacing: 6, fontSize: vert ? 30 : 26, color: P.acc, textTransform: 'uppercase', opacity: 0.85, textShadow: '0 2px 12px #000a'}}>{fe.kicker}</div>
      ) : null}
      {titleOp > 0 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: titleOp}}>
          <div style={{maxWidth: vert ? 900 : 1500, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: vert ? 92 : 104, lineHeight: 1.1, color: P.text, textShadow: '0 4px 30px #000c'}}>{fe.title}</div>
          {fe.subtitle ? <div style={{marginTop: 28, fontFamily: SANS, fontWeight: 500, fontSize: vert ? 40 : 38, color: P.acc, textShadow: '0 2px 14px #000c'}}>{fe.subtitle}</div> : null}
        </AbsoluteFill>
      ) : null}
      {cur && titleOp < 0.05 && outroOp < 0.05 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: vert ? 'center' : 'center', padding: vert ? '0 70px' : '0 200px'}}>
          <div style={{opacity: fadeIO(T, cur.t0 - 0.15, cur.t1 + 0.35), transform: `translateY(${(1 - fadeIO(T, cur.t0 - 0.15, cur.t1 + 0.35)) * 14}px)`, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: fs, lineHeight: 1.28, color: P.text, textShadow: '0 3px 22px rgba(0,0,0,0.85), 0 0 2px rgba(0,0,0,0.6)'}}>{cur.text}</div>
          {cur.ref ? <div style={{marginTop: 26, opacity: fadeIO(T, cur.t0, cur.t1 + 0.35), fontFamily: SANS, fontWeight: 500, fontSize: vert ? 34 : 30, letterSpacing: 2, color: P.acc, textShadow: '0 2px 12px #000c'}}>{cur.ref}</div> : null}
        </AbsoluteFill>
      ) : null}
      {outroOp > 0 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: outroOp, padding: '0 120px'}}>
          <div style={{textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: vert ? 84 : 92, color: P.text, textShadow: '0 4px 30px #000c'}}>{fe.outro}</div>
          {fe.outro2 ? <div style={{marginTop: 26, textAlign: 'center', fontFamily: SANS, fontWeight: 500, fontSize: vert ? 40 : 36, color: P.acc, textShadow: '0 2px 14px #000c'}}>{fe.outro2}</div> : null}
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

// miniaturas 1280x720 — estilos copiados do que funciona no nicho (pesquisa 17/11/2026):
//  plegarias: céu noturno + silhueta de braços erguidos + 2 linhas enormes (branco / amarelo), condensada (Plegarias de la Noche, 49 mil inscritos)
//  luz: pintura de Jesus + título dourado grande com faixa vermelha (LUZ PARA EL ALMA / Oración Divina)
//  why: azul-marinho minimalista, título serifado, ícone (Why Would God)
const ANTON = 'AntonX, Impact, "Arial Narrow", sans-serif';
const useAnton = () => {
  const [h] = useState(() => delayRender('anton'));
  useEffect(() => { new FontFace('AntonX', `url(${staticFile('fonts/anton.woff2')})`).load().then((f) => document.fonts.add(f)).catch(() => null).then(() => continueRender(h)); }, [h]);
};

export const FeThumb = ({fe}) => {
  useFonts(); useAnton();
  const th = fe.thumb || {};
  const P = PAL[fe.scene] || PAL.night;
  const W = 1280, H = 720;
  if (th.style === 'plegarias') {
    return (
      <AbsoluteFill style={{background: 'linear-gradient(180deg, #02030a 0%, #0b1240 46%, #3b2a7a 70%, #c45a8a 84%, #1a0f2a 100%)'}}>
        <Stars W={W} H={H} t={th.t || 2} seed={fe.seed || 3} n={160} />
        <Moon W={W} H={H} x={0.5} y={0.56} r={0.02} />
        <Grass W={W} H={H} color="#020208" seed={fe.seed || 3} />
        <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}><Person x={W * 0.5} y={H * 0.875} h={H * 0.24} color="#020208" /></svg>
        <div style={{position: 'absolute', top: 26, width: '100%', textAlign: 'center', fontFamily: ANTON, lineHeight: 1.02, textShadow: '0 6px 24px #000'}}>
          <div style={{fontSize: th.s1 || 118, color: '#ffffff', letterSpacing: 1}}>{th.l1}</div>
          <div style={{fontSize: th.s2 || 150, color: '#ffc21a', letterSpacing: 1}}>{th.l2}</div>
        </div>
      </AbsoluteFill>
    );
  }
  if (th.style === 'luz') {
    return (
      <AbsoluteFill style={{background: '#000'}}>
        {th.img ? <Img src={staticFile(th.img)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', objectPosition: th.pos || 'center', filter: 'saturate(1.12) contrast(1.06) brightness(1.04)'}} /> : null}
        <AbsoluteFill style={{background: th.side === 'right' ? 'linear-gradient(270deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.45) 48%, rgba(0,0,0,0) 72%)' : 'linear-gradient(90deg, rgba(0,0,0,0.78) 0%, rgba(0,0,0,0.45) 48%, rgba(0,0,0,0) 72%)'}} />
        <div style={{position: 'absolute', top: 40, [th.side === 'right' ? 'right' : 'left']: 46, width: 640, textAlign: 'center'}}>
          {th.top ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 700, fontSize: 58, color: '#fff', textShadow: '0 4px 16px #000'}}>{th.top}</div> : null}
          <div style={{fontFamily: ANTON, fontSize: th.size || 128, lineHeight: 1.0, letterSpacing: 1, background: 'linear-gradient(180deg, #fff6c8 0%, #ffd34d 45%, #e09a12 100%)', WebkitBackgroundClip: 'text', color: 'transparent', WebkitTextStroke: '3px #3a1d00', filter: 'drop-shadow(0 6px 10px #000c)'}}>{th.big}</div>
          {th.sub ? <div style={{display: 'inline-block', marginTop: 16, background: 'linear-gradient(180deg,#d9262b,#a3141a)', color: '#fff', fontFamily: SANS, fontWeight: 700, fontSize: 40, padding: '8px 26px', borderRadius: 8, boxShadow: '0 6px 16px #000a', border: '2px solid #ffd34d'}}>{th.sub}</div> : null}
          {th.date ? <div style={{marginTop: 18, display: 'inline-block', background: '#fff', color: '#7a0f12', fontFamily: SANS, fontWeight: 700, fontSize: 34, padding: '6px 20px', borderRadius: 30, boxShadow: '0 4px 12px #000a'}}>📅 {th.date}</div> : null}
        </div>
      </AbsoluteFill>
    );
  }
  if (th.style === 'why') {
    return (
      <AbsoluteFill style={{background: 'radial-gradient(900px 600px at 50% 45%, #18224a 0%, #0a0f26 70%, #060918 100%)', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{position: 'absolute', top: 70, width: 1100, textAlign: 'center', fontFamily: '"Playfair Display", Georgia, serif', fontWeight: 700, fontSize: th.size || 92, lineHeight: 1.08, color: '#f5f1e6'}}>
          {th.l1}<br /><span style={{color: '#e9b949'}}>{th.l2}</span>
        </div>
        {th.icon ? <div style={{position: 'absolute', bottom: 70, fontSize: 200}}>{th.icon}</div> : null}
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Background fe={{...fe, total: 1}} W={W} H={H} T={th.t || 2} />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.35) 55%, rgba(0,0,0,0) 100%)'}} />
      <div style={{position: 'absolute', left: 60, top: 60, width: 760}}>
        {th.top ? <div style={{display: 'inline-block', background: P.acc, color: '#120c04', fontFamily: SANS, fontWeight: 700, fontSize: 34, padding: '6px 18px', borderRadius: 10, marginBottom: 22}}>{th.top}</div> : null}
        <div style={{fontFamily: SANS, fontWeight: 700, fontSize: th.size || 84, lineHeight: 1.02, color: '#fff', textShadow: '0 6px 0 #000a, 0 0 30px #000'}}>{th.big}</div>
        {th.sub ? <div style={{marginTop: 22, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 46, color: P.acc, textShadow: '0 3px 16px #000'}}>{th.sub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
