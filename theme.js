// Use the white theme by default; remember only explicit theme choices.
(() => {
  let theme = "light";
  try {
    const saved = localStorage.getItem("portfolio-theme-v2");
    if (["light", "dark"].includes(saved)) theme = saved;
  } catch {
    /* Keep the default white theme when storage is unavailable. */
  }
  document.documentElement.dataset.theme = theme;
})();
