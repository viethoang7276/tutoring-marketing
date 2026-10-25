// Run after typing "IE Tower" into the "Search locations" box and waiting 2-3 s.
// Clicks the "IE University - IE Tower" result (Paseo de la Castellana 259, Madrid).
const opt = [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && e.textContent.trim() === 'IE University - IE Tower' && e.offsetParent);
const row = opt.length ? (opt[0].closest('[class*=option], [role=option], li') || opt[0].parentElement) : null;
if (row) row.click();
await new Promise(r => setTimeout(r, 800));
`location ${document.querySelector('input[placeholder="Search locations"]')?.value || [...document.querySelectorAll('*')].find(e=>e.children.length===0&&/IE University - IE Tower/.test(e.textContent)&&e.closest('[class*=location]'))?.textContent || 'NOT SET'} (options found ${opt.length})`
