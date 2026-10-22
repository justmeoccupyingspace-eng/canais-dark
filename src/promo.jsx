import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, delayRender, continueRender} from 'remotion';

// Estilo "promo": vídeos de produto (planilhas) com visual suave, feminino quando a paleta pede.
const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const PF = 'PoppinsX, Poppins, Arial, sans-serif';
const SERIF = 'LoraX, Georgia, serif';

const PALS = {
  rose: {deep: '#8E4A5A', main: '#C9707D', soft: '#F3D3D8', blush: '#FBEDEF', ink: '#4A2E35', muted: '#9C7F85', g1: '#C9707D', g2: '#E8B0A8', g3: '#F6DED6', bg: '#FFF7F5'},
  lilac: {deep: '#5E4775', main: '#9479B0', soft: '#E2D7EE', blush: '#F4EFF9', ink: '#3B2C4A', muted: '#8A7B98', g1: '#7A5C96', g2: '#B298CC', g3: '#E7D6EC', bg: '#FAF7FD'},
  terra: {deep: '#7A4B3A', main: '#B5785C', soft: '#EED8CB', blush: '#F8EEE8', ink: '#4A3027', muted: '#9A7F72', g1: '#965F48', g2: '#CE987A', g3: '#F0DAC8', bg: '#FDF8F4'},
  champagne: {deep: '#7D5A4F', main: '#B98A6E', soft: '#EEDFD2', blush: '#F8F0E9', ink: '#4B352E', muted: '#9C857A', g1: '#A07060', g2: '#D6AA8C', g3: '#F4E2CD', bg: '#FDF9F4'},
  sage: {deep: '#3F5F50', main: '#6F9A84', soft: '#D5E5DB', blush: '#EEF5F0', ink: '#2C3F36', muted: '#76897F', g1: '#4F7362', g2: '#8CB29E', g3: '#D6E8DC', bg: '#F6FAF7'},
  barber: {deep: '#232323', main: '#8C6A3F', soft: '#E6DACB', blush: '#F5F0EA', ink: '#1E1E1E', muted: '#7A746C', g1: '#1E1E1E', g2: '#463A2C', g3: '#8C6A3F', bg: '#F7F3EE'},
  sky: {deep: '#2D5B7A', main: '#4F8FBF', soft: '#D3E5F2', blush: '#EEF5FB', ink: '#1F3A4D', muted: '#6E8798', g1: '#2D5B7A', g2: '#5A96C4', g3: '#C8E2F2', bg: '#F6FAFD'},
  classic: {deep: '#1F3A2E', main: '#2F6F55', soft: '#CFE3D8', blush: '#EEF5F1', ink: '#1E2B25', muted: '#6B7D74', g1: '#1F3A2E', g2: '#2F6F55', g3: '#78AA8C', bg: '#F5F9F6'},
};
const OK = '#3F8A62', BAD = '#C0394B', WARN = '#C98A2E', WA = '#1E8E5A';

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const list = [['PoppinsX', 'fonts/Poppins-Regular.ttf', '400', 'normal'], ['PoppinsX', 'fonts/Poppins-Medium.ttf', '500', 'normal'], ['PoppinsX', 'fonts/Poppins-Bold.ttf', '700', 'normal'], ['LoraX', 'fonts/Lora-Italic-Variable.ttf', '400 700', 'italic']];
    Promise.all(list.map(([fam, u, w, st]) => new FontFace(fam, `url(${staticFile(u)})`, {weight: w, style: st}).load().then((f) => document.fonts.add(f))))
      .then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

const Star = ({x, y, r, color, o}) => (
  <svg style={{position: 'absolute', left: x - r, top: y - r, opacity: o}} width={r * 2} height={r * 2} viewBox="-10 -10 20 20">
    <path d="M0 -10 L2.4 -2.4 L10 0 L2.4 2.4 L0 10 L-2.4 2.4 L-10 0 L-2.4 -2.4 Z" fill={color} />
  </svg>
);

