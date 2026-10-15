// G5 GUI playthrough: plays a whole game through the real UI against a running engine
// (E2E_API_BASE), adopting one option per memorial each season, until the ending screen.
// Screenshots of every season's result scroll land in playtests/screens/playthrough/.
import { expect, test } from '@playwright/test';
import path from 'node:path';
import { REAL, settle, startGame, watchErrors } from './helpers';

const SHOTS = path.resolve(__dirname, '..', '..', 'playtests', 'screens', 'playthrough');
const MAX_SEASONS = 26;

test.skip(!REAL, 'needs a real engine (E2E_API_BASE)');
test.setTimeout(30 * 60_000);

test('a full game can be played through the UI to an ending @playthrough', async ({ page }) => {
  const errors = watchErrors(page);
  const pick = process.env.PLAYTHROUGH_PICK === 'last' ? 'last' : 'first';
  await startGame(page);

  for (let season = 0; season < MAX_SEASONS; season += 1) {
    if (await page.getByTestId('ending.root').isVisible()) break;

    // Pending event choices first.
    if (await page.getByTestId('choice.root').isVisible()) {
      await page.locator('[data-testid^="choice.option."]').first().click();
      await expect(page.getByTestId('choice.root')).toHaveCount(0, { timeout: 15_000 });
    }
    if (await page.getByTestId('desk.choiceBadge').isVisible()) {
      await page.getByTestId('desk.choiceBadge').click();
      await expect(page.getByTestId('choice.root')).toBeVisible();
      await page.locator('[data-testid^="choice.option."]').first().click();
      await expect(page.getByTestId('choice.root')).toHaveCount(0, { timeout: 15_000 });
    }

    // Read the memorials and adopt one option per item.
    await page.getByTestId('desk.memorialBook').click();
    await expect(page.getByTestId('memorial.root')).toBeVisible();
    const items = page.locator('[data-testid^="memorial.item."]');
    const count = await items.count();
    for (let i = 0; i < count; i += 1) {
      const item = items.nth(i);
      const itemId = (await item.getAttribute('data-testid'))!.slice('memorial.item.'.length);
      if (await item.isEnabled()) await item.click(); // the selected item is rendered disabled
      const options = page.locator(`[data-testid^="memorial.option.${itemId}."]`);
      await expect(options.first()).toBeVisible();
      const target = pick === 'last' ? options.last() : options.first();
      await target.click();
    }
    if (count > 0) {
      await page.getByTestId('memorial.toEdict').click();
      await expect(page.getByTestId('edict.root')).toBeVisible();
      await page.getByTestId('edict.preview').click();
      await expect(page.getByTestId('edict.receipt')).toBeVisible({ timeout: 30_000 });
      await page.getByTestId('edict.promulgate').click();
      await expect(page.getByTestId('edict.advance')).toBeVisible({ timeout: 30_000 });
      await page.getByTestId('edict.advance').click();
    } else {
      await page.keyboard.press('Escape');
      await page.getByTestId('desk.advance').click();
      if (await page.getByTestId('desk.advance.confirm').isVisible()) {
        await page.getByTestId('desk.advance.confirm').click();
      }
    }

    // Result scroll (or the ending screen if the season ended the game).
    const result = page.getByTestId('result.root');
    const ending = page.getByTestId('ending.root');
    await expect(result.or(ending)).toBeVisible({ timeout: 60_000 });
    await settle(page, 500);
    await page.screenshot({ path: path.join(SHOTS, `${pick}-season-${String(season + 1).padStart(2, '0')}.png`) });
    if (await result.isVisible()) {
      await page.getByTestId('result.next').click();
      await expect(result).toHaveCount(0);
    }
    await settle(page, 300);
  }

  await expect(page.getByTestId('ending.root')).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId('ending.title')).not.toBeEmpty();
  await page.screenshot({ path: path.join(SHOTS, `${pick}-ending.png`) });
  expect(errors).toEqual([]);
});
