import React from 'react';
import {interpolate} from 'remotion';
import {Char} from './char.jsx';

const INK = '#1d1b2e';
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};

const Bill = ({x, y, w = 400, h = 210, value, label, color, rot = 0, scale = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${scale})`}>
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={26} fill={color} stroke={INK} strokeWidth={9} />
    <rect x={-w / 2 + 16} y={-h / 2 + 16} width={w - 32} height={h - 32} rx={16} fill="none" stroke={INK} strokeWidth={4} opacity={0.35} />
    <circle cx={-w / 2 + 62} cy={0} r={34} fill="#ffffff55" stroke={INK} strokeWidth={5} />
    <text x={-w / 2 + 62} y={14} textAnchor="middle" fontSize={44} fontFamily="Anton, Impact" fill={INK}>R$</text>
    <text x={30} y={22} textAnchor="middle" fontSize={78} fontFamily="Anton, Impact" fill={INK}>{value.replace('R$ ', '')}</text>
    <text x={0} y={h / 2 + 52} textAnchor="middle" fontSize={40} fontWeight={800} fontFamily="Inter, Arial" fill={INK}>{label}</text>
  </g>
);

// compara o mesmo poder de compra: antes x hoje
export const BrlCompare = ({sc, theme, p, t}) => {
  const k = Math.min(1, p(14));
  const grow = interpolate(t, [1.3, 2.4], [0, 1], C);
  return (
    <>
      <Bill x={235} y={250} w={380} value={sc.v1 || 'R$ 3.000'} label={sc.l1 || 'antes'} color="#bff0c7" rot={-4} scale={Math.min(1, p(0))} />
      <g opacity={k}>
        <path d="M440,250 L640,250" stroke={INK} strokeWidth={16} strokeLinecap="round" />
        <path d="M608,222 L643,250 L608,278" stroke={INK} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </g>
      <Bill x={845} y={250} w={380} value={sc.v2 || 'R$ 4.500'} label={sc.l2 || 'hoje'} color="#ffd2c8" rot={4} scale={Math.min(1, p(24)) * (0.9 + 0.1 * grow)} />
      <Char x={540} y={930} s={1.35} kind={theme.kind} theme={theme} lookAt={[845, 250]}
        beats={[{at: 0, pose: 'neutral'}, {at: 1.3, pose: 'worry'}]} />
    </>
  );
};
