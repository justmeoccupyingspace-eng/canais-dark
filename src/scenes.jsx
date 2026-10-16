import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';

const fade = (frame, dur) => interpolate(frame, [0, 8, dur - 8, dur], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

const Caption = ({text, theme}) => {
  if (!text) return null;
  return (
    <div style={{position: 'absolute', left: 70, right: 70, bottom: 190, fontSize: 52, lineHeight: 1.25, fontWeight: 600, textAlign: 'center', color: theme.ink, textShadow: '0 2px 12px rgba(0,0,0,.45)'}}>
      {text}
    </div>
  );
};

export const TitleScene = ({sc, theme, spec}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 14}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: fade(f, durationInFrames)}}>
      <div style={{width: 160, height: 10, background: theme.acc, marginBottom: 50, transform: `scaleX(${s})`}} />
      <div style={{fontSize: 96, fontWeight: 800, lineHeight: 1.1, textAlign: 'center', padding: '0 70px', transform: `translateY(${(1 - s) * 40}px)`}}>
        {sc.text || spec.title}
      </div>
      {sc.sub ? <div style={{fontSize: 46, marginTop: 40, color: theme.acc, textAlign: 'center', padding: '0 70px'}}>{sc.sub}</div> : null}
    </AbsoluteFill>
  );
};

export const TextScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: fade(f, durationInFrames)}}>
      <div style={{fontSize: 74, fontWeight: 700, lineHeight: 1.2, textAlign: 'center', padding: '0 80px'}}>{sc.text}</div>
      <Caption text={sc.caption} theme={theme} />
    </AbsoluteFill>
  );
};

export const StatScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const t = interpolate(f, [0, fps * 1.4], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const target = Number(sc.value);
  const shown = (target * t).toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: sc.decimals ?? 0});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: fade(f, durationInFrames)}}>
      <div style={{fontSize: 52, color: theme.muted === undefined ? theme.ink : theme.ink, opacity: 0.8, marginBottom: 20, textAlign: 'center', padding: '0 80px'}}>{sc.label}</div>
      <div style={{fontSize: 190, fontWeight: 800, color: theme.acc}}>{sc.prefix || ''}{shown}{sc.suffix || ''}</div>
      <Caption text={sc.caption} theme={theme} />
    </AbsoluteFill>
  );
};

export const ChartScene = ({sc, theme}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const draw = interpolate(f, [6, fps * (sc.drawSeconds || 2.6)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const W = 980, H = 1000, padL = 100, padB = 70, padT = 20, padR = 60;
  const data = sc.data || [];
  const xs = data.map((d) => d.x), ys = data.map((d) => d.y);
  const yMin = sc.yMin ?? Math.min(0, ...ys), yMax = sc.yMax ?? Math.max(...ys) * 1.08;
  const px = (i) => padL + (i / Math.max(data.length - 1, 1)) * (W - padL - padR);
  const py = (y) => padT + (1 - (y - yMin) / (yMax - yMin)) * (H - padT - padB);
  const isBar = sc.kind === 'bar';
  const n = data.length;
  const bw = (W - padL - padR) / n * 0.62;
  const pts = data.map((d, i) => [px(i), py(d.y)]);
  const total = pts.reduce((s, p, i) => (i ? s + Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) : 0), 0);
  const visibleLen = total * draw;
  let acc = 0, path = '', tip = pts[0];
  pts.forEach((p, i) => {
    if (i === 0) { path = `M${p[0]},${p[1]}`; return; }
    const seg = Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
    if (acc + seg <= visibleLen) { path += ` L${p[0]},${p[1]}`; tip = p; }
    else if (acc < visibleLen) {
      const r = (visibleLen - acc) / seg;
      const q = [pts[i - 1][0] + (p[0] - pts[i - 1][0]) * r, pts[i - 1][1] + (p[1] - pts[i - 1][1]) * r];
      path += ` L${q[0]},${q[1]}`; tip = q;
    }
    acc += seg;
  });
  const ticks = 4;
  const fmt = (v) => (Math.abs(v) >= 1000 ? v.toLocaleString(sc.locale || 'en-US', {maximumFractionDigits: 0}) : String(Math.round(v * 10) / 10));
  const xEvery = Math.ceil(n / 6);
  return (
    <AbsoluteFill style={{alignItems: 'center', opacity: fade(f, durationInFrames)}}>
      <div style={{marginTop: 150, fontSize: 66, fontWeight: 800, textAlign: 'center', padding: '0 80px', lineHeight: 1.15}}>{sc.title}</div>
      {sc.subtitle ? <div style={{fontSize: 36, marginTop: 14, color: theme.acc, textAlign: 'center', padding: '0 80px'}}>{sc.subtitle}</div> : null}
      <svg width={W} height={H} style={{marginTop: 50}}>
        {Array.from({length: ticks + 1}, (_, k) => {
          const v = yMin + ((yMax - yMin) * k) / ticks;
          return (
            <g key={k}>
              <line x1={padL} x2={W - padR} y1={py(v)} y2={py(v)} stroke={theme.muted} strokeWidth={2} opacity={0.55} />
              <text x={padL - 14} y={py(v) + 10} fill={theme.ink} opacity={0.7} fontSize={30} textAnchor="end">{fmt(v)}</text>
            </g>
          );
        })}
        {data.map((d, i) => (i % xEvery === 0 || i === n - 1) ? (
          <text key={i} x={px(i)} y={H - 20} fill={theme.ink} opacity={0.7} fontSize={30} textAnchor="middle">{d.x}</text>
        ) : null)}
        {isBar
          ? data.map((d, i) => {
              const local = interpolate(draw, [i / n, Math.min((i + 1.2) / n, 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              const h = (py(Math.max(yMin, 0)) - py(d.y)) * local;
              return <rect key={i} x={px(i) - bw / 2} y={py(Math.max(yMin, 0)) - h} width={bw} height={Math.max(h, 0)} rx={8} fill={i === n - 1 || d.hl ? theme.acc : theme.muted} />;
            })
          : (
            <>
              <path d={path} fill="none" stroke={theme.acc} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
              <circle cx={tip[0]} cy={tip[1]} r={16} fill={theme.acc} />
            </>
          )}
      </svg>
      {sc.note ? <div style={{fontSize: 30, opacity: 0.6, marginTop: 8}}>{sc.note}</div> : null}
      <Caption text={sc.caption} theme={theme} />
    </AbsoluteFill>
  );
};
