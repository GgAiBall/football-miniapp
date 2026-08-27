/* 足球记录分析 PWA Service Worker - 离线缓存核心资源 */
const CACHE = 'football-miniapp-v1';
const CORE = ['./', './index.html', './manifest.json', './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

// 竞彩 API 请求走网络优先(数据需实时);本地资源缓存优先
self.addEventListener('fetch', (e) => {
  const url = e.request.url;
  if (url.includes('webapi.sporttery.cn')) {
    e.respondWith(fetch(e.request).then((r) => r.clone(), () => caches.match('./index.html')));
    return;
  }
  e.respondWith(
    caches.match(e.request).then((c) => c || fetch(e.request).then((r) => {
      if (e.request.method === 'GET' && new URL(url).origin === location.origin) {
        const copy = r.clone(); caches.open(CACHE).then((cc) => cc.put(e.request, copy));
      }
      return r;
    }))
  );
});
