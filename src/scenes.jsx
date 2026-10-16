import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';
import {Art} from './art.jsx';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const ANTON = 'Anton, Impact, "Arial Black", sans-serif';

// corte rápido: entra com leve zoom, sem fade longo
const Wrap = ({children, intro}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const sc = intro
    ? interpolate(f, [0, 10], [1.4, 1], {...clamp, easing: Easing.out(Easing.exp)})
    : interpolate(f, [0, 8], [1.05, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const dx = intro ? 0 : interpolate(f, [0, 7], [90, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const shake = intro ? Math.exp(-f / 5) * 26 : 0;
  const sx = Math.sin(f * 2.7) * shake, sy = Math.cos(f * 3.1) * shake;
  const op = interpolate(f, [0, 2, d - 2, d], [intro ? 1 : 0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: op, transform: `translate(${dx + sx}px, ${sy}px) scale(${sc})`}}>
      {children}
      {intro ? <Burst /> : null}
      {intro ? <AbsoluteFill style={{background: '#fff', opacity: interpolate(f, [0, 5], [0.9, 0], clamp), pointerEvents: 'none'}} /> : null}
    </AbsoluteFill>
  );
};

// estouro de formas coloridas no começo
const Burst = () => {
  const f = useCurrentFrame();
  const cols = ['#ffb800', '#ff4d4d', '#2f6bff', '#00c389', '#ff4d8d'];
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: 26}, (_, i) => {
        const ang = (i / 26) * Math.PI * 2 + (i % 3) * 0.2;
        const sp = 520 + (i % 5) * 140;
        const k = 1 - Math.exp(-f / 7);
        const x = 540 + Math.cos(ang) * sp * k, y = 760 + Math.sin(ang) * sp * k * 1.15 + f * f * 0.6;
        const o = interpolate(f, [0, 4, 26, 38], [0, 1, 1, 0], clamp);
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 26 + (i % 4) * 10, height: 26 + (i % 4) * 10, background: cols[i % 5], border: '5px solid #14161f', borderRadius: i % 2 ? '50%' : 6, opacity: o, transform: `rotate(${f * (8 + i)}deg)`}} />;
      })}
    </AbsoluteFill>
  );
};

const Highlight = ({text, hl, theme}) => {
  if (!hl || !text.includes(hl)) return <>{text}</>;
  const [a, b] = text.split(hl);
  return <>{a}<span style={{background: theme.acc, padding: '0 14px', borderRadius: 10, boxDecoration: 'clone'}}>{hl}</span>{b}</>;
};

// cabeçalho: frase-chave da cena
const Headline = ({sc, theme, intro}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const text = sc.text || sc.title;
  if (!text) return null;
  const hl = sc.hl && text.includes(sc.hl) ? sc.hl : null;
  const parts = hl ? text.split(hl) : [text];
  const tokens = [];
  parts.forEach((part, i) => {
    part.split(' ').filter(Boolean).forEach((w) => tokens.push({w, hl: false}));
    if (hl && i < parts.length - 1) tokens.push({w: hl, hl: true});
  });
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: 150, textAlign: 'center', fontFamily: ANTON, fontSize: intro ? 112 : 92, lineHeight: 1.1, color: theme.ink, textTransform: 'uppercase'}}>
      {tokens.map((tk, i) => {
        const s = spring({frame: f - i * (intro ? 2 : 3), fps, config: {damping: intro ? 7 : 10, stiffness: intro ? 260 : 190}});
        return (
          <span key={i} style={{display: 'inline-block', margin: '0 12px', transform: `translateY(${(1 - s) * 50}px) scale(${(intro ? 0.2 : 0.6) + (intro ? 0.8 : 0.4) * s}) rotate(${intro ? (1 - s) * -8 : 0}deg)`, opacity: Math.min(1, s * 1.5), background: tk.hl ? theme.acc : 'transparent', padding: tk.hl ? '0 14px' : 0, borderRadius: 10}}>{tk.w}</span>
        );
      })}
    </div>
  );
};

