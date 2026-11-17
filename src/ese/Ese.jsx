// "E se...?" — simulações com mapa no formato que cresce no Shorts BR (Hiperfocando: território pintado com a BANDEIRA do dono,
// contorno brilhante, emoji 3D reagindo, setas verdes, selo "SÓ IMAGINAÇÃO", título-gancho enorme, legenda palavra a palavra).
// Vertical 1080x1920 (Shorts) ou 1920x1080.
import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender} from 'remotion';
import {geoMercator, geoPath, geoCentroid, geoInterpolate, geoGraticule10} from 'd3-geo';
import {feature, merge} from 'topojson-client';
import world from 'world-atlas/countries-50m.json';
import BRUF from './br_uf.json';

const COUNTRIES = feature(world, world.objects.countries).features;
const GEOMS = world.objects.countries.geometries;
const NUM = {BRA: '076', ARG: '032', CHL: '152', URY: '858', PRY: '600', BOL: '068', PER: '604', COL: '170', VEN: '862', ECU: '218', GUY: '328', SUR: '740', GUF: '254',
  MEX: '484', USA: '840', CAN: '124', PRT: '620', ESP: '724', FRA: '250', GBR: '826', DEU: '276', ITA: '380', RUS: '643', CHN: '156', IND: '356', AUS: '036', JPN: '392',
  PAN: '591', CRI: '188', NIC: '558', HND: '340', GTM: '320', SLV: '222', CUB: '192', DOM: '214', HTI: '332', BLZ: '084', AGO: '024', MOZ: '508', ZAF: '710', NGA: '566', EGY: '818', MAR: '504',
  NLD: '528', BEL: '056', CHE: '756', AUT: '040', POL: '616', UKR: '804', TUR: '792', SAU: '682', IRN: '364', KOR: '410', PRK: '408', IDN: '360', NZL: '554', GRL: '304', ISL: '352',
  NOR: '578', SWE: '752', FIN: '246', DNK: '208', IRL: '372', GRC: '300', CPV: '132', GNB: '624', STP: '678', TLS: '626'};
const BYNUM = Object.fromEntries(COUNTRIES.map((c) => [String(c.id).padStart(3, '0'), c]));
const ISO_OF = Object.fromEntries(Object.entries(NUM).map(([k, v]) => [v, k]));
// estados do Brasil (ids 'BR-AC', 'BR-RS'...) para cenários internos
const STATES = BRUF.features;
const BYKEY = Object.fromEntries(STATES.map((f) => [f.id, f]));
const featOf = (k) => BYKEY[k] || BYNUM[NUM[k]];
// cor de cada "dono" (cor principal da bandeira) e do brilho do contorno
const COL = {BRA: '#1fa84a', ARG: '#6cb4ee', CHL: '#d52b1e', URY: '#3a6fd8', PRY: '#c8102e', BOL: '#f2c200', PER: '#e8112d', COL: '#fcd116', VEN: '#cf142b', ECU: '#ffdd00',
  GUY: '#009e49', SUR: '#377e3f', GUF: '#0055a4', MEX: '#006847', USA: '#3c3b6e', CAN: '#d80621', PRT: '#046a38', ESP: '#c60b1e', FRA: '#0055a4', GBR: '#012169', RUS: '#d52b1e', CHN: '#de2910',
  DEU: '#222', ITA: '#009246', JPN: '#bc002d', IND: '#ff9933', NLD: '#ae1c28', CPV: '#003893', AGO: '#cc092f', MOZ: '#009739', GNB: '#ce1126', STP: '#12ad2b', TLS: '#dc241f', SUL: '#0a3d91'};
const GLOW = {BRA: '#c6ff2e', ARG: '#7fd3ff', URY: '#8fb8ff', CHL: '#ff6b5b', BOL: '#ffe14d', PER: '#ff6b6b', PRY: '#ff8a8a', COL: '#ffe14d', VEN: '#ffd34d', ECU: '#ffe14d', PRT: '#7dff9a', FRA: '#8fb8ff', USA: '#8fb8ff', ESP: '#ffcf40', GUY: '#c6ff2e', SUR: '#9dff9d', SUL: '#7fe0ff'};
const SANS = 'PoppinsX, "Helvetica Neue", Arial, sans-serif';
const ANTON = 'AntonX, Impact, "Arial Narrow", sans-serif';

const useFonts = () => {
  const [h] = useState(() => delayRender('fontes'));
  useEffect(() => {
    const L = [['PoppinsX', '600', 'fonts/Poppins-Medium.ttf'], ['PoppinsX', '800', 'fonts/Poppins-Bold.ttf'], ['AntonX', '400', 'fonts/anton.woff2']];
    Promise.all(L.map(([fam, w, u]) => new FontFace(fam, `url(${staticFile(u)})`, {weight: w}).load().then((f) => document.fonts.add(f)).catch(() => null))).then(() => continueRender(h));
  }, [h]);
};

const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const mix = (a, b, t) => {
  const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
  const r = Math.round(((pa >> 16) & 255) * (1 - t) + ((pb >> 16) & 255) * t), g = Math.round(((pa >> 8) & 255) * (1 - t) + ((pb >> 8) & 255) * t), bl = Math.round((pa & 255) * (1 - t) + (pb & 255) * t);
  return '#' + ((1 << 24) | (r << 16) | (g << 8) | bl).toString(16).slice(1);
};
const LAND = '#223246';