const Bg = ({p}) => {
  const f = useCurrentFrame();
  const stars = [[130, 300, 16], [960, 250, 12], [900, 1350, 18], [110, 1180, 10], [560, 140, 9], [1000, 820, 9], [70, 760, 12]];
  return (
    <AbsoluteFill style={{background: `linear-gradient(170deg, ${p.bg} 0%, ${p.blush} 55%, ${p.g3} 100%)`}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', left: -380 + Math.sin(f / 80) * 40, top: -260, background: p.g3, filter: 'blur(90px)', opacity: 0.8}} />
      <div style={{position: 'absolute', width: 800, height: 800, borderRadius: '50%', right: -360, top: 900 + Math.cos(f / 70) * 50, background: p.g2, filter: 'blur(110px)', opacity: 0.45}} />
      {stars.map(([x, y, r], i) => <Star key={i} x={x} y={y + Math.sin(f / 30 + i) * 6} r={r} color={p.main} o={0.25 + 0.35 * (0.5 + 0.5 * Math.sin(f / 18 + i * 1.7))} />)}
    </AbsoluteFill>
  );
};

const TopTag = ({p, text}) => (
  <div style={{position: 'absolute', top: 62, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
    <div style={{fontFamily: PF, fontWeight: 700, fontSize: 28, letterSpacing: 3, color: p.deep, background: 'rgba(255,255,255,.75)', border: `2px solid ${p.soft}`, borderRadius: 40, padding: '10px 30px'}}>{text}</div>
  </div>
);

const Caps = ({sc, p}) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const words = sc.words || [];
  if (!words.length || sc.nocaps) return null;
  const chunks = [];
  let cur = [];
  words.forEach((w) => {
    const len = cur.reduce((n, x) => n + x.w.length + 1, 0) + w.w.length;
    if (cur.length && (cur.length >= 4 || len > 22)) { chunks.push(cur); cur = []; }
    cur.push(w);
  });
  if (cur.length) chunks.push(cur);
  const active = chunks.find((c) => t >= c[0].t0 && t < c[c.length - 1].t1 + 0.12);
  if (!active) return null;
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: sc.capsTop || 1560, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(255,255,255,.92)', borderRadius: 28, padding: '14px 22px', boxShadow: '0 10px 30px rgba(0,0,0,.08)', textAlign: 'center', fontFamily: PF, fontWeight: 700, fontSize: 56, lineHeight: 1.2, color: p.ink}}>
        {active.map((w, i) => {
          const on = t >= w.t0 && t < w.t1;
          return <span key={i} style={{display: 'inline-block', padding: '0 8px', borderRadius: 14, color: on ? '#fff' : p.ink, background: on ? p.main : 'transparent'}}>{w.w}</span>;
        })}
      </div>
    </div>
  );
};

// título com palavra de destaque em itálico serifado e sublinhado desenhado
const Title = ({text, hl, size = 104, p, delay = 0, color}) => {
  const f = useCurrentFrame();
  const parts = hl && text.includes(hl) ? text.split(hl) : [text];
  const toks = [];
  parts.forEach((part, i) => {
    part.split(' ').filter(Boolean).forEach((w) => toks.push({w, h: false}));
    if (hl && i < parts.length - 1) toks.push({w: hl, h: true});
  });
  const longest = Math.max(...toks.map((t) => t.w.length));
  const sz = Math.min(size, 960 / (longest * 0.62));
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `0 ${sz * 0.26}px`, textAlign: 'center', lineHeight: 1.08}}>
      {toks.map((t, i) => {
        const s = spring({frame: f - delay - i * 3, fps: FPS, config: {damping: 15, stiffness: 200}});
        const dash = interpolate(f - delay - i * 3, [12, 30], [1, 0], C);
        return (
          <span key={i} style={{position: 'relative', display: 'inline-block', fontFamily: t.h ? SERIF : PF, fontStyle: t.h ? 'italic' : 'normal', fontWeight: t.h ? 600 : 700, fontSize: t.h ? sz * 1.08 : sz, color: t.h ? p.main : (color || p.ink), letterSpacing: t.h ? 0 : -sz * 0.02, opacity: interpolate(s, [0, 0.5], [0, 1], C), transform: `translateY(${(1 - s) * 50}px)`}}>
            {t.w}
            {t.h ? (
              <svg style={{position: 'absolute', left: '-4%', bottom: -sz * 0.12, width: '108%', height: sz * 0.3}} viewBox="0 0 100 20" preserveAspectRatio="none">
                <path d="M2 14 C 25 4, 60 4, 98 10" stroke={p.g2} strokeWidth="5" fill="none" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={dash} />
              </svg>
            ) : null}
          </span>
        );
      })}
    </div>
  );
};

