import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, Img, staticFile, useCurrentFrame, interpolate, spring, Easing, delayRender, continueRender} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {geoOrthographic, geoPath, geoGraticule10, geoInterpolate, geoCentroid} from 'd3-geo';
import {feature} from 'topojson-client';
import world from 'world-atlas/countries-50m.json';
import {Mascot, Shadow, Lights} from '../three/Mascot.jsx';
import {PAL} from '../v3/V3.jsx';

// Engine L1 — vídeo longo 16:9 (1920x1080). Um "shot" por parágrafo falado; cues com tempo real (s) vindos do ltts.py.
const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const IO = Easing.inOut(Easing.cubic);
export const SANS = 'InterL, InterX, Inter, "Helvetica Neue", Arial, sans-serif';
const SERIF = 'LoraI, Georgia, serif';
const MONO = 'JBMono, "DejaVu Sans Mono", monospace';
const ramp = (T, t0, dur = 0.6) => (t0 == null ? 0 : interpolate(T, [t0, t0 + dur], [0, 1], {...C, easing: IO}));
const sp = (T, t0, cfg = {damping: 14, stiffness: 170}) => (t0 == null ? 0 : spring({frame: (T - t0) * FPS, fps: FPS, config: cfg}));
const on = (T, t0) => t0 != null && T >= t0;

const NUM = {POL: '616', DEU: '276', JPN: '392', GBR: '826', IRL: '372', ESP: '724', FRA: '250', ITA: '380', NLD: '528', BEL: '056', LUX: '442', DNK: '208', GRC: '300', PRT: '620', AUT: '040', FIN: '246', SWE: '752', CZE: '203', SVK: '703', HUN: '348', SVN: '705', EST: '233', LVA: '428', LTU: '440', CYP: '196', MLT: '470', BGR: '100', ROU: '642', HRV: '191', KOR: '410', UKR: '804', SAU: '682', IRQ: '368', KWT: '414', ISR: '376', USA: '840', CHN: '156', RUS: '643', BLR: '112', SRB: '688', BIH: '070', MDA: '498', ALB: '008', MKD: '807', MNE: '499', NOR: '578', CHE: '756', ISL: '352', ARE: '784', QAT: '634', OMN: '512', BHR: '048', BRN: '096', YEM: '887', JOR: '400', IRN: '364', VNM: '704', IDN: '360', PHL: '608', THA: '764', MYS: '458', IND: '356', BGD: '050', MMR: '104', KHM: '116', LAO: '418'};
const NAME = {POL: 'Poland', JPN: 'Japan', ESP: 'Spain', DEU: 'Germany', GRC: 'Greece', PRT: 'Portugal', UKR: 'Ukraine', KOR: 'South Korea', GBR: 'Britain', IRL: 'Ireland', CHN: 'China', ITA: 'Italy', USA: 'United States', HUN: 'Hungary', ISR: 'Israel', WLD: 'World', EUU: 'EU average', EU: 'EU average', LUX: 'Luxembourg', FRA: 'France', BEL: 'Belgium', NLD: 'Netherlands', DNK: 'Denmark', CHE: 'Switzerland', NOR: 'Norway', LVA: 'Latvia', LTU: 'Lithuania', EST: 'Estonia', BGR: 'Bulgaria', ROU: 'Romania', HRV: 'Croatia', SRB: 'Serbia', BIH: 'Bosnia', ALB: 'Albania', MDA: 'Moldova', CZE: 'Czechia', TUR: 'Turkey', MEX: 'Mexico', ARG: 'Argentina', SVN: 'Slovenia', SVK: 'Slovakia', MLT: 'Malta', SAU: 'Saudi Arabia', KWT: 'Kuwait', ARE: 'UAE', QAT: 'Qatar', OMN: 'Oman', BHR: 'Bahrain', BRN: 'Brunei', VNM: 'Vietnam', IDN: 'Indonesia', PHL: 'Philippines', THA: 'Thailand', MYS: 'Malaysia', IND: 'India', BGD: 'Bangladesh'};
const COUNTRIES = feature(world, world.objects.countries).features;
const BYNUM = Object.fromEntries(COUNTRIES.map((c) => [c.id, c]));

const colOf = (p, iso) => ({POL: p.acc, JPN: p.warm, UKR: '#4aa8ff', ESP: '#c58bff', DEU: '#8fa3c7', GRC: '#5fd3ff', PRT: p.acc2, KOR: '#ff8ad8', CHN: '#ff9f43', ITA: '#5fd3ff', USA: '#8fa3ff', HUN: p.acc, ISR: p.acc2, WLD: '#ffffff', IRL: '#3ddc84', EUU: '#c9d1e6', EU: '#c9d1e6', LUX: '#5fd3ff', FRA: '#8fa3ff', BEL: '#ffd166', LVA: '#ff8ad8', BGR: '#ffb347', LTU: '#3ddc84', ROU: '#5fd3ff', EST: '#8fa3ff', HRV: '#c58bff', SAU: '#3ddc84', KWT: '#ff5a6e', ARE: '#ffd166', QAT: '#c58bff', OMN: '#ff9f43', BRN: '#ff8ad8', BHR: '#5fd3ff', NOR: '#5fd3ff', CZE: '#ff9f43', SVN: '#c58bff', TUR: '#ff5a6e', MEX: '#3ddc84', ARG: '#c58bff', VNM: '#ffd166', IDN: '#ff5a6e', THA: '#8fa3ff', PHL: '#5fd3ff', MYS: '#c58bff', IND: '#3ddc84'}[iso] || '#ffffff');

export const fmt = (v, k) => {
  if (v == null || Number.isNaN(v)) return '';
  const sg = v > 0 ? '+' : v < 0 ? '−' : '';
  switch (k) {
    case 'usdk': return '$' + (v / 1000).toFixed(1) + 'k';
    case 'usdk0': return '$' + Math.round(v / 1000) + 'k';
    case 'usdB': return v >= 1e12 ? '$' + (v / 1e12).toFixed(2) + 'T' : '$' + Math.round(v / 1e9) + 'B';
    case 'usdB0': return '$' + Math.round(v) + 'B';
    case 'pctx': return Math.round(v * 100) + '%';
    case 'mbd': return v.toFixed(1) + 'M b/d';
    case 'x1': return (v / 100).toFixed(1) + '×';
    case 'nokT': return 'NOK ' + v.toFixed(1) + 'T';
    case 'nokM': return 'NOK ' + v.toFixed(1) + 'M';
    case 'usd0': return '$' + Math.round(v).toLocaleString('en-US');
    case 'pct0': return Math.round(v) + '%';
    case 'pct0s': return sg + Math.abs(Math.round(v)) + '%';
    case 'pct1s': return sg + Math.abs(v).toFixed(1) + '%';
    case 'dec2': return v.toFixed(2);
    case 'mil': return (v / 1e6).toFixed(1) + 'M';
    case 'eurb': return '€' + v.toFixed(1) + 'B';
    case 'm': return Math.round(v) + ' million';
    case 'km': return Math.round(v).toLocaleString('en-US') + ' km';
    case 'k0': return v >= 995000 ? (v / 1e6).toFixed(2).replace(/0$/, '') + 'M' : Math.round(v / 1000) + 'k';
    case 'dec1': return v.toFixed(1);
    case 'int': return Math.round(v).toLocaleString('en-US');
    case 'krwT': return '₩' + v.toFixed(1) + 'T';
    case 'hours': return Math.round(v).toLocaleString('en-US') + ' h';
    case 'usdM': return '$' + Math.round(v) + 'M';
    case 'usdM+': return '>$' + Math.round(v) + 'M';
    case 'dec3': return v.toFixed(3);
    case 'pct1': return v.toFixed(1) + '%';
    case 'pct3': return v.toFixed(3) + '%';
    case 'nsec': return (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(Math.round(v)) + ' ns';
    case 'usec': return (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(Math.round(v)) + ' µs';
    case 'eurk': return '€' + Math.round(v / 1000) + 'k';
    case 'eur0': return '€' + Math.round(v).toLocaleString('en-US');
    default: return String(Math.round(v));
  }
};

const ser = (data, set, iso) => {
  const d = (data[set] || {})[iso] || {};
  return Object.keys(d).map(Number).sort((a, b) => a - b).map((y) => [y, d[y]]);
};
const valAt = (pts, x) => {
  if (!pts.length) return null;
  if (x <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) if (x <= pts[i][0]) {
    const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0);
  }
  return pts[pts.length - 1][1];
};
const pickYear = (pts, year) => {
  if (typeof year === 'string' && year.startsWith('max:')) {
    const [a, b] = year.slice(4).split('-').map(Number);
    return pts.filter(([y]) => y >= a && y <= b).reduce((m, q) => (q[1] > m[1] ? q : m), [0, -Infinity]);
  }
  return pts.find(([y]) => y === Number(year)) || [Number(year), null];
};

// valor animado por chaves: começa em v0 e anda até cada key.year em key.dur s a partir de key.t
const keyed = (T, v0, keys = [], field = 'year') => {
  let v = v0;
  for (const k of [...(keys || [])].filter((k) => k.t != null).sort((a, b) => a.t - b.t)) {
    if (T < k.t) break;
    v = v + (k[field] - v) * ramp(T, k.t, k.dur || 1.2);
  }
  return v;
};

export const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const L = [['InterL', '500', 'fonts/inter500.woff2'], ['InterL', '600', 'fonts/inter600.woff2'], ['InterL', '800', 'fonts/inter800.woff2'], ['InterL', '900', 'fonts/inter900.woff2'], ['LoraI', '400 700', 'fonts/Lora-Italic-Variable.ttf'], ['JBMono', '500', 'fonts/jbmono500.woff2'], ['JBMono', '800', 'fonts/jbmono800.woff2']];
    Promise.all(L.map(([fam, w, u]) => new FontFace(fam, `url(${staticFile(u)})`, {weight: w, style: fam === 'LoraI' ? 'italic' : 'normal'}).load().then((f) => document.fonts.add(f))))
      .then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

// ---------------- fundo ----------------
const Backdrop = ({p, T}) => {
  const blobs = [[300, 260, 760, p.acc2], [1500, 300, 820, p.colA], [1100, 980, 900, p.warm]];
  const jx = Math.floor(T * 24) % 7 * 37, jy = Math.floor(T * 24) % 5 * 53;
  return (
    <AbsoluteFill style={{background: `radial-gradient(1500px 1000px at 42% 45%, ${p.bg1}, ${p.bg2})`}}>
      {blobs.map(([x, y, r, c], i) => (
        <div key={i} style={{position: 'absolute', left: x - r + Math.sin(T / (11 + i * 3) + i) * 90, top: y - r + Math.cos(T / (13 + i * 2) + i) * 70, width: r * 2, height: r * 2, background: `radial-gradient(circle, ${c}24 0%, ${c}00 62%)`}} />
      ))}
      <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px)', backgroundSize: '96px 96px', backgroundPosition: `${(T * 6) % 96}px ${(T * 3) % 96}px`}} />
    </AbsoluteFill>
  );
};
const Grain = ({T}) => {
  const jx = (Math.floor(T * 24) * 73) % 256, jy = (Math.floor(T * 24) * 151) % 256;
  return (
    <>
      <AbsoluteFill style={{backgroundImage: `url(${staticFile('img/noise.png')})`, backgroundPosition: `${jx}px ${jy}px`, opacity: 0.07, mixBlendMode: 'overlay'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)'}} />
    </>
  );
};

// ---------------- peças 2D ----------------
const Kicker = ({text, p, T, t0, x = 120, y = 92}) => {
  if (!text) return null;
  const s = sp(T, t0 ?? -99);
  return (
    <div style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: 16, opacity: s, transform: `translateX(${(1 - s) * -30}px)`}}>
      <div style={{width: 10, height: 44, background: p.acc, borderRadius: 4}} />
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 40, color: '#fff', letterSpacing: -0.5}}>{text}</div>
    </div>
  );
};

const Source = ({text}) => (text ? <div style={{position: 'absolute', left: 122, bottom: 34, fontFamily: SANS, fontWeight: 500, fontSize: 21, color: '#ffffff80', letterSpacing: 0.3}}>Source: {text}</div> : null);

