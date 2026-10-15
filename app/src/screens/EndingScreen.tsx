import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useAsset } from '../api/assets';
import { api } from '../api/client';
import type { HistoryEntry } from '../api/types';
import { InkScene } from '../components/EventArt';
import { Baoxiang, CuancaoBand } from '../components/Ornaments';
import { Paper } from '../components/Paper';
import { useToast } from '../components/Toast';
import { useGame } from '../store/game';

export function EndingScreen() {
  const g = useGame();
  const toast = useToast();
  const outcome = g.view?.outcome;
  const [art] = useAsset(outcome ? [`ending.${outcome.id}`, `ending.${outcome.id.replace(/^(e\d)_.*/i, '$1').toLowerCase()}`, 'ending.default'] : null);
  const [chronicle, setChronicle] = useState<HistoryEntry[]>([]);

  useEffect(() => {
    if (!g.sessionId) return;
    api
      .history(g.sessionId)
      .then(setChronicle)
      .catch((err) => toast.error(err, '史册未开'));
  }, [g.sessionId, toast]);

  if (!outcome) {
    return (
      <div className="ending" data-screen="ending" data-testid="ending.root">
        <div className="ending-empty t-title">史册未合。</div>
        <button className="btn btn-ink" data-testid="ending.toTitle" onClick={g.exitToTitle}>
          返回
        </button>
      </div>
    );
  }
  const fail = outcome.kind === 'fail';
  const byTurn = chronicle.filter((e) => e.type !== 'message');

  return (
    <div className={`ending ${fail ? 'ending--fail' : ''}`} data-screen="ending" data-testid="ending.root">
      <div className="ending-bg" aria-hidden="true">
        {art ? <img src={art} alt="" /> : <InkScene seed={`ending-${outcome.id}-${fail ? 'war' : 'court'}`} />}
      </div>
      <div className="ending-shade" aria-hidden="true" />
      <motion.div className="ending-card-wrap" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1.2, ease: [0.22, 0.8, 0.24, 1] }}>
        <Paper variant="silk" seed={1919} className="ending-card">
          <CuancaoBand height={16} color="rgba(138,109,44,.85)" />
          <div className="ending-inner">
            <div className="ending-kind t-title">{fail ? '败局' : '终局'}</div>
            <h1 className="ending-title t-title" data-testid="ending.title">
              {outcome.title}
            </h1>
            <div className="ending-turn">{g.view?.calendar_label}</div>
            <Baoxiang size={40} />
            <p className="ending-text selectable" data-testid="ending.epilogue">
              {outcome.text}
            </p>
          </div>
          <CuancaoBand height={16} color="rgba(138,109,44,.85)" />
        </Paper>
      </motion.div>
      <motion.aside className="ending-chronicle" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.6, duration: 1 }}>
        <Paper variant="paper" seed={77} className="chronicle-paper">
          <div className="chronicle-title t-title">本纪</div>
          <ol className="chronicle-list" data-testid="ending.chronicle">
            {byTurn.length === 0 && <li className="muted">史官尚未落笔。</li>}
            {byTurn.map((e) => (
              <li key={e.id} className={`chronicle-${e.type}`}>
                <span className="chronicle-glyph t-title">{{ start: '始', edict: '诏', choice: '择', turn: '季' }[e.type] ?? '记'}</span>
                <span>{e.label}</span>
              </li>
            ))}
          </ol>
        </Paper>
      </motion.aside>
      <div className="ending-actions">
        <button className="btn btn-outline btn-outline--dark" data-testid="ending.timeline" onClick={() => g.openPanel('timeline')}>
          回溯史册
        </button>
        <button className="btn btn-ink btn-ink--red" data-testid="ending.newGame" onClick={() => g.setScreen('newgame')}>
          再开新局
        </button>
        <button className="btn btn-ink" data-testid="ending.toTitle" onClick={g.exitToTitle}>
          返回标题
        </button>
      </div>
    </div>
  );
}
