import React, {useMemo} from 'react';
import * as THREE from 'three';
import {useCurrentFrame, spring, interpolate} from 'remotion';

const FPS = 30;
const C = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
export const INK = '#1d1b2e';

// gradiente de 3 tons para o toon shading (sombra / meio-tom / luz)
export const useToon = () => useMemo(() => {
  const data = new Uint8Array([90, 90, 90, 255, 170, 170, 170, 255, 255, 255, 255, 255]);
  const t = new THREE.DataTexture(data, 3, 1, THREE.RGBAFormat);
  t.minFilter = THREE.NearestFilter; t.magFilter = THREE.NearestFilter; t.needsUpdate = true;
  return t;
}, []);

// malha com contorno (casca invertida) para o visual "desenho 3D"
export const STYLE = {mat: 'toy'};
export const Toon = ({geo, color, outline = 0.035, toon, position, rotation, scale = [1, 1, 1], ink = INK, emissive, opacity = 1, rough = 0.42}) => (
  <group position={position} rotation={rotation} scale={scale}>
    <mesh geometry={geo}>
      {STYLE.mat === 'toy'
        ? <meshStandardMaterial color={color} roughness={rough} metalness={0} emissive={emissive || '#000000'} emissiveIntensity={emissive ? 0.6 : 0} transparent={opacity < 1} opacity={opacity} />
        : <meshToonMaterial color={color} gradientMap={toon} emissive={emissive || '#000000'} transparent={opacity < 1} opacity={opacity} />}
    </mesh>
    {outline > 0 && STYLE.mat !== 'toy' ? (
      <mesh geometry={geo} scale={[1 + outline / scale[0], 1 + outline / scale[1], 1 + outline / scale[2]]}>
        <meshBasicMaterial color={ink} side={THREE.BackSide} transparent={opacity < 1} opacity={opacity} />
      </mesh>
    ) : null}
  </group>
);

const POSES = {
  idle: {L: [0, 0, -0.38], R: [0, 0, 0.38]},
  wave: {L: [0, 0, -0.38], R: [0, 0, 2.55]},
  point: {L: [0, 0, -0.38], R: [0, 0, 1.5]},
  pointL: {L: [0, 0, -1.5], R: [0, 0, 0.38]},
  pointUp: {L: [0, 0, -0.38], R: [0, 0, 2.75]},
  pointUpL: {L: [0, 0, -2.75], R: [0, 0, 0.38]},
  cheer: {L: [0, 0, -2.65], R: [0, 0, 2.65]},
  shock: {L: [0, 0, -2.2], R: [0, 0, 2.2]},
  think: {L: [0, 0, -0.38], R: [0, 0, 2.2]},
  shrug: {L: [0, 0, -1.25], R: [0, 0, 1.25]},
};