const Pill = ({x, y, text, sub, color, T, t0, align = 'left'}) => {
  const s = sp(T, t0, {damping: 11, stiffness: 190});
  if (s <= 0.001) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(${align === 'left' ? '18px' : align === 'right' ? 'calc(-100% - 18px)' : '-50%'}, -50%) scale(${0.6 + 0.4 * s})`, transformOrigin: align === 'right' ? 'right center' : 'left center', opacity: Math.min(1, s * 1.4)}}>
      <div style={{background: color, color: '#0d1020', fontFamily: SANS, fontWeight: 900, fontSize: 40, padding: '8px 18px', borderRadius: 14, whiteSpace: 'nowrap', boxShadow: '0 10px 30px rgba(0,0,0,.4)'}}>
        {text}{sub ? <span style={{fontWeight: 600, fontSize: 26, marginLeft: 10, opacity: 0.75}}>{sub}</span> : null}
      </div>
    </div>
  );
};

const Burst = ({x, y, T, t0, p, n = 22, r = 190}) => {
  const k = T - (t0 ?? 1e9);
  if (k < 0 || k > 1.4) return null;
  const cols = [p.acc, p.acc2, '#ffffff', p.warm];
  const ring = interpolate(k, [0, 0.9], [0, 1], {...C, easing: Easing.out(Easing.cubic)});
  return (
    <>
      <div style={{position: 'absolute', left: x - r * ring, top: y - r * ring, width: r * 2 * ring, height: r * 2 * ring, borderRadius: '50%', border: `${6 * (1 - ring) + 1}px solid ${p.acc}`, opacity: 1 - ring}} />
      {Array.from({length: n}).map((_, i) => {
        const a = (i / n) * Math.PI * 2 + i;
        const d = (60 + (i % 5) * 30) * Easing.out(Easing.cubic)(Math.min(1, k / 0.8));
        return <div key={i} style={{position: 'absolute', left: x + Math.cos(a) * d * 2.2, top: y + Math.sin(a) * d * 2.2 + k * k * 120, width: 12, height: 12, borderRadius: i % 2 ? 3 : 6, background: cols[i % 4], opacity: 1 - k / 1.4, transform: `rotate(${k * 400 + i * 30}deg)`}} />;
      })}
    </>
  );
};

const Flag = ({iso, w = 150}) => {
  const h = w * 0.66;
  const box = {width: w, height: h, borderRadius: 10, overflow: 'hidden', boxShadow: '0 12px 30px rgba(0,0,0,.45)', position: 'relative'};
  if (iso === 'POL') return <div style={{...box, background: 'linear-gradient(#fff 0 50%, #dc143c 50% 100%)'}} />;
  if (iso === 'JPN') return <div style={{...box, background: '#fff'}}><div style={{position: 'absolute', left: w / 2 - h * 0.3, top: h * 0.2, width: h * 0.6, height: h * 0.6, borderRadius: '50%', background: '#bc002d'}} /></div>;
  if (iso === 'UKR') return <div style={{...box, background: 'linear-gradient(#0057b7 0 50%, #ffd700 50% 100%)'}} />;
  if (iso === 'DEU') return <div style={{...box, background: 'linear-gradient(#000 0 33.3%, #dd0000 33.3% 66.6%, #ffce00 66.6% 100%)'}} />;
  if (iso === 'KOR') return <div style={{...box, background: '#fff'}}><div style={{position: 'absolute', left: w / 2 - h * 0.25, top: h * 0.25, width: h * 0.5, height: h * 0.5, borderRadius: '50%', background: 'linear-gradient(#cd2e3a 0 50%, #0047a0 50% 100%)', transform: 'rotate(-34deg)'}} /></div>;
  if (iso === 'LVA') return <div style={{...box, background: 'linear-gradient(#9e3039 0 40%, #fff 40% 60%, #9e3039 60% 100%)'}} />;
  if (iso === 'BGR') return <div style={{...box, background: 'linear-gradient(#fff 0 33.3%, #00966e 33.3% 66.6%, #d62612 66.6% 100%)'}} />;
  if (iso === 'LTU') return <div style={{...box, background: 'linear-gradient(#fdb913 0 33.3%, #006a44 33.3% 66.6%, #c1272d 66.6% 100%)'}} />;
  if (iso === 'EST') return <div style={{...box, background: 'linear-gradient(#0072ce 0 33.3%, #000 33.3% 66.6%, #fff 66.6% 100%)'}} />;
  if (iso === 'ROU') return <div style={{...box, background: 'linear-gradient(90deg, #002b7f 0 33.3%, #fcd116 33.3% 66.6%, #ce1126 66.6% 100%)'}} />;
  if (iso === 'IRL') return <div style={{...box, background: 'linear-gradient(90deg, #169b62 0 33.3%, #fff 33.3% 66.6%, #ff883e 66.6% 100%)'}} />;
  if (iso === 'TUR') return <div style={{...box, background: '#e30a17'}}><div style={{position: 'absolute', left: w * 0.24, top: h * 0.25, width: h * 0.5, height: h * 0.5, borderRadius: '50%', background: '#fff'}} /><div style={{position: 'absolute', left: w * 0.3, top: h * 0.29, width: h * 0.42, height: h * 0.42, borderRadius: '50%', background: '#e30a17'}} /><div style={{position: 'absolute', left: w * 0.56, top: h * 0.4, width: h * 0.2, height: h * 0.2, background: '#fff', clipPath: 'polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)'}} /></div>;
  if (iso === 'GRC') return <div style={{...box, background: 'repeating-linear-gradient(#0d5eaf 0 11.11%, #fff 11.11% 22.22%)'}}><div style={{position: 'absolute', left: 0, top: 0, width: h * 0.555, height: h * 0.555, background: '#0d5eaf'}} /><div style={{position: 'absolute', left: h * 0.222, top: 0, width: h * 0.111, height: h * 0.555, background: '#fff'}} /><div style={{position: 'absolute', left: 0, top: h * 0.222, width: h * 0.555, height: h * 0.111, background: '#fff'}} /></div>;
  if (iso === 'PRT') return <div style={{...box, background: 'linear-gradient(90deg, #006600 0 40%, #ff0000 40% 100%)'}}><div style={{position: 'absolute', left: w * 0.4 - h * 0.2, top: h * 0.3, width: h * 0.4, height: h * 0.4, borderRadius: '50%', border: `${h * 0.06}px solid #ffcc00`, boxSizing: 'border-box'}} /></div>;
  if (iso === 'SAU') return <div style={{...box, background: '#006c35'}}><div style={{position: 'absolute', left: w * 0.22, top: h * 0.66, width: w * 0.56, height: h * 0.06, background: '#fff', borderRadius: 3}} /><div style={{position: 'absolute', left: w * 0.26, top: h * 0.26, width: w * 0.48, height: h * 0.22, borderTop: `${h * 0.05}px dotted #fff`, borderBottom: `${h * 0.05}px dotted #fff`, opacity: 0.85}} /></div>;
  if (iso === 'KWT') return <div style={{...box, background: 'linear-gradient(#007a3d 0 33.3%, #fff 33.3% 66.6%, #ce1126 66.6% 100%)'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.25, height: h, background: '#000', clipPath: 'polygon(0 0, 100% 33.3%, 100% 66.6%, 0 100%)'}} /></div>;
  if (iso === 'ARE') return <div style={{...box, background: 'linear-gradient(#00732f 0 33.3%, #fff 33.3% 66.6%, #000 66.6% 100%)'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.25, height: h, background: '#ff0000'}} /></div>;
  if (iso === 'QAT') return <div style={{...box, background: '#8d1b3d'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.36, height: h, background: '#fff', clipPath: 'polygon(0 0, 80% 0, 100% 5.5%, 80% 11.1%, 100% 16.6%, 80% 22.2%, 100% 27.7%, 80% 33.3%, 100% 38.8%, 80% 44.4%, 100% 50%, 80% 55.5%, 100% 61.1%, 80% 66.6%, 100% 72.2%, 80% 77.7%, 100% 83.3%, 80% 88.8%, 100% 94.4%, 80% 100%, 0 100%)'}} /></div>;
  if (iso === 'OMN') return <div style={{...box, background: 'linear-gradient(#fff 0 33.3%, #db161b 33.3% 66.6%, #008000 66.6% 100%)'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.25, height: h, background: '#db161b'}} /></div>;
  if (iso === 'BHR') return <div style={{...box, background: '#ce1126'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.36, height: h, background: '#fff', clipPath: 'polygon(0 0, 75% 0, 100% 10%, 75% 20%, 100% 30%, 75% 40%, 100% 50%, 75% 60%, 100% 70%, 75% 80%, 100% 90%, 75% 100%, 0 100%)'}} /></div>;
  if (iso === 'BRN') return <div style={{...box, background: 'linear-gradient(162deg, #f7e017 0 36%, #fff 36% 49%, #000 49% 61%, #f7e017 61% 100%)'}}><div style={{position: 'absolute', left: w * 0.42, top: h * 0.3, width: w * 0.16, height: h * 0.4, borderRadius: '50% 50% 8px 8px', background: '#cf1126'}} /></div>;
  if (iso === 'NOR') return <div style={{...box, background: '#ba0c2f'}}><div style={{position: 'absolute', left: w * 0.27, top: 0, width: w * 0.16, height: h, background: '#fff'}} /><div style={{position: 'absolute', left: 0, top: h * 0.375, width: w, height: h * 0.25, background: '#fff'}} /><div style={{position: 'absolute', left: w * 0.31, top: 0, width: w * 0.08, height: h, background: '#00205b'}} /><div style={{position: 'absolute', left: 0, top: h * 0.4375, width: w, height: h * 0.125, background: '#00205b'}} /></div>;
  if (iso === 'USA') return <div style={{...box, background: 'repeating-linear-gradient(#b22234 0 7.69%, #fff 7.69% 15.38%)'}}><div style={{position: 'absolute', left: 0, top: 0, width: w * 0.4, height: h * 0.538, background: '#3c3b6e'}} /></div>;
  if (iso === 'VNM') return <div style={{...box, background: '#da251d'}}><div style={{position: 'absolute', left: w / 2 - h * 0.3, top: h * 0.2, width: h * 0.6, height: h * 0.6, background: '#ffff00', clipPath: 'polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)'}} /></div>;
  if (iso === 'IDN') return <div style={{...box, background: 'linear-gradient(#ce1126 0 50%, #fff 50% 100%)'}} />;
  return <div style={{...box, background: '#888'}} />;
};

// ---------------- LINHAS ----------------
const PL = {x0: 190, x1: 1300, y0: 230, y1: 880};

const Lines = ({sh, p, data, T, dim}) => {
  const all = sh.series_all || sh.series;
  const [Y0, Y1] = sh.years;
  const S = Object.fromEntries(all.map((iso) => [iso, ser(data, sh.set, iso).filter(([y]) => y >= Y0 && y <= Y1)]));
  const vals = all.flatMap((iso) => S[iso].map((q) => q[1]));
  const [ymin, ymax] = sh.y || [0, Math.max(...vals, 1) * 1.12];
  const X = (y) => PL.x0 + ((y - Y0) / (Y1 - Y0)) * (PL.x1 - PL.x0);
  const Yp = (v) => PL.y1 - ((v - ymin) / (ymax - ymin)) * (PL.y1 - PL.y0);
  const R = keyed(T, sh.start ?? Y0, sh.keys);
  const ticks = niceTicks(ymin, ymax, 5);
  const step = Y1 - Y0 > 30 ? 10 : 5;
  const yrs = [];
  for (let y = Math.ceil(Y0 / step) * step; y <= Y1; y += step) yrs.push(y);
  const fadeOf = (iso) => {
    let a = (sh.fade || []).includes(iso) ? 0.28 : 1;
    if (sh.unfade && sh.unfade.iso === iso) a = 0.28 + 0.72 * ramp(T, sh.unfade.t, 0.6);
    const show = (sh.show || []).find((s) => s.iso === iso);
    if ((sh.hidden || []).includes(iso)) a *= show ? ramp(T, show.t, 0.7) * (show.t_until != null ? 1 - 0.75 * ramp(T, show.t_until, 0.6) : 1) : 0;
    return a;
  };
  const path = (pts, upto) => {
    const out = [];
    for (let i = 0; i < pts.length; i++) {
      const [y, v] = pts[i];
      if (y <= upto) out.push([X(y), Yp(v), y]);
      else {
        if (i > 0 && upto > pts[i - 1][0]) {
          const [ya, va] = pts[i - 1];
          const k = (upto - ya) / (y - ya);
          out.push([X(upto), Yp(va + (v - va) * k), upto]);
        }
        break;
      }
    }
    return out;
  };
  const cross = sh.cross && sh.cross.t != null ? crossPoint(S[sh.series[0]], S[sh.series[1]]) : null;
  const hero = sh.hl || sh.series[0];
  return (
    <AbsoluteFill style={{opacity: dim ? 0.3 : 1}}>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <defs>
          {all.map((iso) => (
            <linearGradient key={iso} id={`g${iso}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={colOf(p, iso)} stopOpacity="0.32" />
              <stop offset="100%" stopColor={colOf(p, iso)} stopOpacity="0" />
            </linearGradient>
          ))}
        </defs>
        {ticks.map((v) => (
          <g key={v}>
            <line x1={PL.x0} x2={PL.x1} y1={Yp(v)} y2={Yp(v)} stroke="#ffffff" strokeOpacity={v === 0 ? 0.3 : 0.09} strokeWidth={2} />
            <text x={PL.x0 - 18} y={Yp(v) + 9} textAnchor="end" fontFamily={SANS} fontWeight={600} fontSize={26} fill="#ffffff70">{fmt(v, sh.fmt === 'usd0' ? 'usdk' : sh.fmt)}</text>
          </g>
        ))}
        {yrs.map((y) => <text key={y} x={X(y)} y={PL.y1 + 46} textAnchor="middle" fontFamily={SANS} fontWeight={600} fontSize={26} fill="#ffffff70">{y}</text>)}
        {(sh.refs || []).map((rf, i) => {
          const a = ramp(T, rf.t, 0.6);
          return a > 0 ? (
            <g key={'rf' + i} opacity={a}>
              <line x1={PL.x0} x2={PL.x0 + (PL.x1 - PL.x0) * a} y1={Yp(rf.value)} y2={Yp(rf.value)} stroke="#ffffff" strokeOpacity={0.7} strokeWidth={3} strokeDasharray="14 12" />
              <text x={PL.x1} y={Yp(rf.value) - 16} textAnchor="end" fontFamily={SANS} fontWeight={800} fontSize={28} fill="#ffffffd0">{rf.label}</text>
            </g>
          ) : null;
        })}
        {sh.ref ? (
          <g>
            <line x1={PL.x0} x2={PL.x1} y1={Yp(sh.ref.value)} y2={Yp(sh.ref.value)} stroke="#ffffff" strokeOpacity={0.55} strokeWidth={3} strokeDasharray="14 12" />
            <text x={sh.ref.pos === 'left' ? PL.x0 + 12 : PL.x1} y={Yp(sh.ref.value) - 16} textAnchor={sh.ref.pos === 'left' ? 'start' : 'end'} fontFamily={SANS} fontWeight={700} fontSize={26} fill="#ffffffb0">{sh.ref.label}</text>
          </g>
        ) : null}
        {sh.fc && R > sh.fc + 0.05 ? (
          <g opacity={Math.min(1, (R - sh.fc) * 2)}>
            <rect x={X(sh.fc)} y={PL.y0} width={PL.x1 - X(sh.fc)} height={PL.y1 - PL.y0} fill="#ffffff" fillOpacity={0.05} />
            <text x={(X(sh.fc) + PL.x1) / 2} y={PL.y0 + 34} textAnchor="middle" fontFamily={SANS} fontWeight={700} fontSize={24} fill="#ffffff90">IMF forecast</text>
          </g>
        ) : null}
        {(sh.bands || []).map((b, i) => {
          const a = ramp(T, b.t, 0.6);
          return a > 0 ? (
            <g key={i} opacity={a}>
              <rect x={X(b.a)} y={PL.y0} width={X(b.b) - X(b.a)} height={PL.y1 - PL.y0} fill={i % 2 ? '#ffffff' : p.warm} fillOpacity={0.08} />
              <text x={(X(b.a) + X(b.b)) / 2} y={PL.y0 + 40} textAnchor="middle" fontFamily={SERIF} fontStyle="italic" fontWeight={600} fontSize={34} fill="#ffffffd0">{b.text}</text>
            </g>
          ) : null;
        })}
        {(sh.marks || []).map((m, i) => {
          const a = ramp(T, m.t, 0.5);
          return a > 0 ? (
            <g key={i} opacity={a}>
              <line x1={X(m.year)} x2={X(m.year)} y1={PL.y0} y2={PL.y1} stroke={p.acc2} strokeWidth={3} strokeDasharray="8 10" />
              <text x={X(m.year) + 14} y={PL.y0 + 34} fontFamily={SANS} fontWeight={800} fontSize={30} fill={p.acc2}>{m.label}</text>
            </g>
          ) : null;
        })}
        {all.map((iso) => {
          const a = fadeOf(iso);
          if (a <= 0.01) return null;
          const pts = path(S[iso], (sh.hidden || []).includes(iso) ? Y1 : R);
          if (pts.length < 1) return null;
          const fc = sh.fc ?? 1e9;
          const solid = pts.filter((q) => q[2] <= fc);
          const fcast = pts.filter((q) => q[2] >= fc);
          const dd = (arr) => arr.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join('');
          const d = dd(solid);
          const df = fcast.length > 1 ? dd(fcast) : '';
          const area = solid.length > 1 ? `${d}L${solid[solid.length - 1][0]},${PL.y1}L${solid[0][0]},${PL.y1}Z` : '';
          const w = iso === hero ? 8 : 6;
          return (
            <g key={iso} opacity={a}>
              {iso === hero && area ? <path d={area} fill={`url(#g${iso})`} /> : null}
              <path d={d} fill="none" stroke={colOf(p, iso)} strokeOpacity={0.22} strokeWidth={w * 3.2} strokeLinecap="round" strokeLinejoin="round" />
              <path d={d} fill="none" stroke={colOf(p, iso)} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" />
              {df ? <path d={df} fill="none" stroke={colOf(p, iso)} strokeWidth={w} strokeDasharray="4 14" strokeLinecap="round" /> : null}
            </g>
          );
        })}
      </svg>
      {/* cabeças + nomes (rótulos afastados para não encavalar) */}
      {(() => {
        const heads = all.map((iso) => {
          const a = fadeOf(iso);
          if (a <= 0.01) return null;
          const upto = (sh.hidden || []).includes(iso) ? Y1 : Math.min(R, S[iso].length ? S[iso][S[iso].length - 1][0] : R);
          const v = valAt(S[iso], upto);
          if (v == null) return null;
          return {iso, a, v, x: X(upto), y: Yp(v), ly: Yp(v)};
        }).filter(Boolean).sort((m, n) => m.y - n.y);
        for (let i = 1; i < heads.length; i++) if (heads[i].ly - heads[i - 1].ly < 40) heads[i].ly = heads[i - 1].ly + 40;
        const pulse = 1 + 0.18 * Math.sin(T * 5);
        return heads.map((h) => (
          <React.Fragment key={h.iso}>
            <div style={{position: 'absolute', left: h.x - 13, top: h.y - 13, width: 26, height: 26, borderRadius: '50%', background: colOf(p, h.iso), opacity: h.a, boxShadow: `0 0 0 ${8 * pulse}px ${colOf(p, h.iso)}33`}} />
            <div style={{position: 'absolute', left: h.x + 24, top: h.ly - 22, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: colOf(p, h.iso), opacity: h.a, whiteSpace: 'nowrap', textShadow: '0 3px 12px rgba(0,0,0,.6)'}}>
              {NAME[h.iso] || h.iso}<span style={{color: '#ffffffd0', fontWeight: 600, marginLeft: 10}}>{fmt(h.v, sh.fmt)}</span>
            </div>
          </React.Fragment>
        ));
      })()}
      {/* ano corrente em marca d'água */}
      {sh.keys && sh.keys.length ? <div style={{position: 'absolute', right: 1920 - PL.x1 + 10, top: sh.wm === 'tr' ? 190 : PL.y1 - 190, fontFamily: SANS, fontWeight: 900, fontSize: 150, color: '#ffffff', opacity: 0.06, letterSpacing: -4}}>{Math.floor(R + 0.001)}</div> : null}
      {(sh.labels || []).map((l, i) => {
        const pt = pickYear(S[l.iso] || [], l.year);
        if (pt[1] == null) return null;
        const right = X(pt[0]) > 1050;
        return <Pill key={i} x={X(pt[0])} y={Yp(pt[1]) - 54} text={fmt(pt[1], sh.fmt)} sub={String(pt[0])} color={colOf(p, l.iso)} T={T} t0={l.t} align={right ? 'right' : 'left'} />;
      })}
      {sh.peak && sh.peak.t != null ? (() => {
        const pts = S[sh.peak.iso];
        const pk = pts.reduce((m, q) => (q[1] > m[1] ? q : m), pts[0]);
        return <Pill x={X(pk[0])} y={Yp(pk[1]) - 60} text={`peak · ${pk[0]}`} sub={fmt(pk[1], sh.fmt)} color={colOf(p, sh.peak.iso)} T={T} t0={sh.peak.t} />;
      })() : null}
      {cross ? (
        <>
          <Burst x={X(cross[0])} y={Yp(cross[1])} T={T} t0={sh.cross.t} p={p} />
          <Pill x={X(cross[0]) - 30} y={Yp(cross[1]) + 110} text={sh.cross.text || 'First time ever'} color="#ffffff" T={T} t0={sh.cross.t + 0.3} align="right" />
        </>
      ) : null}
      {sh.fxbox && sh.fxbox.t != null ? <FxBox sh={sh} p={p} data={data} T={T} /> : null}
    </AbsoluteFill>
  );
};

const niceTicks = (a, b, n) => {
  const span = b - a;
  const raw = span / n;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= n) || 10 * mag;
  const out = [];
  for (let v = Math.ceil(a / step) * step; v <= b + 1e-9; v += step) out.push(+v.toFixed(6));
  return out;
};

