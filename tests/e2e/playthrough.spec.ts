// G5 GUI playthrough: plays a whole game through the real UI against a running engine
// (E2E_API_BASE), adopting one option per memorial each season (PLAYTHROUGH_PICK=first|last),
// until the ending screen. Every season it also checks that the result scroll's 「下一季」 is
// really clickable and that no raw entity id is shown. Screenshots of every season's result
// scroll land in playtests/screens/playthrough/.
import { expect, test, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { REAL, settle, startGame, watchErrors } from './helpers';

const SHOTS = path.resolve(__dirname, '..', '..', 'playtests', 'screens', 'playthrough');
const MAX_SEASONS = 30;
const ID_TOKEN = /\b(tang|yan|tubo|nanzhao|khitan_xi|dashi|huihe)\b|[a-z]+_[a-z0-9_]+/;

test.skip(!REAL, 'needs a real engine (E2E_API_BASE)');
test.setTimeout(40 * 60_000);

const visible = (page: Page, id: string) => page.getByTestId(id).isVisible().catch(() => false);

/** Resolves any pending event choice (modal or the deferred badge on the desk). */
async function settleChoices(page: Page, pick: 'first' | 'last') {
  for (let guard = 0; guard < 6; guard++) {
    if (!(await visible(page, 'choice.root')) && (await visible(page, 'desk.choiceBadge'))) {
      await page.getByTestId('desk.choiceBadge').click();
      await expect(page.getByTestId('choice.root')).toBeVisible();
    }
    if (!(await visible(page, 'choice.root'))) return;
    await settle(page, 400);
    const options = page.locator('[data-testid^="choice.option."]:enabled');
    await expect(options.first()).toBeVisible();
    await (pick === 'last' ? options.last() : options.first()).click();
    await expect(page.getByTestId('choice.root')).toHaveCount(0, { timeout: 20_000 });
    await settle(page, 400);
  }
}

/** The element is on screen and is what a click at its centre would hit. */
async function clickable(page: Page, testid: string): Promise<string> {
  return page.getByTestId(testid).evaluate((el) => {
    const r = el.getBoundingClientRect();
    if (r.bottom > innerHeight || r.right > innerWidth || r.top < 0 || r.left < 0) return 'outside viewport';
    const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return hit && (hit === el || el.contains(hit)) ? 'ok' : `covered by ${hit?.className}`;
  });
}

test('a full game can be played through the UI to an ending @playthrough', async ({ page }) => {
  const errors = watchErrors(page);
  const pick = process.env.PLAYTHROUGH_PICK === 'last' ? 'last' : 'first';
  fs.mkdirSync(SHOTS, { recursive: true });
  await startGame(page);

  for (let season = 0; season < MAX_SEASONS; season += 1) {
    if (await visible(page, 'ending.root')) break;
    await settleChoices(page, pick);

    // Read the memorials and adopt one option per item.
    await page.getByTestId('desk.memorialBook').click();
    await expect(page.getByTestId('memorial.root')).toBeVisible();
    await settle(page, 700);
    const items = page.locator('[data-testid^="memorial.item."]');
    const count = await items.count();
    for (let i = 0; i < count; i += 1) {
      const item = items.nth(i);
      const itemId = (await item.getAttribute('data-testid'))!.slice('memorial.item.'.length);
      if (await item.isEnabled()) await item.click(); // the selected item is rendered disabled
      const options = page.locator(`[data-testid^="memorial.option.${itemId}."]`);
      await expect(options.first()).toBeVisible();
      await (pick === 'last' ? options.last() : options.first()).click();
    }
    expect(await clickable(page, 'memorial.toEdict'), 'memorial.toEdict').toBe('ok');
    if (count > 0) {
      await page.getByTestId('memorial.toEdict').click();
      await expect(page.getByTestId('edict.root')).toBeVisible();
      await settle(page, 800);
      await page.getByTestId('edict.preview').click();
      await expect(page.getByTestId('edict.receipt')).toBeVisible({ timeout: 60_000 });
      await page.getByTestId('edict.promulgate').click();
      await expect(page.getByTestId('edict.advance')).toBeVisible({ timeout: 60_000 });
      await page.getByTestId('edict.advance').click();
    } else {
      await page.getByTestId('memorial.done').click();
      await expect(page.getByTestId('memorial.root')).toHaveCount(0);
      await page.getByTestId('desk.advance').click();
      if (await visible(page, 'desk.advance.confirm')) await page.getByTestId('desk.advance.confirm').click();
    }

    // Result scroll (or the ending screen if the season ended the game).
    const result = page.getByTestId('result.root');
    const ending = page.getByTestId('ending.root');
    await expect(result.or(ending)).toBeVisible({ timeout: 120_000 });
    await settle(page, 1200);
    await page.screenshot({ path: path.join(SHOTS, `${pick}-season-${String(season + 1).padStart(2, '0')}.png`) });
    if (await result.isVisible()) {
      const shown = await result.innerText();
      expect(shown.match(ID_TOKEN)?.[0] ?? null, `raw id on the result scroll (season ${season + 1})`).toBeNull();
      await expect(page.getByTestId('result.figure').or(page.locator('.result--no-figure'))).toBeVisible();
      await expect(page.locator('.result-figure.is-pending'), 'illustration decided').toHaveCount(0, { timeout: 15_000 });
      expect(await clickable(page, 'result.next'), `result.next clickable (season ${season + 1})`).toBe('ok');
      await page.getByTestId('result.next').click();
      await expect(result).toHaveCount(0);
    }
    await settle(page, 500);
  }

  await expect(page.getByTestId('ending.root')).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId('ending.title')).not.toBeEmpty();
  await settle(page, 1500);
  const title = (await page.getByTestId('ending.title').innerText()).trim();
  test.info().annotations.push({ type: 'ending', description: `${pick}: ${title}` });
  console.log(`[playthrough ${pick}] ending: ${title}`);
  await page.screenshot({ path: path.join(SHOTS, `${pick}-ending.png`) });
  expect(errors).toEqual([]);
});
