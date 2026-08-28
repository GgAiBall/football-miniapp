/* 足球记录分析 PWA Service Worker - 离线缓存核心资源 */
const CACHE = 'football-miniapp-v5';
const CORE = ['./', './index.html', './manifest.json', './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const url = e.request.url;
  // 竞彩 API：网络优先（实时赔率）
  if (url.includes('webapi.sporttery.cn')) {
    e.respondWith(fetch(e.request).then((r) => r.clone(), () => caches.match('./index.html')));
    return;
  }
  // 页面导航 index.html：网络优先（确保每次拿到最新版，修复 PWA 缓存旧版问题）
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((cc) => cc.put('./index.html', copy)).catch(() => {});
        return r;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }
  // 其他静态资源：缓存优先
  e.respondWith(
    caches.match(e.request).then((c) => c || fetch(e.request).then((r) => {
      if (e.request.method === 'GET' && new URL(url).origin === location.origin) {
        const copy = r.clone(); caches.open(CACHE).then((cc) => cc.put(e.request, copy)).catch(() => {});
      }
      return r;
    }))
  );
});
