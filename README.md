# dynasty-scans-proxy

Image proxy for [Dynasty Scans](https://dynasty-scans.com/) that is geographically close to Dynasty Scans' servers and
compresses images into the WebP format.

## Deprecation notice

As of 4 May 2024, Dynasty Scans now serves images in the WebP format:

> Image conversion from .png/.jpg to .webp for web view to save on bandwidth when delivering images on the website. This
> means downloaded archives are untouched and remain exactly as the scanlator/volunteer uploaded it.

As of 24 May 2024, the proxy server is no longer active and requests are routed
directly to Dynasty Scans' servers. It is no longer beneficial to use this script.
If you do not use the preload functionality, you should remove it.

## Why use this?

If you are not close to Europe (where Dynasty Scans' servers are located), the time it takes to load an image may be
limited by the bandwidth of the connection to the origin servers. This proxy compresses the image before sending it to
your browser which may significantly improve image loading speeds.

In graphical terms, requesting an image with a direct connection to Dynasty Scans would look like:

```
Server --------------------------> You
```

Whereas, requesting an image with a proxied connection would look like:

```
Server ==> Proxy --------> You
```

Furthermore, the proxy operates behind Cloudflare which also caches the
compressed images. This means requesting the same image more than once
is fast.

## How do I use this?

1. Install the [Tampermonkey](https://www.tampermonkey.net/) extension for your browser.
2. Click [here](https://github.com/nanoskript/dynasty-scans-proxy/raw/main/proxy.user.js) to download the userscript.
3. Click on install.
4. You're done!

If you're experiencing issues, or if the proxy is offline, disable the userscript in Tampermonkey's settings by clicking
on
Tampermonkey's icon near your browser's address bar. You can check if the proxy server is online
by checking if [this page](https://dynasty-scans-proxy.nsk.sh/) loads.

As an additional feature, the userscript adds a `Preload` button that loads all the images for a chapter in the
background:

<img src="docs/preload.png" width="384px">

The image that is currently loading is colored in blue. Images that have been preloaded are colored in green. If you
just want the preloading functionality
without the proxying, here is the preloading script in the bookmarklet format:

```js
javascript:(async () => {
  for (let e = 0; e < pages.length; ++e) {
    let l = document.querySelector(`a[href="#${e + 1}"]`);
    l.style.fontWeight = "bold", l.style.color = "slateblue", await fetch(pages[e].image, {mode: "no-cors"}), l.style.color = "green"
  }
})();
```

## Caveats

The images do not use lossless compression. This means there may be very minor image degradation compared to requesting
images directly. While the WebP format does support lossless encoding, the resultant file size increases are not
considered to be a reasonable compromise.

## Benchmark results

These results were obtained by running `pdm run bench.py` locally.
The amount of time saved is **highly dependent on your geographical location** and your proximity to Dynasty Scans'
servers.

```
001     ... -6.04s (6% in size)
002     ... -3.45s (32% in size)
003     ... -3.93s (31% in size)
004     ... -4.00s (38% in size)
005     ... -1.54s (19% in size)
006     ... -3.26s (30% in size)
007     ... -0.29s (31% in size)
008     ... -3.48s (29% in size)
009     ... -1.98s (30% in size)
010     ... -3.55s (33% in size)
011     ... -3.94s (33% in size)
012     ... -5.95s (32% in size)
013     ... -3.16s (35% in size)
014     ... -2.96s (31% in size)
015     ... -3.01s (31% in size)
016     ... -2.94s (29% in size)
017     ... -3.04s (29% in size)
018     ... +0.95s (22% in size)
019     ... -3.67s (23% in size)
020     ... -1.32s (53% in size)
021     ... -1.83s (32% in size)
022     ... -3.83s (3% in size)
credits ... -1.95s (18% in size)
---
Total difference: -68.18s
Average: -2.96s
```

On average, requesting an image from the proxy is approximately 3 seconds faster.
The amount of time saved is proportional to the size of the original image file.

## Disclaimer

This project is not affiliated with Dynasty Scans. No images are stored
on the proxy's servers.