const Hook = ({sc, p}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: '0 60px', top: -160}}>
      {sc.emoji ? <div style={{fontSize: 150, marginBottom: 30, transform: `scale(${spring({frame: f, fps: FPS, config: {damping: 10}})}) rotate(${Math.sin(f / 12) * 6}deg)`}}>{sc.emoji}</div> : null}
      <Title text={sc.text} hl={sc.hl} size={sc.size || 108} p={p} />
      {sc.sub ? <div style={{marginTop: 46, fontFamily: PF, fontWeight: 500, fontSize: 46, color: p.muted, textAlign: 'center', opacity: interpolate(f, [16, 28], [0, 1], C)}}>{sc.sub}</div> : null}
    </AbsoluteFill>
  );
};

const fmtBRL = (v, dec = 0) => 'R$ ' + Number(v).toLocaleString('pt-BR', {minimumFractionDigits: dec, maximumFractionDigits: dec});

const badgeColor = (txt, p) => {
  const t = String(txt);
  if (/Abaixo|Passou|Faltou|Atrasad/.test(t)) return [BAD, '#fff'];
  if (/Pode subir|Quase|Vence/.test(t)) return ['#FCEBC4', WARN];
  if (/saudável|Tranquilo|Concluído|Em dia|Pago|Já tem/.test(t)) return ['#DDF0E3', OK];
  if (/Chamar hoje|Hoje/.test(t)) return [p.main, '#fff'];
  if (/Chamar|semana|🎂|Este mês/.test(t)) return [p.soft, p.deep];
  return [p.blush, p.deep];
};

const Window = ({p, sc, children, w = 1000}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 16, stiffness: 120}});
  return (
    <div style={{position: 'absolute', left: (1080 - w) / 2, width: w, top: sc.top || 330, transform: `translateY(${(1 - s) * 140}px) scale(${0.94 + 0.06 * s})`, opacity: s, background: '#fff', borderRadius: 34, boxShadow: '0 40px 80px rgba(80,40,50,.18), 0 2px 0 rgba(0,0,0,.04)', overflow: 'hidden'}}>
      <div style={{height: 58, display: 'flex', alignItems: 'center', padding: '0 26px', gap: 12, background: '#FBFAFA', borderBottom: '2px solid #F1ECEC'}}>
        {[p.g2, p.soft, '#E6E1E1'].map((c, i) => <div key={i} style={{width: 18, height: 18, borderRadius: 9, background: c}} />)}
        <div style={{marginLeft: 16, fontFamily: PF, fontWeight: 500, fontSize: 24, color: p.muted}}>{sc.file || 'Planilha.xlsx'}</div>
      </div>
      <div style={{background: `linear-gradient(110deg, ${p.g1}, ${p.g2} 60%, ${p.g3})`, padding: '22px 34px', display: 'flex', alignItems: 'center', gap: 22}}>
        {sc.emoji ? <div style={{width: 78, height: 78, borderRadius: 39, background: 'rgba(255,255,255,.85)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 44}}>{sc.emoji}</div> : null}
        <div>
          <div style={{fontFamily: PF, fontWeight: 700, fontSize: 42, color: '#fff', lineHeight: 1.1}}>{sc.sheet}</div>
          {sc.sheetSub ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 27, color: '#fff', opacity: 0.95}}>{sc.sheetSub}</div> : null}
        </div>
      </div>
      {children}
      {sc.tabs ? (
        <div style={{display: 'flex', gap: 10, padding: '16px 22px', borderTop: '2px solid #F1ECEC', background: '#FBFAFA', overflow: 'hidden'}}>
          {sc.tabs.map((t, i) => <div key={i} style={{fontFamily: PF, fontWeight: 600, fontSize: 21, padding: '8px 18px', borderRadius: 14, whiteSpace: 'nowrap', background: t === sc.sheet ? p.main : '#fff', color: t === sc.sheet ? '#fff' : p.muted, border: `2px solid ${t === sc.sheet ? p.main : '#EEE6E6'}`}}>{t}</div>)}
        </div>
      ) : null}
    </div>
  );
};

