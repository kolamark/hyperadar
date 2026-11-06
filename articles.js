// Approved articles only. Candidate feeds never appear here.
const escapeText = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const demoPosts = posts;
openPost = function(id) {
  const p = posts.find(item => item.id === id);
  if (!p) return;
  const box = document.getElementById('articleContent');
  box.innerHTML = `<div class="meta">${p.tag} · ${p.time}</div><h2>${p.title}</h2>` +
    (p.demo ? '<p class="note">Ez a cikk a HypeRadar tervezett megjelenését mutatja be, és nem aktuális hír.</p>' : '') +
    p.body.map(paragraph => `<p>${paragraph}</p>`).join('') +
    (p.sources?.length ? '<h3>Források</h3><ul>' + p.sources.map(s => `<li><a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.name}</a></li>`).join('') + '</ul>' : '');
  document.getElementById('articleDialog').showModal();
};
demoPosts.forEach(p => p.demo = true);
fetch('./articles.json', {cache: 'no-store'})
  .then(response => { if (!response.ok) throw new Error('No article data'); return response.json(); })
  .then(data => {
    if (!Array.isArray(data.articles) || !data.articles.length) return;
    const valid = data.articles.filter(a => a.status === 'published' &&
      ['gaming','bulvar'].includes(a.category) &&
      typeof a.title === 'string' && typeof a.excerpt === 'string' &&
      Array.isArray(a.body) && a.body.every(p => typeof p === 'string') &&
      Array.isArray(a.sources) && a.sources.length > 0 &&
      a.sources.every(s => typeof s.name === 'string' && /^https:\/\//.test(s.url)));
    if (!valid.length) return;
    posts = valid.map((a, index) => ({
      id: index + 1, category: a.category, tag: escapeText(a.category === 'gaming' ? 'GAMING' : 'POPKULTÚRA'),
      time: escapeText(a.published_at || ''), symbol: a.category === 'gaming' ? 'GG' : 'POP',
      art: a.category === 'gaming' ? 'b' : 'a', title: escapeText(a.title),
      excerpt: escapeText(a.excerpt), body: a.body.map(escapeText),
      sources: a.sources.map(s => ({name: escapeText(s.name), url: escapeText(s.url)})), demo: false
    }));
    document.querySelector('#cikkek .sectionhead p').textContent = 'Ellenőrzött, jóváhagyott történetek.';
    render();
  })
  .catch(() => { /* Keep clearly labelled demo content if article data is unavailable. */ });
