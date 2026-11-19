// "E se...?" — simulações com mapa no formato que cresce no Shorts BR (Hiperfocando: território pintado com a BANDEIRA do dono,
// contorno brilhante, emoji 3D reagindo, setas verdes, selo "SÓ IMAGINAÇÃO", título-gancho enorme, legenda palavra a palavra).
// Vertical 1080x1920 (Shorts) ou 1920x1080.
import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender} from 'remotion';
import {geoMercator, geoPath, geoCentroid, geoInterpolate, geoGraticule10, geoArea} from 'd3-geo';
import {feature, merge} from 'topojson-client';
import world from 'world-atlas/countries-50m.json';
import BRUF from './br_uf.json';
import MERC from '../../public/geo/merc.json';

const COUNTRIES = feature(world, world.objects.countries).features;
const GEOMS = world.objects.countries.geometries;
const NUM = {BRA: '076', ARG: '032', CHL: '152', URY: '858', PRY: '600', BOL: '068', PER: '604', COL: '170', VEN: '862', ECU: '218', GUY: '328', SUR: '740', GUF: '254',
  MEX: '484', USA: '840', CAN: '124', PRT: '620', ESP: '724', FRA: '250', GBR: '826', DEU: '276', ITA: '380', RUS: '643', CHN: '156', IND: '356', AUS: '036', JPN: '392',
  PAN: '591', CRI: '188', NIC: '558', HND: '340', GTM: '320', SLV: '222', CUB: '192', DOM: '214', HTI: '332', BLZ: '084', AGO: '024', MOZ: '508', ZAF: '710', NGA: '566', EGY: '818', MAR: '504',
  NLD: '528', BEL: '056', CHE: '756', AUT: '040', POL: '616', UKR: '804', TUR: '792', SAU: '682', IRN: '364', KOR: '410', PRK: '408', IDN: '360', NZL: '554', GRL: '304', ISL: '352',
  NOR: '578', SWE: '752', FIN: '246', DNK: '208', IRL: '372', GRC: '300', CPV: '132', GNB: '624', STP: '678', TLS: '626',
  FLK: '238', MYS: '458', SGP: '702', THA: '764', BLR: '112', EST: '233', LVA: '428', LTU: '440', CZE: '203', SVK: '703', HUN: '348', ROU: '642', BGR: '100', SRB: '688', HRV: '191', KAZ: '398', MNG: '496', VNM: '704', PHL: '608', TWN: '158', ISR: '376', SYR: '760', IRQ: '368', AFG: '004', PAK: '586', CUB2: '192'};
const BYNUM = Object.fromEntries(COUNTRIES.map((c) => [String(c.id).padStart(3, '0'), c]));
const ISO_OF = Object.fromEntries(Object.entries(NUM).map(([k, v]) => [v, k]));
// estados do Brasil (ids 'BR-AC', 'BR-RS'...) para cenários internos
const STATES = BRUF.features;
const BYKEY = Object.fromEntries(STATES.map((f) => [f.id, f]));
// recortes derivados: Alasca (parte do polígono dos EUA)
{
  const usa = COUNTRIES.find((c) => String(c.id) === '840');
  if (usa) BYKEY['US-AK'] = {type: 'Feature', id: 'US-AK', properties: {}, geometry: {type: 'MultiPolygon', coordinates: usa.geometry.coordinates.filter((p) => p[0].every(([x, y]) => (x < -129 || x > 170) && y > 50))}};
  const fra = COUNTRIES.find((c) => String(c.id) === '250');
  if (fra) BYKEY['FR-GF'] = {type: 'Feature', id: 'FR-GF', properties: {}, geometry: {type: 'MultiPolygon', coordinates: fra.geometry.coordinates.filter((p) => p[0].every(([x, y]) => x < -50 && x > -56 && y > 1 && y < 7))}};
  if (usa) BYKEY['US-48'] = {type: 'Feature', id: 'US-48', properties: {}, geometry: {type: 'MultiPolygon', coordinates: usa.geometry.coordinates.filter((p) => !p[0].every(([x, y]) => (x < -129 || x > 170) && y > 50))}};
}
const featOf = (k) => BYKEY[k] || BYNUM[NUM[k]];
// cor de cada "dono" (cor principal da bandeira) e do brilho do contorno
const COL = {BRA: '#1fa84a', ARG: '#6cb4ee', CHL: '#d52b1e', URY: '#3a6fd8', PRY: '#c8102e', BOL: '#f2c200', PER: '#e8112d', COL: '#fcd116', VEN: '#cf142b', ECU: '#ffdd00',
  GUY: '#009e49', SUR: '#377e3f', GUF: '#0055a4', MEX: '#006847', USA: '#3c3b6e', CAN: '#d80621', PRT: '#046a38', ESP: '#c60b1e', FRA: '#0055a4', GBR: '#012169', RUS: '#d52b1e', CHN: '#de2910',
  DEU: '#222', ITA: '#009246', JPN: '#bc002d', IND: '#ff9933', NLD: '#ae1c28', CPV: '#003893', AGO: '#cc092f', MOZ: '#009739', GNB: '#ce1126', STP: '#12ad2b', TLS: '#dc241f', SUL: '#0a3d91', NDE: '#f07800', NRT: '#0b6b2e', SDE: '#13306b', RSU: '#009739', COE: '#d9a300', NOR: '#ba0c2f', FIN: '#002f6c', SWE: '#006aa7', SOV: '#cc0000', POL: '#dc143c', UKR: '#0057b7', MYS: '#010066', SGP: '#ef3340', THA: '#2d2a4a', FLK: '#012169', KOR: '#0047a0', PRK: '#024fa2', ISR: '#0038b8', DNK: '#c8102e'};
