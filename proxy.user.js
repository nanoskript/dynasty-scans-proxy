// ==UserScript==
// @name         Dynasty Scans Proxy
// @namespace    https://nanoskript.dev/
// @version      0.1
// @description  Requests proxied images to make them load faster and adds preload functionality.
// @author       Nanoskript
// @match        https://dynasty-scans.com/chapters/*
// @match        https://dynasty-scans.com/images/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=dynasty-scans.com
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
        // This request will normally be prematurely cancelled.
        const image = document.querySelector("#image > img, .image > img");
        image.src = replaceLink(image.src);
    });

    $(() => {
        // Add preload functionality.
        const pageList = document.querySelector(".pages-list");
        if (!pageList) return;

        // Add button.
        const button = document.createElement("button");
        button.style.marginBottom = "0.5rem";
        button.textContent = "Preload";

        button.onclick = async () => {
            button.disabled = true;
            for (let index = 0; index < pages.length; ++index) {
                // Style link.
                const link = document.querySelector(`a[href="#${index + 1}"]`);
                link.style.fontWeight = "bold";
                link.style.color = "slateblue";

                // Prefetch image.
                await fetch(pages[index].image, {mode: "no-cors"});
                link.style.color = "green";
            }

            // Enable button to indicate completion.
            button.disabled = false;
        };

        pageList.style.top = 0;
        pageList.insertAdjacentElement("afterbegin", button);
    });
})();
