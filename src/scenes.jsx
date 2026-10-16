import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};

// entrada com "punch" (zoom leve) e saída curta
const Wrap = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const sc = interpolate(f, [0, 10], [1.07, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const op = interpolate(f, [0, 4, d - 4, d], [0, 1, 1, 0], clamp);
  return <AbsoluteFill style={{opacity: op, transform: `scale(${sc})`}}>{children}</AbsoluteFill>;
};

const strokeText = '0 0 6px rgba(0,0,0,.9), 0 4px 16px rgba(0,0,0,.6)';

// destaca o trecho `hl` dentro de `text`
const Highlight = ({text, hl, color}) => {
  if (!hl || !text.includes(hl)) return <>{text}</>;
  const [a, b] = text.split(hl);
  return <>{a}<span style={{color, textShadow: `0 0 40px ${color}88`}}>{hl}</span>{b}</>;
};

// legenda palavra por palavra (karaoke)
export const Karaoke = ({words, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!words || !words.length) return null;
  const t = f / fps;
  const size = 4;
  let cur = words.findIndex((w) => t >= w.t0 && t < w.t1);
  if (cur < 0) cur = t < words[0].t0 ? 0 : words.length - 1;
  const chunk = Math.floor(cur / size);
  const group = words.slice(chunk * size, chunk * size + size);
  return (
    <div style={{position: 'absolute', left: 60, right: 60, bottom: 520, display: 'flex', flexWrap: 'wrap', justifyContent: 'center'}}>
      {group.map((w, i) => {
        const idx = chunk * size + i;
        const on = idx === cur;
        const spoken = idx < cur;
        return (
          <span key={idx} style={{
            fontSize: 74, fontWeight: 900, lineHeight: 1.15, color: on ? theme.acc : '#fff', opacity: on || spoken ? 1 : 0.55,
            margin: '4px 11px', transform: `scale(${on ? 1.14 : 1})`, textShadow: strokeText, WebkitTextStroke: '2px rgba(0,0,0,.55)', paintOrder: 'stroke fill',
            transition: 'none',
          }}>{w.w}</span>
        );
      })}
    </div>
  );
};

export const TitleScene = ({sc, theme, spec}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 11, stiffness: 140}});
  const text = sc.text || spec.title;
  return (
    <Wrap>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 260}}>
        <div style={{width: 220, height: 14, borderRadius: 7, background: `linear-gradient(90deg, ${theme.acc}, ${theme.acc2})`, marginBottom: 56, transform: `scaleX(${s})`}} />
        <div style={{fontSize: 118, fontWeight: 900, lineHeight: 1.05, textAlign: 'center', padding: '0 60px', transform: `scale(${0.8 + 0.2 * s})`, textShadow: strokeText}}>
          <Highlight text={text} hl={sc.hl} color={theme.acc} />
        </div>
        {sc.sub ? <div style={{fontSize: 48, marginTop: 44, color: theme.acc, textAlign: 'center', padding: '0 70px', fontWeight: 700, opacity: interpolate(f, [8, 20], [0, 1], clamp)}}>{sc.sub}</div> : null}
      </AbsoluteFill>
      <Karaoke words={sc.words} theme={theme} />
    </Wrap>
  );
};

export const TextScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 12, stiffness: 120}});
  return (
    <Wrap>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 300}}>
        {sc.n ? <div style={{fontSize: 220, fontWeight: 900, color: theme.acc2, lineHeight: 1, marginBottom: 10, transform: `scale(${0.5 + 0.5 * s})`, textShadow: `0 0 60px ${theme.acc2}77`}}>{sc.n}</div> : null}
        <div style={{margin: '0 56px', padding: '52px 48px', background: theme.panel, borderRadius: 44, border: `3px solid ${theme.acc}55`, backdropFilter: 'blur(6px)', transform: `translateY(${(1 - s) * 60}px)`}}>
          <div style={{fontSize: 80, fontWeight: 800, lineHeight: 1.15, textAlign: 'center', textShadow: strokeText}}>
            <Highlight text={sc.text} hl={sc.hl} color={theme.acc} />
          </div>
        </div>
      </AbsoluteFill>
      <Karaoke words={sc.words} theme={theme} />
    </Wrap>
  );
};

