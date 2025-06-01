importScripts('config.js');

const API = CONFIG.API_URL;
const PERIOD_MIN = 15;
const SEEN_KEY   = "seenJobIds";
const NEWMAP_KEY = "newJobsMap";

// ────────────── on install / update ──────────────
chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create("pollJobs", { periodInMinutes: PERIOD_MIN });
  // kick off immediately
  pollJobs();
});

// ────────────── scheduler callback ──────────────
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "pollJobs") pollJobs();
});

// ────────────── main polling fn ──────────────
async function pollJobs() {
  try {
    const res  = await fetch(API);
    if (!res.ok) throw new Error(res.statusText);
    const jobs = await res.json();

    // pull state
    const store = await chrome.storage.local.get([SEEN_KEY, NEWMAP_KEY]);
    const seen  = store[SEEN_KEY]   || [];
    const newMap = store[NEWMAP_KEY] || {};

    const now = Date.now();
    const oneHour = 60 * 60 * 1000;

    // purge expired entries (older than 1 h)
    for (const [id, ts] of Object.entries(newMap)) {
      if (now - ts > oneHour) delete newMap[id];
    }

    const unseen = jobs.filter(j => !seen.includes(j.id));

    if (unseen.length) {
      unseen.forEach(j => (newMap[j.id] = now));          // mark as new
      const head = unseen[0];
      chrome.notifications.create({
        iconUrl: "icons/48.png",
        type: "basic",
        title: `${unseen.length} new job${unseen.length > 1 ? "s" : ""}`,
        message: `${head.company}: ${head.title}`,
        priority: 1
      });
    }

    // persist (trim seen list to last 5000 ids)
    await chrome.storage.local.set({
      [SEEN_KEY]: [...seen, ...unseen.map(j => j.id)].slice(-5000),
      [NEWMAP_KEY]: newMap
    });
  } catch (err) {
    console.error("[OnlyFAANGs] poll failed:", err);
  }
}
