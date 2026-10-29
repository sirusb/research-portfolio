const siteConfig = {
  title: 'Mohamed Nadhir Djekidel',
  subtitle: 'AI, Bioinformatics, and LLM Research',
};

const markdownToHtml = (text) => {
  const lines = text.replace(/\r/g, '').split('\n');
  const html = [];
  let listBuffer = [];

  const flushList = () => {
    if (!listBuffer.length) return;
    html.push(`<ul>${listBuffer.map(item => `<li>${formatInline(item)}</li>`).join('')}</ul>`);
    listBuffer = [];
  };

  const formatInline = (value) => {
    let output = value;
    output = output.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
    output = output.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    output = output.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    return output;
  };

  lines.forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed) {
      flushList();
      return;
    }

    if (/^#+\s+/.test(trimmed)) {
      flushList();
      const level = Math.min(trimmed.match(/^#+/)[0].length, 3);
      const content = trimmed.replace(/^#+\s*/, '');
      html.push(`<h${level}>${formatInline(content)}</h${level}>`);
      return;
    }

    if (/^-\s+/.test(trimmed)) {
      listBuffer.push(trimmed.replace(/^-\s+/, ''));
      return;
    }

    if (/^\d+\.\s+/.test(trimmed)) {
      flushList();
      html.push(`<p>${formatInline(trimmed.replace(/^\d+\.\s+/, ''))}</p>`);
      return;
    }

    flushList();
    html.push(`<p>${formatInline(trimmed)}</p>`);
  });

  flushList();
  return html.join('');
};

const renderSection = (section) => {
  const fragment = document.createElement('section');
  fragment.className = 'section-card';
  fragment.id = section.id;

  const title = document.createElement('div');
  title.className = 'section-intro';
  title.innerHTML = `
    <div class="kicker">${section.kicker || 'Section'}</div>
    <h2>${section.label}</h2>
  `;

  const body = document.createElement('div');
  body.innerHTML = markdownToHtml(section.content);

  fragment.appendChild(title);
  fragment.appendChild(body);
  return fragment;
};

const loadSite = async () => {
  const app = document.getElementById('app');
  const nav = document.getElementById('site-nav');

  try {
    const response = await fetch('./content/sections.json');
    const sections = await response.json();

    sections.forEach((section) => {
      const navLink = document.createElement('a');
      navLink.href = `#${section.id}`;
      navLink.textContent = section.label;
      nav.appendChild(navLink);
    });

    for (const section of sections) {
      const contentResponse = await fetch(`./content/${section.file}`);
      const contentText = await contentResponse.text();
      const rendered = renderSection({ ...section, content: contentText });
      app.appendChild(rendered);
    }
  } catch (error) {
    app.innerHTML = `<section class="section-card"><h2>Content unavailable</h2><p>The site could not load its markdown content. Please check the content files.</p></section>`;
    console.error(error);
  }
};

window.addEventListener('DOMContentLoaded', loadSite);
