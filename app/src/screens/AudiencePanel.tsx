import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useMemo, useRef, useState } from 'react';
import { useAsset } from '../api/assets';
import { api } from '../api/client';
import { Paper } from '../components/Paper';
import { PanelShell } from '../components/PanelShell';
import { Portrait } from '../components/Portrait';
import { useToast } from '../components/Toast';
import { useGame } from '../store/game';
import { humanize } from '../lib/names';
import { cls } from '../lib/util';

interface Msg {
  role: 'player' | 'minister' | 'system';
  text: string;
  streaming?: boolean;
}

// Conversations survive closing the panel (per session, per character).
const logs = new Map<string, Msg[]>();

const OPENERS = ['卿以为范阳之兵如何？', '朝中近来有何风声？', '此季当以何事为先？'];

export function AudiencePanel() {
  const g = useGame();
  const toast = useToast();
  const view = g.view;
  const chars = view?.state.characters ?? {};
  const roster = useMemo(
    () => Object.values(chars).filter((c) => c.id !== 'xuanzong' && (c.status ?? 'alive') === 'alive'),
    [chars],
  );
  const [who, setWho] = useState<string>(() => g.panelArg ?? roster.find((c) => c.region === 'jingji')?.id ?? roster[0]?.id ?? '');
  const key = `${g.sessionId}:${who}`;
  const [msgs, setMsgs] = useState<Msg[]>(() => logs.get(key) ?? []);
  const [modes, setModes] = useState<Record<string, { label: string; note?: string }>>({});
  const [text, setText] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [sel, setSel] = useState<{ text: string; x: number; y: number } | null>(null);
  const abort = useRef<AbortController | null>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const [bg] = useAsset(['ui.court', 'ui.audience', 'ui.court.background']);
  const c = chars[who];

  useEffect(() => {
    setMsgs(logs.get(key) ?? []);
    setSel(null);
  }, [key]);
  useEffect(() => {
    logs.set(key, msgs);
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [msgs, key]);
  useEffect(() => () => abort.current?.abort(), []);

  if (!view || !g.sessionId) return null;

  const send = async (raw?: string) => {
    const t = (raw ?? text).trim();
    if (!t || streaming || !c) return;
    setText('');
    setStreaming(true);
    const ctl = new AbortController();
    abort.current = ctl;
    setMsgs((m) => [...m, { role: 'player', text: t }, { role: 'minister', text: '', streaming: true }]);
    try {
      for await (const ev of api.chat(g.sessionId!, who, t, ctl.signal)) {
        if (ev.type === 'message') {
          setMsgs((m) => {
            const copy = m.slice();
            const last = copy[copy.length - 1];
            copy[copy.length - 1] = { ...last, text: last.text + ev.text };
            return copy;
          });
        } else if (ev.type === 'status' && ev.mode_label) {
          setModes((m) => ({ ...m, [who]: { label: ev.mode_label!, note: ev.mode_note } }));
        } else if (ev.type === 'status' && ev.status !== 'ok') {
          setMsgs((m) => [...m.slice(0, -1), { role: 'system', text: ev.status === 'remote' ? '远镇之臣，以表章代对。' : '此人无从召对。' }, m[m.length - 1]]);
        } else if (ev.type === 'error') {
          toast.error(new Error(ev.message), '召对中断');
        }
      }
    } catch (err) {
      toast.error(err, '召对中断');
      setMsgs((m) => (m[m.length - 1]?.text ? m : m.slice(0, -1)));
    } finally {
      setMsgs((m) => m.map((x) => (x.streaming ? { ...x, streaming: false } : x)));
      setStreaming(false);
    }
  };

  const onMouseUp = () => {
    const s = window.getSelection();
    const t = s?.toString().trim();
    if (!s || !t || s.rangeCount === 0) {
      setSel(null);
      return;
    }
    const anchor = s.anchorNode?.parentElement?.closest('.msg--minister');
    if (!anchor) return setSel(null);
    const rect = s.getRangeAt(0).getBoundingClientRect();
    const host = listRef.current!.getBoundingClientRect();
    setSel({ text: t, x: rect.left - host.left + rect.width / 2, y: rect.top - host.top + listRef.current!.scrollTop });
  };

  const saveSel = async () => {
    if (!sel) return;
    await g.saveAdvice(who, sel.text, 'audience');
    window.getSelection()?.removeAllRanges();
    setSel(null);
  };

  return (
    <PanelShell screen="audience" onClose={g.closePanel}>
      <div className="audience" style={bg ? { backgroundImage: `url(${bg})` } : undefined}>
        <div className="audience-figure">
          {c && <Portrait key={who} id={who} className="portrait--hero" />}
          {c && (
            <div className="audience-plaque">
              <span className="t-title">{c.title || c.office || ''}</span>
            </div>
          )}
          {c && (
            <div className="audience-name">
              <b className="t-title">{c.name}</b>
              <small>{view.state.regions[c.region]?.name ?? ''}</small>
            </div>
          )}
        </div>
        <Paper variant="paper" seed={66} className="audience-paper">
          <div className="audience-head">
            <div className="audience-roster" role="tablist">
              {roster.map((x) => (
                <button key={x.id} role="tab" aria-selected={x.id === who} className={cls('roster-chip', x.id === who && 'is-on')} data-testid={`audience.pick.${x.id}`} disabled={x.id === who || streaming} onClick={() => setWho(x.id)} title={x.title}>
                  <Portrait id={x.id} className="portrait--mini" />
                  <span className="t-title">{x.name}</span>
                </button>
              ))}
            </div>
            {modes[who] && (
              <span className="audience-mode t-title" data-testid="audience.mode" title={modes[who].note}>
                {modes[who].label}
              </span>
            )}
            <button className="btn btn-outline btn-small audience-library" data-testid="audience.adviceLibrary" onClick={() => g.openPanel('advice')}>
              谏言库{g.advice.length ? `·${g.advice.length}` : ''}
            </button>
          </div>
          <div className="audience-log selectable" ref={listRef} onMouseUp={onMouseUp} data-testid="audience.log">
            {msgs.length === 0 && (
              <div className="audience-empty">
                <p className="t-title">{c ? `${c.name}奉召入对。` : '请择一臣召对。'}</p>
                {c?.persona && <p className="muted">{c.persona}</p>}
              </div>
            )}
            {msgs.map((m, i) => (
              <motion.div key={i} className={cls('msg', `msg--${m.role}`)} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }}>
                {m.role === 'minister' && <Portrait id={who} className="portrait--mini msg-avatar" />}
                {m.role === 'player' && <Portrait id="xuanzong" className="portrait--mini msg-avatar" />}
                <div className="msg-slip">
                  {humanize(m.text)}
                  {m.streaming && <span className="brush-caret" aria-hidden="true" />}
                  {m.role === 'minister' && !m.streaming && m.text && (
                    <button className="msg-save" data-testid={`audience.saveMessage.${i}`} onClick={() => g.saveAdvice(who, humanize(m.text), 'audience')} title="整段存入谏言库">
                      存谏
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
            <AnimatePresence>
              {sel && (
                <motion.button
                  className="sel-save btn btn-ink btn-small"
                  data-testid="audience.saveSelection"
                  style={{ left: sel.x, top: sel.y - 44 }}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={saveSel}
                >
                  存入谏言库
                </motion.button>
              )}
            </AnimatePresence>
          </div>
          <div className="audience-openers">
            {OPENERS.map((o, i) => (
              <button key={o} className="btn btn-outline btn-small" data-testid={`audience.opener.${i}`} disabled={streaming} onClick={() => send(o)}>
                {o}
              </button>
            ))}
          </div>
          <div className="audience-input">
            <textarea
              className="field"
              data-testid="audience.input"
              rows={2}
              placeholder={c ? `垂询${c.name}……（Enter 发问，Shift+Enter 换行）` : ''}
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  void send();
                }
              }}
            />
            {streaming ? (
              <button className="btn btn-outline audience-send" data-testid="audience.stop" onClick={() => abort.current?.abort()}>
                止
              </button>
            ) : (
              <button className="btn btn-ink audience-send" data-testid="audience.send" disabled={!text.trim()} onClick={() => send()} aria-label="发问">
                问
              </button>
            )}
          </div>
        </Paper>
      </div>
    </PanelShell>
  );
}