// bandeira simplificada num retângulo qualquer (território inteiro ou bolinha)
const FlagArt = ({iso, x, y, w, h}) => {
  const m = Math.min(w, h), cx = x + w / 2, cy = y + h / 2;
  const Hs = (cols) => cols.map((c, i) => <rect key={i} x={x} y={y + (h * i) / cols.length} width={w} height={h / cols.length + 0.6} fill={c} />);
  const Vs = (cols) => cols.map((c, i) => <rect key={i} x={x + (w * i) / cols.length} y={y} width={w / cols.length + 0.6} height={h} fill={c} />);
  const R = (c) => <rect x={x} y={y} width={w} height={h} fill={c} />;
  const star = (sx, sy, r, c = '#fff') => <path d={Array.from({length: 10}, (_, i) => { const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.42 : r; return `${i ? 'L' : 'M'}${sx + rr * Math.cos(a)},${sy + rr * Math.sin(a)}`; }).join(' ') + 'Z'} fill={c} />;
  switch (iso) {
    case 'BRA': return <g>{R('#009c3b')}<path d={`M${cx},${y + h * 0.1} L${x + w * 0.93},${cy} L${cx},${y + h * 0.9} L${x + w * 0.07},${cy} Z`} fill="#fedf00" />
      <circle cx={cx} cy={cy} r={m * 0.215} fill="#002776" /><path d={`M${cx - m * 0.21},${cy - m * 0.03} Q${cx},${cy - m * 0.1} ${cx + m * 0.2},${cy + m * 0.06}`} stroke="#fff" strokeWidth={m * 0.035} fill="none" />
      {[[-0.08, 0.07], [0.02, 0.1], [0.1, 0.05], [-0.03, 0.15], [0.07, 0.14]].map(([a, b], i) => <circle key={i} cx={cx + a * m} cy={cy + b * m} r={m * 0.012} fill="#fff" />)}</g>;
    case 'ARG': return <g>{Hs(['#74acdf', '#fff', '#74acdf'])}<circle cx={cx} cy={cy} r={m * 0.085} fill="#f6b40e" stroke="#85340a" strokeWidth={m * 0.008} /></g>;
    case 'URY': { const ch = (h * 5) / 9, cw = Math.min(w * 0.42, ch * 1.1); return <g>{Hs(['#fff', '#0038a8', '#fff', '#0038a8', '#fff', '#0038a8', '#fff', '#0038a8', '#fff'])}<rect x={x} y={y} width={cw} height={ch} fill="#fff" /><circle cx={x + cw / 2} cy={y + ch / 2} r={Math.min(cw, ch) * 0.27} fill="#fcd116" stroke="#7b3f00" strokeWidth={m * 0.006} /></g>; }
    case 'CHL': return <g><rect x={x} y={y} width={w} height={h / 2} fill="#fff" /><rect x={x} y={cy} width={w} height={h / 2} fill="#d52b1e" /><rect x={x} y={y} width={Math.min(w * 0.38, h * 0.5)} height={h / 2} fill="#0039a6" />{star(x + Math.min(w * 0.38, h * 0.5) / 2, y + h / 4, Math.min(w * 0.38, h * 0.5) * 0.22)}</g>;
    case 'PRY': return <g>{Hs(['#d52b1e', '#fff', '#0038a8'])}<circle cx={cx} cy={cy} r={m * 0.1} fill="#fff" stroke="#1c7a33" strokeWidth={m * 0.012} />{star(cx, cy, m * 0.04, '#f2c200')}</g>;
    case 'BOL': return <g>{Hs(['#d52b1e', '#f9e300', '#007934'])}</g>;
    case 'PER': return <g>{Vs(['#d91023', '#fff', '#d91023'])}</g>;
    case 'COL': return <g><rect x={x} y={y} width={w} height={h / 2} fill="#fcd116" /><rect x={x} y={cy} width={w} height={h / 4} fill="#003893" /><rect x={x} y={cy + h / 4} width={w} height={h / 4} fill="#ce1126" /></g>;
    case 'ECU': return <g><rect x={x} y={y} width={w} height={h / 2} fill="#ffdd00" /><rect x={x} y={cy} width={w} height={h / 4} fill="#034ea2" /><rect x={x} y={cy + h / 4} width={w} height={h / 4} fill="#ed1c24" /><circle cx={cx} cy={cy} r={m * 0.1} fill="#7fb2e5" stroke="#8a5a2b" strokeWidth={m * 0.015} /></g>;
    case 'VEN': return <g>{Hs(['#ffcc00', '#00247d', '#cf142b'])}{Array.from({length: 8}, (_, i) => { const a = Math.PI * (1.12 + (i * 0.76) / 7); return <circle key={i} cx={cx + Math.cos(a) * m * 0.16} cy={cy + m * 0.1 + Math.sin(a) * m * 0.16} r={m * 0.014} fill="#fff" />; })}</g>;
    case 'GUY': return <g>{R('#009e49')}<path d={`M${x},${y} L${x + w},${cy} L${x},${y + h} Z`} fill="#fcd116" stroke="#fff" strokeWidth={m * 0.03} /><path d={`M${x},${y} L${x + w * 0.5},${cy} L${x},${y + h} Z`} fill="#ce1126" stroke="#111" strokeWidth={m * 0.02} /></g>;
    case 'SUR': return <g>{Hs(['#377e3f', '#377e3f', '#fff', '#b40a2d', '#b40a2d', '#b40a2d', '#b40a2d', '#fff', '#377e3f', '#377e3f'])}{star(cx, cy, m * 0.13, '#ecc81d')}</g>;
    case 'PRT': return <g><rect x={x} y={y} width={w * 0.4} height={h} fill="#046a38" /><rect x={x + w * 0.4} y={y} width={w * 0.6 + 0.6} height={h} fill="#da291c" /><circle cx={x + w * 0.4} cy={cy} r={m * 0.2} fill="#ffe900" /><rect x={x + w * 0.4 - m * 0.09} y={cy - m * 0.1} width={m * 0.18} height={m * 0.2} rx={m * 0.05} fill="#fff" stroke="#da291c" strokeWidth={m * 0.03} /></g>;
    case 'ESP': return <g>{Hs(['#c60b1e', '#ffc400', '#ffc400', '#c60b1e'])}</g>;
    case 'USA': return <g>{Hs(['#b22234', '#fff', '#b22234', '#fff', '#b22234', '#fff', '#b22234', '#fff', '#b22234', '#fff', '#b22234', '#fff', '#b22234'])}<rect x={x} y={y} width={w * 0.4} height={(h * 7) / 13} fill="#3c3b6e" /></g>;
    case 'MEX': return <g>{Vs(['#006847', '#fff', '#ce1126'])}<circle cx={cx} cy={cy} r={m * 0.09} fill="#8a5a2b" /></g>;
    case 'FRA': case 'GUF': return <g>{Vs(['#0055a4', '#fff', '#ef4135'])}</g>;
    case 'ITA': return <g>{Vs(['#009246', '#fff', '#ce2b37'])}</g>;
    case 'DEU': return <g>{Hs(['#000', '#dd0000', '#ffce00'])}</g>;
    case 'NLD': return <g>{Hs(['#ae1c28', '#fff', '#21468b'])}</g>;
    case 'RUS': return <g>{Hs(['#fff', '#0039a6', '#d52b1e'])}</g>;
    case 'JPN': return <g>{R('#fff')}<circle cx={cx} cy={cy} r={m * 0.3} fill="#bc002d" /></g>;
    case 'CHN': return <g>{R('#de2910')}{star(x + w * 0.17, y + h * 0.25, m * 0.15, '#ffde00')}</g>;
    case 'GBR': return <g>{R('#012169')}<path d={`M${x},${y} L${x + w},${y + h} M${x + w},${y} L${x},${y + h}`} stroke="#fff" strokeWidth={m * 0.12} /><path d={`M${x},${y} L${x + w},${y + h} M${x + w},${y} L${x},${y + h}`} stroke="#c8102e" strokeWidth={m * 0.04} /><path d={`M${cx},${y} V${y + h} M${x},${cy} H${x + w}`} stroke="#fff" strokeWidth={m * 0.2} /><path d={`M${cx},${y} V${y + h} M${x},${cy} H${x + w}`} stroke="#c8102e" strokeWidth={m * 0.12} /></g>;
    case 'CAN': return <g>{Vs(['#d80621', '#fff', '#fff', '#d80621'])}{star(cx, cy, m * 0.14, '#d80621')}</g>;
    case 'AGO': return <g>{Hs(['#cc092f', '#000'])}{star(cx, cy, m * 0.1, '#ffcb00')}</g>;
    case 'CPV': return <g>{R('#003893')}<rect x={x} y={y + h * 0.5} width={w} height={h * 0.08} fill="#fff" /><rect x={x} y={y + h * 0.58} width={w} height={h * 0.08} fill="#cf2027" /><rect x={x} y={y + h * 0.66} width={w} height={h * 0.08} fill="#fff" /></g>;
    case 'SUL': return <g>{R('#0a3d91')}<rect x={x} y={y + h * 0.78} width={w} height={h * 0.22} fill="#1fa84a" /><rect x={x} y={y + h * 0.74} width={w} height={h * 0.05} fill="#ffd400" />{[[0.5, 0.18, 0.07], [0.5, 0.56, 0.08], [0.36, 0.36, 0.065], [0.62, 0.32, 0.06], [0.56, 0.44, 0.035]].map(([u, v, k], i) => <g key={i}>{star(x + w * u, y + h * v, m * k)}</g>)}</g>;
    case 'MOZ': return <g>{Hs(['#009739', '#000', '#fce100'])}<path d={`M${x},${y} L${x + w * 0.45},${cy} L${x},${y + h} Z`} fill="#d21034" /></g>;
    default: return R(COL[iso] || '#888');
  }
};
const FlagFill = ({iso, r}) => <FlagArt iso={iso} x={-r} y={-r} w={2 * r} h={2 * r} />;

