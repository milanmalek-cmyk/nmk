#!/usr/bin/env node
// Posnetki strani pri več širinah (namizje, tablica, mobilno) – za analizo in test odzivnosti.
//
// Uporaba:
//   node screenshot.mjs URL_ALI_POT IZHODNA_MAPA [--predpona obstojeca] [--sirine 1440,768,390]
//                       [--zaslon] [--jpg] [--ua brskalnik]
//
// Privzeto posname celo stran (fullPage); --zaslon posname samo prvi zaslon.
// Animacije so izklopljene (prefers-reduced-motion), da so vsi elementi vidni.
// Chromium: CHROMIUM_PATH ali prednameščen /opt/pw-browsers/chromium-*/chrome-linux/chrome.
import { chromium } from "playwright-core";
import { existsSync, mkdirSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const UA_BRSKALNIK = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36";

const args = process.argv.slice(2);
const opcija = (ime, privzeto) => {
  const i = args.indexOf(ime);
  return i >= 0 ? args.splice(i, 2)[1] : privzeto;
};
const zastavica = (ime) => {
  const i = args.indexOf(ime);
  return i >= 0 ? (args.splice(i, 1), true) : false;
};
const predpona = opcija("--predpona", "stran");
const sirine = opcija("--sirine", "1440,768,390").split(",").map(Number);
const ua = opcija("--ua", "");
const samoZaslon = zastavica("--zaslon");
const jpg = zastavica("--jpg");
const [cilj, izhod] = args;
if (!cilj || !izhod) {
  console.error("Uporaba: node screenshot.mjs URL_ALI_POT IZHODNA_MAPA [--predpona X] [--sirine 1440,768,390] [--zaslon] [--jpg]");
  process.exit(1);
}

function najdiChromium() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const koren = "/opt/pw-browsers";
  if (existsSync(koren)) {
    for (const d of readdirSync(koren).filter((d) => /^chromium-\d+$/.test(d)).sort().reverse()) {
      const p = join(koren, d, "chrome-linux", "chrome");
      if (existsSync(p)) return p;
    }
  }
  return undefined; // playwright-core poskusi sistemski brskalnik
}

const url = /^https?:\/\//.test(cilj) ? cilj : pathToFileURL(resolve(cilj)).href;
mkdirSync(izhod, { recursive: true });
const brskalnik = await chromium.launch({ executablePath: najdiChromium() });
try {
  for (const w of sirine) {
    const ctx = await brskalnik.newContext({
      viewport: { width: w, height: w < 600 ? 844 : 900 },
      deviceScaleFactor: w < 600 ? 2 : 1,
      isMobile: w < 600,
      hasTouch: w < 600,
      reducedMotion: "reduce",
      userAgent: ua === "brskalnik" ? UA_BRSKALNIK : undefined,
    });
    const stran = await ctx.newPage();
    await stran.goto(url, { waitUntil: "load", timeout: 60000 });
    // strani z analitiko ali odprtimi povezavami nikoli ne utihnejo – počakaj največ 10 s
    await stran.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    if (!samoZaslon) {
      // počasno drsenje sproži leno nalaganje slik
      await stran.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) {
          window.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 120));
        }
        window.scrollTo(0, 0);
      });
      await stran.waitForTimeout(500);
    }
    const datoteka = join(izhod, `${predpona}-${w}.${jpg ? "jpg" : "png"}`);
    await stran.screenshot({ path: datoteka, fullPage: !samoZaslon, ...(jpg ? { type: "jpeg", quality: 80 } : {}) });
    const sirokost = await stran.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    console.log(`${datoteka}${sirokost > 1 ? `  ⚠ vodoravni drsnik (+${sirokost}px)` : ""}`);
    await ctx.close();
  }
} finally {
  await brskalnik.close();
}