const Cell = ({v, kind, p, pop, align}) => {
  if (v === null || v === undefined || v === '') return <span />;
  if (kind === 'badge' || kind === 'link') {
    const [bg, fg] = kind === 'link' ? [WA, '#fff'] : badgeColor(v, p);
    return <span style={{display: 'inline-block', transform: `scale(${pop})`, background: bg, color: fg, borderRadius: 30, padding: '8px 18px', fontWeight: 700, fontSize: 26, whiteSpace: 'nowrap'}}>{v}</span>;
  }
  if (kind === 'money') return <span style={{fontWeight: 700, color: p.deep}}>{fmtBRL(v, Number.isInteger(v) ? 0 : 2)}</span>;
  if (kind === 'bold') return <span style={{fontWeight: 700, color: p.deep}}>{v}</span>;
  return <span>{v}</span>;
};

const Sheet = ({sc, p}) => {
  const f = useCurrentFrame();
  const cols = sc.cols;
  const tot = cols.reduce((n, c) => n + (c.w || 1), 0);
  const W = 1000;
  const step = sc.step || 7;
  const focusF = sc.focus_at != null ? sc.focus_at * FPS : null;
  return (
    <AbsoluteFill>
      {sc.text ? <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 70} p={p} /></div> : null}
      <Window p={p} sc={sc}>
        <div style={{display: 'flex', background: p.deep}}>
          {cols.map((c, i) => <div key={i} style={{width: (c.w || 1) / tot * W, padding: '18px 14px', fontFamily: PF, fontWeight: 700, fontSize: 26, color: '#fff', textAlign: c.align || 'left', whiteSpace: 'nowrap', overflow: 'hidden'}}>{c.h}</div>)}
        </div>
        {sc.rows.map((row, ri) => {
          const t0 = 14 + ri * step;
          const a = interpolate(f, [t0, t0 + 8], [0, 1], {...C, easing: Easing.out(Easing.cubic)});
          const pop = spring({frame: f - t0 - 10, fps: FPS, config: {damping: 9, stiffness: 180}});
          const focused = focusF != null && sc.focus === ri && f >= focusF;
          const fs = focused ? spring({frame: f - focusF, fps: FPS, config: {damping: 12}}) : 0;
          return (
            <div key={ri} style={{display: 'flex', alignItems: 'center', minHeight: sc.rowH || 96, background: focused ? p.soft : (ri % 2 ? p.blush : '#fff'), opacity: a, transform: `translateX(${(1 - a) * 40}px) scale(${1 + 0.025 * fs})`, boxShadow: focused ? `0 0 0 4px ${p.main} inset` : 'none', position: 'relative', zIndex: focused ? 2 : 1}}>
              {row.map((v, ci) => {
                const c = cols[ci];
                const typed = c.type && typeof v === 'string' ? v.slice(0, Math.ceil(interpolate(f, [t0, t0 + 14], [0, v.length], C))) : v;
                return <div key={ci} style={{width: (c.w || 1) / tot * W, padding: '10px 12px', fontFamily: PF, fontWeight: 500, fontSize: c.fs || 30, color: p.ink, textAlign: c.align || 'left', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}><Cell v={typed} kind={c.kind} p={p} pop={c.kind === 'badge' || c.kind === 'link' ? pop : 1} /></div>;
              })}
              {focused && sc.tap != null ? <Tap x={cols.slice(0, sc.tap).reduce((n, c) => n + (c.w || 1) / tot * W, 0) + (cols[sc.tap].w || 1) / tot * W / 2} f={f - focusF} p={p} /> : null}
            </div>
          );
        })}
        {sc.total ? (
          <div style={{display: 'flex', justifyContent: 'space-between', padding: '18px 26px', background: p.soft, fontFamily: PF, fontWeight: 700, fontSize: 30, color: p.deep, opacity: interpolate(f, [14 + sc.rows.length * step, 24 + sc.rows.length * step], [0, 1], C)}}>
            <span>{sc.total[0]}</span>
            <span>{typeof sc.total[1] === 'number' ? fmtBRL(interpolate(f, [16 + sc.rows.length * step, 46 + sc.rows.length * step], [0, sc.total[1]], {...C, easing: Easing.out(Easing.cubic)})) : sc.total[1]}</span>
          </div>
        ) : null}
      </Window>
    </AbsoluteFill>
  );
};