// bolinha com rosto: skin 'flag' (countryball), 'emoji' (amarela 3D) ou 'red' (vermelha furiosa)
const Ball = ({iso, x, y, r, face = 'neutral', t = 1, skin = 'emoji', uid = 0}) => {
  const s = ease(Math.min(1, t * 2.2)) * (1 + 0.1 * Math.sin(t * 10) * Math.max(0, 1 - t)) * (1 + 0.025 * Math.sin(t * 3.1));
  const eye = (cx) => {
    const L = cx < 0;
    if (face === 'angry' || face === 'rage') return <g><ellipse cx={cx} cy={-r * 0.06} rx={r * 0.17} ry={r * 0.15} fill="#fff" stroke="#111" strokeWidth={r * 0.03} /><circle cx={cx + (L ? r * 0.04 : -r * 0.04)} cy={-r * 0.03} r={r * 0.075} fill="#111" /><path d={`M${cx - r * 0.25},${-r * (L ? 0.36 : 0.17)} L${cx + r * 0.25},${-r * (L ? 0.17 : 0.36)}`} stroke="#111" strokeWidth={r * 0.11} strokeLinecap="round" /></g>;
    if (face === 'shock') return <g><ellipse cx={cx} cy={-r * 0.14} rx={r * 0.2} ry={r * 0.25} fill="#fff" stroke="#111" strokeWidth={r * 0.035} /><circle cx={cx} cy={-r * 0.12} r={r * 0.075} fill="#111" /><path d={`M${cx - r * 0.18},${-r * 0.5} Q${cx},${-r * 0.6} ${cx + r * 0.18},${-r * 0.5}`} stroke="#111" strokeWidth={r * 0.06} fill="none" strokeLinecap="round" /></g>;
    if (face === 'happy') return <path d={`M${cx - r * 0.17},${-r * 0.06} Q${cx},${-r * 0.3} ${cx + r * 0.17},${-r * 0.06}`} stroke="#111" strokeWidth={r * 0.09} fill="none" strokeLinecap="round" />;
    if (face === 'smirk') return <g><path d={`M${cx - r * 0.19},${-r * 0.1} L${cx + r * 0.19},${-r * 0.1}`} stroke="#111" strokeWidth={r * 0.06} strokeLinecap="round" /><path d={`M${cx - r * 0.18},${-r * 0.1} A${r * 0.18},${r * 0.14} 0 0 0 ${cx + r * 0.18},${-r * 0.1}`} fill="#fff" stroke="#111" strokeWidth={r * 0.035} /><circle cx={cx + r * 0.06} cy={-r * 0.04} r={r * 0.06} fill="#111" /><path d={`M${cx - r * 0.2},${-r * (L ? 0.3 : 0.24)} L${cx + r * 0.2},${-r * (L ? 0.24 : 0.32)}`} stroke="#111" strokeWidth={r * 0.07} strokeLinecap="round" /></g>;
    if (face === 'sad') return <g><ellipse cx={cx} cy={-r * 0.1} rx={r * 0.16} ry={r * 0.18} fill="#fff" stroke="#111" strokeWidth={r * 0.03} /><circle cx={cx} cy={-r * 0.03} r={r * 0.075} fill="#111" /><path d={`M${cx - r * 0.2},${-r * (L ? 0.28 : 0.4)} L${cx + r * 0.2},${-r * (L ? 0.4 : 0.28)}`} stroke="#111" strokeWidth={r * 0.07} strokeLinecap="round" /></g>;
    if (face === 'cool') return <rect x={cx - r * 0.27} y={-r * 0.25} width={r * 0.52} height={r * 0.23} rx={r * 0.07} fill="#111" />;
    if (face === 'love') return <path d={`M${cx},${r * 0.02} C${cx - r * 0.3},${-r * 0.16} ${cx - r * 0.12},${-r * 0.36} ${cx},${-r * 0.2} C${cx + r * 0.12},${-r * 0.36} ${cx + r * 0.3},${-r * 0.16} ${cx},${r * 0.02}Z`} fill="#ff2d55" />;
    return <g><ellipse cx={cx} cy={-r * 0.1} rx={r * 0.16} ry={r * 0.2} fill="#fff" stroke="#111" strokeWidth={r * 0.03} /><circle cx={cx + r * 0.03} cy={-r * 0.07} r={r * 0.075} fill="#111" /></g>;
  };
  let mouth;
  if (face === 'rage') mouth = <g><rect x={-r * 0.36} y={r * 0.2} width={r * 0.72} height={r * 0.3} rx={r * 0.1} fill="#fff" stroke="#111" strokeWidth={r * 0.06} />{[-0.18, 0, 0.18].map((k, i) => <line key={i} x1={k * r} y1={r * 0.2} x2={k * r} y2={r * 0.5} stroke="#111" strokeWidth={r * 0.035} />)}<line x1={-r * 0.36} y1={r * 0.35} x2={r * 0.36} y2={r * 0.35} stroke="#111" strokeWidth={r * 0.035} /></g>;
  else if (face === 'shock') mouth = <ellipse cx={0} cy={r * 0.42} rx={r * 0.14} ry={r * 0.19} fill="#5a1010" stroke="#111" strokeWidth={r * 0.04} />;
  else if (face === 'angry') mouth = <path d={`M${-r * 0.25},${r * 0.45} Q0,${r * 0.24} ${r * 0.25},${r * 0.45}`} stroke="#111" strokeWidth={r * 0.09} fill="none" strokeLinecap="round" />;
  else if (face === 'sad') mouth = <path d={`M${-r * 0.22},${r * 0.47} Q0,${r * 0.3} ${r * 0.22},${r * 0.47}`} stroke="#111" strokeWidth={r * 0.08} fill="none" strokeLinecap="round" />;
  else if (face === 'smirk') mouth = <path d={`M${-r * 0.22},${r * 0.36} Q${r * 0.08},${r * 0.44} ${r * 0.3},${r * 0.24}`} stroke="#111" strokeWidth={r * 0.08} fill="none" strokeLinecap="round" />;
  else if (face === 'happy' || face === 'love' || face === 'cool') mouth = <path d={`M${-r * 0.32},${r * 0.2} Q0,${r * 0.66} ${r * 0.32},${r * 0.2} Z`} fill="#5a1010" stroke="#111" strokeWidth={r * 0.06} strokeLinejoin="round" />;
  else mouth = <path d={`M${-r * 0.26},${r * 0.3} Q0,${r * 0.52} ${r * 0.26},${r * 0.3}`} stroke="#111" strokeWidth={r * 0.08} fill="none" strokeLinecap="round" />;
  const id = `cl${uid}`;
  const body = skin === 'flag'
    ? <g><clipPath id={id}><circle r={r} /></clipPath><g clipPath={`url(#${id})`}><FlagFill iso={iso} r={r} /></g></g>
    : <circle r={r} fill={skin === 'red' ? 'url(#gRed)' : 'url(#gEmoji)'} />;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <ellipse rx={r * 0.95} ry={r * 0.28} cy={r * 1.02} fill="#000" opacity={0.35} />
      {body}
      <circle r={r} fill="url(#gShade)" />
      <circle r={r} fill="none" stroke="#111" strokeWidth={r * 0.06} />
      <ellipse cx={-r * 0.38} cy={-r * 0.55} rx={r * 0.28} ry={r * 0.15} transform={`rotate(-30 ${-r * 0.38} ${-r * 0.55})`} fill="#fff" opacity={0.55} />
      {eye(-r * 0.32)}{eye(r * 0.32)}
      {mouth}
    </g>
  );
};

