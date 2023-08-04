// ==UserScript==
// @name         Dynasty Scans Proxy
// @namespace    https://nanoskript.dev/
// @version      0.1
// @description  Requests proxied images to make them load faster.
// @author       Nanoskript
// @match        https://dynasty-scans.com/chapters/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=dynasty-scans.com
// @downloadURL  https://github.com/nanoskript/dynasty-scans-proxy/raw/main/proxy.user.js
// @supportURL   https://github.com/nanoskript/dynasty-scans-proxy/issues
// @grant        none
// @run-at       document-body
// ==/UserScript==

(function () {
    'use strict';

    function replaceLink(s) {
        const base = "https://dynasty-scans-proxy.nanoskript.dev/dynasty-scans-image";
        const pattern = /\/system\/(.+)/;
        const match = s.match(pattern);
        if (!match) return s;

        const [_match, path] = match;
        return `${base}/${path}`;
    }

    // Hijack reader image sourcing.
    // This script is ran after the body element appears but
    // should complete before the DOM is fully loaded. Otherwise,
    // the hijack will be unsuccessful.
    $.fn.readerOriginal = $.fn.reader;
    $.fn.reader = (pages, i) => {
        // Replace links in page list.
        for (const page of pages) {
            page.image = replaceLink(page.image);
        }

        $("#reader").readerOriginal(pages, i);
    };

    $(() => {
        // Replace source in initial image.
        // Note: The request on page load will still be sent to origin servers.
        const image = document.querySelector("#image > img");
        image.src = replaceLink(image.src);
    });
})();