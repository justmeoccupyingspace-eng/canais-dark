import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';

const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const S = {stroke: '#14161f', strokeWidth: 9, strokeLinecap: 'round', strokeLinejoin: 'round', fill: 'none'};

const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return {f, fps, t: f / fps, pop: (d = 0, damping = 11) => spring({frame: f - d, fps, config: {damping, stiffness: 150}})};
};

// ---------- personagem ----------
export const TalkCtx = React.createContext([]);
const D2R = Math.PI / 180;
const POSES = {
  idle: {L: [14, 12], R: [14, 12]},
  up: {L: [150, 8], R: [150, 8]},
  point: {L: [14, 12], R: [96, 4]},
  shock: {L: [105, -35], R: [105, -35]},
  hold: {L: [20, 20], R: [48, 62]},
  wave: {L: [14, 12], R: [150, 10]},
};
export const Bob = ({x = 540, y = 760, s = 1, pose = 'idle', theme, children}) => {
  const {f, fps, t, pop} = useT();
  const words = React.useContext(TalkCtx);
  const p = pop(0, 9);
  const target = POSES[pose] || POSES.idle;
  const idle = POSES.idle;
  const sway = Math.sin(f / 11);
  const mix = (a, b) => a + (b - a) * p;
  let La = [mix(idle.L[0], target.L[0]) + sway * 3, mix(idle.L[1], target.L[1])];
  let Ra = [mix(idle.R[0], target.R[0]) - sway * 3, mix(idle.R[1], target.R[1])];
  if (pose === 'wave') { Ra = [150 + Math.sin(f / 3) * 14, 10 + Math.sin(f / 3) * 30]; }
  if (pose === 'shock') { La[0] += Math.sin(f * 0.9) * 2; Ra[0] += Math.sin(f * 0.9) * 2; }
  const SH = [0, -110], L1 = 64, L2 = 58;
  const arm = (side, [a1, a2]) => {
    const e = [SH[0] + side * L1 * Math.sin(a1 * D2R), SH[1] + L1 * Math.cos(a1 * D2R)];
    const h = [e[0] + side * L2 * Math.sin((a1 + a2) * D2R), e[1] + L2 * Math.cos((a1 + a2) * D2R)];
    return {e, h};
  };
  const aL = arm(-1, La), aR = arm(1, Ra);
  // entrada: salta de baixo com squash & stretch
  const rise = (1 - p) * 420;
  const squash = 1 + (1 - p) * 0.12 - Math.max(0, Math.sin(Math.min(f, 14) / 14 * Math.PI)) * 0.0;
  // respiração e peso
  const breathe = Math.sin(f / 13) * 3;
  // cabeça: balanço + aceno a cada palavra
  let nod = 0, speaking = false;
  for (const w of words) {
    if (t >= w.t0 && t < w.t1) speaking = true;
    if (t >= w.t0) nod = 9 * Math.exp(-(t - w.t0) * 11);
  }
  const tilt = Math.sin(f / 23) * 3 + (speaking ? Math.sin(f / 5) * 1.5 : 0);
  // piscar
  const blink = f % 96 > 91;
  const talk = speaking ? 0.25 + 0.75 * Math.abs(Math.sin(f * 0.95)) : 0;
  const shocked = pose === 'shock';
  const legSwing = Math.sin(f / 15) * 2;
  const headY = -175 + breathe * 0.6 + nod;
  return (
    <g transform={`translate(${x},${y + rise}) scale(${s}, ${s * squash})`}>
      <ellipse cx={0} cy={72} rx={70 - (1 - p) * 30} ry={10} fill="#14161f" opacity={0.15 * p} />
      <path d={`M0,${-130 + breathe} L0,-30`} {...S} />
      <path d={`M0,-30 L${-38 + legSwing},70 M0,-30 L${38 - legSwing},70`} {...S} />
      <path d={`M${SH[0]},${SH[1] + breathe} L${aL.e[0]},${aL.e[1]} L${aL.h[0]},${aL.h[1]}`} {...S} />
      <path d={`M${SH[0]},${SH[1] + breathe} L${aR.e[0]},${aR.e[1]} L${aR.h[0]},${aR.h[1]}`} {...S} />
      {children ? children({hand: aR.h, handL: aL.h}) : null}
      <g transform={`rotate(${tilt} 0 -125) translate(0 ${headY + 175})`}>
        <circle cx={0} cy={-175} r={52} fill="#fff" stroke="#14161f" strokeWidth={9} />
        {blink
          ? <><path d="M-26,-186 L-10,-186 M10,-186 L26,-186" {...S} strokeWidth={5} /></>
          : <><circle cx={-18} cy={-185} r={shocked ? 8 : 6} fill="#14161f" /><circle cx={18} cy={-185} r={shocked ? 8 : 6} fill="#14161f" /></>}
        {shocked && <path d="M-30,-208 L-8,-214 M30,-208 L8,-214" {...S} strokeWidth={5} />}
        {talk > 0 || shocked
          ? <ellipse cx={0} cy={-150} rx={shocked ? 14 : 11 + talk * 4} ry={shocked ? 18 : 4 + talk * 13} fill="#14161f" />
          : <path d="M-18,-155 Q0,-138 18,-155" {...S} strokeWidth={6} />}
        <path d="M-56,-205 Q0,-262 56,-205 Z" fill={theme.hat} stroke="#14161f" strokeWidth={8} strokeLinejoin="round" />
        <path d="M-74,-205 L74,-205" {...S} />
      </g>
    </g>
  );
};

