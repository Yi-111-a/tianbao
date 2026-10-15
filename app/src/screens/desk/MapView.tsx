// 舆图: full-bleed painted map with an SVG region overlay (hover, select, five layers),
// army tokens, the canal lifeline and the historical rebel route.
import { memo, useCallback, useEffect, useMemo, useRef, useState, type MouseEvent, type PointerEvent, type WheelEvent } from 'react';
import { useAsset, useMapData, type MapData } from '../../api/assets';
import type { Army, PublicState, ViewResponse } from '../../api/types';
import type { MapLayer } from '../../store/game';
import { cls, fmtWan, mulberry32 } from '../../lib/util';
import {
  CANAL,
  GEO_H,
  GEO_W,
  LAND_PATH,
  MOUNTAINS,
  REBEL_PATH,
  RIVERS,
  SEAT_NAMES,
  SEATS,
  schematicCells,
  smoothPath,
  toPath,
  type Pt,
} from './geo';

const FOREIGN = new Set(['tubo', 'nanzhao', 'khitan_xi', 'huihe']);
const CANAL_REGIONS = ['jiangnan', 'huainan', 'henan', 'duji', 'tongguan', 'jingji'];
const AN_OFFICES = ['fanyang', 'pinglu', 'hedong'];

interface Shape {
  id: string;
  d: string;
  seat: Pt;
  label: Pt;
  foreign?: boolean;
}

interface Geometry {
  width: number;
  height: number;
  shapes: Shape[];
  mode: 'art' | 'image-only' | 'schematic';
  scale: number;
}

function centroid(poly: number[][]): Pt {
  let x = 0;
  let y = 0;
  for (const p of poly) {
    x += p[0];
    y += p[1];
  }
  return [x / poly.length, y / poly.length];
}

function geometryFrom(map: MapData | null, hasImage: boolean, imgSize: [number, number] | null): Geometry {
  if (map) {
    const shapes: Shape[] = map.regions.map((r) => {
      const polys = r.polygons ?? (r.polygon ? [r.polygon] : []);
      const d = polys.map((p) => toPath(p as Pt[])).join(' ');
      const fallback: Pt = polys[0] ? centroid(polys[0]) : [0, 0];
      const seatRaw = r.capital ?? (Array.isArray(r.seat) ? r.seat : r.seat ? [r.seat.x, r.seat.y] : null) ?? r.center ?? r.label;
      const seat = (seatRaw as Pt | null) ?? fallback;
      const label = ((r.label ?? r.center) as Pt | undefined) ?? seat;
      return { id: r.id, d, seat, label, foreign: r.foreign };
    });
    return { width: map.width, height: map.height, shapes, mode: hasImage ? 'art' : 'schematic', scale: map.width / GEO_W };
  }
  if (hasImage && imgSize) {
    const sx = imgSize[0] / GEO_W;
    const sy = imgSize[1] / GEO_H;
    return {
      width: imgSize[0],
      height: imgSize[1],
      mode: 'image-only',
      scale: sx,
      shapes: Object.entries(SEATS).map(([id, p]) => ({ id, d: '', seat: [p[0] * sx, p[1] * sy] as Pt, label: [p[0] * sx, p[1] * sy] as Pt })),
    };
  }
  const cells = schematicCells();
  return {
    width: GEO_W,
    height: GEO_H,
    mode: 'schematic',
    scale: 1,
    shapes: Object.entries(SEATS).map(([id, seat]) => ({ id, d: cells[id], seat, label: seat })),
  };
}

