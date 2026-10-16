import { AnimatePresence, motion } from 'framer-motion';
import { useState } from 'react';
import { api } from '../api/client';
import type { Clause, EdictReceipt } from '../api/types';
import { Baoxiang } from '../components/Ornaments';
import { Paper, Roller } from '../components/Paper';
import { PanelShell } from '../components/PanelShell';
import { useToast } from '../components/Toast';
import { useGame } from '../store/game';
import { cls, opSummary } from '../lib/util';

const STATUS: Record<string, { glyph: string; name: string; cls: string }> = {
  applied: { glyph: '行', name: '施行', cls: 'st--applied' },
  delayed: { glyph: '缓', name: '迟滞', cls: 'st--delayed' },
  rejected: { glyph: '驳', name: '驳回', cls: 'st--rejected' },
  narrative_only: { glyph: '记', name: '载记', cls: 'st--narrative' },
  needs_clarification: { glyph: '疑', name: '待明', cls: 'st--unclear' },
};

const SOURCE: Record<string, string> = { memorial: '奏议', text: '诏文', client: '客令' };

export function EdictPanel() {
  const g = useGame();
  const toast = useToast();
  const view = g.view!;
  const [focus, setFocus] = useState<string>('other');
  const [polished, setPolished] = useState<string | null>(null);
  const [polishing, setPolishing] = useState(false);
  const receipt = g.receipt;
  const chars = view.state.characters;
  const resName = (id: string) => view.state.resources[id]?.name ?? id;
  const hidden = (id: string) => Boolean(view.state.resources[id]?.hidden);
  const entName = (id: string) =>
    view.state.armies?.[id]?.name ?? view.state.regions[id]?.name ?? chars[id]?.name ?? view.state.offices?.[id]?.name ?? id;
  const catName = (id: string) => g.categories.find((c) => c.id === id)?.name ?? (id === 'memorial' ? '奏议' : id === 'client' ? '客令' : id);
  const empty = g.draft.adopted.length === 0 && !Object.values(g.draft.sections).some((t) => t.trim());

  const cite = (character: string, text: string) => {
    const name = chars[character]?.name ?? '';
    const prev = g.draft.sections[focus] ?? '';
    g.setSection(focus, `${prev}${prev && !/[。；\n]$/.test(prev) ? '。' : ''}援${name}之议：${text}`);
  };

  const polish = async () => {
    if (!g.sessionId) return;
    setPolishing(true);
    try {
      const sections = Object.fromEntries(
        g.categories.map((c) => [c.name, g.draft.sections[c.id] ?? '']).filter(([, v]) => v.trim()),
      );
      const r = await api.polishEdict(g.sessionId, sections);
      setPolished(r.text);
    } catch (err) {
      toast.error(err, '润色未成');
    } finally {
      setPolishing(false);
    }
  };

  return (
    <PanelShell screen="edict" onClose={g.closePanel} unroll="horizontal">
      <div className="edict-desk">
        <aside className="advice-slips" aria-label="谏言">
          <div className="advice-slips-title t-title">谏言</div>
          {g.advice.length === 0 && <p className="advice-slips-empty">召对、廷议时选中臣下之言，可存为谏言，于此援引。</p>}
          {g.advice.slice(-6).map((a, i) => (
            <button key={a.id ?? i} className="advice-slip" data-testid={`edict.cite.${i}`} onClick={() => cite(a.character, a.text)} title="援引入诏">
              <span className="advice-slip-string" aria-hidden="true" />
              <Paper variant="slip" seed={i + 40} amp={2}>
                <span className="advice-slip-who t-title">{chars[a.character]?.name ?? (a.character === 'xuanzong' ? '御批' : a.character)}</span>
                <span className="advice-slip-text">{a.text}</span>
              </Paper>
            </button>
          ))}
        </aside>

        <div className="edict-scroll-wrap">
          <Roller orientation="vertical" thickness={34} />
          <Paper variant="edict" seed={12} amp={2} sides="tb" className="edict-paper">
            <div className="edict-border">
              <header className="edict-head">
                <Baoxiang size={30} />
                <h2 className="panel-title edict-title">门下</h2>
                <Baoxiang size={30} />
              </header>

              <AnimatePresence mode="wait">
                {!receipt ? (
                  <motion.div key="compose" className="edict-compose" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                    <div className="adopted-strip">
                      <span className="adopted-label t-title">采纳奏议</span>
                      {g.draft.adopted.length === 0 ? (
                        <span className="adopted-empty">尚未采纳。于奏疏中朱批「采入诏书」，即列于此。</span>
                      ) : (
                        g.draft.adopted.map((a) => (
                          <span key={a.memorial_id} className="adopted-chip">
                            <b className="t-title">{a.title}</b>
                            <span>{a.label}</span>
                            {a.hint && <small>{a.hint}</small>}
                            <button data-testid={`edict.removeAdopted.${a.memorial_id}`} onClick={() => g.unadopt(a.memorial_id)} aria-label={`撤回${a.title}`}>
                              ×
                            </button>
                          </span>
                        ))
                      )}
                    </div>
                    <div className="edict-grid">
                      {g.categories.map((c) => (
                        <label key={c.id} className={cls('edict-section', focus === c.id && 'is-focus')}>
                          <span className="edict-seal t-title" aria-hidden="true">
                            {c.name.split('').map((ch, i) => (
                              <span key={i}>{ch}</span>
                            ))}
                          </span>
                          <textarea
                            className="edict-text selectable"
                            data-testid={`edict.section.${c.id}`}
                            value={g.draft.sections[c.id] ?? ''}
                            placeholder={c.hint ? `${c.hint}……` : ''}
                            onFocus={() => setFocus(c.id)}
                            onChange={(e) => g.setSection(c.id, e.target.value)}
                          />
                        </label>
                      ))}
                    </div>
                  </motion.div>
                ) : (
                  <Receipt key="receipt" receipt={receipt} turn={g.view?.state.turn ?? 0} catName={catName} resName={resName} entName={entName} hidden={hidden} />
                )}
              </AnimatePresence>

              <AnimatePresence>
                {polished && (
                  <motion.div className="polish-sheet" data-testid="edict.polished" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                    <div className="section-label">润色稿（仅供参阅，颁布仍以四栏为准）</div>
                    <p className="selectable">{polished}</p>
                    <button className="btn btn-outline btn-small" data-testid="edict.polishClose" onClick={() => setPolished(null)}>
                      收起
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </Paper>
          <Roller orientation="vertical" thickness={34} />
        </div>

        <aside className="edict-actions">
          {!receipt && (
            <>
              <button className="plaque-btn" data-testid="edict.debate" onClick={() => g.openPanel('debate')}>
                <span className="t-title">廷议</span>
              </button>
              <button className="plaque-btn" data-testid="edict.polish" disabled={polishing || !Object.values(g.draft.sections).some((t) => t.trim())} onClick={polish}>
                <span className="t-title">{polishing ? '润色中' : '润色'}</span>
              </button>
              <button className="plaque-btn plaque-btn--primary" data-testid="edict.preview" disabled={g.busy.draft || empty} onClick={g.draftEdict}>
                <span className="t-title">{g.busy.draft ? '拟定中' : '预览'}</span>
              </button>
              {g.busy.draft && (
                <button className="btn btn-outline btn-outline--dark btn-small" data-testid="edict.cancel" onClick={g.cancelDraft}>
                  中止
                </button>
              )}
              <div className="edict-hint">先「预览」，由有司逐条回执，再用宝颁布。</div>

            </>
          )}
          {receipt && !receipt.confirmed && (
            <>
              <button className="plaque-btn" data-testid="edict.backToEdit" onClick={g.clearReceipt}>
                <span className="t-title">改拟</span>
              </button>
              <button className="seal-btn edict-seal-btn" data-testid="edict.promulgate" disabled={g.busy.confirm} onClick={g.confirmEdict}>
                <span className="t-title">{g.busy.confirm ? '用宝' : '颁布'}</span>
              </button>
            </>
          )}
          {receipt?.confirmed && (
            <>
              <div className="promulgated-stamp t-title" aria-label="已颁行">
                已颁行
              </div>
              <button className="btn btn-ink" data-testid="edict.advance" onClick={() => void g.advanceTurn()} disabled={g.busy.turn}>
                推演本季
              </button>
              <button className="btn btn-outline btn-outline--dark" data-testid="edict.newDraft" onClick={g.clearReceipt}>
                续拟一道
              </button>
            </>
          )}
        </aside>
      </div>
    </PanelShell>
  );
}

function Receipt({ receipt, turn, catName, resName, entName, hidden }: { receipt: EdictReceipt; turn: number; catName: (id: string) => string; resName: (id: string) => string; entName: (id: string) => string; hidden: (id: string) => boolean }) {
  const counts = receipt.clauses.reduce<Record<string, number>>((acc, c) => ({ ...acc, [c.status]: (acc[c.status] ?? 0) + 1 }), {});
  return (
    <motion.div className="receipt" data-testid="edict.receipt" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <div className="receipt-head">
        <span className="t-title">有司回执</span>
        <span className="receipt-rate">
          施行率 <b className="t-num">{Math.round(receipt.execution_rate * 100)}%</b>
        </span>
        <span className="receipt-counts">
          {Object.entries(counts).map(([k, v]) => (
            <span key={k} className={cls('receipt-count', STATUS[k]?.cls)}>
              {STATUS[k]?.name ?? k} <b className="t-num">{v}</b>
            </span>
          ))}
        </span>
      </div>
      <ol className="receipt-list">
        {groupClauses(receipt.clauses).map((g, i) => (
          <ClauseRow key={i} c={g.first} group={g.items} i={i} turn={turn} catName={catName} resName={resName} entName={entName} hidden={hidden} />
        ))}
      </ol>
    </motion.div>
  );
}

/** The engine emits one clause per op; show one row per edict sentence / adopted option and status. */
export function groupClauses(clauses: Clause[]): { first: Clause; items: Clause[] }[] {
  const out: { key: string; first: Clause; items: Clause[] }[] = [];
  for (const c of clauses) {
    const key = `${c.group ?? ''}|${c.memorial_id ?? ''}|${c.category}|${c.text}|${c.status}`;
    const last = out[out.length - 1];
    if (last && last.key === key) last.items.push(c);
    else out.push({ key, first: c, items: [c] });
  }
  return out;
}

/** Rejection codes worth naming for the player (the reason text carries the detail). */
const CODE_NAMES: Record<string, string> = {
  OP_NOT_PERMITTED: '非君命所及',
  INVALID_TARGET: '查无其人其地',
};

function ClauseRow({ c, group, i, turn, catName, resName, entName, hidden }: { c: Clause; group: Clause[]; i: number; turn: number; catName: (id: string) => string; resName: (id: string) => string; entName: (id: string) => string; hidden: (id: string) => boolean }) {
  const st = STATUS[c.status] ?? STATUS.narrative_only;
  const ops = group
    .flatMap((g) => (g.summary ? [g.summary] : (g.ops?.length ? g.ops : g.op ? [g.op] : []).map((o) => opSummary(o, { res: resName, ent: entName, hidden }))))
    .filter((x) => x && !/记入档案/.test(x));
  const reason = Array.from(new Set(group.map((g) => g.delay_reason || g.reason).filter(Boolean))).join('；');
  const due = c.status === 'delayed' && c.due_turn != null ? (c.due_turn <= turn + 1 ? '次季施行' : `${c.due_turn - turn}季后施行`) : '';
  const code = c.code ? CODE_NAMES[c.code] : undefined;
  return (
    <motion.li className={cls('clause', st.cls)} data-testid={`edict.clause.${i}`} data-status={c.status} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}>
      <span className="clause-seal t-title">{st.glyph}</span>
      <div className="clause-body">
        <div className="clause-meta">
          {c.category !== 'memorial' && c.category !== 'client' && <span>{catName(c.category)}</span>}
          {c.source && <span className="clause-source">{SOURCE[c.source] ?? c.source}</span>}
          <span className="clause-status">{st.name}</span>
          {due && <span className="clause-due">{due}</span>}
          {code && <span className="clause-code" data-code={c.code}>{code}</span>}
        </div>
        <div className="clause-text">{c.text}</div>
        {ops.length > 0 && <div className="clause-ops">{ops.join('　')}</div>}
        {reason && <div className="clause-reason">{reason}</div>}
      </div>
    </motion.li>
  );
}

