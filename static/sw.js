const CACHE_NAME = 'almacen-medline-v1';
const URLS_TO_CACHE = [
  '/',
  '/dashboard',
  '/login',
  '/kiosco',
  '/static/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request)
    )
  );
});