const Tap = ({x, f, p}) => {
  const r = interpolate(f % 36, [0, 30], [10, 70], C);
  const o = interpolate(f % 36, [0, 30], [0.55, 0], C);
  return (
    <>
      <div style={{position: 'absolute', left: x - r, top: '50%', marginTop: -r, width: r * 2, height: r * 2, borderRadius: '50%', background: p.main, opacity: o}} />
      <div style={{position: 'absolute', left: x + 30, top: '50%', marginTop: 14, fontSize: 70, transform: `translateY(${Math.sin(f / 5) * 4}px)`}}>👆</div>
    </>
  );
};

const Chat = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f - 6, fps: FPS, config: {damping: 15, stiffness: 110}});
  const n = Math.ceil(interpolate(f, [26, 26 + sc.msg.length * 0.55], [0, sc.msg.length], C));
  const sent = f > 30 + sc.msg.length * 0.55;
  const btn = spring({frame: f, fps: FPS, config: {damping: 8, stiffness: 220}});
  return (
    <AbsoluteFill>
      {sc.text ? <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={68} p={p} /></div> : null}
      <div style={{position: 'absolute', top: sc.text ? 400 : 300, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <div style={{background: WA, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 34, borderRadius: 40, padding: '16px 36px', transform: `scale(${0.9 + 0.1 * btn - (f > 8 && f < 14 ? 0.06 : 0)})`, boxShadow: '0 12px 30px rgba(30,142,90,.35)'}}>💬 Chamar no WhatsApp</div>
      </div>
      <div style={{position: 'absolute', left: 150, width: 780, top: (sc.text ? 540 : 440) + (1 - s) * 400, opacity: s, height: 860, borderRadius: 70, background: '#1d1d1f', padding: 16, boxShadow: '0 40px 90px rgba(0,0,0,.25)'}}>
        <div style={{width: '100%', height: '100%', borderRadius: 56, overflow: 'hidden', background: '#EFE7DD', position: 'relative'}}>
          <div style={{height: 130, background: '#1F6E56', display: 'flex', alignItems: 'center', padding: '30px 28px 0', gap: 20}}>
            <div style={{width: 72, height: 72, borderRadius: 36, background: p.soft, color: p.deep, fontFamily: PF, fontWeight: 700, fontSize: 34, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{sc.name[0]}</div>
            <div style={{fontFamily: PF, fontWeight: 600, fontSize: 34, color: '#fff'}}>{sc.name}</div>
          </div>
          <div style={{position: 'absolute', right: 26, top: 190, maxWidth: 600, background: '#D9FDD3', borderRadius: '28px 6px 28px 28px', padding: '22px 26px 40px', fontFamily: PF, fontSize: 32, lineHeight: 1.35, color: '#1d2b22', boxShadow: '0 2px 0 rgba(0,0,0,.06)', opacity: n > 0 ? 1 : 0}}>
            {sc.msg.slice(0, n)}
            <span style={{position: 'absolute', right: 20, bottom: 10, fontSize: 22, color: sent ? '#3497F9' : '#8a9a8f'}}>{sc.time || '10:02'} ✓✓</span>
          </div>
          {sc.reply && f > 40 + sc.msg.length * 0.55 ? (
            <div style={{position: 'absolute', left: 26, top: 520, maxWidth: 560, background: '#fff', borderRadius: '6px 28px 28px 28px', padding: '22px 26px', fontFamily: PF, fontSize: 32, color: '#1d2b22', transform: `scale(${spring({frame: f - 40 - sc.msg.length * 0.55, fps: FPS, config: {damping: 12}})})`, transformOrigin: 'left top'}}>{sc.reply}</div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Kpis = ({sc, p}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 200, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 76} p={p} /></div>
      <div style={{position: 'absolute', top: 520, left: 60, right: 60, display: 'flex', flexWrap: 'wrap', gap: 34}}>
        {sc.items.map((it, i) => {
          const s = spring({frame: f - 10 - i * 6, fps: FPS, config: {damping: 14, stiffness: 140}});
          const v = interpolate(f, [14 + i * 6, 50 + i * 6], [0, it.value], {...C, easing: Easing.out(Easing.cubic)});
          const shown = it.money ? fmtBRL(v) : Math.round(v).toLocaleString('pt-BR') + (it.suffix || '');
          return (
            <div key={i} style={{width: 463, height: 330, background: it.hi ? p.main : '#fff', borderRadius: 36, boxShadow: '0 24px 50px rgba(80,40,50,.12)', padding: '40px 36px', boxSizing: 'border-box', opacity: s, transform: `translateY(${(1 - s) * 60}px)`}}>
              <div style={{fontFamily: PF, fontWeight: 700, fontSize: 24, letterSpacing: 2, color: it.hi ? '#fff' : p.muted, textTransform: 'uppercase'}}>{it.label}</div>
              <div style={{fontFamily: PF, fontWeight: 700, fontSize: shown.length > 9 ? 66 : 80, color: it.hi ? '#fff' : p.deep, marginTop: 30, letterSpacing: -1}}>{shown}</div>
              {it.note ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 28, color: it.hi ? '#fff' : p.muted, marginTop: 8}}>{it.note}</div> : null}
            </div>
          );
        })}
      </div>
      {sc.foot ? <div style={{position: 'absolute', top: 1270, left: 0, right: 0, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontSize: 28, color: p.muted}}>{sc.foot}</div> : null}
    </AbsoluteFill>
  );
};

const Cal = ({sc, p}) => {
  const f = useCurrentFrame();
  const days = sc.counts.length;
  const cells = [];
  for (let i = 0; i < sc.start; i++) cells.push(null);
  for (let d = 1; d <= days; d++) cells.push(d);
  const col = (n) => (n >= 5 ? [p.deep, '#fff'] : n >= 3 ? [p.main, '#fff'] : n >= 1 ? [p.soft, p.deep] : ['#fff', p.muted]);
  return (
    <AbsoluteFill>
      {sc.text ? <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 70} p={p} /></div> : null}
      <Window p={p} sc={{...sc, top: sc.top || 400}}>
        <div style={{padding: '18px 22px 26px'}}>
          <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 50, color: p.deep, textAlign: 'center', marginBottom: 12}}>{sc.month}</div>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 10}}>
            {['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB'].map((d) => <div key={d} style={{fontFamily: PF, fontWeight: 700, fontSize: 20, color: p.muted, textAlign: 'center'}}>{d}</div>)}
            {cells.map((d, i) => {
              if (!d) return <div key={i} />;
              const n = sc.counts[d - 1];
              const t0 = 12 + d * 1.6;
              const a = interpolate(f, [t0, t0 + 6], [0, 1], C);
              const [bg, fg] = a > 0.5 ? col(n) : ['#fff', p.muted];
              const today = sc.today === d;
              return (
                <div key={i} style={{height: 128, borderRadius: 18, background: bg, border: today ? `5px solid ${p.g2}` : `2px solid ${p.blush}`, boxSizing: 'border-box', padding: '8px 10px', fontFamily: PF, color: fg, transform: `scale(${0.85 + 0.15 * a})`}}>
                  <div style={{fontWeight: 700, fontSize: 26}}>{d}</div>
                  <div style={{fontWeight: 600, fontSize: sc.labels ? 19 : 20, lineHeight: 1.2, whiteSpace: 'pre-line', textAlign: 'center', marginTop: 6, opacity: a}}>{sc.labels ? sc.labels[d - 1] : (n ? `${n} ${n === 1 ? sc.unit || 'cliente' : (sc.units || 'clientes')}` : 'livre')}</div>
                </div>
              );
            })}
          </div>
        </div>
      </Window>
    </AbsoluteFill>
  );
};

