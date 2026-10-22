import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Sequence, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, delayRender, continueRender} from 'remotion';

// Estilo "promo" v2: vídeos de produto (planilhas). Arte própria em SVG (vem no spec), sem emoji,
// efeitos sonoros por evento, cena de dispositivos (deixa claro que é planilha) e encerramento.
const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const PF = 'PoppinsX, Poppins, Arial, sans-serif';
const SERIF = 'LoraX, Georgia, serif';
const GOLD = '#B8936A';

const PALS = {
  rose: {deep: '#8E4A5A', main: '#C9707D', soft: '#F3D3D8', blush: '#FBEDEF', ink: '#4A2E35', muted: '#9C7F85', g1: '#C9707D', g2: '#E8B0A8', g3: '#F6DED6', bg: '#FFF7F5'},
  lilac: {deep: '#5E4775', main: '#9479B0', soft: '#E2D7EE', blush: '#F4EFF9', ink: '#3B2C4A', muted: '#8A7B98', g1: '#7A5C96', g2: '#B298CC', g3: '#E7D6EC', bg: '#FAF7FD'},
  terra: {deep: '#7A4B3A', main: '#B5785C', soft: '#EED8CB', blush: '#F8EEE8', ink: '#4A3027', muted: '#9A7F72', g1: '#965F48', g2: '#CE987A', g3: '#F0DAC8', bg: '#FDF8F4'},
  champagne: {deep: '#7D5A4F', main: '#B98A6E', soft: '#EEDFD2', blush: '#F8F0E9', ink: '#4B352E', muted: '#9C857A', g1: '#A07060', g2: '#D6AA8C', g3: '#F4E2CD', bg: '#FDF9F4'},
  sage: {deep: '#3F5F50', main: '#6F9A84', soft: '#D5E5DB', blush: '#EEF5F0', ink: '#2C3F36', muted: '#76897F', g1: '#4F7362', g2: '#8CB29E', g3: '#D6E8DC', bg: '#F6FAF7'},
  barber: {dark: true, deep: '#232323', main: '#8C6A3F', soft: '#E6DACB', blush: '#F5F0EA', ink: '#1E1E1E', muted: '#7A746C', g1: '#1E1E1E', g2: '#463A2C', g3: '#8C6A3F', bg: '#1B1A19', text: '#F3EADF', hl: '#E6C98F', sub: '#CBBFAF'},
  sky: {deep: '#2D5B7A', main: '#4F8FBF', soft: '#D3E5F2', blush: '#EEF5FB', ink: '#1F3A4D', muted: '#6E8798', g1: '#2D5B7A', g2: '#5A96C4', g3: '#C8E2F2', bg: '#F6FAFD'},
  concurso: {deep: '#6B2236', main: '#8C2F45', soft: '#F0D5D6', blush: '#FBF1EE', ink: '#1F2433', muted: '#6F6461', g1: '#8C2F45', g2: '#C47887', g3: '#F3DCD6', bg: '#FBF7F4', navy: '#23365C'},
  classic: {deep: '#1F3A2E', main: '#2F6F55', soft: '#CFE3D8', blush: '#EEF5F1', ink: '#1E2B25', muted: '#6B7D74', g1: '#1F3A2E', g2: '#2F6F55', g3: '#78AA8C', bg: '#F5F9F6'},
};
const OK = '#3F8A62', BAD = '#C0394B', WARN = '#C98A2E', WA = '#1E8E5A';
const txt = (p) => p.text || p.ink;
const hlc = (p) => p.hl || p.main;
const subc = (p) => p.sub || p.muted;

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const list = [['PoppinsX', 'fonts/Poppins-Regular.ttf', '400', 'normal'], ['PoppinsX', 'fonts/Poppins-Medium.ttf', '500', 'normal'], ['PoppinsX', 'fonts/Poppins-Bold.ttf', '700', 'normal'], ['LoraX', 'fonts/Lora-Italic-Variable.ttf', '400 700', 'italic']];
    Promise.all(list.map(([fam, u, w, st]) => new FontFace(fam, `url(${staticFile(u)})`, {weight: w, style: st}).load().then((f) => document.fonts.add(f))))
      .then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

const Svg = ({html, style}) => <div style={style} dangerouslySetInnerHTML={{__html: html}} />;
const Sfx = ({at, src, vol = 0.4}) => (at >= 0 ? <Sequence from={Math.round(at)} durationInFrames={45}><Audio src={staticFile(`audio/fx/${src}.wav`)} volume={vol} /></Sequence> : null);

