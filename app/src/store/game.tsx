// Game store: session, view, edict draft, panels. Every API failure is routed to the toast.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { api, SCENARIO_ID } from '../api/client';
import type {
  AdoptedOption,
  Advice,
  EdictReceipt,
  MemorialItem,
  PublicState,
  ScenarioInfo,
  TurnResponse,
  ViewResponse,
} from '../api/types';
import { useToast } from '../components/Toast';

export type Screen = 'title' | 'newgame' | 'desk' | 'ending';
export type PanelName = 'memorial' | 'audience' | 'debate' | 'edict' | 'result' | 'timeline' | 'settings' | 'advice' | 'region';
export type MapLayer = 'jurisdiction' | 'morale' | 'troops' | 'canal' | 'beacon';

export interface AdoptedEntry extends AdoptedOption {
  title: string;
  label: string;
  hint?: string;
}

export const DEFAULT_CATEGORIES = [
  { id: 'military', name: '军务', hint: '节度、禁军、关防、征伐' },
  { id: 'interior', name: '内政', hint: '任免、财赋、漕运、赈济、吏治' },
  { id: 'diplomacy', name: '外交', hint: '吐蕃、南诏、契丹、大食、回纥' },
  { id: 'other', name: '其他', hint: '宫廷、礼仪、东宫、密旨' },
];

interface DraftStore {
  turn: number;
  sections: Record<string, string>;
  adopted: AdoptedEntry[];
}

interface GameState {
  screen: Screen;
  panel: PanelName | null;
  panelArg: string | null;
  sessionId: string | null;
  view: ViewResponse | null;
  scenario: ScenarioInfo | null;
  deltas: Record<string, number>;
  draft: DraftStore;
  receipt: EdictReceipt | null;
  lastEdict: EdictReceipt | null;
  lastTurn: TurnResponse | null;
  advice: Advice[];
  busy: Record<string, boolean>;
  choiceDeferred: boolean;
  mapLayer: MapLayer;
  selectedRegion: string | null;
}

interface GameApi extends GameState {
  setScreen: (s: Screen) => void;
  openPanel: (p: PanelName, arg?: string | null) => void;
  closePanel: () => void;
  startGame: (seed: number) => Promise<void>;
  loadSession: (id: string) => Promise<void>;
  refresh: () => Promise<void>;
  adopt: (memorial: MemorialItem, optionId: string) => void;
  unadopt: (memorialId: string) => void;
  setSection: (category: string, text: string) => void;
  draftEdict: () => Promise<void>;
  cancelDraft: () => void;
  confirmEdict: () => Promise<void>;
  clearReceipt: () => void;
  advanceTurn: () => Promise<void>;
  choose: (choiceId: string, optionId: string) => Promise<void>;
  deferChoice: (deferred: boolean) => void;
  saveAdvice: (character: string, text: string, source: string) => Promise<void>;
  loadAdvice: () => Promise<void>;
  rewind: (entryId: string) => Promise<void>;
  setMapLayer: (l: MapLayer) => void;
  selectRegion: (id: string | null) => void;
  exitToTitle: () => void;
  categories: { id: string; name: string; hint?: string }[];
}

const Ctx = createContext<GameApi | null>(null);
export function useGame(): GameApi {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useGame outside provider');
  return ctx;
}

const LS_SESSION = 'tianbao.session';
const draftKey = (id: string) => `tianbao.draft.${id}`;
const deltaKey = (id: string) => `tianbao.deltas.${id}`;

function readLS<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}
function writeLS(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* ignore */
  }
}

function resourceAmounts(state: PublicState | undefined): Record<string, number> {
  const out: Record<string, number> = {};
  for (const [id, r] of Object.entries(state?.resources ?? {})) {
    if (typeof r.amount === 'number' && !r.hidden) out[id] = r.amount;
  }
  return out;
}

const emptyDraft = (turn: number): DraftStore => ({ turn, sections: {}, adopted: [] });

