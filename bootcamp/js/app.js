(function () {
  var PAGES = window.COURSE.pages;
  var KEY = "forge-progress-v1";
  var BACKUP_KEY = "forge-progress-backup-v1";
  var done = {};
  var currentId = null;

  try {
    var raw = localStorage.getItem(KEY);
    if (raw) done = JSON.parse(raw) || {};
  } catch (e) { done = {}; }

  var elNav = document.getElementById("nav"),
      elContent = document.getElementById("content"),
      elPager = document.getElementById("pager"),
      elBar = document.getElementById("progbar"),
      elTxt = document.getElementById("progtext"),
      elSearch = document.getElementById("search"),
      elSide = document.getElementById("sidebar"),
      elSaveTxt = document.getElementById("savetxt");

  /* ---------- storage ---------- */

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(done));
      // Redundant copy: if the primary key is ever lost or corrupted,
      // progress can still be recovered from the backup.
      localStorage.setItem(BACKUP_KEY, JSON.stringify({
        savedAt: new Date().toISOString(),
        done: done
      }));
    } catch (e) {}
    stampSaved();
  }

  function stampSaved() {
    if (!elSaveTxt) return;
    var n = new Date();
    var t = ("0" + n.getHours()).slice(-2) + ":" + ("0" + n.getMinutes()).slice(-2);
    var d = trackable().filter(function (p) { return done[p.id]; }).length;
    elSaveTxt.textContent = "Saved locally at " + t + " · " + d + " done · last backed up " + t;
  }

  function trackable() { return PAGES.filter(function (p) { return p.track !== false; }); }

  function updateProgress() {
    var t = trackable(), d = t.filter(function (p) { return done[p.id]; }).length;
    var pct = t.length ? Math.round((d / t.length) * 100) : 0;
    elBar.style.width = pct + "%";
    elTxt.textContent = pct + "% · " + d + "/" + t.length + " lessons";
    elTxt.setAttribute("aria-live", "polite");
    stampSaved();
  }

  /* ---------- progress backup / restore ---------- */

  function flash(msg, isError) {
    var t = document.createElement("div");
    t.className = "toast" + (isError ? " err" : "");
    t.setAttribute("role", "status");
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.classList.add("show"); }, 10);
    setTimeout(function () {
      t.classList.remove("show");
      setTimeout(function () { t.remove(); }, 300);
    }, 3200);
  }

  function exportProgress() {
    var payload = {
      app: "forge-bootcamp",
      version: 1,
      exportedAt: new Date().toISOString(),
      lessonsTotal: trackable().length,
      lessonsDone: trackable().filter(function (p) { return done[p.id]; }).length,
      done: done
    };
    var blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "forge-progress-" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
    flash("Progress file downloaded — keep it in your forge-notes repo.");
  }

  function importProgress(file) {
    var r = new FileReader();
    r.onload = function () {
      try {
        var data = JSON.parse(r.result);
        var incoming = data && data.done ? data.done : data;
        if (!incoming || typeof incoming !== "object") throw new Error("bad shape");
        var valid = {};
        PAGES.forEach(function (p) { if (incoming[p.id]) valid[p.id] = true; });
        if (!Object.keys(valid).length) throw new Error("no matching lessons");
        done = valid;
        save();
        updateProgress();
        buildNav();
        if (currentId) markActive(currentId);
        flash("Restored " + Object.keys(valid).length + " completed lessons.");
      } catch (e) {
        flash("That file did not contain valid FORGE progress.", true);
      }
    };
    r.readAsText(file);
  }

  /* ---------- code copy buttons ---------- */

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        resolve();
      } catch (e) { reject(e); }
    });
  }

  function addCopyButtons() {
    elContent.querySelectorAll("pre").forEach(function (pre) {
      if (pre.querySelector(".copybtn")) return;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "copybtn";
      b.textContent = "Copy";
      b.setAttribute("aria-label", "Copy code block to clipboard");
      b.onclick = function () {
        var code = pre.querySelector("code");
        copyText(code ? code.textContent : pre.textContent).then(function () {
          b.textContent = "Copied";
          b.classList.add("ok");
          setTimeout(function () { b.textContent = "Copy"; b.classList.remove("ok"); }, 1600);
        }, function () {
          b.textContent = "Select + Ctrl-C";
          setTimeout(function () { b.textContent = "Copy"; }, 2000);
        });
      };
      pre.appendChild(b);
    });
  }

  /* ---------- nav ---------- */

  function buildNav() {
    var groups = [], map = {};
    PAGES.forEach(function (p) {
      if (!map[p.group]) { map[p.group] = []; groups.push(p.group); }
      map[p.group].push(p);
    });
    elNav.innerHTML = groups.map(function (gname) {
      return '<div class="navgroup"><h4>' + gname + "</h4>" + map[gname].map(function (p) {
        return '<a class="navitem' + (done[p.id] ? " done" : "") + '" href="#' + p.id + '" data-id="' + p.id + '"' +
          (p.track === false ? ' title="Reference page — not counted in progress"' : "") + ">" +
          (p.track === false ? '<span class="tick none"></span>' : '<span class="tick"></span>') +
          '<span class="lbl">' + p.title + (p.sub ? "<small>" + p.sub + "</small>" : "") + "</span></a>";
      }).join("") + "</div>";
    }).join("");
    elNav.querySelectorAll(".navitem").forEach(function (n) {
      n.onclick = function (ev) {
        ev.preventDefault();
        go(n.dataset.id);
        if (window.innerWidth < 880) elSide.classList.remove("open");
      };
    });
  }

  function markActive(id) {
    elNav.querySelectorAll(".navitem").forEach(function (n) {
      var on = n.dataset.id === id;
      n.classList.toggle("active", on);
      if (on) n.setAttribute("aria-current", "page");
      else n.removeAttribute("aria-current");
    });
  }

  /* ---------- routing ---------- */

  function go(id, noHash) {
    var idx = PAGES.findIndex(function (p) { return p.id === id; });
    if (idx < 0) idx = 0;
    var p = PAGES[idx];
    currentId = p.id;
    var head = '<div class="eyebrow">' + (p.eyebrow || p.group) + "</div>" +
      '<h1 class="page">' + p.title + "</h1>" +
      (p.subtitle ? '<p class="subtitle">' + p.subtitle + "</p>" : "") +
      (p.chips ? '<div class="chiprow">' + p.chips.map(function (c, i) {
        return '<span class="chip ' + (i === 0 ? "acc" : i === 1 ? "b" : "") + '">' + c + "</span>";
      }).join("") + "</div>" : "");
    var body = '<div class="markdown">' + MD.render(p.body) + "</div>";
    var btn = p.track === false ? "" :
      '<button class="markbtn' + (done[p.id] ? " done" : "") + '" id="markbtn" aria-pressed="' + (!!done[p.id]) + '">' +
      (done[p.id] ? "✓ Completed — click to undo" : "Mark this lesson complete") + "</button>";
    elContent.innerHTML = head + body + btn;
    var mb = document.getElementById("markbtn");
    if (mb) mb.onclick = function () {
      done[p.id] = !done[p.id];
      if (!done[p.id]) delete done[p.id];
      save();
      updateProgress();
      buildNav();
      markActive(p.id);
      mb.classList.toggle("done", !!done[p.id]);
      mb.setAttribute("aria-pressed", String(!!done[p.id]));
      mb.textContent = done[p.id] ? "✓ Completed — click to undo" : "Mark this lesson complete";
      if (done[p.id] && PAGES[idx + 1]) setTimeout(function () { go(PAGES[idx + 1].id); }, 350);
    };
    addCopyButtons();
    var prev = PAGES[idx - 1], next = PAGES[idx + 1];
    elPager.innerHTML =
      (prev ? '<button data-go="' + prev.id + '" rel="prev"><span>◀ PREVIOUS</span>' + prev.title + "</button>" : "<div></div>") +
      (next ? '<button data-go="' + next.id + '" rel="next" style="text-align:right"><span>NEXT ▶</span>' + next.title + "</button>" : "<div></div>");
    elPager.querySelectorAll("button").forEach(function (b) { b.onclick = function () { go(b.dataset.go); }; });
    markActive(p.id);
    window.scrollTo(0, 0);
    if (!noHash) location.hash = id;
    document.title = p.title + " · FORGE";
  }

  /* ---------- search ---------- */

  elSearch.addEventListener("input", function () {
    var q = elSearch.value.trim().toLowerCase();
    if (q.length < 2) { if (location.hash) go(location.hash.slice(1), true); return; }
    var hits = PAGES.filter(function (p) {
      return (p.title + " " + (p.subtitle || "") + " " + p.body).toLowerCase().indexOf(q) >= 0;
    }).slice(0, 30);
    elContent.innerHTML = '<div class="eyebrow">SEARCH</div><h1 class="page">' + hits.length + ' result' + (hits.length === 1 ? "" : "s") + ' for "' + q + '"</h1>' +
      hits.map(function (p) {
        var i = p.body.toLowerCase().indexOf(q);
        var snip = i >= 0 ? p.body.substr(Math.max(0, i - 70), 190).replace(/[#*`>|]/g, "") : (p.subtitle || "");
        return '<div class="searchres" data-id="' + p.id + '"><b>' + p.title + "</b><p>" + p.group + " — …" + snip + "…</p></div>";
      }).join("");
    elPager.innerHTML = "";
    elContent.querySelectorAll(".searchres").forEach(function (r) {
      r.onclick = function () { elSearch.value = ""; go(r.dataset.id); };
    });
  });

  /* ---------- controls ---------- */

  document.getElementById("resetbtn").onclick = function () {
    if (confirm("Clear all lesson progress? This cannot be undone — export a backup file first if you want to keep it.")) {
      done = {};
      save();
      updateProgress();
      buildNav();
    }
  };
  document.getElementById("printbtn").onclick = function () { window.print(); };

  var exportBtn = document.getElementById("exportbtn");
  if (exportBtn) exportBtn.onclick = exportProgress;
  var importBtn = document.getElementById("importbtn");
  var importFile = document.getElementById("importfile");
  if (importBtn && importFile) {
    importBtn.onclick = function () { importFile.click(); };
    importFile.addEventListener("change", function () {
      if (importFile.files && importFile.files[0]) importProgress(importFile.files[0]);
      importFile.value = "";
    });
  }

  document.getElementById("menubtn").onclick = function () { elSide.classList.toggle("open"); };

  // Keyboard shortcut: "/" focuses search, like GitHub and every docs site.
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== elSearch) {
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      e.preventDefault();
      elSide.classList.add("open");
      elSearch.focus();
    }
    if (e.key === "Escape") elSide.classList.remove("open");
  });

  window.addEventListener("hashchange", function () {
    var id = location.hash.slice(1);
    if (id && PAGES.some(function (p) { return p.id === id })) go(id, true);
  });

  buildNav();
  updateProgress();
  go(location.hash ? location.hash.slice(1) : PAGES[0].id, true);

  /* ---------- offline support ---------- */

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  }

  window.addEventListener("offline", showOffline);
  window.addEventListener("online", hideOffline);

  function showOffline() {
    if (document.getElementById("offbanner")) return;
    var b = document.createElement("div");
    b.id = "offbanner";
    b.className = "offline";
    b.setAttribute("role", "status");
    b.textContent = "Offline — you are reading a saved copy. Everything still works.";
    document.body.appendChild(b);
  }
  function hideOffline() {
    var b = document.getElementById("offbanner");
    if (b) b.remove();
  }
  if (!navigator.onLine) showOffline();

  // Recover progress if the primary key was lost but the backup survived.
  if (!Object.keys(done).length) {
    try {
      var b = JSON.parse(localStorage.getItem(BACKUP_KEY) || "null");
      if (b && b.done && Object.keys(b.done).length) {
        done = b.done;
        save();
        updateProgress();
        buildNav();
        flash("Recovered your progress from a local backup.");
      }
    } catch (e) {}
  }
})();