const Bg = ({p, motifs}) => {
  const f = useCurrentFrame();
  const spots = [[-70, 1270, 300, -12], [850, 1400, 240, 10], [930, 640, 200, 8]];
  return (
    <AbsoluteFill style={{background: p.dark ? 'linear-gradient(170deg,#141312 0%,#221F1C 55%,#2E2822 100%)' : `linear-gradient(170deg, ${p.bg} 0%, ${p.blush} 55%, ${p.g3} 100%)`}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', left: -380 + Math.sin(f / 80) * 40, top: -260, background: p.dark ? '#3a3128' : p.g3, filter: 'blur(90px)', opacity: p.dark ? 0.55 : 0.8}} />
      <div style={{position: 'absolute', width: 800, height: 800, borderRadius: '50%', right: -360, top: 900 + Math.cos(f / 70) * 50, background: p.dark ? '#5a4632' : p.g2, filter: 'blur(110px)', opacity: p.dark ? 0.35 : 0.4}} />
      {(motifs || []).slice(0, 3).map((m, i) => {
        const [x, y, w, r] = spots[i];
        return <Svg key={i} html={m} style={{position: 'absolute', left: x, top: y + Math.sin(f / 45 + i * 2) * 10, width: w, opacity: p.dark ? 0.35 : 0.26, transform: `rotate(${r + Math.sin(f / 60 + i) * 3}deg)`}} />;
      })}
    </AbsoluteFill>
  );
};

const TopTag = ({p, text, icon}) => (
  <div style={{position: 'absolute', top: 62, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 12, fontFamily: PF, fontWeight: 700, fontSize: 26, letterSpacing: 4, color: p.dark ? p.hl : p.deep, background: p.dark ? 'rgba(255,255,255,.06)' : 'rgba(255,255,255,.8)', border: `2px solid ${p.dark ? '#5a4632' : p.soft}`, borderRadius: 40, padding: '10px 28px'}}>
      {icon ? <Svg html={icon} style={{width: 34, height: 34}} /> : null}{text}
    </div>
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
    <div style={{position: 'absolute', left: 50, right: 50, top: sc.capsTop || 1590, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(255,255,255,.94)', borderRadius: 28, padding: '14px 22px', boxShadow: '0 10px 30px rgba(0,0,0,.10)', textAlign: 'center', fontFamily: PF, fontWeight: 700, fontSize: 54, lineHeight: 1.2, color: p.ink}}>
        {active.map((w, i) => {
          const on = t >= w.t0 && t < w.t1;
          return <span key={i} style={{display: 'inline-block', padding: '0 8px', borderRadius: 14, color: on ? '#fff' : p.ink, background: on ? (p.dark ? p.main : p.main) : 'transparent'}}>{w.w}</span>;
        })}
      </div>
    </div>
  );
};

const Title = ({text, hl, size = 100, p, delay = 0}) => {
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
          <span key={i} style={{position: 'relative', display: 'inline-block', fontFamily: t.h ? SERIF : PF, fontStyle: t.h ? 'italic' : 'normal', fontWeight: t.h ? 600 : 700, fontSize: t.h ? sz * 1.08 : sz, color: t.h ? hlc(p) : txt(p), letterSpacing: t.h ? 0 : -sz * 0.02, opacity: interpolate(s, [0, 0.5], [0, 1], C), transform: `translateY(${(1 - s) * 50}px)`}}>
            {t.w}
            {t.h ? (
              <svg style={{position: 'absolute', left: '-4%', bottom: -sz * 0.12, width: '108%', height: sz * 0.3}} viewBox="0 0 100 20" preserveAspectRatio="none">
                <path d="M2 14 C 25 4, 60 4, 98 10" stroke={p.dark ? GOLD : p.g2} strokeWidth="5" fill="none" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={dash} />
              </svg>
            ) : null}
          </span>
        );
      })}
    </div>
  );
};

const Badge = ({p, text}) => (
  <div style={{display: 'inline-flex', alignItems: 'center', gap: 12, background: p.dark ? p.main : p.deep, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 30, letterSpacing: 3, borderRadius: 40, padding: '12px 28px'}}>
    <svg width="34" height="34" viewBox="0 0 48 48" fill="none" stroke="#fff" strokeWidth="3"><rect x="6" y="6" width="36" height="36" rx="6" /><path d="M6 18 H42 M6 30 H42 M18 6 V42 M30 6 V42" /></svg>
    {text}
  </div>
);

const Hook = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 12, stiffness: 120}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: '0 60px', top: -120}}>
      {sc.art ? <Svg html={sc.art} style={{width: sc.artW || 460, marginBottom: 40, opacity: s, transform: `scale(${0.85 + 0.15 * s}) translateY(${Math.sin(f / 20) * 6}px)`}} /> : null}
      <Title text={sc.text} hl={sc.hl} size={sc.size || 104} p={p} delay={4} />
      {sc.sub ? <div style={{marginTop: 40, fontFamily: PF, fontWeight: 500, fontSize: 44, color: subc(p), textAlign: 'center', opacity: interpolate(f, [16, 28], [0, 1], C)}}>{sc.sub}</div> : null}
      {sc.badge ? <div style={{marginTop: 44, opacity: interpolate(f, [22, 32], [0, 1], C), transform: `scale(${spring({frame: f - 22, fps: FPS, config: {damping: 10}})})`}}><Badge p={p} text={sc.badge} /></div> : null}
      <Sfx at={2} src="softwhoosh" vol={0.3} />
      {sc.badge ? <Sfx at={22} src="pop" vol={0.35} /> : null}
    </AbsoluteFill>
  );
};

const fmtBRL = (v, dec = 0) => 'R$ ' + Number(v).toLocaleString('pt-BR', {minimumFractionDigits: dec, maximumFractionDigits: dec});

