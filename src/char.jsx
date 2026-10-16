import React from 'react';
import {useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';

// Personagem v2: corpo "feijão" colorido, membros de borracha, olhos que seguem o dado,
// sobrancelhas que carregam a emoção, boca ligada ao volume real da voz.
export const EnvCtx = React.createContext({env: [], words: []});

const INK = '#1d1b2e';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};

// alvos das mãos (coordenadas do personagem; pés em 0,0; ombros em ±42,-118)
const POSES = {
  neutral: {L: [-78, -70], R: [78, -70], brow: [0, 0, 0, 0], mouth: 'smile', tilt: 0, jump: 0},
  point:   {L: [-70, -78], R: [150, -150], brow: [0, 0, 0, 0], mouth: 'smile', tilt: -4, jump: 0},
  shock:   {L: [-105, -190], R: [105, -190], brow: [-16, -16, 0, 0], mouth: 'o', tilt: 0, jump: 46, lift: true},
  smug:    {L: [30, -100], R: [-30, -100], brow: [4, 4, 6, -6], mouth: 'smirk', tilt: 6, jump: 0},
  confused:{L: [-78, -70], R: [60, -215], brow: [-14, 4, -3, 5], mouth: 'wavy', tilt: 12, jump: 0},
  think:   {L: [-78, -70], R: [34, -160], brow: [-8, 2, 0, 4], mouth: 'flat', tilt: -8, jump: 0},
  cheer:   {L: [-112, -280], R: [112, -280], brow: [-14, -14, 0, 0], mouth: 'big', tilt: 0, jump: 56, lift: true},
  worry:   {L: [-64, -196], R: [64, -196], brow: [6, 6, 10, -10], mouth: 'wavy', tilt: 0, jump: 0},
};
export const POSE_NAMES = Object.keys(POSES);

const rnd = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };

const Limb = ({x1, y1, x2, y2, bend, color, w = 15}) => {
  const mx = (x1 + x2) / 2 + bend, my = (y1 + y2) / 2 + Math.abs(bend) * 0.4;
  const d = `M${x1},${y1} Q${mx},${my} ${x2},${y2}`;
  return (
    <g>
      <path d={d} stroke={INK} strokeWidth={w + 11} strokeLinecap="round" fill="none" />
      <path d={d} stroke={color} strokeWidth={w} strokeLinecap="round" fill="none" />
      <circle cx={x2} cy={y2} r={w * 0.95 + 4} fill={color} stroke={INK} strokeWidth={6} />
    </g>
  );
};

const Head = ({kind, color, rot}) => {
  if (kind === 'gear') {
    return (
      <g>
        <g transform={`rotate(${rot})`}>
          {Array.from({length: 10}, (_, i) => (
            <rect key={i} x={-13} y={-78} width={26} height={24} rx={6} fill={color} stroke={INK} strokeWidth={7} transform={`rotate(${i * 36})`} />
          ))}
        </g>
        <circle r={62} fill={color} stroke={INK} strokeWidth={9} />
      </g>
    );
  }
  if (kind === 'pig') {
    return (
      <g>
        <ellipse cx={-48} cy={-50} rx={20} ry={26} transform="rotate(-28 -48 -50)" fill={color} stroke={INK} strokeWidth={8} />
        <ellipse cx={48} cy={-50} rx={20} ry={26} transform="rotate(28 48 -50)" fill={color} stroke={INK} strokeWidth={8} />
        <circle r={64} fill={color} stroke={INK} strokeWidth={9} />
        <rect x={-22} y={-78} width={44} height={9} rx={4} fill={INK} />
        <ellipse cx={0} cy={22} rx={30} ry={21} fill="#ff7fa6" stroke={INK} strokeWidth={6} />
        <ellipse cx={-10} cy={22} rx={4} ry={7} fill={INK} />
        <ellipse cx={10} cy={22} rx={4} ry={7} fill={INK} />
      </g>
    );
  }
  // coin
  return (
    <g>
      <circle r={64} fill={color} stroke={INK} strokeWidth={9} />
      <circle r={50} fill="none" stroke={INK} strokeWidth={4} opacity={0.35} />
    </g>
  );
};