// ---------- props ----------
export const Coin = ({x, y, r = 44, theme, label = '$'}) => (
  <g transform={`translate(${x},${y})`}>
    <circle r={r} fill={theme.acc} stroke="#14161f" strokeWidth={8} />
    <text y={r * 0.34} textAnchor="middle" fontSize={r * 1.05} fontWeight={900} fill="#14161f" fontFamily="Inter, Arial">{label}</text>
  </g>
);

export const CoinStack = ({x, y, n, theme, w = 150}) => (
  <g>
    {Array.from({length: n}, (_, i) => (
      <g key={i}>
        <ellipse cx={x} cy={y - i * 26} rx={w / 2} ry={22} fill={theme.acc} stroke="#14161f" strokeWidth={7} />
        <rect x={x - w / 2} y={y - i * 26} width={w} height={26} fill={theme.acc} stroke="none" />
        <path d={`M${x - w / 2},${y - i * 26} L${x - w / 2},${y - i * 26 + 26} M${x + w / 2},${y - i * 26} L${x + w / 2},${y - i * 26 + 26}`} {...S} strokeWidth={7} />
        <ellipse cx={x} cy={y - i * 26 + 26} rx={w / 2} ry={22} fill={theme.acc} stroke="#14161f" strokeWidth={7} style={{clipPath: 'inset(50% 0 0 0)'}} />
        <ellipse cx={x} cy={y - i * 26} rx={w / 2} ry={22} fill={theme.acc} stroke="#14161f" strokeWidth={7} />
      </g>
    ))}
  </g>
);

export const Sign = ({x, y, text, theme, scale = 1, size = 150, color}) => (
  <g transform={`translate(${x},${y}) scale(${scale})`}>
    <rect x={-250} y={-110} width={500} height={220} rx={30} fill="#fff" stroke="#14161f" strokeWidth={9} />
    <text y={size * 0.36} textAnchor="middle" fontSize={size} fontWeight={900} fill={color || theme.acc2} stroke="#14161f" strokeWidth={6} paintOrder="stroke" fontFamily="Anton, Impact, Arial Black">{text}</text>
  </g>
);

export const Satellite = ({x, y, rot = -25, s = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-40} y={-30} width={80} height={60} rx={10} fill="#fff" stroke="#14161f" strokeWidth={8} />
    <rect x={-150} y={-22} width={90} height={44} fill="#9cc7ff" stroke="#14161f" strokeWidth={8} />
    <rect x={60} y={-22} width={90} height={44} fill="#9cc7ff" stroke="#14161f" strokeWidth={8} />
    <path d="M-105,-22 L-105,22 M105,-22 L105,22" {...S} strokeWidth={5} />
    <circle cx={0} cy={0} r={12} fill="#ffb800" stroke="#14161f" strokeWidth={5} />
  </g>
);

export const Phone = ({x, y, s = 1, theme, rot = 0}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-45} y={-80} width={90} height={160} rx={16} fill="#fff" stroke="#14161f" strokeWidth={8} />
    <circle cx={0} cy={55} r={7} fill="#14161f" />
    <circle cx={0} cy={-15} r={22} fill={theme.acc} stroke="#14161f" strokeWidth={5} />
  </g>
);

export const Clock = ({x, y, r = 60, theme, t = 0}) => (
  <g transform={`translate(${x},${y})`}>
    <circle r={r} fill="#fff" stroke="#14161f" strokeWidth={8} />
    <path d={`M0,0 L${Math.sin(t * 6) * r * 0.7},${-Math.cos(t * 6) * r * 0.7}`} {...S} strokeWidth={7} />
    <path d={`M0,0 L${Math.sin(t * 0.5) * r * 0.45},${-Math.cos(t * 0.5) * r * 0.45}`} {...S} strokeWidth={9} />
  </g>
);