const GLOW = {CHE: '#ff6b5b', BRA: '#c6ff2e', ARG: '#7fd3ff', URY: '#8fb8ff', CHL: '#ff6b5b', BOL: '#ffe14d', PER: '#ff6b6b', PRY: '#ff8a8a', COL: '#ffe14d', VEN: '#ffd34d', ECU: '#ffe14d', PRT: '#7dff9a', FRA: '#8fb8ff', USA: '#8fb8ff', ESP: '#ffcf40', GUY: '#c6ff2e', SUR: '#9dff9d', SUL: '#7fe0ff', NDE: '#ffb347', NRT: '#7dff9a', SDE: '#8fb8ff', RSU: '#ff8a8a', COE: '#ffe14d'};
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
    case 'NDE': return <g>{R('#f07800')}<rect x={x} y={y} width={w} height={h * 0.3} fill="#1f5fbf" /><rect x={x} y={y + h * 0.3} width={w} height={h * 0.05} fill="#fff" /><rect x={x} y={y + h * 0.82} width={w} height={h * 0.18 + 0.6} fill="#159447" /><circle cx={cx} cy={y + h * 0.56} r={m * 0.17} fill="#ffd21a" stroke="#fff" strokeWidth={m * 0.02} />{star(cx, y + h * 0.15, m * 0.07, '#fff')}</g>;
    case 'FIN': return <g>{R('#fff')}<rect x={x + w * 0.28} y={y} width={w * 0.17} height={h} fill="#002f6c" /><rect x={x} y={y + h * 0.39} width={w} height={h * 0.22} fill="#002f6c" /></g>;
    case 'SWE': return <g>{R('#006aa7')}<rect x={x + w * 0.31} y={y} width={w * 0.13} height={h} fill="#fecc02" /><rect x={x} y={y + h * 0.4} width={w} height={h * 0.2} fill="#fecc02" /></g>;
    case 'NOR': return <g>{R('#ba0c2f')}<rect x={x + w * 0.25} y={y} width={w * 0.22} height={h} fill="#fff" /><rect x={x} y={y + h * 0.36} width={w} height={h * 0.28} fill="#fff" /><rect x={x + w * 0.3} y={y} width={w * 0.12} height={h} fill="#00205b" /><rect x={x} y={y + h * 0.43} width={w} height={h * 0.14} fill="#00205b" /></g>;
    case 'CHE': return <g>{R('#d52b1e')}<rect x={cx - m * 0.1} y={cy - m * 0.32} width={m * 0.2} height={m * 0.64} fill="#fff" /><rect x={cx - m * 0.32} y={cy - m * 0.1} width={m * 0.64} height={m * 0.2} fill="#fff" /></g>;
    case 'DNK': return <g>{R('#c8102e')}<rect x={x + w * 0.3} y={y} width={w * 0.12} height={h} fill="#fff" /><rect x={x} y={y + h * 0.43} width={w} height={h * 0.14} fill="#fff" /></g>;
    case 'SOV': return <g>{R('#cc0000')}{star(x + w * 0.16, y + h * 0.18, m * 0.07, '#ffd700')}<path d={`M${x + w * 0.1},${y + h * 0.42} q${w * 0.06},${h * 0.1} ${w * 0.14},${-h * 0.02}`} stroke="#ffd700" strokeWidth={m * 0.035} fill="none" /></g>;
    case 'POL': return <g>{Hs(['#fff', '#dc143c'])}</g>;
    case 'UKR': return <g>{Hs(['#0057b7', '#ffd700'])}</g>;
    case 'MYS': return <g>{Hs(['#cc0001', '#fff', '#cc0001', '#fff', '#cc0001', '#fff', '#cc0001', '#fff', '#cc0001', '#fff', '#cc0001', '#fff', '#cc0001', '#fff'])}<rect x={x} y={y} width={w * 0.5} height={h * 0.57} fill="#010066" />{star(x + w * 0.3, y + h * 0.28, m * 0.09, '#fc0')}</g>;
    case 'SGP': return <g>{Hs(['#ef3340', '#fff'])}<circle cx={x + w * 0.2} cy={y + h * 0.25} r={m * 0.11} fill="#fff" /></g>;
    case 'THA': return <g>{Hs(['#a51931', '#f4f5f8', '#2d2a4a', '#2d2a4a', '#f4f5f8', '#a51931'])}</g>;
    case 'FLK': return <g>{R('#012169')}<circle cx={x + w * 0.72} cy={cy} r={m * 0.2} fill="#fff" stroke="#00a" strokeWidth={m * 0.02} /></g>;
    case 'ISR': return <g>{R('#fff')}<rect x={x} y={y + h * 0.12} width={w} height={h * 0.12} fill="#0038b8" /><rect x={x} y={y + h * 0.76} width={w} height={h * 0.12} fill="#0038b8" /></g>;
    case 'KOR': return <g>{R('#fff')}<circle cx={cx} cy={cy} r={m * 0.22} fill="#cd2e3a" /><path d={`M${cx - m * 0.22},${cy} a${m * 0.11},${m * 0.11} 0 0 0 ${m * 0.22},0 a${m * 0.11},${m * 0.11} 0 0 1 ${m * 0.22},0 a${m * 0.22},${m * 0.22} 0 0 1 ${-m * 0.44},0`} fill="#0047a0" /></g>;
    case 'PRK': return <g>{Hs(['#024fa2', '#fff', '#ed1c27', '#ed1c27', '#ed1c27', '#fff', '#024fa2'])}<circle cx={x + w * 0.35} cy={cy} r={m * 0.16} fill="#fff" />{star(x + w * 0.35, cy, m * 0.13, '#ed1c27')}</g>;
    case 'NRT': return <g>{R('#0b6b2e')}<path d={`M${x},${y + h * 0.55} C${x + w * 0.3},${y + h * 0.4} ${x + w * 0.6},${y + h * 0.75} ${x + w},${y + h * 0.55} L${x + w},${y + h * 0.7} C${x + w * 0.6},${y + h * 0.9} ${x + w * 0.3},${y + h * 0.55} ${x},${y + h * 0.7} Z`} fill="#2f8fd6" />{star(x + w * 0.2, y + h * 0.25, m * 0.09, '#fff')}</g>;
    case 'SDE': return <g>{Hs(['#13306b', '#fff', '#c8102e'])}{star(cx, cy, m * 0.11, '#ffd400')}</g>;
    case 'RSU': return <g>{R('#009739')}<path d={`M${x},${y + h} L${x + w},${y} L${x + w},${y + h * 0.45} L${x + w * 0.45},${y + h} Z`} fill="#d52b1e" /><path d={`M${x + w * 0.45},${y + h} L${x + w},${y + h * 0.45} L${x + w},${y + h} Z`} fill="#ffcd00" /></g>;
    case 'COE': return <g>{R('#d9a300')}<rect x={x} y={y + h * 0.62} width={w} height={h * 0.38} fill="#2e7d32" />{star(cx, y + h * 0.33, m * 0.12, '#fff')}</g>;
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
  let balls = [], arrows = [], cards = [], hl = [], pins = [], split = null, line = null, zones = [], date = null, dateAt = 0, focus = [];
  for (const b of beats) {
    if (b.t0 > T) break;
    if (b.cam) { prevCam = cam; cam = b.cam; camT = b.t0; }
    for (const [k, v] of Object.entries(b.own || {})) { ownPrev[k] = own[k] || null; own[k] = v; ownAt[k] = b === beats[0] && !b.od ? -5 : b.t0 + (b.od || 0); }  // 1º quadro já completo
    if (b.balls) balls = b.balls.map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.addballs) balls = balls.concat(b.addballs.map((x) => ({...x, at: b.t0 + (x.d || 0)})));
    if (b.arrows !== undefined) arrows = (b.arrows || []).map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.cards !== undefined) cards = (b.cards || []).map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.pins !== undefined) pins = (b.pins || []).map((x, i) => ({...x, at: b.t0 + (x.d !== undefined ? x.d : 0.3 + i * 0.5)}));
    if (b.split !== undefined) split = b.split ? {...b.split, at: b.t0 + (b.split.d || 0)} : null;
    if (b.line !== undefined) line = b.line ? {...b.line, at: b.t0 + (b.line.d || 0)} : null;
    if (b.zones !== undefined) zones = (b.zones || []).map((x) => ({...x, at: b.t0 + (x.d || 0)}));
    if (b.date !== undefined) { date = b.date; dateAt = b.t0; }
    if (b.focus !== undefined) focus = b.focus || [];
    hl = b.hl || [];
  }
  const k = ease((T - camT) / 1.2);
  const c = geoInterpolate(prevCam.c, cam.c)(k);
  const s = prevCam.s + (cam.s - prevCam.s) * k;
  return {c, s, own, ownPrev, ownAt, balls, arrows, cards, hl, pins, split, line, zones, date, dateAt, focus};
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
// modo 'color' (história no mapa, estilo One Map): território em cor translúcida sobre o satélite, sem bandeira
const TCOL = {GBR: '#2f6fe0', USA: '#2f6fe0', FRA: '#3a7bff', RUS: '#d62828', SOV: '#d62828', FIN: '#5aa9ff', JPN: '#e0352b', DEU: '#6b6b6b', ARG: '#74c0f0', FLK: '#2f6fe0', CAN: '#2f6fe0', THA: '#e6b800', MYS: '#2f6fe0', SGP: '#2f6fe0', POL: '#e8e8e8', ITA: '#2e9e5b', ESP: '#f2b705', CHN: '#e0352b', KOR: '#2f6fe0', PRK: '#d62828'};
const Territories = ({st, T, path, W, H, uid = 'v', sat = false, color = false}) => {
  const groups = {};
  for (const [iso, o] of Object.entries(st.own)) if (o) (groups[o] = groups[o] || []).push(iso);
  const order = Object.entries(groups).flatMap(([o, L]) => L.map((iso) => [o, iso])).sort((a, b) => (a[1].includes('-') ? 1 : 0) - (b[1].includes('-') ? 1 : 0));
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
    if (iso.includes('-')) bb = bboxOf(groups[o].filter((i) => i.includes('-'))) || bb;  // estados: bandeira inteira só na área dos estados desse dono
    const op = ease((T - st.ownAt[iso]) / 0.9) * ((st.focus || []).length && !st.focus.includes(o) && !st.focus.includes(iso) ? 0.25 : 1);
    const id = `tp${uid}${iso}`;
    if (color) { out.push(<path key={'t' + iso} d={path(f)} fill={TCOL[o] || COL[o] || '#888'} fillOpacity={0.42 * op} stroke={TCOL[o] || COL[o] || '#888'} strokeOpacity={0.9 * op} strokeWidth={2.5} />); continue; }
    out.push(<g key={'t' + iso}><clipPath id={id}><path d={path(f)} /></clipPath>
      <g clipPath={`url(#${id})`} opacity={op * (sat ? 0.86 : 1)}><FlagArt iso={o} x={bb[0]} y={bb[1]} w={bb[2]} h={bb[3]} /><rect x={bb[0]} y={bb[1]} width={bb[2]} height={bb[3]} fill="url(#gTerr)" /></g>
      <path d={path(f)} fill="none" stroke="#000" strokeOpacity={0.35 * op} strokeWidth={1.4} /></g>);
  }
  for (const [o, L] of Object.entries(groups)) {
    if ((st.focus || []).length && !st.focus.includes(o)) continue;
    const settled = L.filter((i) => T - st.ownAt[i] > 0.45);
    const cs = settled.filter((i) => !i.includes('-')), ss = settled.filter((i) => i.includes('-'));
    const gc = GLOW[o] || '#ffe14d';
    const ds = (cs.length ? [path(mergedOf(cs))] : []).concat(ss.map((i) => path(featOf(i))));
    ds.forEach((g, j) => glow.push(color ? <g key={'g' + o + j}><path d={g} fill="none" stroke={TCOL[o] || gc} strokeWidth={4} strokeOpacity={0.95} /></g>
      : <g key={'g' + o + j}><path d={g} fill="none" stroke={gc} strokeWidth={18} strokeOpacity={0.75} filter="url(#glow)" /><path d={g} fill="none" stroke={gc} strokeWidth={5} /><path d={g} fill="none" stroke="#fff" strokeWidth={1.6} strokeOpacity={0.9} /></g>));
  }
  return <g>{out}{glow}</g>;
};