const Arrow = ({a, b, t, color = '#b6ff3b', w = 16}) => {
  if (!a || !b) return null;
  const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - Math.hypot(b[0] - a[0], b[1] - a[1]) * 0.25;
  const p = ease(Math.min(1, t * 1.6));
  const q = (u) => [(1 - u) * (1 - u) * a[0] + 2 * (1 - u) * u * mx + u * u * b[0], (1 - u) * (1 - u) * a[1] + 2 * (1 - u) * u * my + u * u * b[1]];
  const pts = Array.from({length: 24}, (_, i) => q((i / 23) * p));
  const d = 'M' + pts.map((z) => z.join(',')).join(' L');
  const e = pts[pts.length - 1], e0 = pts[pts.length - 3] || a;
  const ang = Math.atan2(e[1] - e0[1], e[0] - e0[0]);
  const hl = w * 2.6;
  return (
    <g>
      <path d={d} stroke={color} strokeOpacity={0.45} strokeWidth={w + 14} fill="none" strokeLinecap="round" filter="url(#glow)" />
      <path d={d} stroke="#000" strokeOpacity={0.5} strokeWidth={w + 8} fill="none" strokeLinecap="round" />
      <path d={d} stroke={color} strokeWidth={w} fill="none" strokeLinecap="round" />
      {p > 0.15 ? <path d={`M${e[0] + Math.cos(ang) * hl * 0.6},${e[1] + Math.sin(ang) * hl * 0.6} L${e[0] + Math.cos(ang + 2.4) * hl},${e[1] + Math.sin(ang + 2.4) * hl} L${e[0] + Math.cos(ang - 2.4) * hl},${e[1] + Math.sin(ang - 2.4) * hl} Z`} fill={color} stroke="#000" strokeWidth={4} /> : null}
    </g>
  );
};