const Cta = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 15, stiffness: 120}});
  const pulse = 1 + 0.04 * Math.sin(f / 5);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 150, left: 0, right: 0, textAlign: 'center', fontSize: 90, transform: `translateY(${Math.sin(f / 6) * 14}px)`}}>☝️</div>
      <div style={{position: 'absolute', top: 290, left: 0, right: 0, textAlign: 'center', fontFamily: PF, fontWeight: 700, fontSize: 44, color: p.deep}}>{sc.top_text || 'Link na bio'}</div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 400, background: '#fff', borderRadius: 44, overflow: 'hidden', boxShadow: '0 40px 90px rgba(80,40,50,.18)', opacity: s, transform: `translateY(${(1 - s) * 120}px)`}}>
        <div style={{background: `linear-gradient(110deg, ${p.g1}, ${p.g2} 60%, ${p.g3})`, padding: '40px 44px'}}>
          <div style={{fontFamily: PF, fontWeight: 700, fontSize: 56, color: '#fff', lineHeight: 1.1}}>{sc.emoji ? sc.emoji + ' ' : ''}{sc.product}</div>
          {sc.product_sub ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 32, color: '#fff', marginTop: 10}}>{sc.product_sub}</div> : null}
        </div>
        <div style={{padding: '30px 44px 40px'}}>
          {(sc.bullets || []).map((b, i) => (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, fontFamily: PF, fontWeight: 500, fontSize: 34, color: p.ink, margin: '14px 0', opacity: interpolate(f, [12 + i * 5, 20 + i * 5], [0, 1], C)}}>
              <span style={{width: 44, height: 44, borderRadius: 22, background: p.soft, color: p.deep, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 26, flex: 'none'}}>✓</span>{b}
            </div>
          ))}
          <div style={{display: 'flex', alignItems: 'baseline', gap: 18, marginTop: 26}}>
            {sc.old_price ? <span style={{fontFamily: PF, fontSize: 40, color: p.muted, textDecoration: 'line-through'}}>{sc.old_price}</span> : null}
            <span style={{fontFamily: PF, fontWeight: 700, fontSize: 108, color: p.deep, letterSpacing: -3}}>{sc.price}</span>
          </div>
          <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 30, color: p.muted}}>{sc.price_note || 'pagamento único no Pix · arquivo na hora'}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: sc.btn_top || 1390, display: 'flex', justifyContent: 'center'}}>
        <div style={{transform: `scale(${pulse})`, background: WA, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 42, borderRadius: 60, padding: '26px 50px', boxShadow: '0 18px 40px rgba(30,142,90,.35)'}}>{sc.button || 'Toque no link da bio 💬'}</div>
      </div>
    </AbsoluteFill>
  );
};