// ---------------------------------------------------------------- static painted base (fallback art)
const SchematicBase = memo(function SchematicBase() {
  const peaks = useMemo(() => {
    const out: { x: number; y: number; s: number; v: number }[] = [];
    MOUNTAINS.forEach((m, mi) => {
      const r = mulberry32(100 + mi);
      for (let i = 0; i < m.n; i++) {
        out.push({
          x: m.at[0] + (r() - 0.5) * 2 * m.spread[0],
          y: m.at[1] + (r() - 0.5) * 2 * m.spread[1],
          s: m.scale * (0.75 + r() * 0.6),
          v: r(),
        });
      }
    });
    return out.sort((a, b) => a.y - b.y);
  }, []);
  const dunes = useMemo(() => {
    const r = mulberry32(77);
    return Array.from({ length: 140 }, () => [180 + r() * 380, 270 + r() * 110] as Pt);
  }, []);
  return (
    <svg className="map-base" viewBox={`0 0 ${GEO_W} ${GEO_H}`} preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <radialGradient id="mb-sea" cx="30%" cy="45%" r="90%">
          <stop offset="0%" stopColor="#5f8fa6" />
          <stop offset="60%" stopColor="#2f5d8a" />
          <stop offset="100%" stopColor="#1d3c5c" />
        </radialGradient>
        <radialGradient id="mb-land" cx="55%" cy="50%" r="70%">
          <stop offset="0%" stopColor="#e9d6a6" />
          <stop offset="70%" stopColor="#d9bf88" />
          <stop offset="100%" stopColor="#c4a46c" />
        </radialGradient>
        <linearGradient id="mb-peak" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#2f5d8a" />
          <stop offset="55%" stopColor="#3e7f6b" />
          <stop offset="100%" stopColor="#7ea889" stopOpacity="0.4" />
        </linearGradient>
        <pattern id="mb-waves" width="46" height="18" patternUnits="userSpaceOnUse">
          <path d="M0 12 q 11.5 -9 23 0 t 23 0" fill="none" stroke="#bcd3d4" strokeOpacity="0.28" strokeWidth="1.2" />
        </pattern>
        <filter id="mb-silk" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.9 0.02" numOctaves="2" seed="4" result="f" />
          <feColorMatrix in="f" values="0 0 0 0 0.45  0 0 0 0 0.33  0 0 0 0 0.16  0 0 0 0.16 0" />
          <feComposite in2="SourceGraphic" operator="in" />
        </filter>
        <filter id="mb-blot" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="9" />
          <feColorMatrix values="0 0 0 0 0.42  0 0 0 0 0.28  0 0 0 0 0.12  0 0 0 0.35 0" />
          <feComposite in2="SourceGraphic" operator="in" />
        </filter>
        <clipPath id="mb-landclip">
          <path d={LAND_PATH} />
        </clipPath>
      </defs>
      <rect width={GEO_W} height={GEO_H} fill="url(#mb-sea)" />
      <rect width={GEO_W} height={GEO_H} fill="url(#mb-waves)" />
      {/* coastal bands */}
      <path d={LAND_PATH} fill="none" stroke="#9cc3bf" strokeOpacity="0.35" strokeWidth="26" />
      <path d={LAND_PATH} fill="none" stroke="#d6e4d8" strokeOpacity="0.35" strokeWidth="12" />
      <path d={LAND_PATH} fill="url(#mb-land)" />
      <g clipPath="url(#mb-landclip)">
        <rect width={GEO_W} height={GEO_H} fill="#000" filter="url(#mb-blot)" />
        {/* west: Tarim sands */}
        {dunes.map((p, i) => (
          <circle key={i} cx={p[0]} cy={p[1]} r={1.3} fill="#9a7442" opacity={0.45} />
        ))}
        {/* plateau wash */}
        <ellipse cx={380} cy={760} rx={330} ry={170} fill="#7c9a8a" opacity={0.18} />
        <ellipse cx={1140} cy={150} rx={300} ry={90} fill="#8aa07b" opacity={0.12} />
        {RIVERS.map((r) => (
          <g key={r.id}>
            <path d={smoothPath(r.pts)} fill="none" stroke="#3a6f8f" strokeOpacity="0.65" strokeWidth={r.width + 2.5} strokeLinecap="round" />
            <path d={smoothPath(r.pts)} fill="none" stroke="#9cc6d0" strokeOpacity="0.9" strokeWidth={r.width * 0.55} strokeLinecap="round" />
          </g>
        ))}
        {peaks.map((p, i) => (
          <g key={i} transform={`translate(${p.x} ${p.y}) scale(${p.s})`}>
            <path d="M-34 14 C -22 -6, -14 -26, -4 -30 C 4 -22, 12 -6, 22 2 C 26 -6, 30 -12, 34 -12 C 40 -4, 44 6, 48 14 Z" fill="url(#mb-peak)" opacity={0.78 + p.v * 0.2} />
            <path d="M-34 14 C -22 -6, -14 -26, -4 -30 C 4 -22, 12 -6, 22 2 C 26 -6, 30 -12, 34 -12 C 40 -4, 44 6, 48 14" fill="none" stroke="#1f2f2a" strokeOpacity="0.55" strokeWidth={1.4} />
            <path d="M-4 -30 C -8 -16, -12 -4, -18 8 M34 -12 C 32 -4, 30 4, 26 12" fill="none" stroke="#f3ead2" strokeOpacity="0.55" strokeWidth={1.2} />
          </g>
        ))}
        <rect width={GEO_W} height={GEO_H} fill="#fff" opacity="0.001" filter="url(#mb-silk)" />
      </g>
      <path d={LAND_PATH} fill="none" stroke="#2b3d39" strokeOpacity="0.55" strokeWidth="1.6" />
    </svg>
  );
});

