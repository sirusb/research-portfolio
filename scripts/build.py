#!/usr/bin/env python3
"""Render the portfolio using only Python's standard library.

Content is escaped by default. Markdown supports paragraphs, headings, lists,
strong/emphasis, and links; raw HTML is intentionally not supported.
"""
from html import escape
import json
from pathlib import Path
import re
from string import Template
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'

ICONS = {
    'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    'external': '<path d="M7 17 17 7M7 7h10v10"/>',
    'download': '<path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'pin': '<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    'moon': '<path d="M20.5 13A8.8 8.8 0 0 1 11 3.5a9 9 0 1 0 9.5 9.5Z"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6-10-6Zm4 3v6c4 3 8 3 12 0v-6M22 9v8"/>',
    'github': '<path d="M9 19c-4.3 1.3-4.3-2.2-6-2.6M15 22v-3.6c0-1 .1-1.4-.5-2 3.2-.4 6.5-1.5 6.5-7.1a5.5 5.5 0 0 0-1.5-3.8c.2-1.3.1-2.6-.5-3.5 0 0-1.2-.4-4 1.5a13.5 13.5 0 0 0-7 0C5.2 1.6 4 2 4 2c-.6.9-.7 2.2-.5 3.5A5.5 5.5 0 0 0 2 9.3c0 5.6 3.3 6.7 6.5 7.1-.6.6-.5 1.4-.5 2V22"/>',
    'linkedin': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7.5 10v7m0-10v.1M11 17v-7m0 3a3 3 0 0 1 6 0v4"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    'omics': '<circle cx="12" cy="12" r="3"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="m6.5 6.5 3.3 3.3m4.4 4.4 3.3 3.3m0-11-3.3 3.3m-4.4 4.4-3.3 3.3"/>',
    'cells': '<path d="M18 3c-12 0-12 18 0 18M6 3c12 0 12 18 0 18M7 4h10M9 8h6m-6 8h6M7 20h10M9 12h6"/>',
    'compute': '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="m8 8-3 3 3 3m8-6 3 3-3 3m-3-7-2 8M8 22h8m-4-4v4"/>',
}


def icon(name, extra=''):
    return f'<svg class="icon {escape(extra)}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def safe_url(value):
    if urlsplit(value).scheme not in ('', 'https', 'http', 'mailto', 'tel'):
        raise ValueError(f'Unsupported link scheme: {value}')
    if value.startswith('//'):
        raise ValueError('Protocol-relative links are not supported')
    return escape(value, quote=True)


def inline(value):
    # Keep URLs separate so query-string ampersands are escaped exactly once.
    pieces = re.split(r'(\[[^\]]+\]\([^)]+\))', value)
    rendered = []
    for piece in pieces:
        link = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', piece)
        if link:
            rendered.append(f'<a href="{safe_url(link[2])}">{escape(link[1])}</a>')
        else:
            rendered.append(escape(piece))
    value = ''.join(rendered)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', value)


def markdown(text):
    output, paragraph, items = [], [], []

    def flush():
        if paragraph:
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
        if items:
            output.append('<ul>' + ''.join(f'<li>{inline(item)}</li>' for item in items) + '</ul>')
            items.clear()

    for line in text.splitlines():
        line = line.strip()
        if not line:
            flush()
        elif line.startswith('- '):
            if paragraph:
                flush()
            items.append(line[2:])
        elif re.match(r'^#{1,6} ', line):
            flush()
            heading, title = line.split(' ', 1)
            level = max(3, min(len(heading), 6))
            output.append(f'<h{level}>{inline(title)}</h{level}>')
        else:
            if items:
                flush()
            paragraph.append(line)
    flush()
    return '\n'.join(output)


def read_markdown(name):
    return markdown((CONTENT / name).read_text())


