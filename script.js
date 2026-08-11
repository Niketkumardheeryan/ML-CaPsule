const $ = (s) => document.querySelector(s);
async function load() {
  let projects = [];
  try {
    projects = await fetch('./projects.json').then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    });
  } catch (e) {
    console.error('Failed to load projects.json', e);
    $('#grid').innerHTML = '<p style="color:#9aa4b2">Unable to load project data.</p>';
    return;
  }

  const cats = new Set();
  const diffs = new Set();
  const techs = new Set();

  projects.forEach((p) => {
    cats.add(p.category || 'Other');
    diffs.add(p.difficulty || 'Unknown');
    (p.tech || []).forEach((t) => techs.add(t));
  });

  const catSel = $('#category');
  const diffSel = $('#difficulty');
  const techSel = $('#tech');

  for (const v of Array.from(cats).sort()) catSel.appendChild(option(v, v));
  for (const v of Array.from(diffs).sort()) diffSel.appendChild(option(v, v));
  for (const v of Array.from(techs).sort()) techSel.appendChild(option(v, v));

  function render(list) {
    const grid = $('#grid');
    grid.innerHTML = '';
    if (!list.length) {
      grid.innerHTML = '<p style="color:#9aa4b2">No projects found.</p>';
      return;
    }

    list.forEach((p) => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `
        <h3>${escapeHTML(p.name)}</h3>
        <div class="meta">${escapeHTML(p.category)} • ${escapeHTML(p.difficulty)}</div>
        <div class="tags">${(p.tech || []).map((t) => `<span class="tag">${escapeHTML(t)}</span>`).join('')}</div>
        <div style="margin-top:8px"><a href="./${encodeURIComponent(p.folder)}">Open project</a></div>
      `;
      grid.appendChild(el);
    });
  }

  function matches(p) {
    const q = $('#search').value.trim().toLowerCase();
    const cat = $('#category').value;
    const diff = $('#difficulty').value;
    const tech = $('#tech').value;

    if (cat && p.category !== cat) return false;
    if (diff && p.difficulty !== diff) return false;
    if (tech && !(p.tech || []).includes(tech)) return false;
    if (q) {
      const hay = `${p.name} ${p.folder} ${p.category} ${(p.tech || []).join(' ')}`.toLowerCase();
      return hay.includes(q);
    }
    return true;
  }

  function refresh() {
    render(projects.filter(matches));
  }

  $('#search').addEventListener('input', refresh);
  $('#category').addEventListener('change', refresh);
  $('#difficulty').addEventListener('change', refresh);
  $('#tech').addEventListener('change', refresh);

  render(projects);
}

function option(text, value) { const o = document.createElement('option'); o.value = value; o.textContent = text; return o; }
function escapeHTML(s) { return (s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
load();
