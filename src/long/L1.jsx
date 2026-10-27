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
const SANS = 'InterL, InterX, Inter, "Helvetica Neue", Arial, sans-serif';
const SERIF = 'LoraI, Georgia, serif';
const ramp = (T, t0, dur = 0.6) => (t0 == null ? 0 : interpolate(T, [t0, t0 + dur], [0, 1], {...C, easing: IO}));
const sp = (T, t0, cfg = {damping: 14, stiffness: 170}) => (t0 == null ? 0 : spring({frame: (T - t0) * FPS, fps: FPS, config: cfg}));
const on = (T, t0) => t0 != null && T >= t0;

const NUM = {POL: '616', DEU: '276', JPN: '392', GBR: '826', IRL: '372', ESP: '724', FRA: '250', ITA: '380', NLD: '528', BEL: '056', LUX: '442', DNK: '208', GRC: '300', PRT: '620', AUT: '040', FIN: '246', SWE: '752', CZE: '203', SVK: '703', HUN: '348', SVN: '705', EST: '233', LVA: '428', LTU: '440', CYP: '196', MLT: '470', BGR: '100', ROU: '642', HRV: '191', KOR: '410', UKR: '804', CHN: '156', RUS: '643', BLR: '112'};
const NAME = {POL: 'Poland', JPN: 'Japan', ESP: 'Spain', DEU: 'Germany', GRC: 'Greece', PRT: 'Portugal', UKR: 'Ukraine', KOR: 'South Korea', GBR: 'Britain', IRL: 'Ireland'};
const COUNTRIES = feature(world, world.objects.countries).features;
const BYNUM = Object.fromEntries(COUNTRIES.map((c) => [c.id, c]));

const colOf = (p, iso) => ({POL: p.acc, JPN: p.warm, UKR: '#4aa8ff', ESP: '#c58bff', DEU: '#8fa3c7', GRC: '#5fd3ff', PRT: p.acc2, KOR: '#ff8ad8'}[iso] || '#ffffff');

