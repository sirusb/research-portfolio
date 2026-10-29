(() => {
  "use strict";

  const root = document.documentElement;
  const themeButton = document.querySelector(".theme-toggle");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  let savedTheme;
  try {
    savedTheme = localStorage.getItem("portfolio-theme");
  } catch {
    /* Storage may be unavailable. */
  }
  if (!["light", "dark"].includes(savedTheme)) savedTheme = null;

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    const next = theme === "dark" ? "light" : "dark";
    themeButton?.setAttribute("aria-label", `Switch to ${next} theme`);
    themeButton?.setAttribute("title", `Switch to ${next} theme`);
  };
  applyTheme(savedTheme || (systemTheme.matches ? "dark" : "light"));
  if (themeButton) {
    themeButton.hidden = false;
    themeButton.addEventListener("click", () => {
      savedTheme = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(savedTheme);
      try {
        localStorage.setItem("portfolio-theme", savedTheme);
      } catch {
        /* Keep the session theme. */
      }
    });
  }
  systemTheme.addEventListener("change", (event) => {
    if (!savedTheme) applyTheme(event.matches ? "dark" : "light");
  });

  const navLinks = [...document.querySelectorAll("[data-section-link]")];
  const sections = [...document.querySelectorAll("[data-section]")];
  if ("IntersectionObserver" in window) {
    const visibleSections = new Map();
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) =>
          visibleSections.set(entry.target.id, entry.isIntersecting),
        );
        const current = sections.find((section) =>
          visibleSections.get(section.id),
        );
        if (!current) return;
        navLinks.forEach((link) => {
          if (link.hash === `#${current.id}`)
            link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      },
      { rootMargin: "-8% 0px -45% 0px", threshold: 0 },
    );
    sections.forEach((section) => observer.observe(section));
  }

  const publicationList = document.getElementById("publication-list");
  if (!publicationList) return;
  const publications = [...publicationList.querySelectorAll(".publication")];
  const search = document.getElementById("publication-search");
  const yearFilter = document.getElementById("publication-year");
  const status = document.getElementById("publication-status");
  const toggle = document.getElementById("publication-toggle");
  const clearButton = document.getElementById("publication-clear");
  const emptyState = document.getElementById("publication-empty");
  let showAll = false;

  const filterPublications = () => {
    const query = search.value.trim().toLocaleLowerCase();
    const year = yearFilter.value;
    const filtering = Boolean(query || year);
    let count = 0;
    publications.forEach((publication) => {
      const matchesQuery = publication.textContent
        .toLocaleLowerCase()
        .includes(query);
      const matchesYear = !year || publication.dataset.year === year;
      const matchesSelection =
        filtering || showAll || publication.dataset.selected === "true";
      publication.hidden = !(matchesQuery && matchesYear && matchesSelection);
      if (!publication.hidden) count += 1;
    });
    status.textContent = filtering
      ? `${count} of ${publications.length} outputs match`
      : showAll
        ? `All ${publications.length} research outputs`
        : `${count} selected research outputs`;
    emptyState.hidden = count > 0;
    clearButton.hidden = !filtering;
    toggle.hidden = filtering || (publications.length === count && !showAll);
    toggle.textContent = showAll
      ? "Show selected outputs"
      : `View all ${publications.length} outputs`;
    toggle.setAttribute("aria-expanded", String(showAll));
  };

  document
    .querySelectorAll("[data-publication-controls]")
    .forEach((element) => {
      element.hidden = false;
    });
  search.addEventListener("input", filterPublications);
  yearFilter.addEventListener("change", filterPublications);
  toggle.addEventListener("click", () => {
    showAll = !showAll;
    filterPublications();
    if (!showAll) {
      document
        .getElementById("publications")
        .scrollIntoView({ block: "start" });
      search.focus({ preventScroll: true });
    }
  });
  const clearFilters = () => {
    search.value = "";
    yearFilter.value = "";
    filterPublications();
    search.focus({ preventScroll: true });
  };
  clearButton.addEventListener("click", clearFilters);
  document
    .getElementById("publication-reset")
    .addEventListener("click", clearFilters);
  filterPublications();
})();