export const Char = ({x = 540, y = 800, s = 1.5, kind = 'coin', theme, pose = 'neutral', beats, lookAt, children, flip = 1}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {env, words} = React.useContext(EnvCtx);
  const t = f / fps;
  const body = theme.char || theme.acc;
  const dark = theme.charDark || '#00000026';

  // pose atual: beats = [{at: seg, pose}] ou pose fixa
  let cur = pose, since = f;
  if (beats && beats.length) {
    cur = beats[0].pose; since = f - Math.round(beats[0].at * fps);
    for (const b of beats) if (t >= b.at) { cur = b.pose; since = f - Math.round(b.at * fps); }
  }
  const P = POSES[cur] || POSES.neutral;
  // transição: antecipação (4q) -> ação com overshoot -> repouso
  const sp = spring({frame: Math.max(since - 4, 0), fps, config: {damping: 13, stiffness: 200, mass: 0.6}});
  const wind = since < 4 ? -0.07 * Math.sin((Math.max(since, 0) / 4) * Math.PI) : 0;
  const k = Math.min(Math.max(since < 0 ? 0 : sp, 0), 1.35) + wind;
  // pose anterior (para interpolar)
  let prev = POSES.neutral;
  if (beats && beats.length) {
    const idx = beats.findIndex((b) => b.pose === cur && t >= b.at);
    let last = -1; beats.forEach((b, i) => { if (t >= b.at) last = i; });
    if (last > 0) prev = POSES[beats[last - 1].pose] || POSES.neutral;
  }
  const mix = (a, b) => a + (b - a) * k;
  const hand = (side) => {
    const a = prev[side], b = P[side];
    return [mix(a[0], b[0]), mix(a[1], b[1])];
  };
  const browV = P.brow.map((v, i) => mix(prev.brow[i], v));
  const tilt = mix(prev.tilt, P.tilt) + Math.sin(t * 1.7) * 1.2;

  // entrada: cai do alto, quica
  const enter = spring({frame: f, fps, config: {damping: 9, stiffness: 140, mass: 0.8}});
  const dropY = (1 - enter) * -520;
  const sq = 1 + (1 - enter) * 0.12;
  // pulo da pose
  const jumpEnv = P.jump ? Math.exp(-since / 9) * Math.sin(Math.min(Math.max(since, 0) / 9, 1) * Math.PI) : 0;
  const jumpY = -(P.jump || 0) * Math.min(1, Math.max(0, jumpEnv * 2.2));
  const breathe = Math.sin(t * 2.4) * 1.6;

  // fala: volume real da voz (env a 30 fps) -> abertura da boca
  const e = env && env.length ? env[Math.min(f, env.length - 1)] || 0 : 0;
  const speaking = e > 0.04;
  const open = Math.min(1, e * 2.4);

  // olhos: seguem o alvo
  const eyeC = [x, y + dropY + jumpY - 190 * s];
  let lx = 0, ly = 0;
  if (lookAt) {
    const dx = lookAt[0] - eyeC[0], dy = lookAt[1] + 330 - eyeC[1];
    const d = Math.hypot(dx, dy) || 1;
    lx = (dx / d) * 10 * flip; ly = (dy / d) * 8;
  }
  // piscar: ~3 quadros a cada 2–5 s
  const slot = Math.floor(t / 3.2);
  const blinkAt = slot * 3.2 + 0.8 + rnd(slot + 3) * 2;
  const bf = (t - blinkAt) * fps;
  const lid = bf >= 0 && bf < 4 ? [0.2, 0.9, 0.9, 0.3][Math.floor(bf)] : 0;

  const headRot = f * 0.6;
  const sh = [[-42, -118 + breathe], [42, -118 + breathe]];
  const hL = hand('L'), hR = hand('R');

  const mY = kind === 'pig' ? 24 : 0;
  const mouthShape = (() => {
    const m = P.mouth;
    if (speaking && m !== 'big' && m !== 'o') {
      return <ellipse cx={0} cy={-163} rx={13 + open * 5} ry={4 + open * 17} fill={INK} />;
    }
    switch (m) {
      case 'o': return <ellipse cx={0} cy={-160} rx={13} ry={19} fill={INK} />;
      case 'big': return <path d="M-26,-170 Q0,-128 26,-170 Z" fill={INK} stroke={INK} strokeWidth={5} strokeLinejoin="round" />;
      case 'smirk': return <path d="M-18,-160 Q4,-154 22,-170" stroke={INK} strokeWidth={6} strokeLinecap="round" fill="none" />;
      case 'wavy': return <path d="M-20,-160 Q-10,-170 0,-160 T20,-160" stroke={INK} strokeWidth={6} strokeLinecap="round" fill="none" />;
      case 'flat': return <path d="M-16,-160 L16,-160" stroke={INK} strokeWidth={6} strokeLinecap="round" />;
      default: return <path d="M-20,-166 Q0,-146 20,-166" stroke={INK} strokeWidth={6} strokeLinecap="round" fill="none" />;
    }
  })();

  return (
    <g transform={`translate(${x},${y + dropY + jumpY}) scale(${s * flip},${s * sq})`}>
      <ellipse cx={0} cy={4} rx={72 - Math.abs(jumpY) * 0.2} ry={11} fill={INK} opacity={0.16} />
      {/* pernas */}
      <path d="M-24,-34 L-30,0 M24,-34 L30,0" stroke={INK} strokeWidth={20} strokeLinecap="round" />
      <ellipse cx={-32} cy={-2} rx={26} ry={13} fill={theme.shoe || '#ffffff'} stroke={INK} strokeWidth={7} />
      <ellipse cx={32} cy={-2} rx={26} ry={13} fill={theme.shoe || '#ffffff'} stroke={INK} strokeWidth={7} />
      {/* braços atrás */}
      <Limb x1={sh[0][0]} y1={sh[0][1]} x2={hL[0]} y2={hL[1]} bend={-22} color={body} />
      {/* corpo feijão */}
      <g transform={`translate(0,${breathe * 0.5})`}>
        <path d="M-52,-60 C-58,-130 -34,-148 0,-148 C34,-148 58,-130 52,-60 C48,-30 -48,-30 -52,-60 Z" fill={body} stroke={INK} strokeWidth={9} />
        <path d="M52,-60 C58,-100 40,-136 10,-146 C40,-120 38,-70 22,-36 C42,-36 50,-44 52,-60 Z" fill={dark} />
        {kind === 'gear' && <circle cx={0} cy={-88} r={14} fill="#fff" stroke={INK} strokeWidth={6} />}
        {kind === 'coin' && <text y={-76} textAnchor="middle" fontSize={50} fontWeight={900} fill={INK} fontFamily="Anton, Impact">$</text>}
      </g>
      <Limb x1={sh[1][0]} y1={sh[1][1]} x2={hR[0]} y2={hR[1]} bend={22} color={body} />
      {children ? children({hand: hR, handL: hL}) : null}
      {/* cabeça */}
      <g transform={`translate(0,${-170 + breathe * 0.8}) rotate(${tilt})`}>
        <Head kind={kind} color={body} rot={headRot} />
        <g transform="translate(0,170)">
          {/* olhos */}
          {[-24, 24].map((ex, i) => (
            <g key={i}>
              <ellipse cx={ex} cy={-192} rx={22} ry={26} fill="#fff" stroke={INK} strokeWidth={6} />
              <circle cx={ex + lx} cy={-192 + ly} r={11} fill={INK} />
              <circle cx={ex + lx + 4} cy={-197 + ly} r={3.5} fill="#fff" />
              {lid > 0 && <ellipse cx={ex} cy={-218 + 26 * lid} rx={23} ry={26 * lid} fill={body} stroke={INK} strokeWidth={5} />}
            </g>
          ))}
          {/* sobrancelhas: [alturaL, alturaR, inclinaçãoL, inclinaçãoR] */}
          <path d={`M-42,${-228 + browV[0] * 0.8} L-8,${-228 + browV[0] * 0.8 + browV[2]}`} stroke={INK} strokeWidth={7} strokeLinecap="round" />
          <path d={`M42,${-228 + browV[1] * 0.8} L8,${-228 + browV[1] * 0.8 + browV[3]}`} stroke={INK} strokeWidth={7} strokeLinecap="round" />
          {kind === 'pig' && <ellipse cx={0} cy={-170} rx={0} ry={0} />}
          <circle cx={-44} cy={-168} r={9} fill="#ff6b8a" opacity={0.28} />
          <circle cx={44} cy={-168} r={9} fill="#ff6b8a" opacity={0.28} />
          <g transform={`translate(0,${mY})`}>{mouthShape}</g>
        </g>
      </g>
    </g>
  );
};