const badgeColor = (txt_, p) => {
  const t = String(txt_);
  if (/Abaixo|Passou|Faltou|Atrasad/.test(t)) return [BAD, '#fff'];
  if (/Pode subir|Quase|Vence/.test(t)) return ['#FCEBC4', WARN];
  if (/saudável|Tranquilo|Concluído|Em dia|Pago|Já tem/.test(t)) return ['#DDF0E3', OK];
  if (/Chamar hoje|Hoje/.test(t)) return [p.main, '#fff'];
  if (/Chamar|semana|Este mês|Aniversário/.test(t)) return [p.soft, p.deep];
  return [p.blush, p.deep];
};

const Window = ({p, sc, children, w = 1000}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 16, stiffness: 120}});
  return (
    <div style={{position: 'absolute', left: (1080 - w) / 2, width: w, top: sc.top || 330, transform: `translateY(${(1 - s) * 140}px) scale(${0.94 + 0.06 * s})`, opacity: s, background: '#fff', borderRadius: 30, boxShadow: '0 40px 80px rgba(40,20,25,.22), 0 2px 0 rgba(0,0,0,.04)', overflow: 'hidden'}}>
      <div style={{height: 56, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 12, background: '#F7F6F5', borderBottom: '2px solid #ECE9E8'}}>
        {['#E8B0A8', '#F2D7A6', '#BFD9C6'].map((c, i) => <div key={i} style={{width: 16, height: 16, borderRadius: 8, background: c}} />)}
        <svg style={{marginLeft: 14}} width="30" height="30" viewBox="0 0 48 48"><rect x="6" y="4" width="36" height="40" rx="5" fill="#2F7D53" /><path d="M12 16 H36 M12 24 H36 M12 32 H36 M22 12 V38" stroke="#fff" strokeWidth="2.6" /></svg>
        <div style={{fontFamily: PF, fontWeight: 600, fontSize: 24, color: '#5f5a5b'}}>{sc.file || 'Planilha.xlsx'}</div>
      </div>
      {sc.formula ? (
        <div style={{display: 'flex', alignItems: 'center', height: 46, borderBottom: '2px solid #ECE9E8', fontFamily: 'DejaVu Sans Mono, monospace', fontSize: 20, color: '#555'}}>
          <div style={{width: 70, textAlign: 'center', color: '#999', fontStyle: 'italic', borderRight: '2px solid #ECE9E8', fontFamily: SERIF}}>fx</div>
          <div style={{paddingLeft: 16, whiteSpace: 'nowrap', overflow: 'hidden'}}>{sc.formula.slice(0, Math.ceil(interpolate(f, [10, 40], [0, sc.formula.length], C)))}</div>
        </div>
      ) : null}
      <div style={{background: `linear-gradient(110deg, ${p.dark ? '#1d1b1a' : p.g1}, ${p.dark ? '#3a322b' : p.g2} 60%, ${p.dark ? '#5a4632' : p.g3})`, padding: '18px 30px', display: 'flex', alignItems: 'center', gap: 20}}>
        {sc.icon ? <div style={{width: 72, height: 72, borderRadius: 36, background: 'rgba(255,255,255,.9)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Svg html={sc.icon} style={{width: 44, height: 44}} /></div> : null}
        <div>
          <div style={{fontFamily: PF, fontWeight: 700, fontSize: 40, color: p.dark ? '#E6C98F' : '#fff', lineHeight: 1.1}}>{sc.sheet}</div>
          {sc.sheetSub ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 26, color: '#fff', opacity: 0.95}}>{sc.sheetSub}</div> : null}
        </div>
      </div>
      {children}
      {sc.tabs ? (
        <div style={{display: 'flex', gap: 10, padding: '14px 20px', borderTop: '2px solid #ECE9E8', background: '#F7F6F5', overflow: 'hidden'}}>
          {sc.tabs.map((t, i) => <div key={i} style={{fontFamily: PF, fontWeight: 600, fontSize: 20, padding: '7px 16px', borderRadius: 10, whiteSpace: 'nowrap', background: t === sc.sheet ? p.main : '#fff', color: t === sc.sheet ? '#fff' : '#8a8486', border: `2px solid ${t === sc.sheet ? p.main : '#E6E2E1'}`}}>{t}</div>)}
        </div>
      ) : null}
    </div>
  );
};

const Cell = ({v, kind, p, pop}) => {
  if (v === null || v === undefined || v === '') return <span />;
  if (kind === 'badge' || kind === 'link') {
    const [bg, fg] = kind === 'link' ? [WA, '#fff'] : badgeColor(v, p);
    return <span style={{display: 'inline-block', transform: `scale(${pop})`, background: bg, color: fg, borderRadius: 30, padding: '8px 18px', fontWeight: 700, fontSize: 25, whiteSpace: 'nowrap'}}>{v}</span>;
  }
  if (kind === 'money') return <span style={{fontWeight: 700, color: p.deep}}>{fmtBRL(v, Number.isInteger(v) ? 0 : 2)}</span>;
  if (kind === 'bold') return <span style={{fontWeight: 700, color: p.deep}}>{v}</span>;
  return <span>{v}</span>;
};

const LETTERS = 'ABCDEFGHIJ';

