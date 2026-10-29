# Mohamed Nadhir Djekidel — Research Portfolio

A responsive academic portfolio with an editorial layout, self-hosted typography, light and dark themes, searchable publications, and a downloadable CV. Content is based on [`docs/MND_CV_Oct2026.pdf`](docs/MND_CV_Oct2026.pdf).

The downloadable CV is a public copy with the phone number and telephone link removed.

The site uses plain HTML, CSS, and JavaScript. The generated `index.html` includes all content, so reading and navigation work without JavaScript or a network connection. JavaScript adds publication search, year filters, selected/all views, active navigation, and a saved theme preference.

## Preview

Open `index.html` directly, or run:

```sh
python3 -m http.server 8000
```

Visit <http://localhost:8000>.

## Update content

- `content/profile.json`: identity, links, CV path, research cards, appointments, education, and teaching entries.
- `content/publications.json`: all 45 CV outputs, with authors, years, venues, output types, and selected entries. Set `selected` to `true` to feature a publication. A verified `url` links directly to the paper; entries without one offer a clearly labeled Scholar search.
- `content/about.md`, `research.md`, `publications.md`, `teaching.md`, and `contact.md`: introductory copy.
- `content/cv.md`: expandable research methods and software, awards, intellectual property, technical skills, and languages.
- `content/sections.json`: navigation labels and order. Section IDs correspond to anchors in the template.
- `templates/index.html`: the page template.
- `styles.css`: colors, layout, responsive styles, and print styles.

After editing source content or the template, regenerate the page:

```sh
python3 scripts/build.py
```

The builder uses only Python’s standard library. Its Markdown subset supports paragraphs, lists, headings, bold, italics, and links. Raw HTML is escaped. Commit the generated `index.html` with the source changes. GitHub Pages also regenerates it during deployment.

## Deployment

The existing GitHub Actions workflow deploys the static site on pushes to `main` or a manual workflow run. There is no JavaScript build step, runtime framework, analytics service, or external font request.

## Design references

The design draws on [Minimal Light](https://github.com/yaoyao-liu/minimal-light)’s compact academic profile and publication hierarchy, [HugoBlox Academic CV](https://github.com/HugoBlox/hugo-theme-academic-cv)’s research and career organization, and [UI Skills](https://github.com/ibelick/ui-skills)’ guidance on restrained styling, native controls, contrast, and keyboard access. This is a custom implementation, without either theme as a dependency.

[Lora](https://fonts.google.com/specimen/Lora) and [Source Sans 3](https://fonts.google.com/specimen/Source+Sans+3) are self-hosted as Latin WOFF2 subsets. Their SIL Open Font License files are included in `assets/fonts/`.