// Mascote: corpo de ovo, olhos grandes com brilho, bochechas, braços de cápsula, acessório por canal.
// props: color, belly, acc ('antenna' | 'glasses' | 'cap'), pose, talk (0..1), look ([-1..1, -1..1]), enter (frame de entrada)
export const Mascot = ({color = '#ffb000', belly = '#ffe6a3', acc = 'antenna', pose = 'idle', prevPose, poseAt = 0, talk = 0, look = [0, 0], enter = 0, position = [0, 0, 0], scale = 1, mood = 'happy', accent = '#ff5d73'}) => {
  const f = useCurrentFrame();
  const toon = useToon();
  const g = useMemo(() => ({
    body: new THREE.SphereGeometry(1, 40, 32),
    eye: new THREE.SphereGeometry(0.25, 24, 18),
    pupil: new THREE.SphereGeometry(0.14, 20, 14),
    glint: new THREE.SphereGeometry(0.045, 16, 16),
    cheek: new THREE.SphereGeometry(0.13, 16, 12),
    arm: new THREE.CapsuleGeometry(0.12, 0.48, 8, 16),
    hand: new THREE.SphereGeometry(0.15, 16, 12),
    foot: new THREE.SphereGeometry(0.26, 20, 14),
    mouth: new THREE.SphereGeometry(0.16, 20, 14),
    smile: new THREE.TorusGeometry(0.17, 0.035, 12, 40, Math.PI),
    stick: new THREE.CylinderGeometry(0.035, 0.035, 0.45, 12),
    bulb: new THREE.SphereGeometry(0.11, 24, 24),
    ring: new THREE.TorusGeometry(0.31, 0.04, 12, 40),
    capTop: new THREE.BoxGeometry(1.25, 0.08, 1.25),
    capBase: new THREE.CylinderGeometry(0.52, 0.58, 0.32, 32),
    tassel: new THREE.CylinderGeometry(0.02, 0.02, 0.5, 8),
    brow: new THREE.CapsuleGeometry(0.035, 0.2, 6, 12),
    grin: new THREE.SphereGeometry(0.2, 32, 32, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2),
  }), []);

  const pop = spring({frame: f - enter, fps: FPS, config: {damping: 9, stiffness: 140}});
  const bob = Math.sin(f / 9) * 0.05;
  const squash = 1 + Math.sin(f / 9 + 1.2) * 0.025;
  const blink = ((f + 50) % 96) < 4 ? 0.12 : 1;
  const pA = POSES[prevPose] || POSES[pose] || POSES.idle;
  const pB = POSES[pose] || POSES.idle;
  const k = spring({frame: f - poseAt, fps: FPS, config: {damping: 12, stiffness: 170}});
  const lerp = (a, b) => a.map((v, i) => v + (b[i] - v) * k);
  const L = lerp(pA.L, pB.L), R = lerp(pA.R, pB.R);
  const wave = pose === 'wave' ? Math.sin(f / 4) * 0.35 : pose === 'think' ? Math.sin(f / 10) * 0.08 : 0;
  const jump = pose === 'cheer' || pose === 'shock' ? Math.abs(Math.sin(f / 7)) * 0.18 : 0;
  const lx = look[0] * 0.07, ly = look[1] * 0.06;
  const open = Math.max(0, Math.min(1, talk));
  const shock = pose === 'shock';
  // gesticula enquanto fala: braços balançam e o corpo inclina de leve
  const gest = open * Math.sin(f / 4.5) * 0.22;
  const tilt = open * Math.sin(f / 7) * 0.06;
  const s = scale * Math.max(0.001, pop);

  return (
    <group position={[position[0], position[1] + bob + jump, position[2]]} scale={[s / squash, s * squash, s]} rotation={[open * 0.05, look[0] * 0.25, tilt]}>
      {/* corpo */}
      <Toon geo={g.body} color={color} toon={toon} scale={[1, 1.1, 0.92]} outline={0.04} />
      <Toon geo={g.body} color={belly} toon={toon} position={[0, -0.42, 0.52]} scale={[0.5, 0.42, 0.42]} outline={0} />
      {/* olhos */}
      {[-1, 1].map((sd) => (
        <group key={sd} position={[sd * 0.36, 0.32, 0.76]} scale={[1, blink * (shock ? 1.15 : 1), 1]}>
          <Toon geo={g.eye} color="#ffffff" emissive="#ffffff" toon={toon} outline={0.025} rough={0.15} />
          <mesh geometry={g.pupil} position={[lx, ly, 0.17]}><meshBasicMaterial color={INK} /></mesh>
          <mesh geometry={g.glint} position={[lx + 0.055, ly + 0.065, 0.27]} scale={1.3}><meshBasicMaterial color="#ffffff" /></mesh>
        </group>
      ))}
      {/* sobrancelhas */}
      {[-1, 1].map((sd) => {
        const up = shock ? 0.1 : pose === 'cheer' ? 0.06 : pose === 'think' || pose === 'shrug' ? (sd > 0 ? 0.08 : -0.01) : 0;
        const tilt = mood === 'sad' ? sd * 0.35 : pose === 'think' ? sd * -0.2 : sd * -0.08;
        return <mesh key={sd} geometry={g.brow} position={[sd * 0.36, 0.64 + up, 0.84]} rotation={[0, 0, Math.PI / 2 + tilt]}><meshBasicMaterial color={INK} /></mesh>;
      })}
      {/* bochechas */}
      {[-1, 1].map((sd) => (
        <mesh key={sd} geometry={g.cheek} position={[sd * 0.58, 0.02, 0.72]} scale={[1, 0.6, 0.35]}><meshBasicMaterial color={accent} transparent opacity={0.55} /></mesh>
      ))}
      {/* boca: sorriso fechado ou aberta falando */}
      {pose === 'cheer' && open <= 0.15 ? (
        <mesh geometry={g.grin} position={[0, 0.02, 0.88]} scale={[1.1, 1, 0.5]}><meshBasicMaterial color="#5a1a2a" /></mesh>
      ) : open > 0.15 || shock ? (
        <mesh geometry={g.mouth} position={[0, -0.02, 0.9]} scale={[shock ? 0.9 : 0.85, shock ? 1.1 : 0.35 + open * 0.75, 0.3]}><meshBasicMaterial color="#5a1a2a" /></mesh>
      ) : (
        <mesh geometry={g.smile} position={[0, 0.04, 0.9]} rotation={[0, 0, Math.PI]} scale={[mood === 'sad' ? 1 : 1, mood === 'sad' ? -1 : 1, 1]}><meshBasicMaterial color={INK} /></mesh>
      )}
      {/* braços */}
      <group position={[-0.9, 0.0, 0.32]} rotation={[L[0], L[1], L[2] - gest]}>
        <Toon geo={g.arm} color={color} toon={toon} position={[0, -0.33, 0]} outline={0.03} />
        <Toon geo={g.hand} color={color} toon={toon} position={[0, -0.66, 0]} outline={0.03} />
      </group>
      <group position={[0.9, 0.0, 0.32]} rotation={[R[0], R[1], R[2] + wave + gest * 0.8]}>
        <Toon geo={g.arm} color={color} toon={toon} position={[0, -0.33, 0]} outline={0.03} />
        <Toon geo={g.hand} color={color} toon={toon} position={[0, -0.66, 0]} outline={0.03} />
      </group>
      {/* pés */}
      {[-1, 1].map((sd) => (
        <Toon key={sd} geo={g.foot} color={color} toon={toon} position={[sd * 0.42, -1.12, 0.2]} scale={[1, 0.55, 1.2]} outline={0.03} />
      ))}
      {/* acessórios */}
      {acc === 'antenna' ? (
        <group position={[0, 1.18, 0]} rotation={[0, 0, Math.sin(f / 11) * 0.15]}>
          <Toon geo={g.stick} color={INK} toon={toon} position={[0, 0.12, 0]} outline={0} />
          <Toon geo={g.bulb} color={accent} emissive={accent} toon={toon} position={[0, 0.4, 0]} outline={0.03} />
        </group>
      ) : null}
      {acc === 'glasses' ? (
        <group position={[0, 0.3, 0.98]}>
          {[-1, 1].map((sd) => <mesh key={sd} geometry={g.ring} position={[sd * 0.34, 0, 0]}><meshBasicMaterial color={INK} /></mesh>)}
        </group>
      ) : null}
      {acc === 'cap' ? (
        <group position={[0, 1.02, 0]} rotation={[-0.12, 0.35, 0]}>
          <Toon geo={g.capBase} color={INK} toon={toon} outline={0} />
          <Toon geo={g.capTop} color={INK} toon={toon} position={[0, 0.2, 0]} outline={0} />
          <Toon geo={g.tassel} color={accent} toon={toon} position={[0.55, -0.02, 0.4]} rotation={[0, 0, Math.sin(f / 8) * 0.2]} outline={0} />
        </group>
      ) : null}
    </group>
  );
};

// sombra suave no chão
export const Shadow = ({position = [0, -1.45, 0], scale = 1.4, opacity = 0.28}) => {
  const tex = useMemo(() => {
    const c = document.createElement('canvas'); c.width = c.height = 128;
    const x = c.getContext('2d'); const g = x.createRadialGradient(64, 64, 4, 64, 64, 64);
    g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  }, []);
  return (
    <mesh position={position} rotation={[-Math.PI / 2, 0, 0]} scale={[scale, scale * 0.5, 1]}>
      <planeGeometry args={[2, 2]} />
      <meshBasicMaterial map={tex} transparent opacity={opacity} depthWrite={false} />
    </mesh>
  );
};

export const Lights = ({rim = '#ffffff'}) => (
  <>
    <hemisphereLight args={['#fff6e8', '#5a4a6a', 1.1]} />
    <directionalLight position={[-3, 5, 6]} intensity={2.2} />
    <directionalLight position={[4, 3, -4]} intensity={1.4} color={rim} />
    <directionalLight position={[3, -1, 4]} intensity={0.35} />
  </>
);
