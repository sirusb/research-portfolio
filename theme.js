// Apply the saved theme before the first paint. Storage is optional.
(() => {
  let theme;
  try {
    theme = localStorage.getItem("portfolio-theme");
  } catch {
    /* Use system preference. */
  }
  if (!["light", "dark"].includes(theme)) {
    theme = window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }
  document.documentElement.dataset.theme = theme;
})();