const crossPoint = (A, B) => {
  const bm = Object.fromEntries(B);
  for (let i = 1; i < A.length; i++) {
    const [y0, a0] = A[i - 1], [y1, a1] = A[i];
    if (bm[y0] == null || bm[y1] == null || y0 < 2000) continue;
    const d0 = a0 - bm[y0], d1 = a1 - bm[y1];
    if (d0 < 0 && d1 >= 0) {
      const k = d0 / (d0 - d1);
      return [y0 + k * (y1 - y0), a0 + k * (a1 - a0)];
    }
  }
  return null;
};

const FxBox = ({sh, p, data, T}) => {
  const fx = ser(data, sh.fxbox.set, sh.fxbox.iso);
  const a = valAt(fx, sh.fxbox.a), b = valAt(fx, sh.fxbox.b);
  const s = sp(T, sh.fxbox.t);
  const v = a + (b - a) * ramp(T, sh.fxbox.t + 0.4, 1.4);
  return (
    <div style={{position: 'absolute', left: 820, top: 250, width: 460, padding: '22px 28px', borderRadius: 22, background: '#0b1026e6', border: `2px solid ${p.warm}`, opacity: s, transform: `scale(${0.85 + 0.15 * s})`}}>
      <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, color: '#ffffffb0'}}>Yen per US dollar</div>
      <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 84, color: p.warm, lineHeight: 1.05}}>¥{Math.round(v)}</div>
      <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 26, color: '#ffffffb0'}}>{sh.fxbox.a}: ¥{Math.round(a)} → {sh.fxbox.b}: ¥{Math.round(b)}</div>
    </div>
  );
};

// ---------------- BARRAS ABSOLUTAS (ex.: nascimentos por ano) ----------------
const BarsAbs = ({sh, p, data, T, dim}) => {
  const [Y0, Y1] = sh.years;
  const pts = ser(data, sh.set, sh.iso).filter(([y]) => y >= Y0 && y <= Y1);
  const R = keyed(T, sh.start ?? Y1, sh.keys);
  const vmax = Math.max(...pts.map((q) => q[1]), 1) * 1.12;
  const vmin = Math.min(0, ...pts.map((q) => q[1])) * 1.12;  // valores negativos descem abaixo do zero
  const x0 = 190, x1 = 1300, hpx = 600;
  const Yv = (v) => 880 - ((v - vmin) / (vmax - vmin)) * hpx;
  const base = Yv(0);
  const n = Y1 - Y0 + 1;
  const bw = (x1 - x0) / n;
  const X = (y) => x0 + (y - Y0) * bw;
  const H = (v) => base - Yv(v);
  const [ha, hb] = sh.hl || [0, -1];
  const hlOn = sh.hltext ? ramp(T, sh.hltext.t, 0.6) : (sh.hl ? 1 : 0);
  const ticks = niceTicks(vmin, vmax, 4).filter((v) => v !== 0 && v > vmin && v < vmax);
  return (
    <AbsoluteFill style={{opacity: dim ? 0.3 : 1}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {ticks.map((v) => (
          <g key={v}>
            <line x1={x0} x2={x1} y1={base - H(v)} y2={base - H(v)} stroke="#fff" strokeOpacity={0.08} strokeWidth={2} />
            <text x={x0 - 16} y={base - H(v) + 9} textAnchor="end" fontFamily={SANS} fontWeight={600} fontSize={24} fill="#ffffff60">{fmt(v, sh.fmt)}</text>
          </g>
        ))}
        <line x1={x0} x2={x1} y1={base} y2={base} stroke="#fff" strokeOpacity={0.4} strokeWidth={2} />
        {pts.map(([y, v]) => {
          const g = Math.max(0, Math.min(1, (R - y) + 1));
          if (g <= 0) return null;
          const h = H(v) * Easing.out(Easing.cubic)(g);
          const inHl = y >= ha && y <= hb;
          const col = v < 0 ? '#ff5a6e' : inHl ? mix(p.acc2, p.acc, hlOn) : p.acc2;
          const isLab = (sh.labels || []).some((l) => l.year === y && l.t != null && T >= l.t);
          return <rect key={y} x={X(y) + bw * 0.12} width={bw * 0.76} y={h >= 0 ? base - h : base} height={Math.max(Math.abs(h), 2)} rx={3} fill={isLab ? '#ffffff' : col} fillOpacity={hb >= ha && !inHl && hlOn > 0 ? 1 - 0.5 * hlOn : 1} />;
        })}
        {pts.filter(([y]) => y % 10 === 0 || y === Y1).map(([y]) => <text key={y} x={X(y) + bw / 2} y={base + 44} textAnchor="middle" fontFamily={SANS} fontWeight={600} fontSize={24} fill="#ffffff70">{y}</text>)}
      </svg>
      {(sh.labels || []).map((l, i) => {
        const pt = pts.find(([y]) => y === l.year);
        if (!pt) return null;
        return <Pill key={i} x={X(l.year) + bw / 2} y={pt[1] >= 0 ? base - H(pt[1]) - 50 : base - H(pt[1]) + 14} text={fmt(pt[1], sh.fmt)} sub={String(l.year)} color={i % 2 ? p.acc : '#ffffff'} T={T} t0={l.t} align={X(l.year) > 1000 ? 'right' : 'left'} />;
      })}
      {sh.hltext && hlOn > 0 ? <div style={{position: 'absolute', left: (X(ha) + X(hb) + bw) / 2, top: 180, transform: 'translateX(-50%)', opacity: hlOn, fontFamily: SANS, fontWeight: 900, fontSize: 40, color: p.acc, whiteSpace: 'nowrap'}}>{sh.hltext.text}</div> : null}
    </AbsoluteFill>
  );
};

// ---------------- PESSOAS (gerações) ----------------
const Person = ({x, y, s, col, a}) => (
  <g transform={`translate(${x},${y}) scale(${s})`} opacity={a}>
    <circle cx={0} cy={-14} r={7} fill={col} />
    <path d="M -10 10 Q -10 -4 0 -4 Q 10 -4 10 10 Z" fill={col} />
  </g>
);

const People = ({sh, p, T}) => {
  const gens = sh.gens || [];
  const cols = ['#ffffff', p.acc2, p.acc];
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {gens.map((g, gi) => {
          if (g.t == null) return null;
          const perRow = 10;
          const cx = 280 + gi * 400, top = 260;
          const step = 34;
          return (
            <g key={gi}>
              {Array.from({length: g.n}).map((_, k) => {
                const r = Math.floor(k / perRow), c = k % perRow;
                const st = g.t + (k / Math.max(g.n, 1)) * 0.9;
                const a = ramp(T, st, 0.25);
                if (a <= 0) return null;
                return <Person key={k} x={cx - (perRow - 1) * step / 2 + c * step} y={top + r * 46} s={1.25 + 0.25 * (1 - a)} col={cols[gi % 3]} a={a} />;
              })}
            </g>
          );
        })}
        {gens.slice(1).map((g, gi) => g.t != null ? <text key={gi} x={280 + gi * 400 + 200} y={330} textAnchor="middle" fontFamily={SANS} fontWeight={900} fontSize={60} fill="#ffffff70" opacity={ramp(T, g.t - 0.3, 0.4)}>→</text> : null)}
      </svg>
      {gens.map((g, gi) => {
        if (g.t == null) return null;
        const s = sp(T, g.t + 0.4);
        return (
          <div key={gi} style={{position: 'absolute', left: 280 + gi * 400 - 160, width: 320, top: 760, textAlign: 'center', opacity: s, transform: `translateY(${(1 - s) * 20}px)`}}>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 110, lineHeight: 1, color: cols[gi % 3]}}>{Math.round(g.n * Math.min(1, ramp(T, g.t, 0.9) + 0.001))}</div>
            <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 34, color: '#ffffffc0'}}>{g.label}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 120, top: 92, fontFamily: SANS, fontWeight: 900, fontSize: 36, color: '#0d1020', background: p.acc, padding: '6px 20px', borderRadius: 12}}>at {sh.tfr} babies per woman</div>
    </AbsoluteFill>
  );
};

// ---------------- KIT "COMO FUNCIONA" (How It Ticks) ----------------
// terminal: linhas digitadas {at, in, out, note}
const Code = ({sh, p, T}) => (
  <AbsoluteFill>
    <div style={{position: 'absolute', left: 150, top: 200, width: 1150, borderRadius: 22, overflow: 'hidden', background: '#0a0d14', border: '2px solid #ffffff22', boxShadow: '0 30px 80px rgba(0,0,0,.55)', opacity: sp(T, sh.t0)}}>
      <div style={{height: 54, background: '#161b26', display: 'flex', alignItems: 'center', gap: 12, paddingLeft: 22}}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 16, height: 16, borderRadius: '50%', background: c}} />)}
        <div style={{fontFamily: MONO, fontWeight: 500, fontSize: 22, color: '#ffffff70', marginLeft: 16}}>{sh.title || 'console'}</div>
      </div>
      <div style={{padding: '30px 36px', minHeight: 420}}>
        {(sh.lines || []).map((l, i) => {
          if (l.t == null || T < l.t) return null;
          const n = Math.floor(Math.min(1, (T - l.t) / Math.max(0.35, l.in.length * 0.05)) * l.in.length);
          const typed = l.in.slice(0, n);
          const outOn = l.out != null && T > l.t + l.in.length * 0.05 + 0.5;
          const caret = !outOn && Math.floor(T * 2) % 2 === 0;
          return (
            <div key={i} style={{marginBottom: 26}}>
              <div style={{fontFamily: MONO, fontWeight: 800, fontSize: 52, color: '#ffffff'}}><span style={{color: p.acc}}>&gt; </span>{typed}{caret ? <span style={{color: p.acc}}>▌</span> : null}</div>
              {outOn ? <div style={{fontFamily: MONO, fontWeight: 800, fontSize: 52, color: l.bad ? p.warm : p.acc2, marginTop: 6}}>{l.out}</div> : null}
              {outOn && l.note ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 28, color: '#ffffff90', marginTop: 6}}>{l.note}</div> : null}
            </div>
          );
        })}
      </div>
    </div>
  </AbsoluteFill>
);