const Sheet = ({sc, p}) => {
  const f = useCurrentFrame();
  const cols = sc.cols;
  const tot = cols.reduce((n, c) => n + (c.w || 1), 0);
  const RN = 46;
  const W = 1000 - RN;
  const step = sc.step || 7;
  const focusF = sc.focus_at != null ? sc.focus_at * FPS : null;
  const sfx = [];
  sc.rows.forEach((row, ri) => {
    const t0 = 14 + ri * step;
    sfx.push(<Sfx key={'c' + ri} at={t0} src="click" vol={0.28} />);
    if (cols.some((c, ci) => (c.kind === 'badge' || c.kind === 'link') && row[ci])) sfx.push(<Sfx key={'p' + ri} at={t0 + 10} src="pop" vol={0.18} />);
  });
  return (
    <AbsoluteFill>
      {sc.text ? <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 70} p={p} /></div> : null}
      <Window p={p} sc={sc}>
        <div style={{display: 'flex', background: '#F7F6F5', borderBottom: '2px solid #ECE9E8'}}>
          <div style={{width: RN}} />
          {cols.map((c, i) => <div key={i} style={{width: (c.w || 1) / tot * W, textAlign: 'center', fontFamily: PF, fontSize: 18, color: '#a09a9b', padding: '4px 0', borderLeft: '2px solid #ECE9E8'}}>{LETTERS[i]}</div>)}
        </div>
        <div style={{display: 'flex', background: p.deep}}>
          <div style={{width: RN, background: '#F7F6F5', color: '#a09a9b', fontFamily: PF, fontSize: 18, textAlign: 'center', paddingTop: 18}}>1</div>
          {cols.map((c, i) => <div key={i} style={{width: (c.w || 1) / tot * W, padding: '16px 12px', fontFamily: PF, fontWeight: 700, fontSize: 25, color: '#fff', textAlign: c.align || 'left', whiteSpace: 'nowrap', overflow: 'hidden'}}>{c.h}</div>)}
        </div>
        {sc.rows.map((row, ri) => {
          const t0 = 14 + ri * step;
          const a = interpolate(f, [t0, t0 + 8], [0, 1], {...C, easing: Easing.out(Easing.cubic)});
          const pop = spring({frame: f - t0 - 10, fps: FPS, config: {damping: 9, stiffness: 180}});
          const focused = focusF != null && sc.focus === ri && f >= focusF;
          const fs = focused ? spring({frame: f - focusF, fps: FPS, config: {damping: 12}}) : 0;
          return (
            <div key={ri} style={{display: 'flex', alignItems: 'center', minHeight: sc.rowH || 92, background: focused ? p.soft : (ri % 2 ? p.blush : '#fff'), opacity: a, transform: `translateX(${(1 - a) * 40}px) scale(${1 + 0.025 * fs})`, boxShadow: focused ? `0 0 0 4px ${p.main} inset` : 'none', position: 'relative', zIndex: focused ? 2 : 1, borderBottom: '1.5px solid #EFEBEA'}}>
              <div style={{width: RN, alignSelf: 'stretch', background: '#F7F6F5', color: '#a09a9b', fontFamily: PF, fontSize: 18, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{ri + 2}</div>
              {row.map((v, ci) => {
                const c = cols[ci];
                const typed = c.type && typeof v === 'string' ? v.slice(0, Math.ceil(interpolate(f, [t0, t0 + 14], [0, v.length], C))) : v;
                return <div key={ci} style={{width: (c.w || 1) / tot * W, padding: '10px 12px', fontFamily: PF, fontWeight: 500, fontSize: c.fs || 29, color: p.ink, textAlign: c.align || 'left', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', borderLeft: '1.5px solid #F1EDEC'}}><Cell v={typed} kind={c.kind} p={p} pop={c.kind === 'badge' || c.kind === 'link' ? pop : 1} /></div>;
              })}
              {focused && sc.tap != null ? <Tap x={RN + cols.slice(0, sc.tap).reduce((n, c) => n + (c.w || 1) / tot * W, 0) + (cols[sc.tap].w || 1) / tot * W / 2} f={f - focusF} p={p} /> : null}
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
      {sfx}
      {focusF != null ? <Sfx at={focusF} src={sc.tap != null ? 'tap' : 'pop'} vol={0.45} /> : null}
      {sc.total ? <Sfx at={46 + sc.rows.length * step} src="cash" vol={0.3} /> : null}
    </AbsoluteFill>
  );
};

const Tap = ({x, f, p}) => {
  const r = interpolate(f % 36, [0, 30], [10, 70], C);
  const o = interpolate(f % 36, [0, 30], [0.55, 0], C);
  return (
    <>
      <div style={{position: 'absolute', left: x - r, top: '50%', marginTop: -r, width: r * 2, height: r * 2, borderRadius: '50%', background: p.main, opacity: o}} />
      <svg style={{position: 'absolute', left: x + 14, top: '50%', marginTop: 8, transform: `translateY(${Math.sin(f / 5) * 4}px)`}} width="64" height="76" viewBox="0 0 64 76">
        <path d="M22 6 c4 0 7 3 7 7 v22 l4 -1 c3 0 5 2 6 4 l2 -1 c3 0 5 2 6 4 l2 0 c4 0 7 3 7 7 v10 c0 9 -7 16 -16 16 h-8 c-6 0 -11 -3 -14 -8 l-12 -20 c-2 -3 -1 -7 2 -8 c3 -2 6 -1 8 2 l4 6 V13 c0 -4 3 -7 7 -7Z" fill="#fff" stroke="#3b3335" strokeWidth="3" strokeLinejoin="round" />
      </svg>
    </>
  );
};

const WaIcon = ({s = 40, c = '#fff'}) => (
  <svg width={s} height={s} viewBox="0 0 48 48" fill="none" stroke={c} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M9 39 l2.5-8 A15 15 0 1 1 17 37 Z" /><path d="M18 18 c0 7 5 12 12 12 l2-3 -4-2 -2 2 c-2-1-4-3-5-5 l2-2 -2-4 Z" /></svg>
);

const Chat = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f - 6, fps: FPS, config: {damping: 15, stiffness: 110}});
  const typeEnd = 26 + sc.msg.length * 0.55;
  const n = Math.ceil(interpolate(f, [26, typeEnd], [0, sc.msg.length], C));
  const sent = f > typeEnd + 4;
  const btn = spring({frame: f, fps: FPS, config: {damping: 8, stiffness: 220}});
  const clicks = [];
  for (let t = 28; t < typeEnd; t += 5) clicks.push(<Sfx key={t} at={t} src="click" vol={0.14} />);
  return (
    <AbsoluteFill>
      {sc.text ? <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={68} p={p} /></div> : null}
      <div style={{position: 'absolute', top: sc.text ? 400 : 300, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 14, background: WA, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 34, borderRadius: 40, padding: '16px 36px', transform: `scale(${0.9 + 0.1 * btn - (f > 8 && f < 14 ? 0.06 : 0)})`, boxShadow: '0 12px 30px rgba(30,142,90,.35)'}}><WaIcon s={38} />Chamar no WhatsApp</div>
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
          {sc.reply && f > typeEnd + 14 ? (
            <div style={{position: 'absolute', left: 26, top: 540, maxWidth: 560, background: '#fff', borderRadius: '6px 28px 28px 28px', padding: '22px 26px', fontFamily: PF, fontSize: 32, color: '#1d2b22', transform: `scale(${spring({frame: f - typeEnd - 14, fps: FPS, config: {damping: 12}})})`, transformOrigin: 'left top'}}>{sc.reply}</div>
          ) : null}
        </div>
      </div>
      <Sfx at={8} src="tap" vol={0.45} />
      {clicks}
      <Sfx at={typeEnd + 4} src="ding" vol={0.35} />
      {sc.reply ? <Sfx at={typeEnd + 14} src="pop" vol={0.3} /> : null}
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
            <div key={i} style={{width: 463, height: 330, background: it.hi ? p.main : '#fff', borderRadius: 36, boxShadow: '0 24px 50px rgba(40,20,25,.14)', padding: '40px 36px', boxSizing: 'border-box', opacity: s, transform: `translateY(${(1 - s) * 60}px)`}}>
              <div style={{fontFamily: PF, fontWeight: 700, fontSize: 24, letterSpacing: 2, color: it.hi ? '#fff' : p.muted, textTransform: 'uppercase'}}>{it.label}</div>
              <div style={{fontFamily: PF, fontWeight: 700, fontSize: shown.length > 9 ? 66 : 80, color: it.hi ? '#fff' : p.deep, marginTop: 30, letterSpacing: -1}}>{shown}</div>
              {it.note ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 28, color: it.hi ? '#fff' : p.muted, marginTop: 8}}>{it.note}</div> : null}
            </div>
          );
        })}
      </div>
      {sc.foot ? <div style={{position: 'absolute', top: 1270, left: 0, right: 0, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontSize: 28, color: subc(p)}}>{sc.foot}</div> : null}
      {sc.items.map((it, i) => <Sfx key={i} at={10 + i * 6} src="click" vol={0.22} />)}
      {sc.items.some((it) => it.money) ? <Sfx at={50 + (sc.items.length - 1) * 6} src="cash" vol={0.32} /> : null}
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
  const ticks = [];
  for (let d = 1; d <= days; d += 4) ticks.push(<Sfx key={d} at={12 + d * 1.6} src="click" vol={0.12} />);
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
                <div key={i} style={{height: 128, borderRadius: 18, background: bg, border: today ? `5px solid ${GOLD}` : `2px solid ${p.blush}`, boxSizing: 'border-box', padding: '8px 10px', fontFamily: PF, color: fg, transform: `scale(${0.85 + 0.15 * a})`}}>
                  <div style={{fontWeight: 700, fontSize: 26}}>{d}</div>
                  <div style={{fontWeight: 600, fontSize: sc.labels ? 19 : 20, lineHeight: 1.2, whiteSpace: 'pre-line', textAlign: 'center', marginTop: 6, opacity: a}}>{sc.labels ? sc.labels[d - 1] : (n ? `${n} ${n === 1 ? sc.unit || 'cliente' : (sc.units || 'clientes')}` : 'livre')}</div>
                </div>
              );
            })}
          </div>
        </div>
      </Window>
      {ticks}
    </AbsoluteFill>
  );
};