const SplitFill = ({sp, proj, path, W, H, k = 1}) => {
  const f = featOf(sp.iso || 'BRA'); if (!f) return null;
  const xl = proj([sp.lon, sp.lat || -15])[0], [[a, b], [c, d]] = path.bounds(f);
  return <g opacity={k}><clipPath id="spF"><path d={path(f)} /></clipPath><clipPath id="spW"><rect x={-W} y={-H} width={xl + W} height={3 * H} /></clipPath><clipPath id="spE"><rect x={xl} y={-H} width={2 * W} height={3 * H} /></clipPath>
    <g clipPath="url(#spF)"><g clipPath="url(#spW)"><FlagArt iso={sp.west} x={a} y={b} w={Math.max(1, xl - a)} h={d - b} /></g><g clipPath="url(#spE)"><FlagArt iso={sp.east} x={xl} y={b} w={Math.max(1, c - xl)} h={d - b} /></g><rect x={a} y={b} width={c - a} height={d - b} fill="url(#gTerr)" /></g>
    <path d={path(f)} fill="none" stroke="#fff" strokeWidth={3} strokeOpacity={0.8} />
    <path d={`M${xl},${-20} L${xl},${H + 20}`} stroke="#ffd400" strokeWidth={22} strokeOpacity={0.45} filter="url(#glow)" /><path d={`M${xl},${-20} L${xl},${H + 20}`} stroke="#000" strokeWidth={12} strokeOpacity={0.5} /><path d={`M${xl},${-20} L${xl},${H + 20}`} stroke="#ffd400" strokeWidth={7} strokeDasharray="26 14" /></g>;
};