export const fmt = (v, k) => {
  if (v == null || Number.isNaN(v)) return '';
  const sg = v > 0 ? '+' : v < 0 ? '−' : '';
  switch (k) {
    case 'usdk': return '$' + (v / 1000).toFixed(1) + 'k';
    case 'usd0': return '$' + Math.round(v).toLocaleString('en-US');
    case 'pct0': return Math.round(v) + '%';
    case 'pct0s': return sg + Math.abs(Math.round(v)) + '%';
    case 'pct1s': return sg + Math.abs(v).toFixed(1) + '%';
    case 'dec2': return v.toFixed(2);
    case 'mil': return (v / 1e6).toFixed(1) + 'M';
    case 'eurb': return '€' + v.toFixed(1) + 'B';
    case 'm': return Math.round(v) + ' million';
    case 'km': return Math.round(v).toLocaleString('en-US') + ' km';
    case 'hours': return Math.round(v).toLocaleString('en-US') + ' h';
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

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const L = [['InterL', '500', 'fonts/inter500.woff2'], ['InterL', '600', 'fonts/inter600.woff2'], ['InterL', '800', 'fonts/inter800.woff2'], ['InterL', '900', 'fonts/inter900.woff2'], ['LoraI', '400 700', 'fonts/Lora-Italic-Variable.ttf']];
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
        {sh.ref ? (
          <g>
            <line x1={PL.x0} x2={PL.x1} y1={Yp(sh.ref.value)} y2={Yp(sh.ref.value)} stroke="#ffffff" strokeOpacity={0.55} strokeWidth={3} strokeDasharray="14 12" />
            <text x={PL.x1} y={Yp(sh.ref.value) - 16} textAnchor="end" fontFamily={SANS} fontWeight={700} fontSize={26} fill="#ffffffb0">{sh.ref.label}</text>
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
  const proj = geoOrthographic().scale(R).translate([820, 560]).rotate([-view.lon - (T - sh.t0) * 0.35, -view.lat]).clipAngle(90).precision(0.6);
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
            const target = v > 0 ? '#2fe39a' : mix('#7a2232', '#ff3b55', Math.min(1, -v / 10));
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
      {sh.choro && sh.choro.t_last != null ? (() => {
        const c = BYNUM[NUM.POL];
        const xy = proj(geoCentroid(c));
        return xy ? <Burst x={xy[0]} y={xy[1]} T={T} t0={sh.choro.t_last} p={{...p, acc: '#2fe39a'}} r={150} /> : null;
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

const StatCard = ({st, p, data, T, x, y, small, center}) => {
  if (st.t == null) return null;
  const [v, yr] = statValue(st, data);
  const s = sp(T, st.t, {damping: 12, stiffness: 160});
  const out = st.t_until != null ? 1 - ramp(T, st.t_until, 0.4) : 1;
  if (s <= 0.001 || out <= 0.001) return null;
  const k = ramp(T, st.t, 1.1);
  const v0 = st.count_from ?? 0;
  const shown = v0 + (v - v0) * Easing.out(Easing.cubic)(k);
  const label = (st.label || '').replace('{year}', yr ?? '');
  const size = small ? 120 : 210;
  return (
    <div style={{position: 'absolute', left: center ? '50%' : x, top: y, transform: `${center ? 'translateX(-50%) ' : ''}scale(${0.7 + 0.3 * s})`, transformOrigin: 'left center', opacity: Math.min(1, s * 1.5) * out, padding: small ? '20px 32px' : 0, borderRadius: 24, background: small ? '#0b1026d9' : 'transparent', border: small ? `2px solid ${p.acc}55` : 'none'}}>
      <div style={{fontFamily: SANS, fontWeight: 900, fontSize: size, lineHeight: 1, color: p.acc, letterSpacing: -size * 0.03, textShadow: '0 10px 40px rgba(0,0,0,.45)'}}>{st.prefix && v > 0 ? st.prefix : ''}{fmt(shown, st.fmt)}</div>
      <div style={{fontFamily: SANS, fontWeight: 700, fontSize: small ? 30 : 44, color: '#ffffffd0', marginTop: 10}}>{label}</div>
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
        <StatCard key={i} st={st} p={p} data={data} T={T} x={n > 1 ? 150 + i * 620 : 220} y={n > 1 ? 330 : 300} />
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
    const pt = pickYear(ser(data, sh.set, sh[w]), sh.year);
    const c = cue(w);
    return {iso: sh[w], v: pt[1], t: c?.t ?? (dim ? -99 : sh.t0)};
  });
  return (
    <AbsoluteFill style={{opacity: dim ? 0.3 : 1}}>
      {vals.map((d, i) => {
        const s = sp(T, d.t - 0.9);
        const k = ramp(T, d.t - 0.2, 1.0);
        const x = 300 + i * 600;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: 300, width: 540, height: 520, borderRadius: 32, background: '#0b1026cc', border: `3px solid ${colOf(p, d.iso)}66`, opacity: Math.max(0.25, s), transform: `translateY(${(1 - s) * 40}px)`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 20}}>
            <Flag iso={d.iso} w={170} />
            <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 48, color: '#fff'}}>{NAME[d.iso]}</div>
            <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 118, color: colOf(p, d.iso), letterSpacing: -3, opacity: k > 0 ? 1 : 0.15}}>{k > 0 ? fmt(d.v * Easing.out(Easing.cubic)(k), sh.fmt) : '?'}</div>
          </div>
        );
      })}
      {(() => {
        const tb = vals[1].t + 0.9;
        const s = sp(T, tb);
        if (s <= 0.01 || sh.set === 'tfr' || !vals[0].v || !vals[1].v) return null;
        const r = vals[1].v / vals[0].v;
        return <div style={{position: 'absolute', left: 1440 - 170, top: 240, transform: `scale(${s}) rotate(-6deg)`, background: p.acc, color: '#0d1020', fontFamily: SANS, fontWeight: 900, fontSize: 52, padding: '10px 26px', borderRadius: 18, boxShadow: '0 12px 30px rgba(0,0,0,.4)'}}>×{r.toFixed(1)}</div>;
      })()}
    </AbsoluteFill>
  );
};

const List = ({sh, p, T}) => (
  <AbsoluteFill>
    {(sh.items || []).map((it, i) => {
      const s = sp(T, it.t);
      if (s <= 0.001) return null;
      const y = 250 + i * 118;
      if (it.kind === 'title') {
        const shake = Math.max(0, 1 - (T - it.t) / 0.5) * Math.sin(T * 60) * 8;
        return <div key={i} style={{position: 'absolute', left: 700, top: 560, transform: `translate(-50%, -50%) rotate(-5deg) scale(${1.6 - 0.6 * s}) translateX(${shake}px)`, opacity: Math.min(1, s * 2), fontFamily: SANS, fontWeight: 900, fontSize: 150, color: p.warm, letterSpacing: -4, border: `10px solid ${p.warm}`, padding: '6px 40px', borderRadius: 24, whiteSpace: 'nowrap', background: '#0b1026e6'}}>{it.text}</div>;
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
    {(sh.chips || []).map((c, i) => <Pill key={i} x={150 + i * 290} y={390} text={c.text} color={i % 2 ? p.acc2 : '#ffffff'} T={T} t0={c.t} />)}
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
              const duck = 1 - 0.55 * Math.min(1, e * 2.5);
              const fade = Math.min(1, lf / 30, (dur - lf) / 36);
              return m.vol * 2.2 * duck * Math.max(0, fade);
            }} />
          </Sequence>
        );
      })}
    </>
  );
};

// ---------------- composição ----------------
const VIEWS = {lines: Lines, bars: Bars, globe: Globe, stats: Stats, duel: Duel, list: List, cards: Cards, hbars: HBars, end: End};

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
      </AbsoluteFill>
      {sh.type === 'list' || sh.type === 'duel' ? <Kicker text={sh.title} p={p} T={T} t0={sh.t0} /> : null}
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