// bits: expansão binária com registrador de N bits e o resto cortado
const Bits = ({sh, p, T}) => {
  const bits = sh.bits || '';
  const reg = sh.reg || bits.length;
  const t0 = sh.show?.t ?? sh.t0 + 0.3;
  const shown = Math.floor(Math.max(0, (T - t0) / (sh.speed || 0.07)));
  const chop = sh.chop && sh.chop.t != null ? ramp(T, sh.chop.t, 0.5) : 0;
  const per = Math.min(30, bits.length);
  const W = 44, G = 7, HB = 64;
  const rows = Math.ceil(bits.length / per);
  const yb = 400, yEnd = yb + rows * (HB + G);
  const rep = sh.repeat;  // [início, tamanho] do padrão que se repete
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 150, top: 190, fontFamily: MONO, fontWeight: 800, fontSize: 80, color: '#fff', whiteSpace: 'nowrap'}}>{sh.label}</div>
      {sh.sub ? <div style={{position: 'absolute', left: 154, top: 300, fontFamily: MONO, fontWeight: 500, fontSize: 40, color: '#ffffff80', whiteSpace: 'nowrap'}}>{sh.sub}</div> : null}
      <div style={{position: 'absolute', left: 150, top: yb, width: per * (W + G), display: 'flex', flexWrap: 'wrap', gap: G}}>
        {bits.split('').map((b, i) => {
          if (i >= shown) return null;
          const out = i >= reg;
          const inRep = rep && i >= rep[0] && ((i - rep[0]) % (rep[1] * 2)) < rep[1];
          return (
            <div key={i} style={{width: W, height: HB, borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO, fontWeight: 800, fontSize: 40,
              background: out && chop > 0 ? `rgba(255,77,109,${0.22 * chop})` : inRep ? p.acc + '33' : '#ffffff12', color: out && chop > 0.5 ? p.warm : b === '1' ? p.acc : '#ffffffc0', opacity: out ? 1 - 0.55 * chop : 1, textDecoration: out && chop > 0.5 ? 'line-through' : 'none',
              border: i === reg - 1 ? `2px solid ${p.acc2}` : '2px solid transparent'}}>{b}</div>
          );
        })}
      </div>
      {sh.chop && chop > 0 ? (
        <div style={{position: 'absolute', left: 150 + (reg % per) * (W + G) - 5, top: yb - 20 + Math.floor(reg / per) * (HB + G), height: HB + 40, width: 6, background: p.warm, opacity: chop, borderRadius: 3}} />
      ) : null}
      {sh.reg && sh.regtext ? <Pill x={150} y={yEnd + 30} text={'◧ ' + sh.regtext.text} color={p.acc2} T={T} t0={sh.regtext.t} /> : null}
      {sh.chop && chop > 0 ? <Pill x={150} y={yEnd + (sh.regtext ? 120 : 40)} text={sh.chop.text} color={p.warm} T={T} t0={sh.chop.t} /> : null}
    </AbsoluteFill>
  );
};

// contador gigante que estoura (ex.: 2,147,483,647 → −2,147,483,648)
const Counter = ({sh, p, T}) => {
  const t0 = sh.go?.t ?? sh.t0 + 0.3;
  const k = ramp(T, t0, sh.dur || 2.5);
  const from = sh.from, to = sh.to;
  const v = Math.floor(from + (to - from) * Easing.out(Easing.cubic)(k));
  const wrapped = sh.wrap && sh.wrap.t != null && T >= sh.wrap.t;
  const shake = wrapped ? Math.max(0, 1 - (T - sh.wrap.t) / 0.6) * Math.sin(T * 70) * 10 : 0;
  const txt = wrapped ? sh.wrap.value.toLocaleString('en-US').replace('-', '−') : v.toLocaleString('en-US');
  return (
    <AbsoluteFill>
      <Rays p={p} T={T} t0={wrapped ? sh.wrap.t : null} />
      <div style={{position: 'absolute', left: 150, top: 230, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: '#ffffffb0'}}>{sh.title}</div>
      <div style={{position: 'absolute', left: 150, top: 330, fontFamily: MONO, fontWeight: 800, fontSize: txt.length > 14 ? 120 : 150, color: wrapped ? p.warm : '#fff', letterSpacing: -4, transform: `translateX(${shake}px)`, textShadow: '0 12px 40px rgba(0,0,0,.5)'}}>{txt}</div>
      {sh.unit ? <div style={{position: 'absolute', left: 156, top: 520, fontFamily: SANS, fontWeight: 700, fontSize: 36, color: '#ffffff90'}}>{sh.unit}</div> : null}
      {wrapped && sh.wrap.text ? <Pill x={150} y={640} text={sh.wrap.text} color={p.warm} T={T} t0={sh.wrap.t + 0.3} /> : null}
      {(sh.notes || []).map((n, i) => <Pill key={i} x={150} y={720 + i * 80} text={n.text} color={i % 2 ? p.acc2 : '#ffffff'} T={T} t0={n.t} />)}
    </AbsoluteFill>
  );
};

