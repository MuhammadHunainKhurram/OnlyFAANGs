/// <reference path="config.js" />
const API = CONFIG.API_URL;
const SEEN_KEY   = "seenJobIds";
const APPLIED_KEY = "appliedJobIds";
const NEWMAP_KEY  = "newJobsMap";

const ONE_DAY_MS  = 24 * 60 * 60 * 1000;
const INTERN_KEYS = ["intern", "internship", "co-op", "apprentice"];

const UL      = document.getElementById("jobs");
const SEARCH  = document.getElementById("searchBox");
const BTN     = document.getElementById("internBtn");

let showInternsOnly = false;
let allJobs = [], applied = [], newMap = [];

// toggle handler ──────────────────────────────
BTN.addEventListener("click", () => {
  showInternsOnly = !showInternsOnly;
  BTN.classList.toggle("active", showInternsOnly);
  render();
});

// search handler
SEARCH.addEventListener("input", render);

// checkbox handler (unchanged) …
UL.addEventListener("change", async (e) => {
  if (!e.target.matches(".apply-box")) return;
  const id = e.target.closest("li").dataset.id;
  if (e.target.checked) {
    if (!applied.includes(id)) applied.push(id);
  } else {
    applied = applied.filter(x => x !== id);
  }
  await chrome.storage.local.set({ [APPLIED_KEY]: applied });
});

// initial fetch + render ──────────────────────
document.addEventListener("DOMContentLoaded", async () => {
  const store  = await chrome.storage.local.get([APPLIED_KEY, NEWMAP_KEY]);
  applied = store[APPLIED_KEY] || [];
  newMap  = store[NEWMAP_KEY]  || {};

  try {
    allJobs = await (await fetch(API)).json();
    render();
  } catch (err) {
    console.error(err);
    UL.innerHTML = "<li>Failed to load jobs.</li>";
  }
});

function render() {
  const term = SEARCH.value.trim().toLowerCase();

  UL.innerHTML = "";   // clear before re-inserting

  allJobs
    .filter(j => {
      const companyOK = term ? j.company.toLowerCase().includes(term) : true;
      const internOK  = showInternsOnly
        ? INTERN_KEYS.some(k => j.title.toLowerCase().includes(k))
        : true;
      return companyOK && internOK;
    })
    .forEach(j => {
      const isApplied = applied.includes(j.id);
      const isNew     = Date.now() - new Date(j.posted).getTime() < ONE_DAY_MS
                     || (j.id in newMap);

      UL.insertAdjacentHTML("beforeend", `
        <li data-id="${j.id}">
          <input type="checkbox" class="apply-box" ${isApplied ? "checked" : ""}/>
          ${isNew ? '<span class="new-badge"></span>' : ''}
          <div class="content">
            <div class="title">${j.company} — <a href="${j.url}" target="_blank">${j.title}</a></div>
            <div class="meta">${j.location || "Remote"} • ${new Date(j.posted).toLocaleDateString()}</div>
            <div class="meta">ID: ${j.id}</div>
          </div>
        </li>
      `);
    });

  if (!UL.children.length) UL.innerHTML = "<li>No jobs match filters.</li>";
}
