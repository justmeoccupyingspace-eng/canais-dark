import React from 'react';
import {interpolate} from 'remotion';
import {Char} from './char.jsx';

const INK = '#1d1b2e';
const MONO = '"DejaVu Sans Mono", Menlo, Consolas, "Liberation Mono", monospace';
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};

const Chip = ({x, y, text, color = '#fff', size = 54, hlIndex = -1, hlColor}) => {
  const w = text.length * size * 0.62 + 60;
  return (
    <g transform={`translate(${x},${y})`}>
      <rect x={-w / 2} y={-size * 0.95} width={w} height={size * 1.6} rx={20} fill={color} stroke={INK} strokeWidth={7} />
      <text textAnchor="middle" y={size * 0.22} fontSize={size} fontWeight={800} fontFamily={MONO} fill={INK}>
        {text.split('').map((c, i) => <tspan key={i} fill={i === hlIndex ? hlColor : INK} fontWeight={i === hlIndex ? 900 : 800}>{c}</tspan>)}
      </text>
    </g>
  );
};

const Hex = ({x, y, hex, other, show, theme, size = 40}) => {
  const lines = [hex.slice(0, 32), hex.slice(32)];
  const lo = [other ? other.slice(0, 32) : '', other ? other.slice(32) : ''];
  return (
    <g>
      {lines.map((ln, li) => (
        <text key={li} x={x} y={y + li * (size + 14)} textAnchor="middle" fontSize={size} fontFamily={MONO} fontWeight={700} fill={INK}>
          {ln.split('').map((c, i) => {
            const idx = li * 32 + i;
            const diff = other && c !== lo[li][i];
            const on = diff && show > idx / 64;
            return <tspan key={i} fill={on ? '#fff' : INK} style={on ? {paintOrder: 'stroke'} : {}} stroke={on ? theme.acc2 : 'none'} strokeWidth={on ? 10 : 0}>{c}</tspan>;
          })}
        </text>
      ))}
    </g>
  );
};

const firstDiff = (a, b) => { for (let i = 0; i < Math.max(a.length, b.length); i++) if (a[i] !== b[i]) return i; return -1; };

export const HashCompare = ({sc, theme, p, t, f}) => {
  const h = sc.hashdata || {a: 'hello', b: 'hellp', ha: '0'.repeat(64), hb: '1'.repeat(64)};
  const show = interpolate(t, [1.6, 3.2], [0, 1], C);
  const pop = (d) => Math.min(1, p(d));
  const di = firstDiff(h.a, h.b);
  return (
    <>
      <g opacity={pop(0)}>
        <Chip x={540} y={70} text={h.a} color="#fff" />
        <Hex x={540} y={165} hex={h.ha} theme={theme} show={0} />
      </g>
      <g opacity={pop(12)}>
        <Chip x={540} y={380} text={h.b} color="#fff" hlIndex={di} hlColor={theme.acc2} />
        <Hex x={540} y={475} hex={h.hb} other={h.ha} theme={theme} show={show} />
      </g>
      <Char x={540} y={950} s={1.1} kind={theme.kind} theme={theme} lookAt={[540, 470]}
        beats={[{at: 0, pose: 'neutral'}, {at: 1.6, pose: 'shock'}]} />
    </>
  );
};

export const HashOne = ({sc, theme, p, t, f}) => {
  const h = sc.hashdata || {a: 'hello', ha: '0'.repeat(64)};
  const pop = (d) => Math.min(1, p(d));
  return (
    <>
      <g opacity={pop(0)}><Chip x={250} y={150} text={h.a} /></g>
      <g opacity={pop(10)}>
        <path d="M400,150 L520,150" stroke={INK} strokeWidth={14} strokeLinecap="round" />
        <path d="M500,125 L530,150 L500,175" stroke={INK} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </g>
      <g opacity={pop(18)} transform={`translate(790,150) scale(${0.8 + 0.2 * pop(18)})`}>
        <rect x={-190} y={-80} width={380} height={160} rx={28} fill={theme.acc} stroke={INK} strokeWidth={8} />
        <text textAnchor="middle" y={22} fontSize={64} fontFamily="Anton, Impact" fill={INK}>SHA-256</text>
      </g>
      <g opacity={interpolate(t, [1.4, 1.9], [0, 1], C)}>
        <Chip x={540} y={400} text="64 characters" color={theme.acc2} size={50} />
        <Hex x={540} y={500} hex={h.ha} theme={theme} show={0} />
      </g>
      <Char x={540} y={950} s={1.1} kind={theme.kind} theme={theme} lookAt={[540, 500]}
        beats={[{at: 0, pose: 'neutral'}, {at: 1.2, pose: 'point'}]} />
    </>
  );
};

export const BitGrid = ({sc, theme, p, t, f}) => {
  const flips = (sc.hashdata && sc.hashdata.flips) || Array.from({length: 256}, (_, i) => i % 2 === 0);
  const rowsShown = interpolate(t, [0.4, 3.0], [0, 16], C);
  const cell = 46, gap = 4, ox = (1080 - 16 * (cell + gap)) / 2 + 2, oy = 30;
  const count = flips.reduce((n, b, i) => n + (b && Math.floor(i / 16) < rowsShown ? 1 : 0), 0);
  return (
    <>
      <g>
        {flips.map((b, i) => {
          const r = Math.floor(i / 16), c = i % 16;
          const vis = interpolate(rowsShown - r, [0, 1], [0, 1], C);
          return (
            <rect key={i} x={ox + c * (cell + gap)} y={oy + r * (cell + gap)} width={cell} height={cell} rx={9}
              fill={b ? theme.acc2 : '#e7e9f1'} stroke={INK} strokeWidth={b ? 5 : 3} opacity={vis} transform={`scale(${0.6 + 0.4 * vis})`} style={{transformOrigin: `${ox + c * (cell + gap) + cell / 2}px ${oy + r * (cell + gap) + cell / 2}px`}} />
          );
        })}
      </g>
      <g transform="translate(470,930)">
        <rect x={-250} y={-58} width={500} height={92} rx={24} fill="#fff" stroke={INK} strokeWidth={7} />
        <text textAnchor="middle" y={12} fontSize={56} fontFamily="Anton, Impact" fill={INK}>{count} / 256 flipped</text>
      </g>
      <Char x={930} y={1010} s={0.7} kind={theme.kind} theme={theme} lookAt={[540, 400]}
        beats={[{at: 0, pose: 'confused'}, {at: 3.0, pose: 'smug'}]} />
    </>
  );
};