// radar: o relógio atrasa e a "janela" de rastreio sai de cima do míssil
const Radar = ({sh, p, T}) => {
  const H = keyed(T, sh.start ?? 0, sh.keys, 'hours');
  const drift = (sh.perHour || 0.003433) * H;  // s
  const shift = drift * (sh.speed || 1676) * (sh.gateScale || 1.2);  // m (com a escala da janela usada no relatório)
  const m = shift / (sh.maxM || 700);
  const cx = 640, cy = 560, R = 330;
  const sweep = (T * 90) % 360;
  const tx = cx + 60, ty = cy - 120;  // posição real do Scud
  const gx = tx - m * 300, gy = ty + m * 120;  // onde o radar olha
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <circle cx={cx} cy={cy} r={R} fill="#06120c" stroke={p.acc2} strokeOpacity={0.6} strokeWidth={3} />
        {[0.33, 0.66].map((k) => <circle key={k} cx={cx} cy={cy} r={R * k} fill="none" stroke={p.acc2} strokeOpacity={0.2} strokeWidth={2} />)}
        <line x1={cx - R} x2={cx + R} y1={cy} y2={cy} stroke={p.acc2} strokeOpacity={0.15} />
        <line x1={cx} x2={cx} y1={cy - R} y2={cy + R} stroke={p.acc2} strokeOpacity={0.15} />
        <path d={`M${cx},${cy} L${cx + R * Math.cos((sweep * Math.PI) / 180)},${cy + R * Math.sin((sweep * Math.PI) / 180)} A${R},${R} 0 0,0 ${cx + R * Math.cos(((sweep - 40) * Math.PI) / 180)},${cy + R * Math.sin(((sweep - 40) * Math.PI) / 180)} Z`} fill={p.acc2} fillOpacity={0.12} />
        <rect x={gx - 70} y={gy - 70} width={140} height={140} fill="none" stroke={m > 0.6 ? p.warm : p.acc} strokeWidth={5} strokeDasharray="12 8" />
        <circle cx={tx} cy={ty} r={14} fill={p.warm} />
        <circle cx={tx} cy={ty} r={14 + 10 * Math.abs(Math.sin(T * 4))} fill="none" stroke={p.warm} strokeOpacity={0.6} strokeWidth={3} />
        <text x={tx + 24} y={ty - 18} fontFamily={SANS} fontWeight={900} fontSize={30} fill={p.warm}>SCUD</text>
        <text x={gx - 70} y={gy + 104} fontFamily={SANS} fontWeight={800} fontSize={26} fill={m > 0.6 ? p.warm : p.acc}>where the radar looks</text>
      </svg>
      <div style={{position: 'absolute', left: 1040, top: 270, display: 'flex', flexDirection: 'column', gap: 26}}>
        {[[`${H.toFixed(0)} h`, 'running nonstop'], [`${drift.toFixed(4)} s`, 'clock error'], [`${Math.round(shift)} m`, 'off target']].map(([v, l], i) => (
          <div key={i}>
            <div style={{fontFamily: MONO, fontWeight: 800, fontSize: 72, color: i === 2 && m > 0.6 ? p.warm : '#fff', lineHeight: 1}}>{v}</div>
            <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 28, color: '#ffffff90'}}>{l}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// escada: duas réguas (ex.: 1.000 vs 1.024) que se afastam a cada degrau
const Ladder = ({sh, p, T}) => {
  const rows = sh.rows || [];
  const W = sh.w || 760, x0 = 420;
  const rmax = Math.max(...rows.map((r) => r.b / r.a));
  return (
    <AbsoluteFill>
      {sh.title ? <div style={{position: 'absolute', left: 150, top: 170, fontFamily: SANS, fontWeight: 800, fontSize: 46, color: '#ffffffd0', opacity: sp(T, sh.t0)}}>{sh.title}</div> : null}
      <div style={{position: 'absolute', left: x0, top: 250, display: 'flex', gap: 34, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: '#ffffffa0', opacity: sp(T, sh.t0 + 0.3)}}>
        <span><span style={{display: 'inline-block', width: 22, height: 22, borderRadius: 5, background: '#ffffff55', marginRight: 10, verticalAlign: -3}} />{sh.la || 'decimal'}</span>
        <span><span style={{display: 'inline-block', width: 22, height: 22, borderRadius: 5, background: p.acc, marginRight: 10, verticalAlign: -3}} />{sh.lb || 'binary'}</span>
      </div>
      {rows.map((r, i) => {
        if (r.t == null || T < r.t - 0.1) return null;
        const k = ramp(T, r.t, 0.8);
        const y = 320 + i * 118;
        const wb = W * (1 + (r.b / r.a - 1) * Easing.out(Easing.cubic)(k));
        const hot = r.hot && T >= r.t;
        return (
          <div key={i} style={{position: 'absolute', left: 0, top: y, opacity: Math.min(1, k * 3)}}>
            <div style={{position: 'absolute', left: 150, top: 2, width: 250, fontFamily: MONO, fontWeight: 800, fontSize: 46, color: '#fff'}}>{r.label}</div>
            <div style={{position: 'absolute', left: x0, top: 0, width: wb, height: 64, borderRadius: 12, background: p.acc}} />
            <div style={{position: 'absolute', left: x0, top: 0, width: W, height: 64, borderRadius: 12, background: '#3a3a44', display: 'flex', alignItems: 'center', paddingLeft: 20, fontFamily: MONO, fontWeight: 500, fontSize: 28, color: '#ffffffb0'}}>{r.text}</div>
            <div style={{position: 'absolute', left: x0 + W * rmax + 30, top: 4, fontFamily: SANS, fontWeight: 900, fontSize: 52, color: hot ? p.warm : p.acc, whiteSpace: 'nowrap'}}>{r.gap}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// pilha: uma barra dividida em partes (ex.: 931 GB visíveis + 69 GB "sumidos")
const Stack = ({sh, p, T}) => {
  const segs = sh.segs || [];
  const total = sh.total || segs.reduce((a, g) => a + g.value, 0);
  const W = 1300, x0 = 150, y0 = 420, H = 130;
  let acc = 0;
  return (
    <AbsoluteFill>
      {sh.title ? <div style={{position: 'absolute', left: 150, top: 200, fontFamily: SANS, fontWeight: 800, fontSize: 52, color: '#fff', opacity: sp(T, sh.t0)}}>{sh.title}</div> : null}
      {sh.sub ? <div style={{position: 'absolute', left: 152, top: 272, fontFamily: SANS, fontWeight: 600, fontSize: 32, color: '#ffffff90', opacity: sp(T, sh.t0 + 0.3)}}>{sh.sub}</div> : null}
      <div style={{position: 'absolute', left: x0, top: y0, width: W, height: H, borderRadius: 18, border: '3px solid #ffffff30', opacity: sp(T, sh.t0)}} />
      {segs.map((g, i) => {
        const x = x0 + (W * acc) / total;
        acc += g.value;
        if (g.t == null || T < g.t - 0.05) return null;
        const k = Easing.out(Easing.cubic)(ramp(T, g.t, 0.9));
        const w = (W * g.value) / total;
        const col = p[g.color] || g.color || p.acc;
        const narrow = w < 330;
        return (
          <div key={i}>
            <div style={{position: 'absolute', left: x, top: y0, width: w * k, height: H, background: g.ghost ? 'transparent' : col, border: g.ghost ? `4px dashed ${col}` : 'none',
              borderRadius: i === 0 ? '18px 0 0 18px' : i === segs.length - 1 ? '0 18px 18px 0' : 0, opacity: g.ghost ? 0.5 + 0.5 * Math.abs(Math.sin(T * 3)) : 1}} />
            <div style={{position: 'absolute', ...(narrow ? {right: 1920 - (x + w), textAlign: 'right'} : {left: x}), top: y0 + H + 22, opacity: k, whiteSpace: 'nowrap'}}>
              <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 64, color: col, lineHeight: 1}}>{g.text}</div>
              <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 30, color: '#ffffff90', marginTop: 6}}>{g.label}</div>
            </div>
          </div>
        );
      })}
      {sh.kicker && sh.kicker.t != null ? <Pill x={150} y={800} text={sh.kicker.text} color={p.warm} T={T} t0={sh.kicker.t} /> : null}
    </AbsoluteFill>
  );
};

// órbita: Terra, anel de satélites, sinais até o celular e esferas de distância (GPS)
const Orbit = ({sh, p, T}) => {
  const cx = 640, cy = 580, RE = 165, RO = 395;
  const n = sh.sats || 6;
  const ph = (-62 * Math.PI) / 180;
  const px = cx + RE * Math.cos(ph), py = cy + RE * Math.sin(ph);
  const sats = Array.from({length: n}).map((_, i) => {
    const a = (i / n) * Math.PI * 2 - Math.PI / 2 + (T - sh.t0) * 0.045;
    return [cx + RO * Math.cos(a), cy + RO * 0.82 * Math.sin(a)];
  });
  const vis = sats.map((q, i) => [i, Math.hypot(q[0] - px, q[1] - py)]).sort((a, b) => a[1] - b[1]).slice(0, 4).map((x) => x[0]);
  const lk = sh.link && sh.link.t != null ? ramp(T, sh.link.t, 0.8) : 0;
  const sph = sh.spheres && sh.spheres.t != null ? ramp(T, sh.spheres.t, 1.2) : 0;
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <radialGradient id="earthG" cx="40%" cy="35%" r="70%"><stop offset="0%" stopColor="#3b82f6" /><stop offset="70%" stopColor="#1e3a8a" /><stop offset="100%" stopColor="#0b1530" /></radialGradient>
        </defs>
        <ellipse cx={cx} cy={cy} rx={RO} ry={RO * 0.82} fill="none" stroke="#ffffff" strokeOpacity={0.18} strokeWidth={3} strokeDasharray="10 12" />
        <circle cx={cx} cy={cy} r={RE + 18} fill={p.acc2} opacity={0.08} />
        <circle cx={cx} cy={cy} r={RE} fill="url(#earthG)" />
        {[0.35, 0.7].map((k) => <ellipse key={k} cx={cx} cy={cy} rx={RE} ry={RE * k} fill="none" stroke="#ffffff" strokeOpacity={0.12} strokeWidth={2} />)}
        {[0.4, 0.8].map((k) => <ellipse key={'v' + k} cx={cx} cy={cy} rx={RE * k} ry={RE} fill="none" stroke="#ffffff" strokeOpacity={0.12} strokeWidth={2} />)}
        {vis.slice(0, 3).map((i) => {
          const [sx, sy] = sats[i];
          const r = Math.hypot(sx - px, sy - py);
          return sph > 0 ? <circle key={'s' + i} cx={sx} cy={sy} r={r * sph} fill="none" stroke={p.acc} strokeOpacity={0.45} strokeWidth={3} /> : null;
        })}
        {vis.map((i, j) => {
          const [sx, sy] = sats[i];
          const k = Math.max(0, Math.min(1, lk * 1.6 - j * 0.2));
          if (k <= 0) return null;
          const ex = sx + (px - sx) * k, ey = sy + (py - sy) * k;
          const pulse = ((T * 0.9 + j * 0.25) % 1);
          return (
            <g key={'l' + i}>
              <line x1={sx} y1={sy} x2={ex} y2={ey} stroke={p.acc} strokeOpacity={0.7} strokeWidth={3} strokeDasharray="6 10" />
              {k >= 1 ? <circle cx={sx + (px - sx) * pulse} cy={sy + (py - sy) * pulse} r={7} fill={p.acc} /> : null}
            </g>
          );
        })}
        {sats.map(([sx, sy], i) => (
          <g key={i} transform={`translate(${sx},${sy})`}>
            <rect x={-34} y={-8} width={24} height={16} rx={3} fill="#5fd3ff" opacity={0.9} />
            <rect x={10} y={-8} width={24} height={16} rx={3} fill="#5fd3ff" opacity={0.9} />
            <rect x={-10} y={-12} width={20} height={24} rx={5} fill="#e5e7eb" />
            <circle cx={0} cy={0} r={4} fill={vis.includes(i) && lk > 0 ? p.acc : '#94a3b8'} />
          </g>
        ))}
        <circle cx={px} cy={py} r={13} fill="#fff" />
        <circle cx={px} cy={py} r={13 + 10 * Math.abs(Math.sin(T * 3))} fill="none" stroke="#fff" strokeOpacity={0.5} strokeWidth={3} />
      </svg>
      {sh.msg && sh.msg.t != null && T >= sh.msg.t ? (
        <div style={{position: 'absolute', left: 1080, top: 250, maxWidth: 700, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: '#0d1020', background: '#fff', padding: '16px 24px', borderRadius: 18, opacity: sp(T, sh.msg.t), boxShadow: '0 12px 30px rgba(0,0,0,.4)'}}>{sh.msg.text}</div>
      ) : null}
      {sh.tag && sh.tag.t != null ? <Pill x={1080} y={sh.msg ? 420 : 300} text={sh.tag.text} color={p.warm} T={T} t0={sh.tag.t} /> : null}
    </AbsoluteFill>
  );
};

// lançamento: foguete sobe com relógio T+ e explode no cue
const Launch = ({sh, p, T}) => {
  const t0 = sh.go?.t ?? sh.t0 + 0.5;
  const boomT = sh.boom?.t;
  const tl = Math.max(0, T - t0);
  const clock = boomT != null && T >= boomT ? sh.boom.at_s : Math.min(sh.boom?.at_s ?? 37, tl * ((sh.boom?.at_s ?? 37) / Math.max(0.1, (boomT ?? t0 + 6) - t0)));
  const k = Math.min(1, clock / (sh.boom?.at_s ?? 37));
  const x = 520 + 420 * k * k, y = 900 - 640 * k;
  const ang = -10 - 40 * k;
  const boom = boomT != null && T >= boomT;
  const bk = boom ? Math.min(1, (T - boomT) / 1.2) : 0;
  return (
    <AbsoluteFill style={{background: `linear-gradient(${mix('#0b1a3a', '#1d3b78', 1 - k)}, #06080f)`}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <path d={`M520,900 Q${520 + 100 * k},${900 - 320 * k} ${x},${y}`} fill="none" stroke="#ffffff" strokeOpacity={0.35} strokeWidth={10} strokeLinecap="round" />
        {!boom ? (
          <g transform={`translate(${x},${y}) rotate(${ang})`}>
            <path d="M0,-70 C14,-50 16,-10 16,40 L-16,40 C-16,-10 -14,-50 0,-70 Z" fill="#f2f2f2" />
            <path d="M-16,20 L-32,48 L-16,44 Z M16,20 L32,48 L16,44 Z" fill={p.warm} />
            <path d={`M-10,42 Q0,${90 + 20 * Math.sin(T * 30)} 10,42 Z`} fill={p.acc} />
          </g>
        ) : (
          <g>
            {Array.from({length: 26}).map((_, i) => {
              const a = (i / 26) * Math.PI * 2;
              const d = 40 + 260 * bk * (0.6 + 0.4 * ((i * 7) % 5) / 5);
              return <circle key={i} cx={x + Math.cos(a) * d} cy={y + Math.sin(a) * d + bk * bk * 60} r={18 * (1 - bk) + 4} fill={i % 3 ? p.acc : p.warm} opacity={1 - bk * 0.8} />;
            })}
            <circle cx={x} cy={y} r={120 * bk + 20} fill="#fff" opacity={0.6 * (1 - bk)} />
          </g>
        )}
        <rect x={0} y={960} width={1920} height={120} fill="#05070c" />
      </svg>
      <div style={{position: 'absolute', left: 150, top: 150, fontFamily: MONO, fontWeight: 800, fontSize: 110, color: boom ? p.warm : '#fff'}}>T+{clock.toFixed(0).padStart(2, '0')} s</div>
      {sh.title ? <div style={{position: 'absolute', left: 156, top: 290, fontFamily: SANS, fontWeight: 800, fontSize: 38, color: '#ffffffb0'}}>{sh.title}</div> : null}
      {(sh.notes || []).map((n, i) => <Pill key={i} x={1000} y={600 + i * 90} text={n.text} color={i % 2 ? p.acc2 : '#ffffff'} T={T} t0={n.t} />)}
    </AbsoluteFill>
  );
};

// ---------------- BARRAS (crescimento anual) ----------------
const Bars = ({sh, p, data, T, dim}) => {
  const [Y0, Y1] = sh.years;
  const pts = ser(data, sh.set, sh.iso).filter(([y]) => y >= Y0 && y <= Y1);
  const R = keyed(T, sh.start ?? Y0 - 1, sh.keys);
  const vmax = Math.max(...pts.map((q) => Math.abs(q[1])), 1);
  const lim = Math.ceil(vmax / 2) * 2;
  const x0 = 190, x1 = 1300, zero = 600, hpx = 300;
  const bw = (x1 - x0) / pts.length;
  const X = (y) => x0 + (y - Y0) * bw;
  const br = sh.bracket;
  return (
    <AbsoluteFill style={{opacity: dim ? 0.3 : 1}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={x0} x2={x1} y1={zero} y2={zero} stroke="#fff" strokeOpacity={0.4} strokeWidth={2} />
        {[-lim, -lim / 2, lim / 2, lim].map((v) => <text key={v} x={x0 - 16} y={zero - (v / lim) * hpx + 9} textAnchor="end" fontFamily={SANS} fontWeight={600} fontSize={24} fill="#ffffff60">{v > 0 ? '+' : ''}{v}%</text>)}
        {pts.map(([y, v]) => {
          const g = Math.max(0, Math.min(1, (R - y) + 1));
          if (g <= 0) return null;
          const h = (Math.abs(v) / lim) * hpx * Easing.out(Easing.cubic)(g);
          const col = v >= 0 ? p.acc2 : p.warm;
          const inBr = br && br.t != null && T >= br.t && y >= br.a && y <= br.b;
          return <rect key={y} x={X(y) + bw * 0.14} width={bw * 0.72} y={v >= 0 ? zero - h : zero} height={Math.max(h, 2)} rx={4} fill={col} fillOpacity={inBr || !br || br.t == null || T < br.t ? 1 : 0.45} />;
        })}
        {pts.filter(([y]) => y % 5 === 0).map(([y]) => <text key={y} x={X(y) + bw / 2} y={zero + hpx + 60} textAnchor="middle" fontFamily={SANS} fontWeight={600} fontSize={24} fill="#ffffff70">{y}</text>)}
      </svg>
      {br && br.t != null ? (() => {
        const a = ramp(T, br.t, 0.8);
        const xa = X(br.a), xb = X(br.b) + bw;
        return (
          <>
            <div style={{position: 'absolute', left: xa, top: zero - hpx - 40, width: (xb - xa) * a, height: 14, borderTop: `4px solid ${p.acc}`, borderLeft: `4px solid ${p.acc}`, borderRight: a > 0.98 ? `4px solid ${p.acc}` : 'none'}} />
            <div style={{position: 'absolute', left: (xa + xb) / 2, top: zero - hpx - 104, transform: 'translateX(-50%)', fontFamily: SANS, fontWeight: 900, fontSize: 46, color: p.acc, opacity: a, whiteSpace: 'nowrap'}}>{br.text}</div>
          </>
        );
      })() : null}
      {sh.kicker && sh.kicker.t != null ? <Pill x={1300} y={980} text={sh.kicker.text} color={p.warm} T={T} t0={sh.kicker.t} align="right" /> : null}
    </AbsoluteFill>
  );
};

// ---------------- GLOBO ----------------
const Globe = ({sh, p, data, T}) => {
  const v0 = sh.view;
  let view = {...v0};
  let hl = sh.hl || [];
  for (const k of (sh.keys || []).filter((k) => k.t != null)) {
    if (T < k.t) break;
    const e = ramp(T, k.t, k.dur || 2);
    const dip = Math.sin(e * Math.PI) * (k.dip ?? 0.55);
    view = {lon: view.lon + (k.lon - view.lon) * e, lat: view.lat + (k.lat - view.lat) * e, zoom: (view.zoom + (k.zoom - view.zoom) * e) * (1 - dip)};
    if (e > 0.5 && k.hl) hl = k.hl;
  }
  view.zoom *= 1 + 0.04 * Math.sin(T / 6);
  const R = 300 * view.zoom;
  const proj = geoOrthographic().scale(R).translate([820, 560]).rotate([-view.lon - (T - sh.t0) * 0.35 / Math.max(1, view.zoom / 3), -view.lat]).clipAngle(90).precision(0.6);
  const path = geoPath(proj);
  const fillOf = (iso) => {
    if (hl.includes(iso) || (sh.hl2 || []).includes(iso)) return p.acc;
    if (sh.fills && sh.fills.EU && sh.fills.EU.includes(iso)) return '#3e5fae';
    return null;
  };
  const seqAt = {};
  if (sh.seq && sh.seq.t != null) sh.seq.isos.forEach((iso, i) => (seqAt[iso] = sh.seq.t + i * sh.seq.step));
  const choroAt = {};
  if (sh.choro && sh.choro.t != null) {
    const g = data[sh.choro.set] || {};
    const order = sh.choro.isos.filter((i) => i !== sh.choro.last).sort((a, b) => (g[a] ?? 0) - (g[b] ?? 0));
    order.forEach((iso, i) => (choroAt[iso] = sh.choro.t + i * sh.choro.step));
    if (sh.choro.t_last != null) choroAt[sh.choro.last] = sh.choro.t_last;
  }
  const g2009 = sh.choro ? data[sh.choro.set] || {} : {};
  const isoOf = Object.fromEntries(Object.entries(NUM).map(([k, v]) => [v, k]));
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <radialGradient id="ocean" cx="40%" cy="35%" r="75%">
            <stop offset="0%" stopColor="#16244f" />
            <stop offset="100%" stopColor="#070c22" />
          </radialGradient>
          <radialGradient id="halo" cx="50%" cy="50%" r="50%">
            <stop offset="88%" stopColor={p.acc2} stopOpacity="0.0" />
            <stop offset="96%" stopColor={p.acc2} stopOpacity="0.18" />
            <stop offset="100%" stopColor={p.acc2} stopOpacity="0" />
          </radialGradient>
        </defs>
        <circle cx={820} cy={560} r={R * 1.06} fill="url(#halo)" />
        <path d={path({type: 'Sphere'})} fill="url(#ocean)" stroke={p.acc2} strokeOpacity={0.35} strokeWidth={2} />
        <path d={path(geoGraticule10())} fill="none" stroke="#ffffff" strokeOpacity={0.05} strokeWidth={1} />
        {COUNTRIES.map((c) => {
          const iso = isoOf[c.id];
          let fill = '#22325f', op = 1;
          const base = iso && fillOf(iso);
          if (base) fill = base;
          if (iso && seqAt[iso] != null) {
            const a = ramp(T, seqAt[iso], 0.35);
            if (a > 0) fill = mix(fill, iso === 'POL' ? p.acc : p.acc2, a);
          }
          if (iso && choroAt[iso] != null) {
            const a = ramp(T, choroAt[iso], 0.3);
            const v = g2009[iso] ?? 0;
            const target = v > 0 ? '#2fe39a' : mix('#7a2232', '#ff3b55', Math.min(1, -v / (sh.choro.scale || 10)));
            if (a > 0) fill = mix(fill, target, a);
          }
          const d = path(c);
          if (!d) return null;
          return <path key={c.id} d={d} fill={fill} fillOpacity={op} stroke="#0a1230" strokeWidth={0.8} />;
        })}
        {sh.route && sh.route.t != null ? <Route sh={sh} proj={proj} p={p} T={T} /> : null}
        {(sh.flows || []).map((fl, i) => <Flow key={i} fl={fl} proj={proj} p={p} T={T} />)}
      </svg>
      {/* rótulos dos países em destaque */}
      {hl.map((iso) => {
        const c = BYNUM[NUM[iso]];
        if (!c) return null;
        const xy = proj(geoCentroid(c));
        if (!xy) return null;
        return <div key={iso} style={{position: 'absolute', left: xy[0], top: xy[1] - 20, transform: 'translate(-50%, -50%)', fontFamily: SANS, fontWeight: 900, fontSize: 34, letterSpacing: 3, color: '#0d1020', background: '#ffffffe6', padding: '4px 14px', borderRadius: 10, whiteSpace: 'nowrap'}}>{(NAME[iso] || iso).toUpperCase()}</div>;
      })}
      {(sh.cities || []).map((c, i) => {
        const xy = proj([c.lon, c.lat]);
        const a = sp(T, c.t ?? sh.t0);
        if (!xy || a <= 0.01) return null;
        const pulse = 1 + 0.3 * Math.abs(Math.sin(T * 3));
        return (
          <React.Fragment key={'c' + i}>
            <div style={{position: 'absolute', left: xy[0] - 14 * pulse, top: xy[1] - 14 * pulse, width: 28 * pulse, height: 28 * pulse, borderRadius: '50%', border: `4px solid ${p.acc}`, opacity: a}} />
            <div style={{position: 'absolute', left: xy[0] - 8, top: xy[1] - 8, width: 16, height: 16, borderRadius: '50%', background: p.acc, opacity: a}} />
            <div style={{position: 'absolute', left: xy[0] + 26, top: xy[1] - 30, fontFamily: SANS, fontWeight: 900, fontSize: 44, color: '#fff', opacity: a, textShadow: '0 4px 14px #000c'}}>{c.name}</div>
          </React.Fragment>
        );
      })}
      {sh.choro && sh.choro.t_last != null ? (() => {
        const c = BYNUM[NUM[sh.choro.last || 'POL']];
        const xy = c ? proj(geoCentroid(c)) : null;
        return xy ? <Burst x={xy[0]} y={xy[1]} T={T} t0={sh.choro.t_last} p={{...p, acc: (g2009[sh.choro.last] ?? 1) > 0 ? '#2fe39a' : '#ff3b55'}} r={150} /> : null;
      })() : null}
      {(sh.stats || []).map((st, i) => <StatCard key={i} st={st} p={p} data={data} T={T} x={120} y={640 + i * 10} small />)}
    </AbsoluteFill>
  );
};

const mix = (a, b, k) => {
  const pa = hex(a), pb = hex(b);
  return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * k)).join(',')})`;
};
const hex = (c) => {
  if (c.startsWith('rgb')) return c.match(/\d+/g).map(Number);
  const h = c.replace('#', '');
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
};

const Route = ({sh, proj, p, T}) => {
  const r = sh.route;
  const k = ramp(T, r.t, 1.6);
  const ip = geoInterpolate(r.a, r.b);
  const pts = Array.from({length: 40}, (_, i) => proj(ip((i / 39) * k))).filter(Boolean);
  const A = proj(r.a), B = proj(r.b), M = proj(ip(0.5));
  const d = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x},${y}`).join('');
  return (
    <g>
      <path d={d} fill="none" stroke="#fff" strokeWidth={6} strokeDasharray="16 12" strokeDashoffset={-T * 40} />
      {[A, B].map((q, i) => q ? <circle key={i} cx={q[0]} cy={q[1]} r={12} fill={i ? p.acc : '#fff'} /> : null)}
      {A ? <text x={A[0] - 20} y={A[1] - 24} textAnchor="end" fontFamily={SANS} fontWeight={900} fontSize={38} fill="#fff" stroke="#0d1020" strokeWidth={8} paintOrder="stroke">{r.la}</text> : null}
      {B && k > 0.95 ? <text x={B[0] + 22} y={B[1] - 24} fontFamily={SANS} fontWeight={900} fontSize={38} fill="#fff" stroke="#0d1020" strokeWidth={8} paintOrder="stroke">{r.lb}</text> : null}
      {M && k > 0.9 ? <text x={M[0]} y={M[1] + 70} textAnchor="middle" fontFamily={SANS} fontWeight={900} fontSize={54} fill="#fff" stroke="#0d1020" strokeWidth={10} paintOrder="stroke" opacity={ramp(T, r.t + 1.4, 0.4)}>{r.text}</text> : null}
    </g>
  );
};