// estado no tempo T (cada beat pode mudar câmera, donos, bolinhas, setas, cartões, destaques)
const stateAt = (beats, T) => {
  let cam = beats[0]?.cam || {c: [-58, -18], s: 1.0}, prevCam = cam, camT = 0;
  const own = {}, ownPrev = {}, ownAt = {};
  let balls = [], arrows = [], cards = [], hl = [];
  for (const b of beats) {
    if (b.t0 > T) break;
    if (b.cam) { prevCam = cam; cam = b.cam; camT = b.t0; }
    for (const [k, v] of Object.entries(b.own || {})) { ownPrev[k] = own[k] || null; own[k] = v; ownAt[k] = b.t0 + (b.od || 0); }
    if (b.balls) balls = b.balls.map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.addballs) balls = balls.concat(b.addballs.map((x) => ({...x, at: b.t0 + (x.d || 0)})));
    if (b.arrows !== undefined) arrows = (b.arrows || []).map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.cards !== undefined) cards = (b.cards || []).map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    hl = b.hl || [];
  }
  const k = ease((T - camT) / 1.2);
  const c = geoInterpolate(prevCam.c, cam.c)(k);
  const s = prevCam.s + (cam.s - prevCam.s) * k;
  return {c, s, own, ownPrev, ownAt, balls, arrows, cards, hl};
};

const mergedCache = new Map();
const mergedOf = (isos) => {
  const key = isos.slice().sort().join(',');
  if (!mergedCache.has(key)) {
    const set = new Set(isos.map((i) => NUM[i]));
    mergedCache.set(key, merge(world, GEOMS.filter((g) => set.has(String(g.id).padStart(3, '0')))));
  }
  return mergedCache.get(key);
};

