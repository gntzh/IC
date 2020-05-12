/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "404.html",
    "revision": "9d6baf39ad1ee61d182fdfa939cc666b"
  },
  {
    "url": "about.html",
    "revision": "3d88cdac098e82014022bfb77b464f7d"
  },
  {
    "url": "assets/css/0.styles.0a437329.css",
    "revision": "44475278ecb4f1df05b0708b1db38755"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.5130bff5.js",
    "revision": "398e879c392507dc75ca67bd49470057"
  },
  {
    "url": "assets/js/11.8f92b553.js",
    "revision": "490d45d474fc03a2d100d24047797b0f"
  },
  {
    "url": "assets/js/12.a512bbd5.js",
    "revision": "e78da1662a92e48f0bb3356e154e4fbc"
  },
  {
    "url": "assets/js/2.6896a865.js",
    "revision": "54531fe7421304b9af6207b59ad7ad4c"
  },
  {
    "url": "assets/js/3.77384424.js",
    "revision": "b969c8720a2d7ff3cd63ac543e8a46d5"
  },
  {
    "url": "assets/js/4.406f636c.js",
    "revision": "4ee47831f0b35d9b795bc5c10907a02e"
  },
  {
    "url": "assets/js/5.3bc35277.js",
    "revision": "e9cc2a1f0783da9f730da8d25756222f"
  },
  {
    "url": "assets/js/6.383213df.js",
    "revision": "3820f1e0baf0899578833fcdb6c24456"
  },
  {
    "url": "assets/js/7.064cd68d.js",
    "revision": "5764dcfc1494cdf46fc20c4e83944d52"
  },
  {
    "url": "assets/js/8.828d53c8.js",
    "revision": "8f2b98ef27e5c9348f28468e32163601"
  },
  {
    "url": "assets/js/9.9328a374.js",
    "revision": "63a817af62ae4fced46c9619e718c023"
  },
  {
    "url": "assets/js/app.a49375eb.js",
    "revision": "b162e28ff54166b3a502d362c69ffe54"
  },
  {
    "url": "favicon-192x192.png",
    "revision": "eb601363c3ee26c5f5ed2cdeb9b68de3"
  },
  {
    "url": "favicon-512x512.png",
    "revision": "9a46650ea25fea0d2257f4d61eb1582c"
  },
  {
    "url": "favicon.png",
    "revision": "9c991f815b60cb4ec33e55e1ffe00925"
  },
  {
    "url": "guide/index.html",
    "revision": "d963a375512b42a534dae04036247fbc"
  },
  {
    "url": "guide/前端.html",
    "revision": "22beb139f8926767be966cc86a1bcd98"
  },
  {
    "url": "guide/后端.html",
    "revision": "3451a357c8e16de6370985b065316598"
  },
  {
    "url": "guide/部署.html",
    "revision": "28b056e26956a75da59883dcbaf90166"
  },
  {
    "url": "guide/部署参考.html",
    "revision": "8a304c76e7070d4f1b06b284e765e5ee"
  },
  {
    "url": "index.html",
    "revision": "c02d95e0973b46fad252cfe53fbdbbde"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