const Flow = ({fl, proj, p, T}) => {
  if (fl.t == null) return null;
  const srcs = Array.isArray(fl.a[0]) ? fl.a : [fl.a];
  const dsts = Array.isArray(fl.b[0]) ? fl.b : [fl.b];
  return (
    <g>
      {Array.from({length: fl.n}).map((_, i) => {
        const s = srcs[i % srcs.length], d = dsts[i % dsts.length];
        const st = fl.t + (i / fl.n) * fl.dur;
        const k = interpolate(T, [st, st + 1.4], [0, 1], {...C, easing: Easing.inOut(Easing.quad)});
        if (k <= 0 || k >= 1) return null;
        const jit = [((i * 37) % 11 - 5) * 0.25, ((i * 53) % 9 - 4) * 0.2];
        const q = proj(geoInterpolate([s[0] + jit[0], s[1] + jit[1]], [d[0] + jit[1], d[1] + jit[0]])(k));
        return q ? <circle key={i} cx={q[0]} cy={q[1]} r={7} fill={p.acc} opacity={Math.sin(k * Math.PI)} /> : null;
      })}
    </g>
  );
};

// ---------------- números ----------------
const statValue = (st, data) => {
  if (st.value != null) return [st.value, null];
  const pts = ser(data, st.set, st.iso);
  return pickYear(pts, st.year).slice().reverse();
};

const StatCard = ({st, p, data, T, x, y, small, center, multi}) => {
  if (st.t == null) return null;
  const [v, yr] = statValue(st, data);
  const s = sp(T, st.t, {damping: 12, stiffness: 160});
  const out = st.t_until != null ? 1 - ramp(T, st.t_until, 0.4) : 1;
  if (s <= 0.001 || out <= 0.001) return null;
  const k = ramp(T, st.t, 1.1);
  const v0 = st.count_from ?? 0;
  const shown = v0 + (v - v0) * Easing.out(Easing.cubic)(k);
  const label = (st.label || '').replace('{year}', yr ?? '');
  const size = small ? 120 : multi ? 150 : 210;
  return (
    <div style={{position: 'absolute', left: center ? '50%' : x, top: y, transform: `${center ? 'translateX(-50%) ' : ''}scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center', opacity: Math.min(1, s * 1.5) * out, padding: small ? '20px 32px' : 0, borderRadius: 24, background: small ? '#0b1026d9' : 'transparent', border: small ? `2px solid ${p.acc}55` : 'none'}}>
      <div style={{fontFamily: SANS, fontWeight: 900, fontSize: size, lineHeight: 1, color: p.acc, letterSpacing: -size * 0.03, textShadow: '0 10px 40px rgba(0,0,0,.45)'}}>{st.prefix && v > 0 ? st.prefix : ''}{fmt(shown, st.fmt)}</div>
      <div style={{fontFamily: SANS, fontWeight: 700, fontSize: small ? 30 : multi ? 34 : 44, color: '#ffffffd0', marginTop: 10, maxWidth: multi ? 680 : 'none'}}>{label}</div>
    </div>
  );
};

const Stats = ({sh, p, data, T}) => {
  const n = (sh.stats || []).length;
  const first = sh.stats?.[0]?.t;
  const up = first != null ? ramp(T, first - 0.2, 0.6) : 0;
  return (
    <AbsoluteFill>
      <Rays p={p} T={T} t0={first} />
      {sh.title ? <div style={{position: 'absolute', left: 150, top: 470 - 290 * up, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 96 - 46 * up, color: up > 0.5 ? '#ffffffb0' : '#fff', opacity: sp(T, sh.t0 + 0.1), transform: `translateY(${(1 - sp(T, sh.t0 + 0.1)) * 30}px)`, whiteSpace: 'nowrap'}}>{sh.title}</div> : null}
      {(sh.stats || []).map((st, i) => (
        <StatCard key={i} st={st} p={p} data={data} T={T} x={n > 1 ? 150 + i * 760 : 220} y={n > 1 ? 330 : 300} multi={n > 1} />
      ))}
    </AbsoluteFill>
  );
};

const Rays = ({p, T, t0, x = 640, y = 520}) => {
  const a = t0 == null ? 0 : ramp(T, t0, 0.8);
  return <div style={{position: 'absolute', left: x - 700, top: y - 700, width: 1400, height: 1400, borderRadius: '50%', background: `repeating-conic-gradient(from ${T * 8}deg, ${p.acc}14 0deg 10deg, transparent 10deg 20deg)`, opacity: a, WebkitMaskImage: 'radial-gradient(circle, black 20%, transparent 65%)'}} />;
};

const Duel = ({sh, p, data, T, dim}) => {
  const cue = (w) => (sh.cues || []).find((c) => c.show === w);
  const vals = ['a', 'b'].map((w) => {
    const c = cue(w);
    const ex = w === 'a' ? sh.left : sh.right;
    if (ex) return {label: ex.label, color: p[ex.color] || ex.color || '#fff', v: ex.value, t: c?.t ?? (dim ? -99 : sh.t0)};
    const pt = pickYear(ser(data, sh.set, sh[w]), sh.year);
    return {iso: sh[w], v: pt[1], t: c?.t ?? (dim ? -99 : sh.t0)};
  });
  return (
    <AbsoluteFill style={{opacity: dim ? 0.3 : 1}}>
      {vals.map((d, i) => {
        const s = sp(T, d.t - 0.9);
        const k = ramp(T, d.t - 0.2, 1.0);
        const x = 300 + i * 600;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: sh.cards ? 350 : 300, width: 540, height: 520, borderRadius: 32, background: '#0b1026cc', border: `3px solid ${colOf(p, d.iso)}66`, opacity: Math.max(0.25, s), transform: `translateY(${(1 - s) * 40}px)`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 20}}>
            {d.iso ? <Flag iso={d.iso} w={170} /> : null}
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: d.iso ? 48 : 60, color: '#fff'}}>{d.iso ? NAME[d.iso] : d.label}</div>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: String(fmt(d.v, sh.fmt)).length > 7 ? 96 : 118, color: d.iso ? colOf(p, d.iso) : d.color, letterSpacing: -3, opacity: k > 0 ? 1 : 0.15}}>{k > 0 ? fmt(d.v * Easing.out(Easing.cubic)(k), sh.fmt) : '?'}</div>
          </div>
        );
      })}
      {(() => {
        const tb = vals[1].t + 0.9;
        const s = sp(T, tb);
        if (s <= 0.01 || sh.set === 'tfr' || !vals[0].v || !vals[1].v || sh.badge === false) return null;
        const r = vals[1].v / vals[0].v;
        return <div style={{position: 'absolute', left: 1440 - 170, top: 240, transform: `scale(${s}) rotate(-6deg)`, background: sh.badge ? p.warm : p.acc, color: '#0d1020', fontFamily: SANS, fontWeight: 900, fontSize: 52, padding: '10px 26px', borderRadius: 18, boxShadow: '0 12px 30px rgba(0,0,0,.4)'}}>{sh.badge || '×' + r.toFixed(1)}</div>;
      })()}
    </AbsoluteFill>
  );
};

const List = ({sh, p, T}) => (
  <AbsoluteFill>
    {(sh.items || []).map((it, i) => {
      const s = sp(T, it.t);
      if (s <= 0.001) return null;
      const y = 250 + (sh.items || []).slice(0, i).reduce((acc, q) => acc + (q.kind === 'quote' ? 190 : q.kind === 'date' ? 0 : q.kind === 'title' ? 215 : 118), 0);
      if (it.kind === 'title') {
        const shake = Math.max(0, 1 - (T - it.t) / 0.5) * Math.sin(T * 60) * 8;
        const fs = Math.min(150, Math.round(1450 / (0.62 * Math.max(1, it.text.length))));
        return <div key={i} style={{position: 'absolute', left: 760, top: Math.max(560, y + 105), transform: `translate(-50%, -50%) rotate(-5deg) scale(${1.6 - 0.6 * s}) translateX(${shake}px)`, opacity: Math.min(1, s * 2), fontFamily: SANS, fontWeight: 900, fontSize: fs, color: p.warm, letterSpacing: -4, border: `10px solid ${p.warm}`, padding: '6px 40px', borderRadius: 24, whiteSpace: 'nowrap', background: '#0b1026e6'}}>{it.text}</div>;
      }
      if (it.kind === 'date') {
        return (
          <div key={i} style={{position: 'absolute', left: 1000, top: 250, width: 300, opacity: s, transform: `translateY(${(1 - s) * -40}px) rotate(${(1 - s) * 8 + 3}deg)`, borderRadius: 26, overflow: 'hidden', background: '#fff', boxShadow: '0 20px 50px rgba(0,0,0,.5)', textAlign: 'center'}}>
            <div style={{background: p.warm, color: '#fff', fontFamily: SANS, fontWeight: 900, fontSize: 40, padding: '10px 0'}}>JANUARY</div>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 150, color: '#0d1020', lineHeight: 1.05}}>1</div>
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 46, color: '#0d1020', paddingBottom: 14}}>1990</div>
          </div>
        );
      }
      if (it.kind === 'quote') {
        return (
          <div key={i} style={{position: 'absolute', left: 150, top: y + 10, maxWidth: 1180, opacity: s, transform: `translateX(${(1 - s) * -40}px)`}}>
            <div style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 58, lineHeight: 1.1, color: '#fff'}}>{it.text}</div>
            {it.sub ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, color: p.acc, marginTop: 8, letterSpacing: 2, textTransform: 'uppercase'}}>{it.sub}</div> : null}
          </div>
        );
      }
      const strike = it.kind === 'strike' ? ramp(T, it.t + 0.45, 0.35) : 0;
      return (
        <div key={i} style={{position: 'absolute', left: 150, top: y, opacity: s, transform: `translateX(${(1 - s) * -60}px)`, display: 'flex', alignItems: 'center', gap: 22}}>
          <div style={{width: 22, height: 22, borderRadius: it.kind === 'strike' ? 4 : '50%', background: it.kind === 'strike' ? p.warm : p.acc2}} />
          <div style={{position: 'relative', fontFamily: SANS, fontWeight: 800, fontSize: 66, color: strike > 0.5 ? '#ffffff70' : '#fff', whiteSpace: 'nowrap'}}>
            {it.text}
            {strike > 0 ? <div style={{position: 'absolute', left: -6, top: '54%', height: 8, width: `calc(${strike * 100}% + 12px)`, background: p.warm, borderRadius: 4}} /> : null}
          </div>
          {strike >= 1 ? <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 34, color: p.warm, border: `4px solid ${p.warm}`, borderRadius: 10, padding: '2px 12px', transform: 'rotate(-8deg)'}}>GONE</div> : null}
        </div>
      );
    })}
  </AbsoluteFill>
);

const CardsRow = ({sh, p, T}) => {
  const cards = sh.cards || [];
  const revealT = sh.reveal?.t;
  return (
    <>
      {cards.map((c, i) => {
        const active = sh.n === i + 1;
        const visible = sh.n === 0 ? sp(T, revealT == null ? 1e9 : revealT + i * 0.25) : (i + 1 <= sh.n ? 1 : 0.35);
        if (visible <= 0.001) return null;
        return (
          <div key={i} style={{position: 'absolute', left: 150 + i * 400, top: 120, width: 370, height: 150, borderRadius: 22, padding: '18px 24px', boxSizing: 'border-box', background: active ? p.acc : '#0b1026cc', border: `2px solid ${active ? p.acc : '#ffffff22'}`, opacity: sh.n === 0 ? visible : active ? 1 : 0.45, transform: `scale(${active ? 1.04 : 1}) translateY(${(1 - Math.min(1, visible)) * 30}px)`}}>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 30, color: active ? '#0d1020' : p.acc}}>{i + 1}</div>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: c.t.length > 16 ? 32 : 40, color: active ? '#0d1020' : '#fff', lineHeight: 1.1}}>{c.t}</div>
            {c.s ? <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 24, color: active ? '#0d1020b0' : '#ffffff90'}}>{c.s}</div> : null}
          </div>
        );
      })}
    </>
  );
};

const Cards = ({sh, p, data, T}) => (
  <AbsoluteFill>
    <CardsRow sh={sh} p={p} T={T} />
    {sh.chips ? (
      <div style={{position: 'absolute', left: 168, top: 360, display: 'flex', gap: 16, flexWrap: 'wrap', width: 1600}}>
        {sh.chips.map((c, i) => (c.t == null || T < c.t - 0.05 ? null : (
          <div key={i} style={{fontFamily: SANS, fontWeight: 900, fontSize: 40, color: '#0d1020', background: i % 2 ? p.acc2 : '#ffffff', padding: '8px 18px', borderRadius: 14,
            opacity: sp(T, c.t), transform: `translateY(${(1 - sp(T, c.t)) * 14}px)`, boxShadow: '0 8px 24px rgba(0,0,0,.35)', whiteSpace: 'nowrap'}}>{c.text}</div>
        )))}
      </div>
    ) : null}
    {sh.km && sh.km.t != null ? (() => {
      const s = sp(T, sh.km.t);
      const v = sh.km.a + (sh.km.b - sh.km.a) * ramp(T, sh.km.t_b ?? 1e9, 1.6);
      const fade = sh.stat && sh.stat.t != null ? 1 - ramp(T, sh.stat.t - 0.3, 0.4) : 1;
      return (
        <div style={{position: 'absolute', left: 150, top: 500, opacity: s * fade}}>
          <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 190, color: p.acc2, letterSpacing: -5, lineHeight: 1}}>{fmt(v, 'km')}</div>
          <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 40, color: '#ffffffc0', marginTop: 12}}>{sh.km.label}</div>
          <div style={{marginTop: 28, height: 22, width: 1000, borderRadius: 11, background: '#ffffff18', overflow: 'hidden'}}>
            <div style={{height: '100%', width: `${(v / sh.km.b) * 100}%`, background: p.acc2, borderRadius: 11}} />
          </div>
        </div>
      );
    })() : null}
    {sh.stat ? <StatCard st={sh.stat} p={p} data={data} T={T} x={150} y={500} /> : null}
  </AbsoluteFill>
);

const HBars = ({sh, p, T}) => {
  const vmax = Math.max(...sh.bars.map((b) => b.value));
  return (
    <AbsoluteFill>
      <CardsRow sh={sh} p={p} T={T} />
      {sh.bars.map((b, i) => {
        const k = ramp(T, b.t, 1.2);
        const w = 900 * (b.value / vmax) * Easing.out(Easing.cubic)(k);
        return (
          <div key={i} style={{position: 'absolute', left: 150, top: 420 + i * 180, opacity: Math.min(1, k * 3)}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 12}}>
              <Flag iso={b.iso} w={70} />
              <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 40, color: '#fff'}}>{b.label}</div>
            </div>
            <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
              <div style={{width: w, height: 64, borderRadius: 14, background: colOf(p, b.iso)}} />
              <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 56, color: colOf(p, b.iso)}}>{fmt(b.value * k, 'hours')}</div>
            </div>
          </div>
        );
      })}
      {sh.kicker && sh.kicker.t != null ? <Pill x={150} y={860} text={sh.kicker.text} color={p.acc} T={T} t0={sh.kicker.t} /> : null}
      <div style={{position: 'absolute', left: 1080, top: 380, fontFamily: SANS, fontWeight: 600, fontSize: 26, color: '#ffffff80'}}>hours worked per worker, per year</div>
    </AbsoluteFill>
  );
};

const HostSay = ({sh, p, T}) => (
  <div style={{position: 'absolute', left: 140, top: 300, width: 900, display: 'flex', flexDirection: 'column', gap: 26}}>
    {(sh.items || []).map((it, i) => {
      const s = sp(T, it.t);
      if (s <= 0.001) return null;
      return <div key={i} style={{opacity: s, transform: `translateY(${(1 - s) * 30}px)`, fontFamily: it.serif ? SERIF : SANS, fontStyle: it.serif ? 'italic' : 'normal', fontWeight: it.serif ? 600 : 900, fontSize: it.size || 84, lineHeight: 1.05, color: it.color === 'acc' ? p.acc : '#fff', letterSpacing: it.serif ? 0 : -2, textShadow: '0 8px 30px rgba(0,0,0,.5)'}}>{it.text}</div>;
    })}
  </div>
);

const End = ({sh, p, data, T}) => {
  const s = sp(T, sh.t0 + 0.2);
  const nx = sh.next;
  if (nx) {
    return (
      <AbsoluteFill>
        <div style={{position: 'absolute', left: 140, top: 250, width: 820, height: 462, borderRadius: 28, background: `linear-gradient(135deg, ${p.bg1}, #0b1026)`, border: `3px solid ${p.acc}88`, opacity: s, transform: `scale(${0.9 + 0.1 * s})`, overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: 40, top: 30, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: p.acc, letterSpacing: 3}}>{nx.kicker || 'UP NEXT'}</div>
          <div style={{position: 'absolute', left: 40, top: 90, fontFamily: SANS, fontWeight: 900, fontSize: String(nx.big).length > 6 ? Math.round(1300 / String(nx.big).length) : 210, color: p[nx.color] || nx.color || p.acc, letterSpacing: -6, lineHeight: 1, whiteSpace: 'nowrap'}}>{nx.big}</div>
          <div style={{position: 'absolute', left: 44, top: 318, width: 740, display: 'flex', flexDirection: 'column', gap: 8}}>
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: String(nx.title).length > 30 ? 38 : 44, lineHeight: 1.12, color: '#fff'}}>{nx.title}</div>
            <div style={{fontFamily: SANS, fontWeight: 600, fontSize: 28, color: '#ffffff90'}}>{nx.sub}</div>
          </div>
        </div>
        <div style={{position: 'absolute', left: 140, top: 760, opacity: sp(T, sh.t0 + 0.8), fontFamily: SANS, fontWeight: 900, fontSize: 44, color: '#0d1020', background: p.warm, padding: '14px 34px', borderRadius: 40}}>{sh.cta || 'Subscribe for one chart a day'}</div>
      </AbsoluteFill>
    );
  }
  const v = valAt(ser(data, 'tfr', 'KOR'), 2024);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 140, top: 250, width: 820, height: 462, borderRadius: 28, background: `linear-gradient(135deg, ${p.bg1}, #0b1026)`, border: `3px solid ${p.acc}88`, opacity: s, transform: `scale(${0.9 + 0.1 * s})`, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 40, top: 30, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: p.acc, letterSpacing: 3}}>UP NEXT</div>
        <div style={{position: 'absolute', left: 40, top: 90, fontFamily: SANS, fontWeight: 900, fontSize: 210, color: '#ff8ad8', letterSpacing: -6, lineHeight: 1}}>{v ? v.toFixed(2) : '0.75'}</div>
        <div style={{position: 'absolute', left: 44, top: 320, fontFamily: SANS, fontWeight: 800, fontSize: 44, color: '#fff'}}>South Korea's scariest number</div>
        <div style={{position: 'absolute', left: 44, top: 380, fontFamily: SANS, fontWeight: 600, fontSize: 30, color: '#ffffff90'}}>babies per woman · lowest on Earth</div>
      </div>
      <div style={{position: 'absolute', left: 140, top: 760, opacity: sp(T, sh.t0 + 0.8), fontFamily: SANS, fontWeight: 900, fontSize: 44, color: '#0d1020', background: p.warm, padding: '14px 34px', borderRadius: 40}}>Subscribe for one chart a week</div>
    </AbsoluteFill>
  );
};

