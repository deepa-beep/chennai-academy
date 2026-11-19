self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('pwa-store').then((cache) => {
      return cache.addAll(['/', '/static/manifest.json']);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => {
      return r || fetch(e.request);
    })
  );
});