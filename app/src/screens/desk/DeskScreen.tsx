import { AnimatePresence, motion } from 'framer-motion';
import { useState } from 'react';
import { Paper } from '../../components/Paper';
import { Portrait } from '../../components/Portrait';
import { useGame } from '../../store/game';
import { cls, statName } from '../../lib/util';
import { CalendarSlip, CrisisDrum, EdictScroll, FactionRibbons, LayerSwitcher, Medallion, MemorialBook, Objectives, ResourceBar } from './Hud';
import { MapView } from './MapView';
import { SEAT_NAMES } from './geo';

export function DeskScreen() {
  const g = useGame();
  const view = g.view;
  const [confirming, setConfirming] = useState(false);
  if (!view) return null;
  const pendingDraft = g.draft.adopted.length > 0 || Object.values(g.draft.sections).some((t) => t.trim());
  const choices = view.pending_choices ?? [];

  const onAdvance = () => {
    if (pendingDraft && !confirming) {
      setConfirming(true);
      return;
    }
    setConfirming(false);
    void g.advanceTurn();
  };

  return (
    <div className="desk" data-screen="desk" data-testid="desk.root">
      <div className="desk-wood" aria-hidden="true" />
      <div className="desk-map-frame">
        <MapView view={view} layer={g.mapLayer} selected={g.selectedRegion} onSelect={g.selectRegion} />
        <div className="map-vignette" aria-hidden="true" />
      </div>

      <div className="hud-top">
        <div className="hud-top-left">
          <ResourceBar view={view} deltas={g.deltas} />
        </div>
        <FactionRibbons view={view} onSummon={(id) => g.openPanel('audience', id)} />
        <div className="hud-top-right">
          <CalendarSlip view={view} />
          <Objectives view={view} />
        </div>
      </div>

      <div className="hud-right">
        <CrisisDrum view={view} />
        <nav className="medallions" aria-label="御案">
          <Medallion glyph="召" label="召对" testid="desk.medallion.audience" onClick={() => g.openPanel('audience')} />
          <Medallion glyph="议" label="廷议" testid="desk.medallion.debate" onClick={() => g.openPanel('debate')} />
          <Medallion glyph="谏" label="谏言库" testid="desk.medallion.advice" onClick={() => g.openPanel('advice')} badge={g.advice.length || undefined} />
          <Medallion glyph="史" label="史册" testid="desk.medallion.timeline" onClick={() => g.openPanel('timeline')} />
          <Medallion glyph="设" label="设置" testid="desk.medallion.settings" onClick={() => g.openPanel('settings')} />
          <Medallion glyph="归" label="退朝" testid="desk.medallion.title" onClick={g.exitToTitle} />
        </nav>
      </div>

      <div className="hud-bottom-left">
        <MemorialBook count={view.memorials.length} onOpen={() => g.openPanel('memorial')} />
      </div>

      <div className="hud-bottom-center">
        {view.final_notice?.next_is_final && (
          <div className="final-notice" data-testid="desk.finalNotice" role="status" title={view.final_notice.text}>
            <b className="t-title">下次结算即终局</b>
            <span>{view.final_notice.text.replace(/^下次结算即终局[：:]?/, '')}</span>
          </div>
        )}
        <LayerSwitcher layer={g.mapLayer} onChange={g.setMapLayer} />
      </div>

      <div className="hud-bottom-right">
        {choices.length > 0 && g.choiceDeferred && (
          <button className="choice-badge" data-testid="desk.choiceBadge" onClick={() => g.deferChoice(false)}>
            <span className="t-title">急务待决</span>
            <b className="t-num">{choices.length}</b>
          </button>
        )}
        <EdictScroll count={g.draft.adopted.length} onOpen={() => g.openPanel('edict')} />
        <div className="advance-wrap">
          <AnimatePresence>
            {confirming && (
              <motion.div className="advance-confirm lacquer on-dark" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                <span>诏书尚未颁布，所拟之条将作废。仍要推演本季？</span>
                <div className="advance-confirm-actions">
                  <button className="btn btn-outline btn-outline--dark btn-small" data-testid="desk.advance.cancel" onClick={() => setConfirming(false)}>
                    再议
                  </button>
                  <button className="btn btn-ink btn-ink--red btn-small" data-testid="desk.advance.confirm" onClick={onAdvance}>
                    径行推演
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <button className="btn btn-ink advance-btn" data-testid="desk.advance" disabled={!view.can_advance || g.busy.turn} onClick={onAdvance}>
            <span className="advance-glyph" aria-hidden="true" />
            推演本季
          </button>
        </div>
      </div>

      <AnimatePresence>{g.selectedRegion && view.state.regions[g.selectedRegion] && <RegionCard key={g.selectedRegion} id={g.selectedRegion} />}</AnimatePresence>

      <AnimatePresence>
        {g.busy.turn && (
          <motion.div className="advancing" data-testid="desk.advancing" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, transition: { duration: 0.6 } }}>
            <div className="advancing-ink" />
            <div className="advancing-text t-title">
              <span>{view.calendar_label}</span>
              <small>四时推移 · 有司奏报</small>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function RegionCard({ id }: { id: string }) {
  const g = useGame();
  const s = g.view!.state;
  const r = s.regions[id];
  const armies = Object.values(s.armies ?? {}).filter((a) => a.region === id && a.strength > 0);
  const people = Object.values(s.characters).filter((c) => c.region === id && (c.status ?? 'alive') === 'alive' && c.id !== 'xuanzong');
  const controller = r.controller ? s.factions?.[r.controller]?.name ?? r.controller : '唐廷';
  const office = s.offices?.[`${id}_jds`];
  const holder = office?.holder ? s.characters[office.holder]?.name : null;
  return (
    <motion.aside className="region-card" data-testid="map.regionCard" initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }} transition={{ duration: 0.3, ease: [0.22, 0.8, 0.24, 1] }}>
      <Paper variant="silk" seed={id.length * 13} className="region-card-paper">
        <button className="close-btn" data-testid="map.regionCard.close" onClick={() => g.selectRegion(null)} aria-label="收起">
          ×
        </button>
        <header className="region-card-head">
          <h3 className="t-title">{r.name}</h3>
          <div className="region-card-sub">
            {(r.seat ?? SEAT_NAMES[id]) && <span>治所　{r.seat ?? SEAT_NAMES[id]}</span>}
            <span>隶属　{controller}</span>
            {office && <span>{office.name}　{holder ?? '出缺'}</span>}
          </div>
        </header>
        {r.stats && Object.keys(r.stats).length > 0 && (
          <div className="region-stats">
            {Object.entries(r.stats).map(([k, v]) => (
              <div key={k} className="region-stat">
                <span>{statName(k)}</span>
                <span className="region-stat-bar">
                  <i style={{ width: `${Math.max(0, Math.min(100, v))}%` }} className={cls(v < 35 && 'is-low')} />
                </span>
                <b className="t-num">{Math.round(v)}</b>
              </div>
            ))}
          </div>
        )}
        {armies.length > 0 && (
          <div className="region-armies">
            <div className="section-label">驻军</div>
            {armies.map((a) => (
              <div key={a.id} className="region-army">
                <span>{a.name}</span>
                <span className="muted">{a.commander ? s.characters[a.commander]?.name ?? '' : ''}</span>
                <b className="t-num">{a.strength.toLocaleString('zh-CN')}</b>
              </div>
            ))}
          </div>
        )}
        {people.length > 0 && (
          <div className="region-people">
            <div className="section-label">在此人物</div>
            <div className="region-people-list">
              {people.map((c) => (
                <button key={c.id} className="region-person" data-testid={`map.regionCard.summon.${c.id}`} onClick={() => g.openPanel('audience', c.id)}>
                  <Portrait id={c.id} className="portrait--chip" />
                  <span className="t-title">{c.name}</span>
                  <small>{c.title || ''}</small>
                </button>
              ))}
            </div>
          </div>
        )}
      </Paper>
    </motion.aside>
  );
}