// notebook + celular com a planilha aberta: deixa claro que o produto é uma planilha
const Devices = ({sc, p}) => {
  const f = useCurrentFrame();
  const a = spring({frame: f - 4, fps: FPS, config: {damping: 15, stiffness: 110}});
  const b = spring({frame: f - 16, fps: FPS, config: {damping: 14, stiffness: 120}});
  const pills = sc.pills || ['Excel', 'Google Planilhas', 'Celular e computador'];
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 76} p={p} /></div>
      <div style={{position: 'absolute', left: 60, top: 470, width: 860, opacity: a, transform: `translateY(${(1 - a) * 120}px)`}}>
        <div style={{background: '#1d1d1f', borderRadius: '26px 26px 8px 8px', padding: 18}}>
          <div style={{borderRadius: 10, overflow: 'hidden', background: '#fff', height: 500}}>
            <Img src={staticFile(sc.img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top'}} />
          </div>
        </div>
        <div style={{height: 26, background: 'linear-gradient(#cfcacb,#a9a3a5)', borderRadius: '0 0 30px 30px', margin: '0 -50px'}} />
      </div>
      <div style={{position: 'absolute', left: 720, top: 780, width: 300, height: 600, borderRadius: 46, background: '#1d1d1f', padding: 12, boxShadow: '0 30px 60px rgba(0,0,0,.3)', opacity: b, transform: `translateY(${(1 - b) * 200}px) rotate(${4 * b}deg)`}}>
        <div style={{width: '100%', height: '100%', borderRadius: 36, overflow: 'hidden', background: '#fff'}}>
          <Img src={staticFile(sc.img)} style={{width: '210%', height: '100%', objectFit: 'cover', objectPosition: 'left top'}} />
        </div>
      </div>
      <div style={{position: 'absolute', left: 60, top: 1130, display: 'flex', alignItems: 'center', gap: 16, background: '#fff', borderRadius: 24, padding: '16px 24px', boxShadow: '0 16px 36px rgba(0,0,0,.12)', opacity: interpolate(f, [26, 36], [0, 1], C)}}>
        <svg width="54" height="54" viewBox="0 0 48 48"><rect x="6" y="4" width="36" height="40" rx="5" fill="#2F7D53" /><path d="M12 16 H36 M12 24 H36 M12 32 H36 M22 12 V38" stroke="#fff" strokeWidth="2.6" /></svg>
        <div style={{fontFamily: PF, fontWeight: 700, fontSize: 30, color: '#2b2b2b'}}>{sc.file}</div>
      </div>
      <div style={{position: 'absolute', left: 60, top: 1260, display: 'flex', flexWrap: 'wrap', gap: 14, width: 640}}>
        {pills.map((t, i) => <div key={i} style={{fontFamily: PF, fontWeight: 600, fontSize: 28, color: p.dark ? '#E6C98F' : p.deep, background: p.dark ? 'rgba(255,255,255,.08)' : '#fff', border: `2px solid ${p.dark ? '#5a4632' : p.soft}`, borderRadius: 30, padding: '10px 22px', opacity: interpolate(f, [34 + i * 5, 42 + i * 5], [0, 1], C)}}>{t}</div>)}
      </div>
      <Sfx at={4} src="softwhoosh" vol={0.3} />
      <Sfx at={16} src="softwhoosh" vol={0.25} />
      <Sfx at={28} src="pop" vol={0.3} />
    </AbsoluteFill>
  );
};