// ---------------------------------------------------------------- dynamic overlay
function layerFill(layer: MapLayer, id: string, state: PublicState, crisis: number, armiesBy: Record<string, Army[]>): { fill: string; opacity: number } {
  const region = state.regions[id];
  const controller = region?.controller ?? (FOREIGN.has(id) ? id : 'tang');
  if (controller === 'yan') return { fill: 'var(--zhusha)', opacity: 0.5 };
  if (FOREIGN.has(id)) return { fill: '#5b5148', opacity: 0.18 };
  const anHolds = (rid: string) => {
    if (rid === 'hedong' && state.flags?.hedong_to_an) return true;
    const office = state.offices?.[`${rid}_jds`];
    return office?.holder === 'an_lushan';
  };
  switch (layer) {
    case 'jurisdiction': {
      if (AN_OFFICES.includes(id) && anHolds(id)) return { fill: 'var(--shilv)', opacity: 0.32 + Math.min(0.25, crisis / 300) };
      if (id === 'jingji' || id === 'duji' || id === 'tongguan') return { fill: 'var(--nijin)', opacity: 0.28 };
      if (state.offices?.[`${id}_jds`]) return { fill: 'var(--zheshi)', opacity: 0.2 };
      return { fill: '#f3e6c4', opacity: 0.1 };
    }
    case 'morale': {
      const order = region?.stats?.order ?? 60;
      const t = Math.max(0, Math.min(1, (order - 30) / 50));
      const fill = t < 0.5 ? 'var(--zhusha)' : t < 0.75 ? 'var(--nijin)' : 'var(--shilv)';
      return { fill, opacity: 0.18 + Math.abs(t - 0.6) * 0.45 };
    }
    case 'troops': {
      const total = (armiesBy[id] ?? []).reduce((a, x) => a + x.strength, 0);
      return { fill: 'var(--shiqing)', opacity: total ? Math.min(0.42, 0.05 + total / 260000) : 0.02 };
    }
    case 'canal': {
      if (!CANAL_REGIONS.includes(id)) return { fill: '#3d342b', opacity: 0.16 };
      return { fill: 'var(--nijin)', opacity: 0.34 };
    }
    case 'beacon': {
      const idx = REBEL_PATH.indexOf(id);
      if (idx < 0 && id !== 'pinglu') return { fill: '#3d342b', opacity: 0.12 };
      const heat = Math.max(0, crisis - 20) / 80;
      return { fill: 'var(--zhusha)', opacity: 0.12 + heat * (idx <= 1 || id === 'pinglu' ? 0.5 : 0.3) };
    }
  }
}