// ---------------- capítulos / marca ----------------
const Chapter = ({spec, p, T}) => {
  const firsts = spec.shots.map((s, i) => (i > 0 && s.act !== spec.shots[i - 1].act ? s : null)).filter(Boolean);
  const cur = [...firsts].reverse().find((s) => T >= s.t0 - 1.5 && T < s.t0 + 4.5);
  if (!cur) return null;
  const a = cur.act;
  const card = interpolate(T, [cur.t0 - 1.5, cur.t0 - 1.2, cur.t0 + 0.05, cur.t0 + 0.4], [0, 1, 1, 0], C);
  const tag = interpolate(T, [cur.t0 + 0.3, cur.t0 + 0.8, cur.t0 + 3.8, cur.t0 + 4.4], [0, 1, 1, 0], C);
  return (
    <>
      {card > 0 ? (
        <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${p.bg1}, ${p.bg2})`, opacity: card, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
          <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 32, letterSpacing: 10, color: p.acc}}>CHAPTER {a}</div>
          <div style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 130, color: '#fff', transform: `scale(${0.96 + 0.04 * card})`}}>{spec.acts[a]}</div>
          <div style={{width: 160 * card, height: 6, background: p.acc, borderRadius: 3, marginTop: 10}} />
        </AbsoluteFill>
      ) : null}
      {tag > 0 ? (
        <div style={{position: 'absolute', left: 120, top: 40, opacity: tag, display: 'flex', alignItems: 'baseline', gap: 14}}>
          <span style={{fontFamily: SANS, fontWeight: 800, fontSize: 24, letterSpacing: 4, color: p.acc}}>{a}</span>
          <span style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 34, color: '#ffffffd0'}}>{spec.acts[a]}</span>
        </div>
      ) : null}
    </>
  );
};

const Brand = ({p}) => (
  <div style={{position: 'absolute', right: 70, top: 46, display: 'flex', alignItems: 'center', gap: 12, opacity: 0.75}}>
    <div style={{width: 18, height: 18, borderRadius: '50%', background: p.mascot.color}} />
    <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 24, letterSpacing: 6, color: '#fff'}}>{p.tag}</div>
  </div>
);

// ---------------- apresentador 3D ----------------
const PIP = {x: 2.1, y: -2.45, s: 0.78};
const FULL = {x: 0.25, y: -0.55, s: 1.55};
const modeOf = (sh) => (sh.type === 'host' || sh.type === 'end' ? 1 : 0);

const Host = ({spec, p, f}) => {
  const T = f / FPS;
  const shots = spec.shots;
  let i = shots.findIndex((s) => T >= s.t0 && T < s.t1);
  if (i < 0) i = T < shots[0].t0 ? 0 : shots.length - 1;
  const sh = shots[i];
  const prev = shots[i - 1];
  const k = i === 0 ? 1 : spring({frame: (T - sh.t0) * FPS, fps: FPS, config: {damping: 18, stiffness: 90}});
  const m = (prev ? modeOf(prev) : modeOf(sh)) + (modeOf(sh) - (prev ? modeOf(prev) : modeOf(sh))) * k;
  const pos = {x: PIP.x + (FULL.x - PIP.x) * m, y: PIP.y + (FULL.y - PIP.y) * m, s: PIP.s + (FULL.s - PIP.s) * m};
  const reacts = (sh.react || []).filter((r) => r.t != null && r.t <= T).sort((a, b) => a.t - b.t);
  const cur = reacts[reacts.length - 1];
  const before = reacts[reacts.length - 2];
  const prevLast = prev ? (prev.react || []).filter((r) => r.t != null).sort((a, b) => a.t - b.t).slice(-1)[0] : null;
  const pose = cur ? cur.pose : 'idle';
  const prevPose = cur ? (before ? before.pose : (prevLast ? prevLast.pose : 'idle')) : (prevLast ? prevLast.pose : 'idle');
  const poseAt = Math.round((cur ? cur.t : sh.t0) * FPS);
  const leanOn = cur && cur.lean ? spring({frame: (T - cur.t) * FPS, fps: FPS, config: {damping: 20, stiffness: 80}}) : 0;
  const nods = (sh.react || []).filter((r) => r.nod && r.t != null && T >= r.t && T < r.t + 0.9);
  const nod = nods.length ? Math.sin((T - nods[0].t) * 14) * Math.exp(-(T - nods[0].t) * 3) : 0;
  const talk = Math.min(1, ((spec.env || [])[f] || 0) * 1.2);
  const look = m > 0.5 ? [Math.sin(T / 3) * 0.12, 0.05] : [-0.7, 0.2];
  const turn = -0.32 * (1 - m);
  const shadowY = pos.y - 1.12 * pos.s - 0.08;
  return (
    <div style={{position: 'absolute', left: 960, top: 0, width: 640, height: 720, transform: 'scale(1.5)', transformOrigin: '0 0'}}>
      <ThreeCanvas width={640} height={720} camera={{fov: 30, position: [0, 0, 14]}} gl={{antialias: true, alpha: true}}>
        <Lights />
        <Shadow position={[pos.x, shadowY, 0]} scale={1.3 * pos.s} opacity={0.32} />
        <Mascot {...p.mascot} pose={pose} prevPose={prevPose} poseAt={poseAt} talk={talk} look={look} enter={-30} scale={pos.s} position={[pos.x, pos.y, 0]} nod={nod} lean={leanOn} turn={turn} />
      </ThreeCanvas>
    </div>
  );
};

// ---------------- áudio ----------------
const Sfx = ({spec}) => {
  const ev = [];
  const add = (t, f, v) => t != null && ev.push({t, f, v});
  spec.shots.forEach((s, i) => {
    if (s.riser) add(s.riser.t - 2.35, 'riser', 0.32);
    if (s.cross) add(s.cross.t, 'softhit', 0.55);
    if (s.push) add(s.push.t, 'softwhoosh', 0.18);
    if (s.choro) add(s.choro.t_last, 'sparkle', 0.35);
    (s.items || []).forEach((it) => add(it.t, it.kind === 'title' ? 'softhit' : 'click', it.kind === 'title' ? 0.45 : 0.22));
    (s.labels || []).forEach((l) => add(l.t, 'tap', 0.14));
    (s.cues || []).forEach((c) => add(c.t, 'pop', 0.2));
    (s.stats || []).forEach((st) => add(st.t, 'tap', 0.2));
    if (s.stat) add(s.stat.t, 'tap', 0.2);
    if (s.bracket) add(s.bracket.t, 'softwhoosh', 0.2);
    if (i > 0 && s.act !== spec.shots[i - 1].act) add(s.t0 - 1.5, 'whoosh', 0.28);
  });
  return (
    <>
      {ev.filter((e) => e.t >= 0).map((e, i) => (
        <Sequence key={i} from={Math.round(e.t * FPS)} durationInFrames={FPS * 3}>
          <Audio src={staticFile(`audio/fx/${e.f}.wav`)} volume={e.v} />
        </Sequence>
      ))}
    </>
  );
};

const Music = ({spec}) => {
  const env = spec.env || [];
  return (
    <>
      {(spec.music || []).map((m, i) => {
        const from = Math.round(m.t * FPS);
        const dur = Math.max(1, Math.round((m.end - m.t) * FPS));
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Audio src={staticFile(`audio/music/${m.file}`)} startFrom={Math.round((m.seek || 0) * FPS)} volume={(lf) => {
              const g = from + lf;
              let e = 0;
              for (let k = -6; k <= 6; k++) e = Math.max(e, env[g + k] || 0);
              const duck = 1 - 0.5 * Math.min(1, e * 2.5);
              const fade = Math.min(1, lf / 30, (dur - lf) / 36);
              return m.vol * 2.6 * duck * Math.max(0, fade);
            }} />
          </Sequence>
        );
      })}
    </>
  );
};

// ---------------- composição ----------------
const BarsAny = (props) => (props.sh.mode === 'abs' ? <BarsAbs {...props} /> : <Bars {...props} />);
const VIEWS = {lines: Lines, bars: BarsAny, globe: Globe, stats: Stats, duel: Duel, list: List, cards: Cards, hbars: HBars, end: End, people: People, code: Code, bits: Bits, counter: Counter, radar: Radar, launch: Launch, ladder: Ladder, stack: Stack, orbit: Orbit};

const ShotView = ({sh, idx, p, data}) => {
  const f = useCurrentFrame();
  const T = sh.t0 + f / FPS;
  const dur = Math.max(0.5, sh.t1 - sh.t0);
  const k = (T - sh.t0) / dur;
  const push = sh.push && sh.push.t != null ? spring({frame: (T - sh.push.t) * FPS, fps: FPS, config: {damping: 40, stiffness: 50}}) : 0;
  const scale = 1 + (sh.slow ? 0.05 : 0.022) * k + 0.05 * push;
  const dx = Math.sin(T / 7 + idx) * 7, dy = Math.cos(T / 9 + idx) * 5;
  const isHost = sh.type === 'host';
  const View = VIEWS[isHost ? sh.bg : sh.type];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${dx}px, ${dy}px) scale(${scale})`, transformOrigin: '42% 52%'}}>
        {View ? <View sh={isHost ? {...sh, type: sh.bg, keys: null, labels: null, cues: null, react: null} : sh} p={p} data={data} T={T} dim={isHost} /> : null}
        {isHost ? <HostSay sh={sh} p={p} T={T} /> : null}
        {sh.cards && sh.type !== 'cards' && sh.type !== 'hbars' && !isHost ? <CardsRow sh={sh} p={p} T={T} /> : null}
        {sh.chips && sh.type !== 'cards' && !isHost ? (
          <div style={{position: 'absolute', left: 150, top: sh.type === 'globe' ? 880 : 950, display: 'flex', gap: 18}}>
            {sh.chips.map((c, i) => {
              const k = sp(T, c.t, {damping: 11, stiffness: 190});
              return k > 0.001 ? <div key={'ch' + i} style={{opacity: Math.min(1, k * 1.4), transform: `scale(${0.6 + 0.4 * k})`, transformOrigin: 'left center', background: i % 2 ? p.acc2 : '#ffffff', color: '#0d1020', fontFamily: SANS, fontWeight: 900, fontSize: 34, padding: '8px 18px', borderRadius: 14, whiteSpace: 'nowrap', boxShadow: '0 10px 30px rgba(0,0,0,.4)'}}>{c.text}</div> : null;
            })}
          </div>
        ) : null}
        {sh.kicker && !['bars', 'hbars', 'stack'].includes(sh.type) && !isHost && sh.kicker.t != null ? <Pill x={1300} y={175} text={sh.kicker.text} color={p.acc} T={T} t0={sh.kicker.t} align="right" /> : null}
      </AbsoluteFill>
      {sh.type === 'list' || sh.type === 'duel' ? <Kicker text={sh.title} p={p} T={T} t0={sh.t0} y={sh.cards ? 290 : 92} x={sh.cards ? 300 : 120} /> : null}
      {sh.card ? <div style={{position: 'absolute', left: 120, top: 92, fontFamily: SANS, fontWeight: 900, fontSize: 36, color: '#0d1020', background: p.acc, padding: '6px 20px', borderRadius: 12}}>{sh.card} · {['Money', 'Factories', 'People'][sh.card - 1]}</div> : null}
      <Source text={sh.src} />
    </AbsoluteFill>
  );
};