const Cta = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 15, stiffness: 120}});
  const pulse = 1 + 0.04 * Math.sin(f / 5);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 150, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `translateY(${Math.sin(f / 6) * 12}px)`}}>
        <svg width="90" height="90" viewBox="0 0 48 48" fill="none" stroke={p.dark ? p.hl : p.deep} strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round"><path d="M24 40 V9 M12 21 L24 9 L36 21" /></svg>
      </div>
      <div style={{position: 'absolute', top: 260, left: 0, right: 0, textAlign: 'center', fontFamily: PF, fontWeight: 700, fontSize: 44, color: p.dark ? p.hl : p.deep}}>{sc.top_text || 'WhatsApp na bio'}</div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 370, background: '#fff', borderRadius: 44, overflow: 'hidden', boxShadow: '0 40px 90px rgba(40,20,25,.22)', opacity: s, transform: `translateY(${(1 - s) * 120}px)`}}>
        <div style={{background: `linear-gradient(110deg, ${p.dark ? '#1d1b1a' : p.g1}, ${p.dark ? '#3a322b' : p.g2} 60%, ${p.dark ? '#5a4632' : p.g3})`, padding: '34px 40px', display: 'flex', alignItems: 'center', gap: 24}}>
          {sc.icon ? <div style={{flex: 'none', width: 96, height: 96, borderRadius: 48, background: 'rgba(255,255,255,.92)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Svg html={sc.icon} style={{width: 60, height: 60}} /></div> : null}
          <div>
            <div style={{fontFamily: PF, fontWeight: 700, fontSize: 22, letterSpacing: 4, color: p.dark ? '#E6C98F' : '#fff', opacity: 0.9}}>{sc.kicker || 'PLANILHA PRONTA'}</div>
            <div style={{fontFamily: PF, fontWeight: 700, fontSize: 52, color: p.dark ? '#F3EADF' : '#fff', lineHeight: 1.08}}>{sc.product}</div>
            {sc.product_sub ? <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 30, color: '#fff', marginTop: 6}}>{sc.product_sub}</div> : null}
          </div>
        </div>
        <div style={{padding: '26px 44px 36px'}}>
          {(sc.bullets || []).map((b, i) => (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, fontFamily: PF, fontWeight: 500, fontSize: 33, color: p.ink, margin: '12px 0', opacity: interpolate(f, [12 + i * 5, 20 + i * 5], [0, 1], C)}}>
              <span style={{width: 44, height: 44, borderRadius: 22, background: p.soft, color: p.deep, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 26, flex: 'none'}}>✓</span>{b}
            </div>
          ))}
          <div style={{display: 'flex', alignItems: 'baseline', gap: 18, marginTop: 22}}>
            <span style={{fontFamily: PF, fontWeight: 700, fontSize: 108, color: p.dark ? '#2b2724' : p.deep, letterSpacing: -3}}>{sc.price}</span>
          </div>
          <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 30, color: p.muted}}>{sc.price_note || 'pagamento único no Pix · arquivo na hora'}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: sc.btn_top || 1400, display: 'flex', justifyContent: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 16, transform: `scale(${pulse})`, background: WA, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 42, borderRadius: 60, padding: '24px 46px', boxShadow: '0 18px 40px rgba(30,142,90,.35)'}}><WaIcon s={46} />{sc.button || 'Chama no WhatsApp da bio'}</div>
      </div>
      <Sfx at={2} src="sparkle" vol={0.3} />
      {(sc.bullets || []).map((b, i) => <Sfx key={i} at={12 + i * 5} src="click" vol={0.16} />)}
      <Sfx at={34} src="cash" vol={0.28} />
    </AbsoluteFill>
  );
};