// fundo de satélite (NASA, domínio público) em Mercator: só os blocos que aparecem; versão leve quando o zoom é baixo
const Basemap = ({proj, W, H}) => {
  const tl = proj([-180, MERC.latN]), br = proj([180, MERC.latS]);
  const fw = br[0] - tl[0], fh = br[1] - tl[1];
  const out = [];
  for (const k of [-1, 0, 1]) {
    const ox = tl[0] + k * fw;
    if (ox > W || ox + fw < 0) continue;
    if (fw < MERC.W * 0.3) {
      out.push(<Img key={'lo' + k} src={staticFile('geo/merc_lo.jpg')} style={{position: 'absolute', left: ox, top: tl[1], width: fw + 1, height: fh, maxWidth: 'none'}} />);
      continue;
    }
    for (const [i, j, x0, y0, w, h] of MERC.tiles) {
      const x = ox + (x0 / MERC.W) * fw, y = tl[1] + (y0 / MERC.H) * fh, ww = (w / MERC.W) * fw, hh = (h / MERC.H) * fh;
      if (x > W || x + ww < 0 || y > H || y + hh < 0) continue;
      out.push(<Img key={`t${k}_${i}_${j}`} src={staticFile(`geo/m_${i}_${j}.jpg`)} style={{position: 'absolute', left: x, top: y, width: ww + 1.5, height: hh + 1.5, maxWidth: 'none'}} />);
    }
  }
  return <AbsoluteFill style={{overflow: 'hidden', filter: 'saturate(1.15) brightness(0.92)'}}>{out}</AbsoluteFill>;
};

