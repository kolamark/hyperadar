let articles = [];
const $ = id => document.getElementById(id);
const text = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const safeUrl = value => { try { const url = new URL(value); return url.protocol === 'https:' ? url.href : ''; } catch { return ''; } };
function count() { $('articleCount').textContent = `${articles.length} jóváhagyott cikk az adatfájlban.`; }
function readArticles(data) {
  if (!Array.isArray(data.articles)) throw new Error('A cikkfájlban nincs articles lista.');
  articles = data.articles;
  count();
}
async function importFile(input, callback) {
  const file = input.files?.[0]; if (!file) return;
  try { callback(JSON.parse(await file.text())); $('status').textContent = ''; }
  catch (error) { $('status').textContent = `Nem sikerült beolvasni: ${error.message}`; }
  input.value = '';
}
function showCandidates(data) {
  if (!Array.isArray(data)) throw new Error('A jelöltlista nem tömb.');
  const list = $('candidates'); list.replaceChildren();
  if (!data.length) { list.textContent = 'Még nincs begyűjtött jelölt. Kézzel is írható cikk.'; return; }
  for (const candidate of data.slice(0, 60)) {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'candidate';
    const url = safeUrl(candidate.url); if (!url) continue;
    const small = document.createElement('small'); small.textContent = `${candidate.source || 'Forrás'} · ${candidate.category || ''}`;
    const strong = document.createElement('strong'); strong.textContent = candidate.original_title || 'Cím nélkül';
    const em = document.createElement('em'); em.textContent = candidate.published_at || 'Dátum nélkül';
    button.append(small, strong, em);
    button.addEventListener('click', () => {
      document.querySelectorAll('.candidate').forEach(x => x.classList.remove('selected'));
      button.classList.add('selected'); $('original').value = url;
      $('category').value = candidate.category === 'gaming' ? 'gaming' : 'bulvar';
      $('sources').value = `${candidate.source || 'Eredeti forrás'} | ${url}`;
      window.open(url, '_blank', 'noopener,noreferrer');
    }); list.append(button);
  }
}
function draft() {
  const body = $('body').value.trim().split(/\n\s*\n/).map(x => x.replace(/\s+/g, ' ').trim()).filter(Boolean);
  const sources = $('sources').value.trim().split(/\n/).map(line => {
    const sep = line.indexOf('|');
    return {name: line.slice(0, sep).trim(), url: safeUrl(line.slice(sep + 1).trim())};
  });
  if (body.join(' ').split(/\s+/).length < 120) throw new Error('A cikk legalább 120 szóból álljon.');
  if (body.length < 2) throw new Error('A szöveget oszd legalább két bekezdésre.');
  if (!sources.length || sources.some(s => !s.name || !s.url)) throw new Error('Minden forráshoz név és érvényes HTTPS-link kell.');
  if (articles.some(a => a.title.toLocaleLowerCase('hu') === $('title').value.trim().toLocaleLowerCase('hu'))) throw new Error('Ilyen cím már szerepel a cikkek között.');
  return {status:'published', category:$('category').value, title:$('title').value.trim(), excerpt:$('excerpt').value.trim(), body, sources, published_at:new Date().toISOString()};
}
function preview() {
  try { const a = draft(); $('preview').hidden = false;
    $('preview').innerHTML = `<small>${text(a.category)} · ${text(a.published_at)}</small><h3>${text(a.title)}</h3><p><strong>${text(a.excerpt)}</strong></p>${a.body.map(p => `<p>${text(p)}</p>`).join('')}<h4>Források</h4><ul>${a.sources.map(s => `<li><a href="${text(s.url)}" target="_blank" rel="noopener noreferrer">${text(s.name)}</a></li>`).join('')}</ul>`;
    $('status').textContent = '';
  } catch (error) { $('status').textContent = error.message; }
}
$('previewButton').addEventListener('click', preview);
$('form').addEventListener('submit', event => {
  event.preventDefault();
  try {
    const a = draft();
    const blob = new Blob([JSON.stringify({articles:[a, ...articles]}, null, 2) + '\n'], {type:'application/json'});
    const url = URL.createObjectURL(blob); const link = document.createElement('a');
    link.href = url; link.download = 'articles.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    $('status').textContent = 'A jóváhagyott fájl letöltve. Töltsd fel a GitHub-repó articles.json fájljának helyére.';
  } catch (error) { $('status').textContent = error.message; }
});
$('candidateFile').addEventListener('change', event => importFile(event.target, showCandidates));
$('articleFile').addEventListener('change', event => importFile(event.target, readArticles));
fetch('./articles.json').then(r => r.json()).then(readArticles).catch(() => $('articleCount').textContent = 'Nem sikerült betölteni, nyisd meg kézzel az aktuális fájlt.');
fetch('https://raw.githubusercontent.com/kolamark/hyperadar/main/data/candidates.json')
  .then(r => { if (!r.ok) throw Error(); return r.json(); }).then(showCandidates)
  .catch(() => $('candidates').textContent = 'Még nem érhető el jelöltlista. A fájl kézzel is megnyitható.');