// legenda: 1–3 palavras por vez, fonte de impacto, palavra atual em destaque
export const Karaoke = ({words, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!words || !words.length) return null;
  const t = f / fps;
  const size = 3;
  let cur = words.findIndex((w) => t >= w.t0 && t < w.t1);
  if (cur < 0) cur = t < words[0].t0 ? 0 : words.length - 1;
  const chunk = Math.floor(cur / size);
  const group = words.slice(chunk * size, chunk * size + size);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, bottom: 400, display: 'flex', flexWrap: 'wrap', justifyContent: 'center'}}>
      {group.map((w, i) => {
        const idx = chunk * size + i;
        const on = idx === cur;
        return (
          <span key={idx} style={{
            fontFamily: ANTON, fontSize: 118, lineHeight: 1.12, margin: '0 14px', textTransform: 'uppercase',
            color: on ? theme.acc : '#fff', WebkitTextStroke: '16px #14161f', paintOrder: 'stroke fill',
            transform: `scale(${on ? 1 + 0.26 * Math.exp(-Math.max(0, t - w.t0) * 9) + 0.04 : 1}) rotate(${on ? Math.sin(idx * 2.1) * 2 : 0}deg)`, opacity: idx > cur ? 0.0 : 1,
          }}>{w.w.replace(/[.,;:!?]+$/, '')}</span>
        );
      })}
    </div>
  );
};

export const ArtScene = ({sc, theme, spec}) => (
  <Wrap intro={sc.intro}>
    <Headline sc={sc} theme={theme} intro={sc.intro} />
    <Art sc={sc} theme={theme} />
    <Karaoke words={sc.words} theme={theme} />
  </Wrap>
);

export const StatScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = interpolate(f, [4, fps * 1.5], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const done = interpolate(f, [fps * 1.5, fps * 1.5 + 8, fps * 1.5 + 18], [1, 1.12, 1], clamp);
  const shown = (Number(sc.value) * t).toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: sc.decimals ?? 0});
  return (
    <Wrap>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 380}}>
        <div style={{fontFamily: ANTON, fontSize: 70, textAlign: 'center', padding: '0 70px', textTransform: 'uppercase', marginBottom: 24}}>{sc.label}</div>
        <div style={{fontFamily: ANTON, fontSize: 300, lineHeight: 1, color: theme.acc, WebkitTextStroke: '14px #14161f', paintOrder: 'stroke fill', transform: `scale(${done})`}}>
          {sc.prefix || ''}{shown}{sc.suffix || ''}
        </div>
      </AbsoluteFill>
      <Karaoke words={sc.words} theme={theme} />
    </Wrap>
  );
};