export function MapView({
  view,
  layer,
  selected,
  onSelect,
}: {
  view: ViewResponse;
  layer: MapLayer;
  selected: string | null;
  onSelect: (id: string | null) => void;
}) {
  const [mapData, mapSettled] = useMapData();
  const [baseUrl, baseSettled] = useAsset(['map.base', 'ui.map.base', 'map.base.default']);
  const [imgSize, setImgSize] = useState<[number, number] | null>(null);
  const tipRef = useRef<HTMLDivElement>(null);
  const [hover, setHover] = useState<string | null>(null);
  const state = view.state;
  const crisisValue = Array.isArray(view.crisis.value_or_estimate)
    ? (view.crisis.value_or_estimate[0] + view.crisis.value_or_estimate[1]) / 2
    : view.crisis.value_or_estimate;
  const rebelled = Boolean(state.flags?.rebellion_started);

  const geo = useMemo(() => geometryFrom(mapData, Boolean(baseUrl), imgSize), [mapData, baseUrl, imgSize]);
  const k = geo.scale;
  const armiesBy = useMemo(() => {
    const out: Record<string, Army[]> = {};
    for (const a of Object.values(state.armies ?? {})) {
      if (a.strength <= 0) continue;
      (out[a.region] ??= []).push(a);
    }
    return out;
  }, [state.armies]);
  const seatOf = useMemo(() => Object.fromEntries(geo.shapes.map((s) => [s.id, s.seat])), [geo]);
  const ready = mapSettled && baseSettled && (!baseUrl || mapData || imgSize);

  // ---- pan & zoom (drag to pan, wheel to zoom); the map always covers the viewport
  const rootRef = useRef<HTMLDivElement>(null);
  const [box, setBox] = useState<{ w: number; h: number }>({ w: 0, h: 0 });
  const [tf, setTf] = useState<{ s: number; x: number; y: number; key: string } | null>(null);
  const geoKey = `${geo.width}x${geo.height}`;
  const drag = useRef<{ x: number; y: number; tx: number; ty: number; moved: boolean } | null>(null);
  const suppressClick = useRef(false);
  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setBox({ w: el.clientWidth, h: el.clientHeight }));
    ro.observe(el);
    setBox({ w: el.clientWidth, h: el.clientHeight });
    return () => ro.disconnect();
  }, []);
  const cover = box.w && box.h ? Math.max(box.w / geo.width, box.h / geo.height) : 1;
  const clampTf = useCallback(
    (t: { s: number; x: number; y: number }) => {
      const s = Math.max(cover, Math.min(cover * 2.4, t.s));
      const OVER_Y = 96;
      const x = Math.min(0, Math.max(box.w - geo.width * s, t.x));
      const y = Math.min(OVER_Y, Math.max(box.h - geo.height * s - OVER_Y, t.y));
      return { s, x, y };
    },
    [cover, box.w, box.h, geo.width, geo.height],
  );
  useEffect(() => {
    if (!box.w) return;
    // initial view: north edge just below the top HUD (the north is where the story is)
    setTf((prev) =>
      prev && prev.key === geoKey
        ? { ...clampTf({ ...prev, s: Math.max(prev.s, cover) }), key: geoKey }
        : { ...clampTf({ s: cover, x: (box.w - geo.width * cover) / 2, y: Math.min(96, box.h * 0.11 - geo.height * 0.08 * cover) }), key: geoKey },
    );
  }, [box.w, box.h, cover, geo.width, geo.height, clampTf, geoKey]);
  const t = tf ?? { s: cover, x: 0, y: 0 };

  const onPointerDown = (e: PointerEvent) => {
    if (e.button !== 0) return;
    drag.current = { x: e.clientX, y: e.clientY, tx: t.x, ty: t.y, moved: false };
  };
  const onPointerMove = (e: PointerEvent) => {
    const d = drag.current;
    if (!d || !(e.buttons & 1)) return;
    const dx = e.clientX - d.x;
    const dy = e.clientY - d.y;
    if (!d.moved && Math.hypot(dx, dy) < 5) return;
    if (!d.moved) {
      d.moved = true;
      (e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId);
      setHover(null);
    }
    setTf({ ...clampTf({ s: t.s, x: d.tx + dx, y: d.ty + dy }), key: geoKey });
  };
  const onPointerUp = () => {
    if (drag.current?.moved) suppressClick.current = true;
    drag.current = null;
  };
  const onWheel = (e: WheelEvent) => {
    const host = rootRef.current?.getBoundingClientRect();
    if (!host) return;
    const f = e.deltaY < 0 ? 1.12 : 1 / 1.12;
    const s = Math.max(cover, Math.min(cover * 2.4, t.s * f));
    const px = e.clientX - host.left;
    const py = e.clientY - host.top;
    setTf({ ...clampTf({ s, x: px - ((px - t.x) * s) / t.s, y: py - ((py - t.y) * s) / t.s }), key: geoKey });
  };

  const moveTip = (e: MouseEvent) => {
    const el = tipRef.current;
    if (!el) return;
    const host = (e.currentTarget as Element).closest('.map-root')!.getBoundingClientRect();
    const x = e.clientX - host.left;
    const y = e.clientY - host.top;
    el.style.transform = `translate(${Math.min(x + 18, host.width - 270)}px, ${Math.min(y + 18, host.height - 170)}px)`;
  };

  const hovered = hover ? state.regions[hover] : null;
  const canalBlocked = CANAL_REGIONS.some((id) => state.regions[id]?.controller === 'yan');
  const canalPts: Pt[] = geo.mode === 'schematic' && !mapData ? CANAL : CANAL_REGIONS.slice().map((id) => seatOf[id]).filter(Boolean);
  const rebelPts: Pt[] = REBEL_PATH.map((id) => seatOf[id]).filter(Boolean);
  const showRebel = rebelled || crisisValue >= 40 || layer === 'beacon';

  return (
    <div
      ref={rootRef}
      className={cls('map-root', `map-layer--${layer}`, drag.current?.moved && 'is-dragging')}
      data-testid="map.root"
      data-map-mode={geo.mode}
      data-layer={layer}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      onWheel={onWheel}
      onClickCapture={(e) => {
        if (suppressClick.current) {
          suppressClick.current = false;
          e.stopPropagation();
          e.preventDefault();
        }
      }}
    >
      <div className="map-stage" style={{ width: geo.width, height: geo.height, transform: `translate(${t.x}px, ${t.y}px) scale(${t.s})` }}>
      {baseUrl ? (
        <svg className="map-base" viewBox={`0 0 ${geo.width} ${geo.height}`} preserveAspectRatio="none" aria-hidden="true">
          <image
            href={baseUrl}
            width={geo.width}
            height={geo.height}
            preserveAspectRatio="none"
            onLoad={(e) => {
              if (mapData) return;
              const img = new Image();
              img.onload = () => setImgSize([img.naturalWidth, img.naturalHeight]);
              img.src = (e.target as SVGImageElement).href.baseVal;
            }}
          />
        </svg>
      ) : ready ? (
        <SchematicBase />
      ) : null}
      {ready && (
        <svg className="map-overlay" viewBox={`0 0 ${geo.width} ${geo.height}`} preserveAspectRatio="none">
          <defs>
            <pattern id="mo-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
              <line x1="0" y1="0" x2="0" y2="9" stroke="#3d342b" strokeOpacity="0.35" strokeWidth="1.4" />
            </pattern>
            <clipPath id="mo-land">{geo.mode === 'schematic' && !mapData ? <path d={LAND_PATH} /> : <rect width={geo.width} height={geo.height} />}</clipPath>
            <filter id="mo-glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="6" />
            </filter>
            <radialGradient id="mo-fire">
              <stop offset="0%" stopColor="#ffd27a" />
              <stop offset="45%" stopColor="#e2582f" />
              <stop offset="100%" stopColor="#c0392b" stopOpacity="0" />
            </radialGradient>
            <marker id="mo-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M0 0 L10 5 L0 10 z" fill="#b2321f" />
            </marker>
          </defs>
          <g clipPath="url(#mo-land)">
            {geo.shapes
              .filter((s) => s.d)
              .map((s) => {
                const { fill, opacity } = layerFill(layer, s.id, state, crisisValue, armiesBy);
                return (
                  <g key={s.id}>
                    <path className="region-fill" d={s.d} style={{ fill, fillOpacity: geo.mode === 'schematic' ? opacity : Math.min(0.85, opacity * 1.7) }} />
                    {FOREIGN.has(s.id) && <path d={s.d} fill="url(#mo-hatch)" pointerEvents="none" />}
                  </g>
                );
              })}
            {/* circuit borders: cinnabar dotted lines as on period maps */}
            {geo.shapes
              .filter((s) => s.d)
              .map((s) => (
                <path key={`b${s.id}`} d={s.d} className="region-border" />
              ))}
          </g>

          {/* canal lifeline */}
          {(layer === 'canal' || canalBlocked) && canalPts.length > 1 && (
            <g className={cls('canal', canalBlocked && 'canal--blocked')} data-testid="map.canalRoute">
              <path d={smoothPath(canalPts)} className="canal-under" />
              <path d={smoothPath(canalPts)} className="canal-line" />
            </g>
          )}

          {/* rebel route */}
          {showRebel && rebelPts.length > 1 && (
            <g className={cls('rebel-route', rebelled && 'rebel-route--live')} data-testid="map.rebelRoute">
              <path d={smoothPath(rebelPts)} className="rebel-under" />
              <path d={smoothPath(rebelPts)} className="rebel-line" markerEnd="url(#mo-arrow)" />
            </g>
          )}

          {/* beacons (烽燧) */}
          {(layer === 'beacon' || crisisValue >= 40) &&
            ['fanyang', 'pinglu', 'hebei', 'duji', 'tongguan'].map((id, i) => {
              const p = seatOf[id];
              if (!p) return null;
              const heat = Math.max(0.25, Math.min(1, (crisisValue - 20) / 70 - i * 0.08));
              return (
                <g key={`f${id}`} transform={`translate(${p[0] + 38 * k} ${p[1] - 30 * k}) scale(${k})`} className="beacon" style={{ animationDelay: `${i * 0.37}s` }}>
                  <circle r={22 * heat + 8} fill="url(#mo-fire)" opacity={0.85} />
                  <path d="M-5 10 L -3 -2 L 3 -2 L 5 10 Z" fill="#3d2a1c" />
                </g>
              );
            })}

          {/* hit areas */}
          {geo.shapes.map((s) => {
            const region = state.regions[s.id];
            if (!region) return null;
            const common = {
              'data-testid': `map.region.${s.id}`,
              className: cls('region-hit', selected === s.id && 'is-selected'),
              onMouseEnter: (e: MouseEvent) => {
                if (drag.current?.moved) return;
                moveTip(e);
                setHover(s.id);
              },
              onMouseLeave: () => setHover((h) => (h === s.id ? null : h)),
              onMouseMove: moveTip,
              onClick: () => onSelect(selected === s.id ? null : s.id),
              role: 'button',
              'aria-label': region.name,
            };
            return s.d ? <path key={`h${s.id}`} d={s.d} {...common} /> : <circle key={`h${s.id}`} cx={s.seat[0]} cy={s.seat[1]} r={46 * k} {...common} />;
          })}

          {/* labels */}
          {geo.shapes.map((s) => {
            const region = state.regions[s.id];
            if (!region) return null;
            const foreign = s.foreign ?? FOREIGN.has(s.id);
            const capital = s.id === 'jingji' || s.id === 'duji';
            const split = Math.hypot(s.label[0] - s.seat[0], s.label[1] - s.seat[1]) > 60 * k;
            const lp: Pt = foreign || split ? s.label : s.seat;
            return (
              <g key={`l${s.id}`} className={cls('region-label', foreign && 'is-foreign', selected === s.id && 'is-selected')} pointerEvents="none">
                {!foreign && (
                  <g transform={`translate(${s.seat[0]} ${s.seat[1]}) scale(${k})`}>
                    <g className="seat-mark">
                      {capital ? (
                        <g transform="translate(0 2)">
                          <path d="M-13 -4 L 0 -13 L 13 -4 Z" fill="#7a2a1e" />
                          <rect x="-10" y="-4" width="20" height="9" fill="#c9a24b" stroke="#3a2210" strokeWidth="1.2" />
                          <rect x="-3" y="0" width="6" height="5" fill="#3a2210" />
                        </g>
                      ) : (
                        <rect x="-4.5" y="-4.5" width="9" height="9" transform="rotate(45)" fill="#8a2219" stroke="#f2e6c6" strokeWidth="1.4" />
                      )}
                    </g>
                    {(region.seat ?? SEAT_NAMES[s.id]) && (region.seat ?? SEAT_NAMES[s.id]) !== region.name && (
                      <text className="seat-name" y={22} textAnchor="middle">
                        {region.seat ?? SEAT_NAMES[s.id]}
                      </text>
                    )}
                  </g>
                )}
                <text className="region-name" transform={`translate(${lp[0]} ${lp[1]}) scale(${k})`} y={foreign || split ? 8 : -20} textAnchor="middle">
                  {region.name}
                </text>
              </g>
            );
          })}

          {/* army tokens */}
          {Object.entries(armiesBy).map(([rid, list]) => {
            const p = seatOf[rid];
            if (!p) return null;
            return list.slice(0, 3).map((a, i) => {
              const hostile = a.faction === 'yan';
              const foreign = a.faction && a.faction !== 'tang' && !hostile;
              const shape = geo.shapes.find((x) => x.id === rid);
              return (
                <g
                  key={a.id}
                  className={cls('army-token', hostile && 'is-rebel', foreign && 'is-foreign')}
                  transform={`translate(${p[0] + ((shape?.foreign ?? FOREIGN.has(rid)) ? -30 : 14) * k} ${p[1] + ((shape?.foreign ?? FOREIGN.has(rid)) ? 26 : -2) * k + i * 22 * k}) scale(${k})`}
                  data-testid={`map.army.${a.id}`}
                >
                  <title>{`${a.name}　${a.strength.toLocaleString('zh-CN')}人`}</title>
                  <rect x="0" y="-10" width="60" height="19" rx="3" />
                  <circle cx="9" cy="-0.5" r="4.5" className="army-dot" />
                  <text x="36" y="4.5" textAnchor="middle" className="t-num">
                    {fmtWan(a.strength)}
                  </text>
                </g>
              );
            });
          })}
        </svg>
      )}
      </div>
      {!ready && <div className="map-loading ink-loader"><i /><i /><i /> 展舆图</div>}
      <div ref={tipRef} className={cls('map-tip lacquer', hovered && 'is-on')} aria-hidden={!hovered}>
        {hovered && (
          <>
            <h4 className="t-title">
              {hovered.name}
              {(hovered.seat ?? SEAT_NAMES[hovered.id]) && <small>　治{hovered.seat ?? SEAT_NAMES[hovered.id]}</small>}
            </h4>
            {hovered.stats && Object.keys(hovered.stats).length > 0 ? (
              <div className="map-tip-stats">
                {Object.entries(hovered.stats).map(([k2, v]) => (
                  <span key={k2}>
                    {({ prosperity: '繁荣', order: '治安', defense: '防务', tax: '税基', grain: '粮产' } as Record<string, string>)[k2] ?? k2}
                    <b className="t-num">{Math.round(v)}</b>
                  </span>
                ))}
              </div>
            ) : (
              <div className="map-tip-note">域外之国</div>
            )}
            {(armiesBy[hovered.id] ?? []).map((a) => (
              <div key={a.id} className="map-tip-army">
                {a.name}　<span className="t-num">{a.strength.toLocaleString('zh-CN')}</span>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}