// território de cada dono: bandeira do dono esticada na área conquistada + contorno brilhante
const Territories = ({st, T, path, W, H, uid = 'v'}) => {
  const groups = {};
  for (const [iso, o] of Object.entries(st.own)) if (o) (groups[o] = groups[o] || []).push(iso);
  const order = Object.entries(groups).flatMap(([o, L]) => L.map((iso) => [o, iso])).sort((a, b) => (a[1].startsWith('BR-') ? 1 : 0) - (b[1].startsWith('BR-') ? 1 : 0));
  const bboxOf = (L) => {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const iso of L) {
      const f = featOf(iso); if (!f) continue;
      const [[a, b], [c, d]] = path.bounds(f);
      x0 = Math.min(x0, Math.max(a, -W * 0.2)); y0 = Math.min(y0, Math.max(b, -H * 0.2)); x1 = Math.max(x1, Math.min(c, W * 1.2)); y1 = Math.max(y1, Math.min(d, H * 1.2));
    }
    return isFinite(x0) ? [x0, y0, x1 - x0, y1 - y0] : null;
  };
  const out = [], glow = [], BB = {};
  for (const [o, L] of Object.entries(groups)) {
    const latest = Math.max(...L.map((i) => st.ownAt[i]));
    const old = L.filter((i) => st.ownAt[i] < latest - 0.01);
    const bn = bboxOf(L), bo = old.length ? bboxOf(old) : bn;
    if (!bn) continue;
    const k = ease((T - latest) / 0.9);
    BB[o] = bn.map((v, i) => bo[i] + (v - bo[i]) * k);
  }
  for (const [o, iso] of order) {
    const f = featOf(iso); let bb = BB[o]; if (!f || !bb) continue;
    if (iso.startsWith('BR-')) { const [[a, b2], [c, d]] = path.bounds(f); bb = [a, b2, c - a, d - b2]; }  // estado: bandeira inteira dentro dele
    const op = ease((T - st.ownAt[iso]) / 0.9);
    const id = `tp${uid}${iso}`;
    out.push(<g key={'t' + iso}><clipPath id={id}><path d={path(f)} /></clipPath>
      <g clipPath={`url(#${id})`} opacity={op}><FlagArt iso={o} x={bb[0]} y={bb[1]} w={bb[2]} h={bb[3]} /><rect x={bb[0]} y={bb[1]} width={bb[2]} height={bb[3]} fill="url(#gTerr)" /></g>
      <path d={path(f)} fill="none" stroke="#000" strokeOpacity={0.35 * op} strokeWidth={1.4} /></g>);
  }
  for (const [o, L] of Object.entries(groups)) {
    const settled = L.filter((i) => T - st.ownAt[i] > 0.45);
    const cs = settled.filter((i) => !i.startsWith('BR-')), ss = settled.filter((i) => i.startsWith('BR-'));
    const gc = GLOW[o] || '#ffe14d';
    const ds = (cs.length ? [path(mergedOf(cs))] : []).concat(ss.map((i) => path(featOf(i))));
    ds.forEach((g, j) => glow.push(<g key={'g' + o + j}><path d={g} fill="none" stroke={gc} strokeWidth={18} strokeOpacity={0.75} filter="url(#glow)" /><path d={g} fill="none" stroke={gc} strokeWidth={5} /><path d={g} fill="none" stroke="#fff" strokeWidth={1.6} strokeOpacity={0.9} /></g>));
  }
  return <g>{out}{glow}</g>;
};

const Defs = () => (
  <defs>
    <radialGradient id="gEmoji" cx="38%" cy="32%" r="75%"><stop offset="0" stopColor="#fff3a0" /><stop offset="0.35" stopColor="#ffd21f" /><stop offset="0.85" stopColor="#f29a00" /><stop offset="1" stopColor="#c86e00" /></radialGradient>
    <radialGradient id="gRed" cx="38%" cy="32%" r="75%"><stop offset="0" stopColor="#ff9a8a" /><stop offset="0.35" stopColor="#ff3b2f" /><stop offset="0.85" stopColor="#c4100a" /><stop offset="1" stopColor="#7d0805" /></radialGradient>
    <radialGradient id="gShade" cx="40%" cy="35%" r="70%"><stop offset="0.6" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity="0.28" /></radialGradient>
    <linearGradient id="gTerr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity="0.16" /><stop offset="0.5" stopColor="#fff" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity="0.22" /></linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" /></filter>
  </defs>
);

const Badge = ({text, vert, op = 1}) => (
  <div style={{position: 'absolute', top: vert ? 200 : 34, left: 0, right: 0, textAlign: 'center', opacity: op}}>
    <span style={{display: 'inline-flex', alignItems: 'center', gap: 12, background: 'linear-gradient(180deg,#ffe55c,#ffc400)', color: '#111', fontFamily: SANS, fontWeight: 800, fontSize: vert ? 34 : 26, padding: '8px 22px 8px 14px', borderRadius: 12, letterSpacing: 1, boxShadow: '0 6px 0 #000a'}}>
      <svg width={vert ? 36 : 28} height={vert ? 36 : 28} viewBox="-12 -14 24 28"><circle r={9} cy={-3} fill="#fff8c8" stroke="#111" strokeWidth={2} /><rect x={-4.5} y={6} width={9} height={6} rx={1.5} fill="#555" /><path d="M-3,-2 L0,3 L3,-2" stroke="#e08a00" strokeWidth={1.6} fill="none" /></svg>
      {text}
    </span>
  </div>
);

