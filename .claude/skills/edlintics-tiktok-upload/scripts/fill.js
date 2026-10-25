// TikTok Studio upload page: fill title (photo posts) and caption body for queue item I.
// Needs localStorage 'edl_tt' (from inject.js). Clear the editor first on VIDEO uploads
// (it starts with the file name): click it, cmd+a, Delete. Then run this with I replaced.
const I = '__I__';
const it = JSON.parse(localStorage.getItem('edl_tt'))[I];
const t = document.querySelector('input[placeholder="Add a catchy title"]');
if (t) {
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(t, it.title);
  t.dispatchEvent(new Event('input', {bubbles: true}));
}
const ed = document.querySelector('.public-DraftEditor-content');
ed.focus();
const dt = new DataTransfer();
dt.setData('text/plain', it.body + (it.tags.length ? '\n\n' : ''));
ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
await new Promise(r => setTimeout(r, 800));
`item ${I} ${it.slot} when ${it.when} counter ${document.body.innerText.match(/\d+\/4000/)?.[0]} body ${it.body.length} title ${t ? t.value.length : '-'} tags ${it.tags.join(' ')}`