const Arrow = ({x1, y1, x2, y2, color = '#ff4d4d', w = 14}) => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  const h = 38;
  return (
    <g>
      <path d={`M${x1},${y1} L${x2},${y2}`} stroke="#14161f" strokeWidth={w + 8} strokeLinecap="round" />
      <path d={`M${x2},${y2} L${x2 - h * Math.cos(a - 0.5)},${y2 - h * Math.sin(a - 0.5)} M${x2},${y2} L${x2 - h * Math.cos(a + 0.5)},${y2 - h * Math.sin(a + 0.5)}`} stroke="#14161f" strokeWidth={w + 8} strokeLinecap="round" />
      <path d={`M${x1},${y1} L${x2},${y2}`} stroke={color} strokeWidth={w} strokeLinecap="round" />
    </g>
  );
};

const Label = ({x, y, text, size = 46, bg = '#fff', color = '#14161f'}) => {
  const w = text.length * size * 0.56 + 50;
  return (
    <g transform={`translate(${x},${y})`}>
      <rect x={-w / 2} y={-size * 0.85} width={w} height={size * 1.5} rx={22} fill={bg} stroke="#14161f" strokeWidth={7} />
      <text textAnchor="middle" y={size * 0.2} fontSize={size} fontWeight={800} fill={color} fontFamily="Inter, Arial">{text}</text>
    </g>
  );
};