def build():
    profile = json.loads((CONTENT / 'profile.json').read_text())
    publications = json.loads((CONTENT / 'publications.json').read_text())
    sections = json.loads((CONTENT / 'sections.json').read_text())
    ids = [section['id'] for section in sections]
    if len(set(ids)) != len(ids):
        raise ValueError('Section IDs must be unique')
    if len({item['id'] for item in publications}) != len(publications):
        raise ValueError('Publication IDs must be unique')
    if not (ROOT / profile['cv']).is_file():
        raise ValueError('The downloadable CV is missing')

    values = {key: escape(str(value)) for key, value in profile.items() if isinstance(value, (str, int))}
    values['nav'] = '\n'.join(f'<a href="#{escape(s["id"])}" data-section-link>{escape(s["label"])}</a>' for s in sections if s['id'] in ('about', 'research', 'publications', 'cv'))
    values['sidebar_nav'] = '\n'.join(f'<a href="#{escape(s["id"])}" data-section-link><span aria-hidden="true">{i:02}</span>{escape(s["label"])}</a>' for i, s in enumerate(sections, 1))
    values['topics'] = ''.join(f'<li>{escape(topic)}</li>' for topic in profile['topics'])
    values['institutions'] = ''.join(f'<span>{escape(institution)}</span>' for institution in profile['institutions'])
    values['about'] = read_markdown('about.md')
    values['research_intro'] = read_markdown('research.md')
    values['publication_intro'] = read_markdown('publications.md')
    values['teaching_intro'] = read_markdown('teaching.md')
    values['contact_intro'] = read_markdown('contact.md')
    values['research_cards'] = '\n'.join(f'''<article class="research-card">
      {icon(r['icon'], 'research-art')}
      <h3>{escape(r['title'])}</h3><p>{escape(r['description'])}</p>
      <p class="research-keywords">{escape(r['keywords'])}</p>
    </article>''' for r in profile['research'])

    publication_html = []
    for p in publications:
        url = p.get('url') or f'https://scholar.google.com/scholar?q={quote(p["title"])}'
        link = safe_url(url)
        authors = escape(p['authors'])
        authors = re.sub(r'Djekidel MN|Djekidel N(?=[, ])|Nadhir Djekidel, M\.|Nadhir, D\.M\.', lambda m: f'<strong>{m[0]}</strong>', authors)
        kind = '' if p['type'] == 'Article' else f'<span class="publication-type">· {escape(p["type"])}</span>'
        link_label = 'Read paper' if p.get('url') else 'Find on Scholar'
        publication_html.append(f'''<li class="publication" data-year="{p['year']}" data-selected="{str(p.get('selected', False)).lower()}">
          <span class="publication-year">{p['year']}</span>
          <article><h3><a href="{link}" target="_blank" rel="noopener noreferrer">{escape(p['title'])}<span class="sr-only"> (opens in a new tab)</span></a></h3>
          <p class="publication-authors">{authors}</p>
          <div class="publication-meta"><p class="publication-venue">{escape(p['venue'])}{kind}</p>
          <a class="text-link" href="{link}" target="_blank" rel="noopener noreferrer" aria-label="{link_label}: {escape(p['title'], quote=True)} (opens in a new tab)">{link_label}{icon('external')}</a></div>
          </article></li>''')
    values['publications'] = '\n'.join(publication_html)
    values['output_count'] = str(len(publications))
    values['year_options'] = ''.join(f'<option value="{year}">{year}</option>' for year in sorted({p['year'] for p in publications}, reverse=True))
    values['experience'] = '\n'.join(f'''<li class="timeline-item"><span class="timeline-date">{escape(e['dates'])}</span>
      <div class="timeline-content"><h3>{escape(e['role'])}</h3><p class="timeline-institution">{escape(e['institution'])}<br>{escape(e['division'])}</p><p class="timeline-detail">{escape(e['description'])}</p></div></li>''' for e in profile['experience'])
    values['education'] = '\n'.join(f'''<article class="education-item"><h3>{escape(e['degree'])}</h3><p>{escape(e['institution'])}</p><p>{escape(e['location'])}</p><p class="education-date">{escape(e['dates'])}</p></article>''' for e in profile['education'])
    cv_text = (CONTENT / 'cv.md').read_text()
    details = re.split(r'^## (.+)\n', cv_text, flags=re.M)
    values['cv_details'] = '\n'.join(f'<details><summary>{escape(details[i])}</summary><div class="detail-body">{markdown(details[i+1])}</div></details>' for i in range(1, len(details), 2))
    values['teaching'] = '\n'.join(f'''<li><time>{escape(t['dates'])}</time><div><h3>{escape(t['title'])}</h3><p>{escape(t['description'])}</p></div></li>''' for t in profile['teaching'])
    for name in ICONS:
        values[f'icon_{name}'] = icon(name)
    values['icon_sun'] = icon('sun', 'sun-icon')
    values['icon_moon'] = icon('moon', 'moon-icon')
    structured = {'@context': 'https://schema.org', '@type': 'Person', 'name': profile['name'], 'jobTitle': 'Staff Scientist', 'description': profile['discipline'], 'email': profile['email'], 'worksFor': {'@type': 'Organization', 'name': profile['affiliation']}, 'address': {'@type': 'PostalAddress', 'addressLocality': 'Doha', 'addressCountry': 'QA'}, 'sameAs': [profile[k] for k in ('scholar', 'github', 'linkedin', 'website')], 'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': e['institution']} for e in profile['education'][:3]], 'knowsAbout': profile['topics']}
    values['structured_data'] = json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c')
    result = Template((ROOT / 'templates/index.html').read_text()).substitute(values)
    (ROOT / 'index.html').write_text(result)
    print(f'Built index.html: {len(publications)} outputs, {len(profile["experience"])} career entries; source: {profile["cv"]}')


if __name__ == '__main__':
    build()
