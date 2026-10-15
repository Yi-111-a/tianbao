import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { resolveAsset } from '../api/assets';
import type { Clause, CrisisReport, TurnReport } from '../api/types';
import { EventArt } from '../components/EventArt';
import { ResourceIcon } from '../components/Icons';
import { CuancaoColumn } from '../components/Ornaments';
import { Paper, Roller } from '../components/Paper';
import { PanelShell } from '../components/PanelShell';
import { useGame } from '../store/game';
import { cls, deltaClass, fmtDelta, fmtNum } from '../lib/util';
import { CrisisTermRow, termMid } from './desk/Hud';
import { groupClauses } from './EdictPanel';

const LEDGER_ORDER = ['treasury', 'grain', 'authority', 'morale', 'corruption', 'frontier_pressure', 'fanzhen_power', 'court_strife', 'an_ambition', 'rebellion_risk'];

function Mark({ status }: { status: Clause['status'] }) {
  if (status === 'applied')
    return (
      <svg className="mark mark--ok" viewBox="0 0 40 40" aria-label="施行">
        <path d="M6 22 C 10 24, 13 28, 16 33 C 22 20, 28 12, 36 6" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
      </svg>
    );
  if (status === 'rejected')
    return (
      <svg className="mark mark--no" viewBox="0 0 40 40" aria-label="驳回">
        <path d="M9 9 L 31 31 M31 8 L 9 32" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
      </svg>
    );
  return (
    <svg className="mark mark--wait" viewBox="0 0 40 40" aria-label={status === 'delayed' ? '迟滞' : '载记'}>
      <circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" strokeWidth="4" />
      {status === 'delayed' && <path d="M20 12 V 21 L 26 25" fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" />}
    </svg>
  );
}

export function ResultPanel() {
  const g = useGame();
  const view = g.view!;
  const report: TurnReport | null = g.lastTurn?.report ?? view.last_report;
  const narrative = g.lastTurn?.memorial ?? '';
  const outcome = g.lastTurn?.outcome ?? view.outcome;
  const eventFact = (id: string) => (report?.facts ?? []).find((f) => f.kind === 'event' && f.entity === id);
  const events = (report?.events_fired ?? []).map((e) =>
    typeof e === 'string' ? { id: e, title: eventFact(e)?.display ?? eventFact(e)?.text ?? e } : { ...e, title: e.title ?? eventFact(e.id)?.text ?? e.id },
  );
  const [lead, setLead] = useState<(typeof events)[number] | undefined>(events[0]);
  const eventKey = events.map((e) => e.id).join('|');
  useEffect(() => {
    // lead with the first event that has real art (system/bookkeeping events usually have none)
    let alive = true;
    (async () => {
      for (const e of events) {
        const ill = 'illustration' in e ? (e as { illustration?: string }).illustration : undefined;
        const url = await resolveAsset([ill, `event.${e.id}`].filter(Boolean) as string[]);
        if (url && alive) return setLead(e);
      }
    })();
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [eventKey]);
  const crisis = (report?.crisis ?? {}) as CrisisReport;
  const res = view.state.resources;

  const deltas = LEDGER_ORDER.filter((id) => res[id] && (g.deltas[id] ?? 0) !== 0);
  const reasons = (id: string) => {
    const all = (report?.ledger_lines ?? []).filter((l) => l.resource === id);
    const income = all.filter((l) => l.kind === 'income');
    const rest = all.filter((l) => l.kind !== 'income');
    const lines = [
      ...(income.length > 2 ? [`${income.length}道收入${fmtDelta(income.reduce((a, l) => a + l.amount, 0))}`] : income.map((l) => `${l.name}${fmtDelta(l.amount)}`)),
      ...rest.map((l) => `${l.name}${fmtDelta(l.amount)}`),
    ];
    const facts = (report?.facts ?? []).filter((f) => f.kind === 'resource' && f.entity === id).map((f) => f.text.replace(/^.*?（(.*)）$/, '$1'));
    return [...lines, ...facts].slice(0, 3).join('，');
  };
  const maxTerm = Math.max(1, ...(crisis.terms ?? []).map((t) => Math.abs(termMid(t.value))));
  const others = (report?.facts ?? []).filter((f) => !['resource', 'event', 'ledger'].includes(f.kind) && !f.internal).slice(0, 10);

  const next = () => {
    g.closePanel();
    if (outcome) g.setScreen('ending');
  };

  return (
    <PanelShell screen="result" onClose={next} unroll="vertical" closeLabel="合卷">
      <div className="result">
        <figure className="result-figure">
          <div className="result-frame">
            <EventArt ids={lead ? [(lead as { illustration?: string }).illustration, `event.${lead.id}`] : ['event.season']} seed={lead?.id ?? `season${view.state.turn}`} className="result-art" />
          </div>
          <figcaption className="t-title">{lead?.title ?? `${view.calendar_label}·四方无事`}</figcaption>
        </figure>

        <div className="result-scroll">
          <Roller orientation="horizontal" thickness={24} />
          <div className="result-scroll-body">
            <CuancaoColumn width={18} color="rgba(201,162,75,.85)" bg="#30505f" />
            <Paper variant="paper" seed={88} amp={2} sides="lr" className="result-paper">
              <h2 className="result-title t-title">
                <span>推演结果</span>
              </h2>
              <div className="result-season t-title">{view.calendar_label}</div>
              <div className="result-content selectable">
                {g.lastEdict && g.lastEdict.clauses.length > 0 && (
                  <section>
                    <div className="section-label">诏令施行</div>
                    <ul className="result-clauses">
                      {groupClauses(g.lastEdict.clauses).map(({ first: c }, i) => (
                        <li key={i} data-testid={`result.clause.${i}`} data-status={c.status}>
                          <Mark status={c.status} />
                          <span>
                            {c.text}
                            {c.reason && <small>　{c.reason}</small>}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </section>
                )}
                {narrative && (
                  <section>
                    <div className="section-label">纪事</div>
                    <p className="result-narrative">{narrative}</p>
                  </section>
                )}
                {(report?.battles?.length ?? 0) > 0 && (
                  <section>
                    <div className="section-label">战报</div>
                    <ul className="result-battles">
                      {report!.battles!.map((b, i) => (
                        <li key={i} data-testid={`result.battle.${i}`}>
                          <b className="t-title">{(b.region && view.state.regions[b.region]?.name) || ''}</b>
                          {b.text ?? `${b.attacker ?? ''}攻${b.defender ?? ''}，${b.winner ?? ''}胜。`}
                          {(b.attacker_loss || b.defender_loss) && (
                            <small className="t-num">
                              　攻方折损 {fmtNum(b.attacker_loss ?? 0)}，守方折损 {fmtNum(b.defender_loss ?? 0)}
                            </small>
                          )}
                        </li>
                      ))}
                    </ul>
                  </section>
                )}
                {events.length > 0 && (
                  <section>
                    <div className="section-label">时事</div>
                    <ul className="result-events">
                      {events.map((e) => (
                        <li key={e.id} data-testid={`result.event.${e.id}`}>
                          <b className="t-title">{e.title ?? e.id}</b>
                          {'text' in e && e.text && <span>　{e.text}</span>}
                        </li>
                      ))}
                    </ul>
                  </section>
                )}
                {others.length > 0 && (
                  <section>
                    <div className="section-label">有司奏报</div>
                    <ul className="result-facts">
                      {others.map((f, i) => (
                        <li key={i}>{f.display ?? f.text}</li>
                      ))}
                    </ul>
                  </section>
                )}
                {(report?.choices_opened?.length ?? 0) > 0 && <p className="result-choice-note t-title">另有急务{report!.choices_opened!.length}件，待陛下圣裁。</p>}
                {!report && <p className="muted">尚无推演记录。</p>}
              </div>
            </Paper>
            <CuancaoColumn width={18} color="rgba(201,162,75,.85)" bg="#30505f" />
          </div>
          <Roller orientation="horizontal" thickness={24} />
        </div>

        <aside className="result-ledger">
          <Paper variant="silk" seed={31} className="ledger-paper">
            <div className="ledger-title t-title">度支 · 本季增减</div>
            <ul className="ledger-list" data-testid="result.ledger">
              {deltas.length === 0 && <li className="muted">诸项如旧。</li>}
              {deltas.map((id) => {
                const d = g.deltas[id];
                return (
                  <motion.li key={id} initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 + LEDGER_ORDER.indexOf(id) * 0.05 }}>
                    <span className="ledger-icon">
                      <ResourceIcon id={id} size={26} />
                    </span>
                    <span className="ledger-name">
                      {res[id].name}
                      <small>{reasons(id)}</small>
                    </span>
                    <b className={cls('ledger-delta t-num', deltaClass(id, d))}>
                      {d > 0 ? '▲' : '▼'} {fmtDelta(d)}
                    </b>
                  </motion.li>
                );
              })}
            </ul>
            {(crisis.terms?.length ?? 0) > 0 && (
              <div className="ledger-crisis" data-testid="result.crisis">
                <div className="ledger-title t-title">
                  渔阳鼙鼓
                  {crisis.before != null && crisis.value != null ? (
                    <span className="t-num">
                      　{Math.round(crisis.before)} → {Math.round(crisis.value)}
                    </span>
                  ) : crisis.display ? (
                    <span className="t-num">　{crisis.display}</span>
                  ) : null}
                  {crisis.band && <em>　{crisis.band}</em>}
                </div>
                {crisis.terms!.map((t) => (
                  <CrisisTermRow key={t.id ?? t.label} term={t} max={maxTerm} paper />
                ))}
              </div>
            )}
          </Paper>
          <button className="btn btn-ink result-next" data-testid="result.next" onClick={next}>
            {outcome ? '观终局' : '下一季'}
          </button>
        </aside>
      </div>
    </PanelShell>
  );
}