// zonas livres (frentes de batalha, áreas ocupadas): polígonos lon/lat do spec
const zoneGeo = (z) => {
  const ring = z.coords.concat([z.coords[0]]);
  let g = {type: 'Polygon', coordinates: [ring]};
  if (geoArea(g) > 2 * Math.PI) g = {type: 'Polygon', coordinates: [ring.slice().reverse()]};
  return g;
};
const Zones = ({zones, path, T, vert}) => zones.map((z, i) => {
  const k = ease((T - z.at) / 0.8); if (k <= 0) return null;
  const g = zoneGeo(z), c = z.color || '#d62828', cen = path.centroid(g);
  const bnd = z.iso ? path.bounds(g) : null, zid = 'zc' + i + (z.iso || '');
  return <g key={'z' + i} opacity={k}>{bnd ? <><clipPath id={zid}><path d={path(g)} /></clipPath>
      <g clipPath={`url(#${zid})`} opacity={z.op || 0.92}><FlagArt iso={z.iso} x={bnd[0][0]} y={bnd[0][1]} w={Math.max(1, bnd[1][0] - bnd[0][0])} h={Math.max(1, bnd[1][1] - bnd[0][1])} /><rect x={bnd[0][0]} y={bnd[0][1]} width={bnd[1][0] - bnd[0][0]} height={bnd[1][1] - bnd[0][1]} fill="url(#gTerr)" /></g>
      <path d={path(g)} fill="none" stroke={GLOW[z.iso] || c} strokeWidth={vert ? 7 : 5} strokeLinejoin="round" /></> :
    <path d={path(g)} fill={c} fillOpacity={z.op || 0.42} stroke={c} strokeWidth={vert ? 5 : 4} strokeLinejoin="round" />}
    <path d={path(g)} fill="none" stroke="#fff" strokeOpacity={0.6} strokeWidth={1.5} strokeDasharray={z.dash ? '10 8' : 'none'} />
    {z.label ? <text x={cen[0] + (z.lx || 0)} y={cen[1] + (z.ly || 0)} textAnchor="middle" fontFamily={SANS} fontWeight={800} fontSize={vert ? 34 : 26} fill="#fff" stroke="#000" strokeWidth={6} paintOrder="stroke" letterSpacing={2}>{z.label}</text> : null}</g>;
});

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
  const clean = es.style === 'clean';
  const chunks = useMemo(() => {  // estilo limpo: frases curtas (até 6 palavras, quebra em pontuação)
    const out = []; let cur = [];
    words.forEach((w, i) => { cur.push(i); if (cur.length >= 6 || /[.,;:?!]$/.test(w.w)) { out.push(cur); cur = []; } });
    if (cur.length) out.push(cur);
    const of = {}; out.forEach((c, j) => c.forEach((i) => { of[i] = j; })); return {out, of};
  }, [words]);
  if (wi >= 0) {
    if (clean) { const c = chunks.out[chunks.of[wi]]; cap = c.map((i) => ({...words[i], on: i === wi})); }
    else { const blk = Math.floor(wi / 3) * 3; cap = words.slice(blk, blk + 3).map((w, i) => ({...w, on: blk + i === wi})); }
  }
  const hookOp = es.hook ? Math.max(0, Math.min(1, (es.hook_end || 3) - T)) : 0;
  const lines = (es.hook || '').split('|');
  const grat = useMemo(() => geoGraticule10(), []);
  const sat = es.basemap !== false;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(1200px 1500px at 50% 42%, #0f3d5c 0%, #0a2340 50%, #040b18 100%)', overflow: 'hidden'}}>
      {sat ? <Basemap proj={proj} W={W} H={H} /> : null}
      {sat ? <AbsoluteFill style={{background: 'radial-gradient(1100px 1500px at 50% 45%, rgba(0,8,20,0.05) 0%, rgba(0,8,20,0.25) 60%, rgba(0,6,16,0.6) 100%)'}} /> : null}
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <Defs />
        {sat ? null : <path d={path(grat)} fill="none" stroke="#7fd3ff" strokeOpacity={0.07} strokeWidth={1.2} />}
        {sat ? null : <g transform="translate(10,18)" opacity={0.6}>{COUNTRIES.map((c, i) => <path key={'s' + i} d={path(c)} fill="#01040b" />)}</g>}
        {COUNTRIES.map((c, i) => {
          const iso = ISO_OF[String(c.id).padStart(3, '0')];
          const prev = iso && st.ownPrev[iso];
          const fill = prev && COL[prev] ? mix(LAND, COL[prev], 0.85) : (iso && COL[iso] ? mix(LAND, COL[iso], 0.09) : LAND);
          return <path key={i} d={path(c)} fill={sat ? (prev && COL[prev] ? COL[prev] : '#000') : fill} fillOpacity={sat ? (prev && COL[prev] ? 0.55 : 0.12) : 1} stroke={sat ? '#fff' : '#6f86a8'} strokeOpacity={sat ? 0.45 : 0.55} strokeWidth={1.3} />;
        })}
        {es.uf ? STATES.map((f) => <path key={f.id} d={path(f)} fill="none" stroke="#c9d6ea" strokeOpacity={0.35} strokeWidth={1.2} />) : null}
        <Territories st={st} T={T} path={path} W={W} H={H} sat={sat} color={es.terr === 'color' || (es.terr === undefined && es.style === 'clean')} />
        {es.uf ? STATES.map((f) => <path key={'o' + f.id} d={path(f)} fill="none" stroke="#000" strokeOpacity={0.25} strokeWidth={1} />) : null}
        {st.split ? <SplitFill sp={st.split} proj={proj} path={path} W={W} H={H} k={ease((T - st.split.at) / 0.9)} /> : null}
        <Zones zones={st.zones} path={path} T={T} vert={vert} />
        {st.line ? (() => {
          const ln = st.line, xl = proj([ln.lon, 0])[0], k = ease((T - ln.at) / 1.4), y0 = -20, y1 = y0 + (H + 40) * k;
          return <g><path d={`M${xl},${y0} L${xl},${y1}`} stroke={ln.color || '#ffd400'} strokeWidth={22} strokeOpacity={0.5} filter="url(#glow)" /><path d={`M${xl},${y0} L${xl},${y1}`} stroke="#000" strokeWidth={12} strokeOpacity={0.6} /><path d={`M${xl},${y0} L${xl},${y1}`} stroke={ln.color || '#ffd400'} strokeWidth={7} strokeDasharray="26 14" /></g>;
        })() : null}
        {st.hl.map((iso) => { const c = featOf(iso); return c ? <g key={'h' + iso}><path d={path(c)} fill="#fff" fillOpacity={0.14 + 0.12 * Math.sin(T * 6)} stroke="#000" strokeWidth={14} strokeOpacity={0.6} /><path d={path(c)} fill="none" stroke="#fff" strokeWidth={7} strokeDasharray="22 12" /></g> : null; })}
        {st.arrows.map((a, i) => <Arrow key={i} a={pt(a.from)} b={pt(a.to)} t={T - a.at} color={a.color || '#b6ff3b'} w={vert ? 16 : 12} />)}
        {st.balls.map((b, i) => {
          let xy = pt(b.ll || b.iso);
          if (xy && b.to) { const z = pt(b.to); const k = ease((T - b.at - (b.wait || 0.4)) / (b.dur || 1.2)); if (z) xy = [xy[0] + (z[0] - xy[0]) * k, xy[1] + (z[1] - xy[1]) * k]; }
          return xy && T >= b.at ? <Ball key={i} uid={i} iso={b.iso} x={xy[0] + (b.dx || 0)} y={xy[1] + (b.dy || 0)} r={(b.r || 1) * (vert ? 88 : 64)} face={b.face} skin={b.skin || es.skin || 'emoji'} t={T - b.at} /> : null;
        })}
      </svg>
      {st.pins.filter((p) => T >= p.at).map((p, i) => { const xy = pt(p.ll); if (!xy) return null; const k = ease((T - p.at) / 0.3); return (
        <div key={'p' + i} style={{position: 'absolute', ...(p.left ? {right: W - xy[0] - (vert ? 18 : 15)} : {left: xy[0] - (vert ? 18 : 15)}), top: xy[1], transform: `translateY(-50%) scale(${k})`, transformOrigin: p.left ? 'right center' : 'left center', display: 'flex', alignItems: 'center', gap: 8, flexDirection: p.left ? 'row-reverse' : 'row'}}>
          {p.iso ? <svg width={vert ? 54 : 42} height={vert ? 38 : 30} viewBox="0 0 54 38" style={{border: '3px solid #111', boxShadow: '0 4px 10px #000a'}}><FlagArt iso={p.iso} x={0} y={0} w={54} h={38} /></svg> : <div style={{width: vert ? 26 : 20, height: vert ? 26 : 20, borderRadius: 99, background: p.color || '#fff', border: '5px solid #111', boxShadow: '0 0 18px #fff8'}} />}
          <span style={{fontFamily: SANS, fontWeight: 800, fontSize: vert ? 34 : 26, color: '#fff', background: 'rgba(4,10,22,0.85)', padding: '3px 12px', borderRadius: 8, whiteSpace: 'nowrap'}}>{p.label}</span>
        </div>); })}
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
      {st.date ? <div style={{position: 'absolute', left: vert ? 50 : 40, top: vert ? 150 : 36, opacity: ease((T - st.dateAt) / 0.4), fontFamily: SANS, fontWeight: 800, fontSize: vert ? 34 : 26, letterSpacing: 3, color: '#111', background: '#f4f1e8', padding: '6px 16px', borderRadius: 4, boxShadow: '0 6px 16px #0008'}}>{st.date}</div> : null}
      {cap && clean && hookOp < 0.5 ? (
        <div style={{position: 'absolute', left: 60, right: 60, top: vert ? H * 0.76 : H * 0.82, textAlign: 'center', fontFamily: SANS, fontWeight: 800, fontSize: vert ? 58 : 44, lineHeight: 1.18, color: '#fff', WebkitTextStroke: '8px #000', paintOrder: 'stroke', textShadow: '0 4px 14px #000c'}}>
          {cap.map((w, i) => <span key={i} style={{color: w.on ? '#ffd84d' : '#fff'}}>{w.w}{i < cap.length - 1 ? ' ' : ''}</span>)}
        </div>
      ) : null}
      {cap && !clean && hookOp < 0.5 ? (
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
  const sat = es.basemap !== false;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(1000px 1400px at 50% 55%, #0f3d5c 0%, #0a2340 55%, #040b18 100%)'}}>
      {sat ? <Basemap proj={proj} W={W} H={H} /> : null}
      {sat ? <AbsoluteFill style={{background: 'radial-gradient(1000px 1400px at 50% 55%, rgba(0,8,20,0.0) 0%, rgba(0,8,20,0.3) 65%, rgba(0,6,16,0.65) 100%)'}} /> : null}
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <Defs />
        {sat ? null : <g transform="translate(10,16)" opacity={0.6}>{COUNTRIES.map((c, i) => <path key={'s' + i} d={path(c)} fill="#01040b" />)}</g>}
        {COUNTRIES.map((c, i) => { const iso = ISO_OF[String(c.id).padStart(3, '0')]; return <path key={i} d={path(c)} fill={sat ? '#000' : (iso && COL[iso] ? mix(LAND, COL[iso], 0.09) : LAND)} fillOpacity={sat ? 0.12 : 1} stroke={sat ? '#fff' : '#6f86a8'} strokeOpacity={sat ? 0.45 : 0.55} strokeWidth={1.3} />; })}
        <Territories st={st} T={10} path={path} W={W} H={H} uid="th" sat={sat} color={es.terr === 'color' || (es.terr === undefined && es.style === 'clean')} />
        {th.split ? <SplitFill sp={th.split} proj={proj} path={path} W={W} H={H} /> : null}
        {th.zones ? <Zones zones={th.zones.map((z) => ({...z, at: -10}))} path={path} T={10} vert={vert} /> : null}
        {(th.arrows || []).map((a, i) => <Arrow key={i} a={pt(a.from)} b={pt(a.to)} t={5} color={a.color || '#b6ff3b'} w={18} />)}
        {(th.balls || []).map((b, i) => { const xy = pt(b.ll || b.iso); return xy ? <Ball key={i} uid={100 + i} iso={b.iso} x={xy[0] + (b.dx || 0)} y={xy[1] + (b.dy || 0)} r={b.r || 120} face={b.face} skin={b.skin || 'emoji'} t={1} /> : null; })}
      </svg>
      {th.badge !== false ? (vert ? <Badge text={th.badge || 'SÓ IMAGINAÇÃO'} vert={vert} /> : <div style={{position: 'absolute', left: 14, top: 0, width: 400}}><Badge text={th.badge || 'SÓ IMAGINAÇÃO'} vert={false} /></div>) : null}
      <div style={{position: 'absolute', left: vert ? 30 : 44, right: vert ? 30 : 'auto', width: vert ? 'auto' : W * 0.5, top: vert ? 290 : 110, textAlign: vert ? 'center' : 'left', fontFamily: ANTON, lineHeight: 1.0, WebkitTextStroke: '8px #000', paintOrder: 'stroke', textShadow: '0 12px 0 #000'}}>
        {lines.map((ln, i) => <div key={i} style={{fontSize: (i === 0 && lines.length > 2 ? 0.6 : 1) * (th.size || (vert ? 150 : 120)), color: i === lines.length - 1 && lines.length > 1 ? '#d4ff3a' : '#fff'}}>{ln}</div>)}
      </div>
    </AbsoluteFill>
  );
};