export const Long = ({spec}) => {
  useFonts();
  const f = useCurrentFrame();
  const T = f / FPS;
  const p = PAL[spec.channel] || PAL.chartbound;
  const data = spec.data || {};
  return (
    <AbsoluteFill style={{background: p.bg2}}>
      <Backdrop p={p} T={T} />
      {spec.shots.map((sh, i) => {
        const from = Math.round(sh.t0 * FPS);
        const dur = Math.max(1, Math.round(sh.t1 * FPS) - from);
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <ShotView sh={sh} idx={i} p={p} data={data} />
          </Sequence>
        );
      })}
      <Host spec={spec} p={p} f={f} />
      <Chapter spec={spec} p={p} T={T} />
      <Brand p={p} />
      <Grain T={T} />
      {(spec.tracks || []).map((tr, i) => (
        <Sequence key={'v' + i} from={Math.round(tr.t * FPS)}>
          <Audio src={staticFile(tr.file)} volume={1} />
        </Sequence>
      ))}
      <Music spec={spec} />
      <Sfx spec={spec} />
    </AbsoluteFill>
  );
};

export const longDuration = (spec) => Math.max(FPS, Math.ceil((spec.total || 60) * FPS));

// ---------------- thumbnail 1280x720 ----------------
export const Thumb = ({spec}) => {
  useFonts();
  const p = PAL[spec.channel] || PAL.chartbound;
  const data = spec.data || {};
  const th = spec.thumb;
  if (th && (th.kind === 'text' || th.kind === 'code')) {
    return (
      <AbsoluteFill style={{background: `radial-gradient(1000px 700px at 35% 55%, ${p.bg1}, ${p.bg2})`}}>
        {th.top ? <div style={{position: 'absolute', left: 60, top: 46, fontFamily: SANS, fontWeight: 900, fontSize: 76, color: '#fff', textShadow: '0 6px 0 #000a', whiteSpace: 'nowrap'}}>{th.top}</div> : null}
        {th.kind === 'code' ? (
          <div style={{position: 'absolute', left: 50, top: 170, width: 800, borderRadius: 22, overflow: 'hidden', background: '#0a0d14', border: '3px solid #ffffff30', boxShadow: '0 20px 60px rgba(0,0,0,.6)'}}>
            <div style={{height: 40, background: '#161b26', display: 'flex', gap: 10, alignItems: 'center', paddingLeft: 18}}>{['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 14, height: 14, borderRadius: '50%', background: c}} />)}</div>
            <div style={{padding: '22px 30px'}}>
              {(th.lines || []).map((l, i) => (
                <div key={i} style={{marginBottom: 10}}>
                  <div style={{fontFamily: MONO, fontWeight: 800, fontSize: 64, color: '#fff'}}><span style={{color: p.acc}}>&gt; </span>{l.in}</div>
                  {l.out ? <div style={{fontFamily: MONO, fontWeight: 800, fontSize: l.out.length > 16 ? 50 : 72, color: l.bad ? p.warm : p.acc2}}>{l.out}</div> : null}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div style={{position: 'absolute', left: 60, top: 150, fontFamily: SANS, fontWeight: 900, fontSize: 210, lineHeight: 0.9, color: p.acc, letterSpacing: -6, textShadow: '0 10px 0 #000b', whiteSpace: 'nowrap'}}>{th.big}
            <div style={{color: '#fff', fontSize: 120, letterSpacing: -3}}>{th.line2}</div></div>
        )}
        {th.sticker ? <div style={{position: 'absolute', left: th.kind === 'code' ? 90 : 70, top: th.kind === 'code' ? 560 : 560, transform: 'rotate(-5deg)', background: p.warm, color: '#fff', fontFamily: SANS, fontWeight: 900, fontSize: 64, padding: '8px 28px', borderRadius: 16, boxShadow: '0 10px 0 #000a', whiteSpace: 'nowrap'}}>{th.sticker}</div> : null}
        <div style={{position: 'absolute', left: 700, top: 40, width: 640, height: 720}}>
          <ThreeCanvas width={640} height={720} camera={{fov: 30, position: [0, 0, 14]}} gl={{antialias: true, alpha: true}}>
            <Lights />
            <Mascot {...p.mascot} pose="shock" prevPose="shock" poseAt={-60} talk={0} look={[-0.6, 0.2]} enter={-60} scale={1.9} position={[0.25, -0.85, 0]} turn={-0.25} />
          </ThreeCanvas>
        </div>
      </AbsoluteFill>
    );
  }
  if (th) {
    const pts = ser(data, th.set, th.iso).filter(([y]) => y >= th.years[0] && y <= th.years[1]);
    const vmax = th.ymax || Math.max(...pts.map((q) => q[1])) * 1.1;
    const vmin = th.ymin ?? 0;
    const [bt, bb] = th.band || [280, 680];
    const X = (y) => 60 + ((y - th.years[0]) / (th.years[1] - th.years[0])) * 700;
    const Y = (v) => bb - ((v - vmin) / (vmax - vmin)) * (bb - bt);
    const d = pts.map(([y, v], i) => `${i ? 'L' : 'M'}${X(y)},${Y(v)}`).join('');
    const last = pts[pts.length - 1];
    return (
      <AbsoluteFill style={{background: `radial-gradient(1000px 700px at 35% 55%, ${p.bg1}, ${p.bg2})`}}>
        <svg width={1280} height={720} style={{position: 'absolute'}}>
          <path d={d} fill="none" stroke={th.color || '#ff8ad8'} strokeOpacity={0.3} strokeWidth={40} strokeLinecap="round" strokeLinejoin="round" />
          <path d={d} fill="none" stroke={th.color || '#ff8ad8'} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" />
          {last ? <circle cx={X(last[0])} cy={Y(last[1])} r={28} fill="#fff" stroke={p.acc} strokeWidth={10} /> : null}
        </svg>
        <div style={{position: 'absolute', left: 60, top: 40, display: 'flex', gap: 18, alignItems: 'center'}}>
          {(th.flags || []).map((f) => <Flag key={f} iso={f} w={150} />)}
          <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 64, color: '#fff', textShadow: '0 6px 0 #000a'}}>{th.top}</div>
        </div>
        <div style={{position: 'absolute', left: 60, top: 170, fontFamily: SANS, fontWeight: 900, fontSize: 150, lineHeight: 0.92, color: p.acc, letterSpacing: -5, textShadow: '0 10px 0 #000b'}}>{th.big}<br /><span style={{color: '#fff', fontSize: 104}}>{th.line2}</span></div>
        <div style={{position: 'absolute', left: 600, top: 0, width: 640, height: 720}}>
          <ThreeCanvas width={640} height={720} camera={{fov: 30, position: [0, 0, 14]}} gl={{antialias: true, alpha: true}}>
            <Lights />
            <Mascot {...p.mascot} pose="shock" prevPose="shock" poseAt={-60} talk={0} look={[-0.6, 0.2]} enter={-60} scale={1.9} position={[0.05, -0.85, 0]} turn={-0.2} />
          </ThreeCanvas>
        </div>
      </AbsoluteFill>
    );
  }
  const A = ser(data, 'ppp', 'POL'), B = ser(data, 'ppp', 'JPN');
  const X = (y) => 60 + ((y - 1990) / 36) * 700;
  const Y = (v) => 660 - (v / 64000) * 420;
  const d = (pts) => pts.map(([y, v], i) => `${i ? 'L' : 'M'}${X(y)},${Y(v)}`).join('');
  const cr = crossPoint(A, B);
  return (
    <AbsoluteFill style={{background: `radial-gradient(1000px 700px at 35% 55%, ${p.bg1}, ${p.bg2})`}}>
      <svg width={1280} height={720} style={{position: 'absolute'}}>
        <path d={d(B)} fill="none" stroke={p.warm} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
        <path d={d(A)} fill="none" stroke={p.acc} strokeOpacity={0.3} strokeWidth={40} strokeLinecap="round" strokeLinejoin="round" />
        <path d={d(A)} fill="none" stroke={p.acc} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" />
        {cr ? <circle cx={X(cr[0])} cy={Y(cr[1])} r={30} fill="#fff" stroke={p.acc} strokeWidth={10} /> : null}
      </svg>
      <div style={{position: 'absolute', left: 60, top: 40, display: 'flex', gap: 18, alignItems: 'center'}}>
        <Flag iso="POL" w={150} />
        <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 92, color: '#fff', letterSpacing: -3, textShadow: '0 8px 0 #000a'}}>&gt;</div>
        <Flag iso="JPN" w={150} />
      </div>
      <div style={{position: 'absolute', left: 60, top: 170, fontFamily: SANS, fontWeight: 900, fontSize: 118, lineHeight: 0.95, color: p.acc, letterSpacing: -4, textShadow: '0 10px 0 #000b'}}>PASSED<br /><span style={{color: '#fff'}}>JAPAN?!</span></div>
      <div style={{position: 'absolute', left: 600, top: 0, width: 640, height: 720}}>
        <ThreeCanvas width={640} height={720} camera={{fov: 30, position: [0, 0, 14]}} gl={{antialias: true, alpha: true}}>
          <Lights />
          <Mascot {...p.mascot} pose="shock" prevPose="shock" poseAt={-60} talk={0} look={[-0.6, 0.2]} enter={-60} scale={1.9} position={[0.05, -0.85, 0]} turn={-0.2} />
        </ThreeCanvas>
      </div>
    </AbsoluteFill>
  );
};
