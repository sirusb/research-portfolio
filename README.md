# Research Portfolio

This repository contains a lightweight, customizable academic portfolio website inspired by modern personal research and CV sites. It is designed so that content is managed through simple Markdown files rather than hardcoded HTML.

## Quick start

- Open `index.html` directly in a browser, or
- Serve the folder locally with a static server such as:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Customization

Update the content in the `content/` folder:

- `about.md` — short bio and research summary
- `cv.md` — CV or timeline details
- `publications.md` — papers, preprints, and talks
- `research.md` — ongoing projects and interests
- `blog.md` — updates and posts
- `contact.md` — contact details and links

The navigation and page order are controlled by `content/sections.json`.

## Notes

This version is intentionally simple and minimal so it is easy to maintain and adapt. It is suitable for a personal academic website with a strong research emphasis and a CV-focused layout.
