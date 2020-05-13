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
    "revision": "d3d179721af962fbd4716c941e546923"
  },
  {
    "url": "about.html",
    "revision": "fd6474d644ea0dbeee2fa88e1cabb5f7"
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
    "url": "assets/js/10.092b3731.js",
    "revision": "5a47e2bcdf09849c1c006d9f1f8cfa86"
  },
  {
    "url": "assets/js/11.7054579a.js",
    "revision": "99be45a440754a24492b0eaca652e1ca"
  },
  {
    "url": "assets/js/12.fe9ba30d.js",
    "revision": "3cfdf27b9bd25f3bd4910a013455d5a3"
  },
  {
    "url": "assets/js/13.62643193.js",
    "revision": "4ed3d02db1380fb3d63ecfaa21c0a4f5"
  },
  {
    "url": "assets/js/2.6896a865.js",
    "revision": "54531fe7421304b9af6207b59ad7ad4c"
  },
  {
    "url": "assets/js/3.e914d67c.js",
    "revision": "63d79517a4e20abcbb339e62adfced16"
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
    "url": "assets/js/7.a0ad6bce.js",
    "revision": "746dd27483cee5b4772b7d5961e09cba"
  },
  {
    "url": "assets/js/8.828d53c8.js",
    "revision": "8f2b98ef27e5c9348f28468e32163601"
  },
  {
    "url": "assets/js/9.30e92171.js",
    "revision": "81e0e942f078eb81230c6557fd6eb06c"
  },
  {
    "url": "assets/js/app.5973aebe.js",
    "revision": "5991ae457ca089e72774cb26a326b767"
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
    "revision": "a7ef7635d76cb928c351a37313513dce"
  },
  {
    "url": "guide/前端.html",
    "revision": "e0c99779701f0f0eb2a531d2f655c4e1"
  },
  {
    "url": "guide/功能需求.html",
    "revision": "7bda21d803c8139445956783472ea26c"
  },
  {
    "url": "guide/后端.html",
    "revision": "c063ef92d0f5480bf922661ed0ab0d33"
  },
  {
    "url": "guide/部署.html",
    "revision": "8e4658205e64c44991f6c7deb3c7a056"
  },
  {
    "url": "guide/部署参考.html",
    "revision": "130a9b07a986aeb2125f7b6f71c081d2"
  },
  {
    "url": "index.html",
    "revision": "7111e9af52584ff12d5b93f8ff06c2d8"
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