const End = ({sc, p}) => {
  const f = useCurrentFrame();
  const s = spring({frame: f, fps: FPS, config: {damping: 13, stiffness: 120}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', top: -80}}>
      {sc.art ? <Svg html={sc.art} style={{width: sc.artW || 300, marginBottom: 30, opacity: s}} /> : null}
      <div style={{fontFamily: PF, fontWeight: 700, fontSize: 92, color: txt(p), opacity: s, transform: `scale(${0.9 + 0.1 * s})`}}>{sc.brand || 'Vale o Preço?'}</div>
      <div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 46, color: hlc(p), marginTop: 10, opacity: interpolate(f, [8, 18], [0, 1], C)}}>{sc.line || 'planilhas prontas para o seu negócio'}</div>
      <div style={{marginTop: 50, display: 'flex', alignItems: 'center', gap: 16, background: WA, color: '#fff', fontFamily: PF, fontWeight: 700, fontSize: 40, borderRadius: 60, padding: '20px 42px', opacity: interpolate(f, [14, 24], [0, 1], C)}}><WaIcon s={44} />WhatsApp na bio</div>
      <Sfx at={0} src="sparkle" vol={0.32} />
    </AbsoluteFill>
  );
};


// Questão estilo prova: enunciado, 5 alternativas, contagem regressiva e revelação da correta.
const Quiz = ({sc, p}) => {
  const f = useCurrentFrame();
  const {durationInFrames: dq} = useVideoConfig();
  const rv = sc.revealFromEnd ? dq - Math.round(sc.revealFromEnd * FPS) : Math.round((sc.reveal || 5) * FPS);
  const cd = Math.round((sc.countdown || 3) * FPS);
  const s = spring({frame: f, fps: FPS, config: {damping: 15, stiffness: 120}});
  const revealed = f >= rv;
  const k = revealed ? spring({frame: f - rv, fps: FPS, config: {damping: 11, stiffness: 160}}) : 0;
  const left = Math.max(0, Math.ceil((rv - f) / FPS));
  const inCd = f >= rv - cd && f < rv;
  const navy = p.navy || p.deep;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 150, left: 60, right: 60, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{fontFamily: PF, fontWeight: 700, fontSize: 26, letterSpacing: 3, color: '#fff', background: navy, borderRadius: 30, padding: '10px 24px'}}>{sc.label || 'QUESTÃO ESTILO VUNESP'}</div>
        <div style={{width: 96, height: 96, borderRadius: 48, border: `6px solid ${inCd ? p.main : p.soft}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: PF, fontWeight: 700, fontSize: 48, color: inCd ? p.main : p.muted, background: '#fff', transform: `scale(${inCd ? 1 + 0.08 * Math.sin(f / 3) : 1})`}}>{revealed ? '✓' : left}</div>
      </div>
      <div style={{position: 'absolute', top: 290, left: 60, right: 60, background: '#fff', borderRadius: 36, boxShadow: '0 30px 70px rgba(40,20,25,.16)', padding: '40px 44px', opacity: s, transform: `translateY(${(1 - s) * 80}px)`}}>
        <div style={{fontFamily: PF, fontWeight: 600, fontSize: sc.qsize || 40, lineHeight: 1.3, color: p.ink}}>{sc.q}</div>
        <div style={{marginTop: 26}}>
          {sc.alts.map((a, i) => {
            const ok = i === sc.correct;
            const a0 = interpolate(f, [10 + i * 5, 18 + i * 5], [0, 1], C);
            const fade = revealed && !ok ? 1 - 0.65 * k : 1;
            return (
              <div key={i} style={{display: 'flex', alignItems: 'flex-start', gap: 20, margin: '16px 0', padding: '16px 20px', borderRadius: 22, background: revealed && ok ? OK : (p.blush), opacity: a0 * fade, transform: `scale(${revealed && ok ? 1 + 0.04 * k : 1})`, boxShadow: revealed && ok ? '0 16px 34px rgba(63,138,98,.35)' : 'none'}}>
                <span style={{flex: 'none', width: 56, height: 56, borderRadius: 28, background: revealed && ok ? '#fff' : navy, color: revealed && ok ? OK : '#fff', fontFamily: PF, fontWeight: 700, fontSize: 30, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{'ABCDE'[i]}</span>
                <span style={{fontFamily: PF, fontWeight: 500, fontSize: sc.asize || 34, lineHeight: 1.25, color: revealed && ok ? '#fff' : p.ink, paddingTop: 6}}>{a}</span>
              </div>
            );
          })}
        </div>
      </div>
      {revealed && sc.why ? <div style={{position: 'absolute', left: 70, right: 70, top: sc.whyTop || 1330, textAlign: 'center', fontFamily: SERIF, fontStyle: 'italic', fontSize: 38, color: p.deep, opacity: interpolate(f, [rv + 8, rv + 18], [0, 1], C)}}>{sc.why}</div> : null}
      {sc.alts.map((a, i) => <Sfx key={i} at={10 + i * 5} src="click" vol={0.14} />)}
      {[3, 2, 1].map((n) => <Sfx key={n} at={rv - n * FPS} src="tick" vol={0.3} />)}
      <Sfx at={rv} src="ding" vol={0.4} />
    </AbsoluteFill>
  );
};

// Páginas do PDF em leque.
const Pages = ({sc, p}) => {
  const f = useCurrentFrame();
  const imgs = sc.imgs || [];
  const n = imgs.length;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 160, left: 50, right: 50}}><Title text={sc.text} hl={sc.hl} size={sc.size || 76} p={p} /></div>
      {imgs.map((im, i) => {
        const s = spring({frame: f - 6 - i * 6, fps: FPS, config: {damping: 14, stiffness: 120}});
        const mid = (n - 1) / 2;
        const rot = (i - mid) * 7 * s;
        const x = (i - mid) * 150 * s;
        const y = Math.abs(i - mid) * 30 * s;
        return (
          <div key={i} style={{position: 'absolute', left: 540 - 250 + x, top: 470 + y + (1 - s) * 300, width: 500, height: 707, background: '#fff', borderRadius: 14, overflow: 'hidden', boxShadow: '0 30px 60px rgba(40,20,25,.25)', transform: `rotate(${rot}deg)`, transformOrigin: '50% 100%', opacity: s, zIndex: i === n - 1 ? 9 : i}}>
            <Img src={staticFile(im)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top'}} />
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1250, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 14, padding: '0 60px'}}>
        {(sc.pills || []).map((t, i) => <div key={i} style={{fontFamily: PF, fontWeight: 600, fontSize: 30, color: p.deep, background: '#fff', border: `2px solid ${p.soft}`, borderRadius: 30, padding: '10px 24px', opacity: interpolate(f, [30 + i * 5, 38 + i * 5], [0, 1], C)}}>{t}</div>)}
      </div>
      {imgs.map((im, i) => <Sfx key={i} at={6 + i * 6} src="softwhoosh" vol={0.22} />)}
      <Sfx at={30} src="pop" vol={0.3} />
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
    const ps = PALS[sc.pal] || p;
    const T = {sheet: Sheet, chat: Chat, kpis: Kpis, cal: Cal, cta: Cta, devices: Devices, end: End, quiz: Quiz, pages: Pages}[sc.type] || Hook;
    const el = (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <SceneWrap>
          <T sc={sc} p={ps} />
          <Caps sc={sc} p={p} />
        </SceneWrap>
        {sc.audio ? <Audio src={staticFile(sc.audio)} /> : null}
        {i > 0 ? <Audio src={staticFile('audio/fx/softwhoosh.wav')} volume={0.18} /> : null}
      </Sequence>
    );
    from += dur;
    return el;
  });
  const total = from;
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: p.bg}}>
      <Bg p={p} motifs={spec.motifs} />
      {parts}
      {spec.tag ? <TopTag p={p} text={spec.tag} icon={spec.tagIcon} /> : null}
      <div style={{position: 'absolute', bottom: 0, left: 0, height: 8, width: `${Math.min(f / total, 1) * 100}%`, background: p.dark ? GOLD : p.main}} />
      <Audio src={staticFile('audio/fx/music_loja.wav')} volume={0.07} loop />
    </AbsoluteFill>
  );
};