// ---------- composições ----------
const ARTS = {
  // personagem chocado com placa grande
  'bob-big': ({sc, theme, p}) => (
    <>
      <Bob x={540} y={800} s={1.7} pose="shock" theme={theme} />
      <Sign x={540} y={270} text={sc.big || '!'} theme={theme} scale={0.5 + 0.5 * p(4)} />
    </>
  ),
  'bob-phone': ({sc, theme, p, t}) => (
    <>
      <Bob x={540} y={820} s={1.7} pose="hold" theme={theme}>{({hand}) => <Phone x={hand[0] + 10} y={hand[1] - 30} s={0.75} theme={theme} rot={-8} />}</Bob>
      {[0, 1, 2].map((i) => (
        <text key={i} x={330 + i * 190} y={260 + Math.sin(t * 4 + i) * 20 + (i % 2) * 70} fontSize={150} fontWeight={900} fill={theme.acc2} stroke="#14161f" strokeWidth={8} paintOrder="stroke" fontFamily="Anton, Impact" opacity={Math.min(1, p(i * 5))}>?</text>
      ))}
    </>
  ),
  'sat-signal': ({theme, p, t}) => {
    const k = (t * 1.2) % 1;
    return (
      <>
        <Satellite x={820} y={280} s={1.6} />
        {[0, 1, 2].map((i) => {
          const kk = (k + i / 3) % 1;
          return <circle key={i} cx={820} cy={280} r={80 + kk * 560} fill="none" stroke={theme.acc} strokeWidth={10} opacity={1 - kk} />;
        })}
        <Label x={820} y={470} text="TIME 12:00:00.000" size={38} bg={theme.acc} />
        <Bob x={290} y={880} s={1.6} pose="hold" theme={theme}>{({hand}) => <Phone x={hand[0] + 10} y={hand[1] - 30} s={0.75} theme={theme} rot={-8} />}</Bob>
      </>
    );
  },
  'signal-travel': ({theme, p, t}) => {
    const k = Math.min((t % 2.2) / 1.6, 1);
    const x1 = 840, y1 = 300, x2 = 300, y2 = 860;
    return (
      <>
        <Satellite x={x1} y={y1} s={1.5} />
        <path d={`M${x1},${y1} L${x2},${y2}`} {...S} strokeDasharray="4 22" strokeWidth={8} />
        <circle cx={x1 + (x2 - x1) * k} cy={y1 + (y2 - y1) * k} r={26} fill={theme.acc} stroke="#14161f" strokeWidth={7} />
        <Bob x={260} y={1040} s={1.3} pose="point" theme={theme}>{({handL}) => <Phone x={handL[0] - 5} y={handL[1] - 10} s={0.6} theme={theme} />}</Bob>
        <Label x={540} y={560} text="delay × speed of light" size={40} bg="#fff" />
        <Label x={540} y={650} text="= distance" size={52} bg={theme.acc} />
      </>
    );
  },
  'ruler': ({sc, theme, p, t}) => (
    <>
      <rect x={140} y={520} width={800} height={150} rx={14} fill="#fff" stroke="#14161f" strokeWidth={9} />
      {Array.from({length: 31}, (_, i) => (
        <path key={i} d={`M${160 + i * 25.8},520 L${160 + i * 25.8},${i % 5 === 0 ? 590 : 560}`} {...S} strokeWidth={5} />
      ))}
      {[0, 10, 20, 30].map((v, i) => (
        <text key={i} x={160 + v * 25.8} y={650} textAnchor="middle" fontSize={34} fontWeight={800} fontFamily="Inter, Arial" fill="#14161f">{v}</text>
      ))}
      <circle cx={160 + 25.8 * 30 * Math.min(1, t / 1.4)} cy={440} r={30} fill={theme.acc} stroke="#14161f" strokeWidth={8} />
      <Arrow x1={160} y1={440} x2={160 + 25.8 * 30 * Math.min(1, t / 1.4)} y2={440} color={theme.acc2} w={12} />
      <Label x={540} y={800} text="1 nanosecond" size={52} bg={theme.acc} />
    </>
  ),
  'trilat': ({theme, p, t}) => {
    const k = Math.min(t / 1.6, 1);
    const pts = [[260, 360], [830, 330], [540, 1000]];
    const target = [545, 620];
    return (
      <>
        {pts.map(([x, y], i) => {
          const r = Math.hypot(target[0] - x, target[1] - y);
          return (
            <g key={i}>
              <circle cx={x} cy={y} r={r * k} fill="none" stroke={[theme.acc, theme.acc2, theme.blue][i]} strokeWidth={10} />
              <Satellite x={x} y={y} s={0.8} rot={i * 20 - 20} />
            </g>
          );
        })}
        <circle cx={target[0]} cy={target[1]} r={22 * Math.min(1, p(40))} fill="#14161f" />
        <Phone x={target[0] + 70} y={target[1] - 20} s={0.7} theme={theme} />
        <Clock x={900} y={1000} r={64} theme={theme} t={t} />
        <Label x={900} y={1120} text="+1 clock fix" size={34} bg={theme.acc} />
      </>
    );
  },
  'inflation': ({theme, p, t}) => {
    const k = Math.min(t / 2, 1);
    return (
      <>
        <Coin x={300} y={560} r={70 * (1 - 0.45 * k)} theme={theme} />
        <Label x={300} y={760} text="$1 buys less" size={40} bg="#fff" />
        {[0, 1, 2].map((i) => (
          <g key={i} transform={`translate(${650 + i * 120},${900 - (160 + i * 120) * Math.min(1, Math.max(0, (t - 0.2 * i) / 1.2))})`} opacity={Math.min(1, t / 0.4)}>
            <rect x={-45} y={0} width={90} height={160 + i * 120} rx={10} fill={theme.acc2} stroke="#14161f" strokeWidth={8} />
          </g>
        ))}
        <Arrow x1={640} y1={430} x2={900} y2={330} color={theme.acc2} />
        <Label x={760} y={1020} text="PRICES ↑" size={60} bg={theme.acc} />
      </>
    );
  },
  'cta': ({theme, p, t}) => (
    <>
      <Bob x={540} y={800} s={1.7} pose="wave" theme={theme} />
      <g transform={`translate(540,330) scale(${0.85 + 0.1 * Math.sin(t * 6)})`}>
        <rect x={-260} y={-70} width={520} height={140} rx={70} fill={theme.acc2} stroke="#14161f" strokeWidth={9} />
        <text y={32} textAnchor="middle" fontSize={96} fill="#fff" stroke="#14161f" strokeWidth={6} paintOrder="stroke" fontFamily="Anton, Impact">FOLLOW</text>
      </g>
    </>
  ),
  'coins-grow': ({theme, p, t}) => (
    <>
      <Bob x={300} y={900} s={1.5} pose="up" theme={theme} />
      {[0, 1, 2].map((i) => <CoinStack key={i} x={600 + i * 170} y={900} n={Math.max(1, Math.round((i + 1) * 3 * Math.min(1, t / 1.5)))} theme={theme} w={140} />)}
    </>
  ),
};

export const Art = ({sc, theme}) => {
  const {f, fps, t, pop} = useT();
  const Comp = ARTS[sc.art] || ARTS['bob-big'];
  return (
    <TalkCtx.Provider value={sc.words || []}>
      <svg width={1080} height={1100} viewBox="0 0 1080 1100" style={{position: 'absolute', left: 0, top: 330, overflow: 'visible', transform: `scale(${1 + 0.05 * Math.min(t / 6, 1)})`, transformOrigin: '540px 500px'}}>
        <Comp sc={sc} theme={theme} p={pop} t={t} f={f} fps={fps} />
      </svg>
    </TalkCtx.Provider>
  );
};