export function GameProvider({ children }: { children: ReactNode }) {
  const toast = useToast();
  const [s, setS] = useState<GameState>({
    screen: 'title',
    panel: null,
    panelArg: null,
    sessionId: null,
    view: null,
    scenario: null,
    deltas: {},
    draft: emptyDraft(0),
    receipt: null,
    lastEdict: null,
    lastTurn: null,
    advice: [],
    busy: {},
    choiceDeferred: false,
    mapLayer: 'jurisdiction',
    selectedRegion: null,
  });
  const ref = useRef(s);
  ref.current = s;
  const abortRef = useRef<AbortController | null>(null);

  const patch = useCallback((p: Partial<GameState> | ((prev: GameState) => Partial<GameState>)) => {
    setS((prev) => ({ ...prev, ...(typeof p === 'function' ? p(prev) : p) }));
  }, []);
  const setBusy = useCallback((k: string, v: boolean) => setS((prev) => ({ ...prev, busy: { ...prev.busy, [k]: v } })), []);

  // scenario metadata (edict categories)
  useEffect(() => {
    api
      .scenarios()
      .then((list) => patch({ scenario: list.find((x) => x.id === SCENARIO_ID) ?? list[0] ?? null }))
      .catch(() => {
        /* engine not up yet: title screen shows its own status */
      });
  }, [patch]);

  const persistDraft = useCallback((id: string | null, draft: DraftStore) => {
    if (id) writeLS(draftKey(id), draft);
  }, []);

  const applyView = useCallback(
    (id: string, view: ViewResponse) => {
      const saved = readLS<DraftStore>(draftKey(id), emptyDraft(view.state.turn));
      const draft = saved.turn === view.state.turn ? saved : emptyDraft(view.state.turn);
      patch({
        sessionId: id,
        view,
        draft,
        deltas: readLS<Record<string, number>>(deltaKey(id), {}),
        screen: view.outcome ? 'ending' : ref.current.screen === 'title' || ref.current.screen === 'newgame' ? 'desk' : ref.current.screen,
      });
    },
    [patch],
  );

  const loadSession = useCallback(
    async (id: string) => {
      setBusy('load', true);
      try {
        const view = await api.view(id);
        writeLS(LS_SESSION, id);
        patch({ receipt: null, lastTurn: null, choiceDeferred: false, panel: null, selectedRegion: null });
        applyView(id, view);
        if (!view.outcome) patch({ screen: 'desk' });
        api
          .advice(id)
          .then((advice) => patch({ advice }))
          .catch(() => {});
      } catch (err) {
        toast.error(err, '读档失败');
      } finally {
        setBusy('load', false);
      }
    },
    [applyView, patch, setBusy, toast],
  );

  const refresh = useCallback(async () => {
    const id = ref.current.sessionId;
    if (!id) return;
    try {
      const view = await api.view(id);
      applyView(id, view);
    } catch (err) {
      toast.error(err, '朝报未至');
    }
  }, [applyView, toast]);

  useEffect(() => {
    const onRefresh = () => void refresh();
    window.addEventListener('tianbao:refresh', onRefresh);
    return () => window.removeEventListener('tianbao:refresh', onRefresh);
  }, [refresh]);

  const startGame = useCallback(
    async (seed: number) => {
      setBusy('start', true);
      try {
        const created = await api.createSession(SCENARIO_ID, seed);
        writeLS(LS_SESSION, created.id);
        writeLS(deltaKey(created.id), {});
        patch({ advice: [], receipt: null, lastTurn: null });
        const view = await api.view(created.id);
        applyView(created.id, view);
        patch({ screen: 'desk', panel: null });
      } catch (err) {
        toast.error(err, '开局失败');
      } finally {
        setBusy('start', false);
      }
    },
    [applyView, patch, setBusy, toast],
  );

  const openPanel = useCallback((p: PanelName, arg: string | null = null) => patch({ panel: p, panelArg: arg }), [patch]);
  const closePanel = useCallback(() => {
    abortRef.current?.abort();
    patch({ panel: null, panelArg: null });
  }, [patch]);

  const updateDraft = useCallback(
    (fn: (d: DraftStore) => DraftStore) => {
      setS((prev) => {
        const draft = fn(prev.draft);
        persistDraft(prev.sessionId, draft);
        return { ...prev, draft, receipt: prev.receipt?.confirmed ? prev.receipt : null };
      });
    },
    [persistDraft],
  );

  const adopt = useCallback(
    (memorial: MemorialItem, optionId: string) => {
      const opt = memorial.options.find((o) => o.id === optionId);
      if (!opt) return;
      updateDraft((d) => ({
        ...d,
        adopted: [
          ...d.adopted.filter((a) => a.memorial_id !== memorial.id),
          { memorial_id: memorial.id, option_id: opt.id, title: memorial.title, label: opt.label, hint: opt.hint },
        ],
      }));
    },
    [updateDraft],
  );
  const unadopt = useCallback(
    (memorialId: string) => updateDraft((d) => ({ ...d, adopted: d.adopted.filter((a) => a.memorial_id !== memorialId) })),
    [updateDraft],
  );
  const setSection = useCallback(
    (category: string, text: string) => updateDraft((d) => ({ ...d, sections: { ...d.sections, [category]: text } })),
    [updateDraft],
  );

  const draftEdict = useCallback(async () => {
    const { sessionId, draft } = ref.current;
    if (!sessionId) return;
    abortRef.current?.abort();
    const ctl = new AbortController();
    abortRef.current = ctl;
    setBusy('draft', true);
    try {
      const sections = Object.fromEntries(Object.entries(draft.sections).filter(([, v]) => v.trim()));
      const receipt = await api.draftEdict(
        sessionId,
        { sections, adopted: draft.adopted.map(({ memorial_id, option_id }) => ({ memorial_id, option_id })) },
        ctl.signal,
      );
      patch({ receipt });
    } catch (err) {
      toast.error(err, '诏令未能拟定');
    } finally {
      setBusy('draft', false);
    }
  }, [patch, setBusy, toast]);

  const cancelDraft = useCallback(() => {
    abortRef.current?.abort();
    const id = ref.current.sessionId;
    if (id) api.abort(id).catch(() => {});
    setBusy('draft', false);
  }, [setBusy]);

  const confirmEdict = useCallback(async () => {
    const { sessionId, receipt } = ref.current;
    if (!sessionId || !receipt) return;
    setBusy('confirm', true);
    try {
      const confirmed = await api.confirmEdict(sessionId, receipt.id);
      patch({ receipt: confirmed });
      const view = await api.view(sessionId);
      const draft = emptyDraft(view.state.turn);
      persistDraft(sessionId, draft);
      patch({ view, draft });
      toast.success('诏书已用宝颁行，有司奉诏。', '颁布');
    } catch (err) {
      toast.error(err, '颁布未成');
    } finally {
      setBusy('confirm', false);
    }
  }, [patch, persistDraft, setBusy, toast]);

  const clearReceipt = useCallback(() => patch({ receipt: null }), [patch]);

  const advanceTurn = useCallback(async () => {
    const { sessionId, view, receipt } = ref.current;
    if (!sessionId || !view) return;
    const lastEdict = receipt?.confirmed ? receipt : null;
    setBusy('turn', true);
    const before = resourceAmounts(view.state);
    try {
      const result = await api.advanceTurn(sessionId);
      const after = resourceAmounts(result.state);
      const deltas: Record<string, number> = {};
      for (const [k, v] of Object.entries(after)) if (k in before) deltas[k] = Math.round((v - before[k]) * 10) / 10;
      writeLS(deltaKey(sessionId), deltas);
      const nextView = await api.view(sessionId);
      const draft = emptyDraft(nextView.state.turn);
      persistDraft(sessionId, draft);
      patch({ lastTurn: result, lastEdict, deltas, view: nextView, draft, receipt: null, panel: 'result', panelArg: null, choiceDeferred: false });
    } catch (err) {
      toast.error(err, '推演受阻');
    } finally {
      setBusy('turn', false);
    }
  }, [patch, persistDraft, setBusy, toast]);

  const choose = useCallback(
    async (choiceId: string, optionId: string) => {
      const id = ref.current.sessionId;
      if (!id) return;
      setBusy(`choice`, true);
      try {
        await api.choose(id, choiceId, optionId);
        const view = await api.view(id);
        patch({ view });
        toast.success('圣意已决。', '抉择');
      } catch (err) {
        toast.error(err, '抉择未成');
      } finally {
        setBusy('choice', false);
      }
    },
    [patch, setBusy, toast],
  );

  const loadAdvice = useCallback(async () => {
    const id = ref.current.sessionId;
    if (!id) return;
    try {
      patch({ advice: await api.advice(id) });
    } catch (err) {
      toast.error(err, '谏言库未开');
    }
  }, [patch, toast]);

  const saveAdvice = useCallback(
    async (character: string, text: string, source: string) => {
      const id = ref.current.sessionId;
      if (!id) return;
      try {
        const saved = await api.saveAdvice(id, { character, text, source });
        patch((prev) => ({ advice: [...prev.advice, saved ?? { character, text, source }] }));
        toast.success('已录入谏言库，可于诏书中援引。', '存谏');
      } catch (err) {
        toast.error(err, '存谏未成');
      }
    },
    [patch, toast],
  );

  const rewind = useCallback(
    async (entryId: string) => {
      const id = ref.current.sessionId;
      if (!id) return;
      setBusy('rewind', true);
      try {
        await api.rewind(id, entryId);
        writeLS(deltaKey(id), {});
        const view = await api.view(id);
        patch({ receipt: null, lastTurn: null, deltas: {} });
        applyView(id, view);
        patch({ screen: view.outcome ? 'ending' : 'desk', panel: null });
        toast.success('时光回溯，史册改写自此页。', '回溯');
      } catch (err) {
        toast.error(err, '回溯未成');
      } finally {
        setBusy('rewind', false);
      }
    },
    [applyView, patch, setBusy, toast],
  );

  const value = useMemo<GameApi>(
    () => ({
      ...s,
      categories: s.scenario?.categories?.length ? s.scenario.categories : DEFAULT_CATEGORIES,
      setScreen: (screen) => patch({ screen, panel: null }),
      openPanel,
      closePanel,
      startGame,
      loadSession,
      refresh,
      adopt,
      unadopt,
      setSection,
      draftEdict,
      cancelDraft,
      confirmEdict,
      clearReceipt,
      advanceTurn,
      choose,
      deferChoice: (choiceDeferred) => patch({ choiceDeferred }),
      saveAdvice,
      loadAdvice,
      rewind,
      setMapLayer: (mapLayer) => patch({ mapLayer }),
      selectRegion: (selectedRegion) => patch({ selectedRegion }),
      exitToTitle: () => patch({ screen: 'title', panel: null, selectedRegion: null }),
    }),
    [s, patch, openPanel, closePanel, startGame, loadSession, refresh, adopt, unadopt, setSection, draftEdict, cancelDraft, confirmEdict, clearReceipt, advanceTurn, choose, saveAdvice, loadAdvice, rewind],
  );

  // the ending screen takes over whenever the engine reports an outcome
  useEffect(() => {
    if (s.view?.outcome && s.screen === 'desk' && s.panel !== 'result') patch({ screen: 'ending' });
  }, [s.view?.outcome, s.screen, s.panel, patch]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export const lastSessionId = () => readLS<string | null>(LS_SESSION, null);
