const API = CONFIG.API_URL;
const SEEN_KEY  = "seenJobIds";
const APPLIED_KEY = "appliedJobIds";
const NEWMAP_KEY = "newJobsMap";

document.addEventListener("DOMContentLoaded", async () => {
  const ul = document.getElementById("jobs");
  const store = await chrome.storage.local.get([APPLIED_KEY, NEWMAP_KEY]);
  const applied = store[APPLIED_KEY] || [];
  const newMap  = store[NEWMAP_KEY]  || {};

  try {
    const jobs = await (await fetch(API)).json();
    if (!jobs.length) {
      ul.innerHTML = "<li>No jobs yet.  Check back soon.</li>";
      return;
    }

    ul.innerHTML = jobs.map(j => {
        const isApplied = applied.includes(j.id);
        const ONE_DAY  = 24 * 60 * 60 * 1000;
        const isNew     =
            (Date.now() - new Date(j.posted).getTime() < ONE_DAY)   // posted < 24 h
        || (j.id in newMap);                                       // keep old logic

        return `
            <li data-id="${j.id}">
            <input type="checkbox" class="apply-box" ${isApplied ? "checked" : ""}/>
            ${isNew ? '<span class="new-badge"></span>' : ''}
            <div class="content">
                <div class="title">${j.company} — <a href="${j.url}" target="_blank">${j.title}</a></div>
                <div class="meta">${j.location || "Remote"} • ${new Date(j.posted).toLocaleDateString()}</div>
                <div class="meta">ID: ${j.id}</div>
            </div>
            </li>
        `;
    }).join("");

    // ───── checkbox handler ─────
    ul.addEventListener("change", async (e) => {
      if (e.target.matches(".apply-box")) {
        const id = e.target.closest("li").dataset.id;
        let list = await chrome.storage.local.get(APPLIED_KEY);
        list = list[APPLIED_KEY] || [];
        if (e.target.checked) {
          if (!list.includes(id)) list.push(id);
        } else {
          list = list.filter(x => x !== id);
        }
        await chrome.storage.local.set({ [APPLIED_KEY]: list });
      }
    });

  } catch (err) {
    console.error(err);
    ul.innerHTML = "<li>Failed to load jobs.</li>";
  }
});
