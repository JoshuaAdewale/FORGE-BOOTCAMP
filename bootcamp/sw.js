/* FORGE service worker — makes the whole curriculum work offline.
 *
 * Strategy:
 *   - Documents (index.html, 404.html, /data/*)  -> stale-while-revalidate:
 *     instant from cache, refreshed in the background, so edits appear on the
 *     next visit without ever showing a loading state.
 *   - Everything else (css, js, icons, images)    -> cache-first:
 *     these are immutable within a version, so serve from cache and refresh
 *     in the background.
 *
 * Bump VERSION to force every client to pick up a new cache.
 */
var VERSION = "forge-v2";
var PRECACHE = [
  "./",
  "./index.html",
  "./404.html",
  "./css/style.css",
  "./js/md.js",
  "./js/app.js",
  "./favicon.ico",
  "./favicon.png",
  "./apple-touch-icon.png",
  "./og-image.png",
  "./site.webmanifest",
  "./robots.txt",
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(VERSION).then(function (c) {
      // addAll() rejects entirely if any single request fails, so add
      // individually and swallow failures so one missing file cannot
      // break the whole install.
      return Promise.all(
        PRECACHE.map(function (u) {
          return c.add(new Request(u, { cache: "reload" })).catch(function () {});
        })
      );
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (k) { return k === VERSION ? null : caches.delete(k); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

function isDocument(url) {
  var p = url.pathname;
  return p === "/" || p.slice(-5) === ".html" || p.indexOf("/data/") >= 0;
}

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;

  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // never touch cross-origin

  // Documents and lesson data: stale-while-revalidate.
  if (isDocument(url)) {
    e.respondWith(
      caches.match(req).then(function (cached) {
        var network = fetch(req).then(function (res) {
          if (res && res.ok) {
            var copy = res.clone();
            caches.open(VERSION).then(function (c) { c.put(req, copy); });
          }
          return res;
        }).catch(function () { return cached; });
        return cached || network;
      })
    );
    return;
  }

  // Static assets: cache-first with background refresh.
  e.respondWith(
    caches.match(req).then(function (cached) {
      var network = fetch(req).then(function (res) {
        if (res && res.ok) {
          var copy = res.clone();
          caches.open(VERSION).then(function (c) { c.put(req, copy); });
        }
        return res;
      }).catch(function () { return cached; });
      return cached || network;
    })
  );
});

// Let the page tell the user an update is available.
self.addEventListener("message", function (e) {
  if (e.data === "skipWaiting") self.skipWaiting();
});
