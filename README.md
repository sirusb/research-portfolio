# Mohamed Nadhir Djekidel — Research Portfolio

A responsive academic portfolio with a white background, self-hosted Source Sans Pro typography, an optional dark theme, searchable publications, and a downloadable CV. Content is based on [`docs/MND_CV_Oct2026.pdf`](docs/MND_CV_Oct2026.pdf).

The downloadable CV is a public copy with the phone number and telephone link removed.

The site uses plain HTML, CSS, and JavaScript. The generated `index.html` includes all content, so reading and navigation work without JavaScript or a network connection. JavaScript adds publication search, year filters, selected/all views, active navigation, and a saved theme preference. The white theme is the default, including on devices set to dark mode.

## Preview

Open `index.html` directly, or run:

```sh
python3 -m http.server 8000
```

Visit <http://localhost:8000>.

## Update content

- `content/profile.json`: identity, links, CV path, research cards, appointments, education, and teaching entries.
- `content/publications.json`: publication and software records, with authors, years, venues, output types, and selected entries. Set `selected` to `true` to feature a publication. A verified `url` links directly to the paper; entries without one offer a clearly labeled Scholar search.
- `content/about.md`, `research.md`, `publications.md`, `teaching.md`, and `contact.md`: introductory copy.
- `content/cv.md`: expandable research methods and software, awards, intellectual property, technical skills, and languages.
- `content/mercor.md`: a brief summary of bioinformatics contributions to LLM training and evaluation at Mercor.
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

[Source Sans Pro](https://github.com/adobe-fonts/source-sans), also used by [Hugging Face](https://huggingface.co/), is self-hosted in regular, semibold, and bold Latin WOFF2 subsets. Its SIL Open Font License is included in `assets/fonts/`.
