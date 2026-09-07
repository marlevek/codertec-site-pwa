const CACHE_NAME = "codertec-pwa-v6";

const OFFLINE_URL = "/offline.html";

const CORE_ASSETS = [
  "/",
  "/manifest.json",
  "/offline.html",

  // Idiomas
  "/pt/index.html",
  "/en/index.html",
  "/es/index.html",

  // Partials
  "/pt/partials/header.html",
  "/pt/partials/footer.html",
  "/en/partials/header_en.html",
  "/en/partials/footer_en.html",
  "/es/partials/header_es.html",
  "/es/partials/footer_es.html",

  // CSS essenciais
  "/static/css/estilos.css",
  "/static/css/chatbot.css",

  // JS essenciais
  "/static/js/include.js",
  "/static/js/btn_topo.js",
  "/static/js/chatbot-loader.js"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      await Promise.all(
        CORE_ASSETS.map(url =>
          fetch(url)
            .then(res => res.ok && cache.put(url, res))
            .catch(() => console.warn("Falha ao cachear:", url))
        )
      );
    })
  );
  self.skipWaiting();
});


// ACTIVATE
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(k => k !== CACHE_NAME && caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// FETCH
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  const pathname = new URL(event.request.url).pathname;
  if (/^\/(?:contact\.php|en\/contact_site_en\.php|es\/contacto_site_es\.php)(?:\/|$)/i.test(pathname)) return;


  // Não cachear vídeos, demos, mp4
  if (event.request.url.match(/\.(mp4|webm|ogg)$/)) {
    return;
  }

  // Navegação (HTML)
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache =>
            cache.put(event.request, copy)
          );
          return response;
        })
        .catch(() =>
          caches.match(event.request).then(r => r || caches.match(OFFLINE_URL))
        )
    );
    return;
  }


  // Assets
  event.respondWith(
    caches.match(event.request).then(cached => {
      const fetchPromise = fetch(event.request).then(networkResponse => {
        caches.open(CACHE_NAME).then(cache =>
          cache.put(event.request, networkResponse.clone())
        );
        return networkResponse;
      });
      return cached || fetchPromise;
    })
  );

});