export const Ese = ({es}) => {
  useFonts();
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const T = f / fps;
  const vert = H > W;
  const st = stateAt(es.beats || [], T);
  const base = (vert ? W * 0.95 : H * 1.0);
  const proj = useMemo(() => geoMercator(), []);
  proj.center(st.c).scale(base * st.s).translate([W / 2, H * (vert ? 0.47 : 0.52)]);
  const path = geoPath(proj);
  const pt = (v) => { if (!v) return null; if (Array.isArray(v)) return proj(v); const c = featOf(v); if (!c) return null; const fix = {USA: [-98, 39], FRA: [2.5, 46.5], CHL: [-71, -33], RUS: [95, 61], CAN: [-100, 57], PRT: [-8, 39.6], NOR: [9, 61], BRA: [-51, -10], ECU: [-78.4, -1.5]}[v]; return proj(fix || geoCentroid(c)); };
  const words = es.words || [];
  const wi = words.findIndex((w) => T >= w.t0 - 0.05 && T < w.t1 + 0.25);
  let cap = null;
  if (wi >= 0) {
    const blk = Math.floor(wi / 3) * 3;
    cap = words.slice(blk, blk + 3).map((w, i) => ({...w, on: blk + i === wi}));
  }
  const hookOp = es.hook ? Math.max(0, Math.min(1, (es.hook_end || 3) - T)) : 0;
  const lines = (es.hook || '').split('|');
  const grat = useMemo(() => geoGraticule10(), []);
  return (
    <AbsoluteFill style={{background: 'radial-gradient(1200px 1500px at 50% 42%, #0f3d5c 0%, #0a2340 50%, #040b18 100%)', overflow: 'hidden'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <Defs />
        <path d={path(grat)} fill="none" stroke="#7fd3ff" strokeOpacity={0.07} strokeWidth={1.2} />
        <g transform="translate(10,18)" opacity={0.6}>{COUNTRIES.map((c, i) => <path key={'s' + i} d={path(c)} fill="#01040b" />)}</g>
        {COUNTRIES.map((c, i) => {
          const iso = ISO_OF[String(c.id).padStart(3, '0')];
          const prev = iso && st.ownPrev[iso];
          const fill = prev && COL[prev] ? mix(LAND, COL[prev], 0.85) : (iso && COL[iso] ? mix(LAND, COL[iso], 0.09) : LAND);
          return <path key={i} d={path(c)} fill={fill} stroke="#6f86a8" strokeOpacity={0.55} strokeWidth={1.3} />;
        })}
        {es.uf ? STATES.map((f) => <path key={f.id} d={path(f)} fill="none" stroke="#c9d6ea" strokeOpacity={0.35} strokeWidth={1.2} />) : null}
        <Territories st={st} T={T} path={path} W={W} H={H} />
        {es.uf ? STATES.map((f) => <path key={'o' + f.id} d={path(f)} fill="none" stroke="#000" strokeOpacity={0.25} strokeWidth={1} />) : null}
        {st.hl.map((iso) => { const c = featOf(iso); return c ? <g key={'h' + iso}><path d={path(c)} fill="#fff" fillOpacity={0.14 + 0.12 * Math.sin(T * 6)} stroke="#000" strokeWidth={14} strokeOpacity={0.6} /><path d={path(c)} fill="none" stroke="#fff" strokeWidth={7} strokeDasharray="22 12" /></g> : null; })}
        {st.arrows.map((a, i) => <Arrow key={i} a={pt(a.from)} b={pt(a.to)} t={T - a.at} color={a.color || '#b6ff3b'} w={vert ? 16 : 12} />)}
        {st.balls.map((b, i) => {
          let xy = pt(b.ll || b.iso);
          if (xy && b.to) { const z = pt(b.to); const k = ease((T - b.at - (b.wait || 0.4)) / (b.dur || 1.2)); if (z) xy = [xy[0] + (z[0] - xy[0]) * k, xy[1] + (z[1] - xy[1]) * k]; }
          return xy && T >= b.at ? <Ball key={i} uid={i} iso={b.iso} x={xy[0] + (b.dx || 0)} y={xy[1] + (b.dy || 0)} r={(b.r || 1) * (vert ? 88 : 64)} face={b.face} skin={b.skin || es.skin || 'emoji'} t={T - b.at} /> : null;
        })}
      </svg>
      {es.badge ? <Badge text={es.badge} vert={vert} op={1 - hookOp * 0} /> : null}
      {st.cards.filter((c) => T >= c.at).map((c, i) => {
        const k = ease((T - c.at) / 0.35);
        return (
          <div key={i} style={{position: 'absolute', left: 60, right: vert ? 60 : 'auto', top: (vert ? 300 : 120) + i * (vert ? 122 : 96), transform: `translateX(${(1 - k) * -60}px) scale(${0.9 + 0.1 * k})`, opacity: k,
            background: 'rgba(4,10,22,0.88)', border: `4px solid ${GLOW[c.iso] || COL[c.iso] || '#ffd400'}`, borderRadius: 18, padding: vert ? '14px 26px' : '10px 22px', display: 'flex', alignItems: 'center', gap: 18, boxShadow: '0 10px 30px #000a'}}>
            {c.iso ? <svg width={vert ? 70 : 56} height={vert ? 70 : 56} viewBox="-1.1 -1.1 2.2 2.2"><clipPath id={`cc${i}`}><circle r={1} /></clipPath><g clipPath={`url(#cc${i})`}><FlagFill iso={c.iso} r={1} /></g><circle r={1} fill="none" stroke="#111" strokeWidth={0.08} /></svg> : null}
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: vert ? 44 : 36, color: '#fff', lineHeight: 1.1}}>{c.text}{c.big ? <span style={{color: '#ffd400'}}> {c.big}</span> : null}</div>
          </div>
        );
      })}
      {hookOp > 0 ? (
        <div style={{position: 'absolute', top: vert ? 290 : 60, left: 30, right: 30, textAlign: 'center', opacity: hookOp, transform: `scale(${1 + 0.04 * Math.max(0, 1 - T * 2)})`, fontFamily: ANTON, lineHeight: 1.0, WebkitTextStroke: '7px #000', paintOrder: 'stroke', textShadow: '0 10px 0 #000, 0 0 40px #0008'}}>
          {lines.map((ln, i) => <div key={i} style={{fontSize: (i === 0 && lines.length > 2 ? 0.62 : 1) * (vert ? 138 : 112), color: i === lines.length - 1 && lines.length > 1 ? '#d4ff3a' : '#fff'}}>{ln}</div>)}
        </div>
      ) : null}
      {cap && hookOp < 0.5 ? (
        <div style={{position: 'absolute', left: 40, right: 40, top: vert ? H * 0.75 : H * 0.8, textAlign: 'center', fontFamily: ANTON, fontSize: vert ? 96 : 72, lineHeight: 1.08, WebkitTextStroke: '6px #000', paintOrder: 'stroke', textShadow: '0 8px 0 #000'}}>
          {cap.map((w, i) => <span key={i} style={{color: w.on ? '#d4ff3a' : '#fff', margin: '0 12px', display: 'inline-block', transform: w.on ? 'scale(1.1)' : 'none'}}>{w.w.toUpperCase()}</span>)}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// miniatura: mapa com o território na bandeira do dono + emoji + título enorme no estilo do nicho
export const EseThumb = ({es}) => {
  useFonts();
  const th = es.thumb || {};
  const W = th.w || es.w || 1080, H = th.h || es.h || 1920;
  const vert = H > W;
  const proj = geoMercator().center(th.c || [-58, -18]).scale((vert ? W * 0.95 : H * 1.0) * (th.s || 1)).translate([W * (th.x || 0.5), H * (th.y || (vert ? 0.62 : 0.55))]);
  const path = geoPath(proj);
  const own = th.own || {};
  const st = {own, ownAt: Object.fromEntries(Object.keys(own).map((k) => [k, -10])), ownPrev: {}};
  const pt = (v) => { if (Array.isArray(v)) return proj(v); const c = featOf(v); return c ? proj({BRA: [-51, -10]}[v] || geoCentroid(c)) : null; };
  const lines = (th.title || '').split('|');
  return (
    <AbsoluteFill style={{background: 'radial-gradient(1000px 1400px at 50% 55%, #0f3d5c 0%, #0a2340 55%, #040b18 100%)'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <Defs />
        <g transform="translate(10,16)" opacity={0.6}>{COUNTRIES.map((c, i) => <path key={'s' + i} d={path(c)} fill="#01040b" />)}</g>
        {COUNTRIES.map((c, i) => { const iso = ISO_OF[String(c.id).padStart(3, '0')]; return <path key={i} d={path(c)} fill={iso && COL[iso] ? mix(LAND, COL[iso], 0.09) : LAND} stroke="#6f86a8" strokeOpacity={0.55} strokeWidth={1.3} />; })}
        <Territories st={st} T={10} path={path} W={W} H={H} uid="th" />
        {(th.arrows || []).map((a, i) => <Arrow key={i} a={pt(a.from)} b={pt(a.to)} t={5} color={a.color || '#b6ff3b'} w={18} />)}
        {(th.balls || []).map((b, i) => { const xy = pt(b.ll || b.iso); return xy ? <Ball key={i} uid={100 + i} iso={b.iso} x={xy[0] + (b.dx || 0)} y={xy[1] + (b.dy || 0)} r={b.r || 120} face={b.face} skin={b.skin || 'emoji'} t={1} /> : null; })}
      </svg>
      {th.badge !== false ? <Badge text={th.badge || 'SÓ IMAGINAÇÃO'} vert={vert} /> : null}
      <div style={{position: 'absolute', left: 30, right: 30, top: vert ? 290 : 90, textAlign: 'center', fontFamily: ANTON, lineHeight: 1.0, WebkitTextStroke: '8px #000', paintOrder: 'stroke', textShadow: '0 12px 0 #000'}}>
        {lines.map((ln, i) => <div key={i} style={{fontSize: (i === 0 && lines.length > 2 ? 0.6 : 1) * (th.size || (vert ? 150 : 120)), color: i === lines.length - 1 && lines.length > 1 ? '#d4ff3a' : '#fff'}}>{ln}</div>)}
      </div>
    </AbsoluteFill>
  );
};