export const ChartScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = interpolate(f, [8, fps * (sc.drawSeconds || 3)], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const W = 940, H = 800, padL = 175, padB = 70, padT = 30, padR = 50;
  const data = sc.data || [];
  const ys = data.map((d) => d.y);
  const yMin = sc.yMin ?? Math.min(0, ...ys);
  const rawMax = Math.max(...ys) * 1.05;
  const mag = Math.pow(10, Math.floor(Math.log10((rawMax - yMin) / 4)));
  const stepN = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((st) => st * 4 >= rawMax - yMin);
  const yMax = sc.yMax ?? yMin + stepN * 4;
  const px = (i) => padL + (i / Math.max(data.length - 1, 1)) * (W - padL - padR);
  const py = (y) => padT + (1 - (y - yMin) / (yMax - yMin)) * (H - padT - padB);
  const isBar = sc.kind === 'bar';
  const n = data.length;
  const bw = ((W - padL - padR) / n) * 0.62;
  const pts = data.map((d, i) => [px(i), py(d.y)]);
  const total = pts.reduce((s, p, i) => (i ? s + Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) : 0), 0);
  const visibleLen = total * draw;
  let acc = 0, path = '', tip = pts[0], tipY = ys[0];
  pts.forEach((p, i) => {
    if (i === 0) { path = `M${p[0]},${p[1]}`; return; }
    const seg = Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
    if (acc + seg <= visibleLen) { path += ` L${p[0]},${p[1]}`; tip = p; tipY = ys[i]; }
    else if (acc < visibleLen) {
      const r = (visibleLen - acc) / seg;
      const q = [pts[i - 1][0] + (p[0] - pts[i - 1][0]) * r, pts[i - 1][1] + (p[1] - pts[i - 1][1]) * r];
      path += ` L${q[0]},${q[1]}`; tip = q; tipY = ys[i - 1] + (ys[i] - ys[i - 1]) * r;
    }
    acc += seg;
  });
  const ticks = 4;
  const pre = sc.prefix || '';
  const fmt = (v) => pre + (Math.abs(v) >= 1000 ? v.toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: 0}) : String(Math.round(v * 10) / 10));
  const xEvery = Math.ceil(n / 6);
  const base = py(Math.max(yMin, 0));
  return (
    <Wrap>
      <Headline sc={{text: sc.title, hl: sc.hl}} theme={theme} />
      <AbsoluteFill style={{alignItems: 'center', top: 330}}>
        <div style={{background: '#fffdf6', borderRadius: 36, padding: '24px 10px 6px', border: '9px solid #14161f', boxShadow: '12px 12px 0 #14161f'}}>
          <svg width={W} height={H}>
            {Array.from({length: ticks + 1}, (_, k) => {
              const v = yMin + ((yMax - yMin) * k) / ticks;
              return (
                <g key={k}>
                  <line x1={padL} x2={W - padR} y1={py(v)} y2={py(v)} stroke="#14161f" strokeWidth={2} opacity={0.2} />
                  <text x={padL - 16} y={py(v) + 12} fill="#14161f" fontSize={34} fontWeight={800} textAnchor="end" fontFamily="Inter, Arial">{fmt(v)}</text>
                </g>
              );
            })}
            <path d={`M${padL},${padT} L${padL},${base} L${W - padR},${base}`} fill="none" stroke="#14161f" strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
            {data.map((d, i) => (i % xEvery === 0 || i === n - 1) ? (
              <text key={i} x={px(i)} y={H - 22} fill="#14161f" fontSize={34} fontWeight={800} textAnchor="middle" fontFamily="Inter, Arial">{d.x}</text>
            ) : null)}
            {isBar
              ? data.map((d, i) => {
                  const local = interpolate(draw, [i / n, Math.min((i + 1.2) / n, 1)], [0, 1], clamp);
                  const h = (base - py(d.y)) * local;
                  const hl = i === n - 1 || d.hl;
                  return <rect key={i} x={px(i) - bw / 2} y={base - h} width={bw} height={Math.max(h, 0)} fill={hl ? theme.acc2 : theme.acc} stroke="#14161f" strokeWidth={7} />;
                })
              : (
                <>
                  <path d={path} fill="none" stroke="#14161f" strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" />
                  <path d={path} fill="none" stroke={theme.acc2} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" />
                  <circle cx={tip[0]} cy={tip[1]} r={22} fill={theme.acc} stroke="#14161f" strokeWidth={8} />
                  <g transform={`translate(${Math.min(tip[0], W - 160)}, ${Math.max(tip[1] - 70, 24)})`} opacity={draw > 0.02 ? 1 : 0}>
                    <rect x={-100} y={-36} width={200} height={62} rx={16} fill={theme.acc} stroke="#14161f" strokeWidth={6} />
                    <text x={0} y={9} textAnchor="middle" fontSize={38} fill="#14161f" fontFamily={ANTON}>{fmt(tipY)}</text>
                  </g>
                </>
              )}
          </svg>
        </div>
        {sc.note ? <div style={{fontSize: 30, fontWeight: 700, opacity: 0.6, marginTop: 24, fontFamily: 'Inter, Arial'}}>{sc.note}</div> : null}
      </AbsoluteFill>
      <Karaoke words={sc.words} theme={theme} />
    </Wrap>
  );
};