const SceneWrap = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  return <AbsoluteFill style={{opacity: interpolate(f, [0, 4, d - 4, d], [0, 1, 1, 0], C)}}>{children}</AbsoluteFill>;
};

export const PromoVideo = ({spec}) => {
  useFonts();
  const p = PALS[spec.pal] || PALS.rose;
  let from = 0;
  const parts = spec.scenes.map((sc, i) => {
    const dur = Math.ceil((sc.duration || 4) * FPS);
    const body = sc.type === 'sheet' ? <Sheet sc={sc} p={p} /> : sc.type === 'chat' ? <Chat sc={sc} p={p} /> : sc.type === 'kpis' ? <Kpis sc={sc} p={p} /> : sc.type === 'cal' ? <Cal sc={sc} p={p} /> : sc.type === 'cta' ? <Cta sc={sc} p={p} /> : <Hook sc={sc} p={p} />;
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <SceneWrap>
          {body}
          <Caps sc={sc} p={p} />
        </SceneWrap>
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
        <Audio src={staticFile(i === 0 ? 'audio/fx/pop.wav' : 'audio/fx/whoosh.wav')} volume={i === 0 ? 0.5 : 0.22} />
      </Sequence>
    );
    from += dur;
    return el;
  });
  const total = from;
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: p.bg}}>
      <Bg p={p} />
      {parts}
      {spec.tag ? <TopTag p={p} text={spec.tag} /> : null}
      <div style={{position: 'absolute', bottom: 0, left: 0, height: 8, width: `${Math.min(f / total, 1) * 100}%`, background: p.main}} />
      <Audio src={staticFile('audio/fx/music_loja.wav')} volume={0.08} loop />
    </AbsoluteFill>
  );
};