export const StatScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = interpolate(f, [4, fps * 1.5], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const done = interpolate(f, [fps * 1.5, fps * 1.5 + 8, fps * 1.5 + 18], [1, 1.12, 1], clamp);
  const target = Number(sc.value);
  const shown = (target * t).toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: sc.decimals ?? 0});
  return (
    <Wrap>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 300}}>
        <div style={{fontSize: 54, fontWeight: 700, opacity: 0.92, marginBottom: 34, textAlign: 'center', padding: '0 80px', textShadow: strokeText}}>{sc.label}</div>
        <div style={{fontSize: 230, fontWeight: 900, color: theme.acc, transform: `scale(${done})`, textShadow: `0 0 80px ${theme.acc}99, ${strokeText}`, letterSpacing: -4}}>
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
  const W = 940, H = 760, padL = 175, padB = 70, padT = 30, padR = 50;
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
  const area = `${path} L${tip[0]},${py(Math.max(yMin, 0))} L${pts[0][0]},${py(Math.max(yMin, 0))} Z`;
  const ticks = 4;
  const pre = sc.prefix || '';
  const fmt = (v) => pre + (Math.abs(v) >= 1000 ? v.toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: 0}) : String(Math.round(v * 10) / 10));
  const xEvery = Math.ceil(n / 6);
  const gid = 'g' + (sc.title || '').length;
  return (
    <Wrap>
      <AbsoluteFill style={{alignItems: 'center'}}>
        <div style={{marginTop: 210, fontSize: 74, fontWeight: 900, textAlign: 'center', padding: '0 70px', lineHeight: 1.1, textShadow: strokeText}}>{sc.title}</div>
        {sc.subtitle ? <div style={{fontSize: 40, marginTop: 14, color: theme.acc, fontWeight: 700}}>{sc.subtitle}</div> : null}
        <div style={{marginTop: 36, background: theme.panel, borderRadius: 40, padding: '30px 10px 10px', border: `2px solid ${theme.acc}33`}}>
          <svg width={W} height={H}>
            <defs>
              <linearGradient id={gid} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={theme.acc} stopOpacity="0.45" />
                <stop offset="100%" stopColor={theme.acc} stopOpacity="0" />
              </linearGradient>
              <linearGradient id={gid + 'b'} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={theme.acc} />
                <stop offset="100%" stopColor={theme.acc2} />
              </linearGradient>
            </defs>
            {Array.from({length: ticks + 1}, (_, k) => {
              const v = yMin + ((yMax - yMin) * k) / ticks;
              return (
                <g key={k}>
                  <line x1={padL} x2={W - padR} y1={py(v)} y2={py(v)} stroke="#fff" strokeWidth={1.5} opacity={0.18} />
                  <text x={padL - 16} y={py(v) + 11} fill="#fff" opacity={0.85} fontSize={32} fontWeight={600} textAnchor="end">{fmt(v)}</text>
                </g>
              );
            })}
            {data.map((d, i) => (i % xEvery === 0 || i === n - 1) ? (
              <text key={i} x={px(i)} y={H - 22} fill="#fff" opacity={0.85} fontSize={32} fontWeight={600} textAnchor="middle">{d.x}</text>
            ) : null)}
            {isBar
              ? data.map((d, i) => {
                  const local = interpolate(draw, [i / n, Math.min((i + 1.2) / n, 1)], [0, 1], clamp);
                  const h = (py(Math.max(yMin, 0)) - py(d.y)) * local;
                  const hl = i === n - 1 || d.hl;
                  return <rect key={i} x={px(i) - bw / 2} y={py(Math.max(yMin, 0)) - h} width={bw} height={Math.max(h, 0)} rx={10} fill={hl ? `url(#${gid}b)` : theme.muted} />;
                })
              : (
                <>
                  <path d={area} fill={`url(#${gid})`} />
                  <path d={path} fill="none" stroke={theme.acc} strokeWidth={11} strokeLinecap="round" strokeLinejoin="round" style={{filter: `drop-shadow(0 0 14px ${theme.acc})`}} />
                  <circle cx={tip[0]} cy={tip[1]} r={20} fill="#fff" stroke={theme.acc} strokeWidth={8} />
                  <g transform={`translate(${Math.min(tip[0], W - 150)}, ${Math.max(tip[1] - 62, 20)})`} opacity={draw > 0.02 ? 1 : 0}>
                    <rect x={-95} y={-34} width={190} height={58} rx={29} fill={theme.acc} />
                    <text x={0} y={7} textAnchor="middle" fontSize={34} fontWeight={900} fill="#10131f">{fmt(tipY)}</text>
                  </g>
                </>
              )}
          </svg>
        </div>
        {sc.note ? <div style={{fontSize: 30, opacity: 0.7, marginTop: 16}}>{sc.note}</div> : null}
      </AbsoluteFill>
      <Karaoke words={sc.words} theme={theme} />
    </Wrap>
  );
};
