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
    "revision": "6055a607597baa48677ad7972f3ac71c"
  },
  {
    "url": "about.html",
    "revision": "25cdb7c0fb269bb7b5282805bea97dbd"
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
    "url": "assets/js/10.a862db66.js",
    "revision": "fd86895965c1467f37c0109dce3f9c3b"
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
    "url": "assets/js/7.0d9b7aa3.js",
    "revision": "a7e1bd8c32f578ca4a67aeb3799e1042"
  },
  {
    "url": "assets/js/8.0487c79f.js",
    "revision": "7b39d4aaac3d9d968c0193f634be596f"
  },
  {
    "url": "assets/js/9.92d70850.js",
    "revision": "a8f4affa6700d7de7f7fd3604db82557"
  },
  {
    "url": "assets/js/app.d3091c8a.js",
    "revision": "8f613b6198ede71e0c0ceffa943bc6c5"
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
    "revision": "34809673ee930be73760bd8dbd31a6bc"
  },
  {
    "url": "guide/前端.html",
    "revision": "3685c22b90e3af4bc50270340ba75252"
  },
  {
    "url": "guide/后端.html",
    "revision": "8641cc2860d003abe6e47d8f14f25cf6"
  },
  {
    "url": "guide/部署.html",
    "revision": "8686e619ab41bc4014f82a05c346927f"
  },
  {
    "url": "guide/部署参考.html",
    "revision": "d13708c1d44074a85e7d598acb8c3157"
  },
  {
    "url": "index.html",
    "revision": "f16fc7d51e881ad1716b8093233a85bb"
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
