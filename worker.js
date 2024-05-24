// Fallback worker proxy script in case older versions of the
// userscript are still in use.
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const [_string, path] = url.pathname.match(/\/dynasty-scans-image\/(.+)/);
    return fetch(`https://dynasty-scans.com/system/${path}?${url.search}`);
  },
};
