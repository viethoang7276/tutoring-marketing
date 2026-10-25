// Run ONCE per session on any tiktok.com/tiktokstudio page (javascript_tool). Stores the helper
// bodies in localStorage; each later step runs one of them with the queue index I:
//   const R=n=>new (Object.getPrototypeOf(async function(){}).constructor)('I',localStorage.getItem(n)); await R('edl_fill')('12')
// Needs 'edl_tt' from inject.js (build_items.py) first.
const H = {};

// Title (photo posts only) + caption body pasted into the Draft.js editor. Hashtags are typed after.
H.edl_fill = `const it=JSON.parse(localStorage.getItem('edl_tt'))[I];
const t=document.querySelector('input[placeholder="Add a catchy title"]');
if(t){Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(t,it.title);t.dispatchEvent(new Event('input',{bubbles:true}));}
const ed=document.querySelector('.public-DraftEditor-content'); ed.focus();
const dt=new DataTransfer(); dt.setData('text/plain', it.body+(it.tags.length?'\\n\\n':''));
ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));
await new Promise(r=>setTimeout(r,800));
return 'item '+I+' '+it.slot+' when '+it.when+' counter '+(document.body.innerText.match(/\\d+\\/4000/)||[''])[0]+' body '+it.body.length+' title '+(t?t.value.length:'-')+' tags '+it.tags.join(' ');`;

// Click the "IE University - IE Tower" result after "IE Tower" was typed in Search locations. NOW posts only.
H.edl_loc = `const o=[...document.querySelectorAll('.Select__itemLabel')].find(e=>e.textContent.trim()==='IE University - IE Tower');
if(!o) return 'LOCATION OPTION NOT FOUND'; o.closest('.Select__item').click(); await new Promise(r=>setTimeout(r,800));
return 'location '+document.querySelector('input[placeholder="Search locations"]').value;`;

// In the open Sounds dialog, after searching "lofi study": use "Lofi Study" by Lofi Studies & FASSounds.
H.edl_snd = `const rows=[...document.querySelectorAll('*')].filter(e=>e.children.length===0&&e.textContent.trim()==='Lofi Study'&&e.offsetParent);
for(const t of rows){let r=t; for(let i=0;i<6&&r;i++){r=r.parentElement; if(r&&/FASSounds/.test(r.innerText)){const b=[...r.querySelectorAll('button')].find(b=>b.innerText.trim()==='Use'); if(b){b.click(); await new Promise(x=>setTimeout(x,2000)); return 'sound set';}}}}
return 'SOUND NOT FOUND';`;

// Schedule radio (+ "Allow" dialog the first time), date (month arrows), hour and minute pickers.
H.edl_sched = `const it=JSON.parse(localStorage.getItem('edl_tt'))[I]; const [d,t]=it.when.split(' '); const S=ms=>new Promise(r=>setTimeout(r,ms));
const vals=()=>[...document.querySelectorAll('input')].map(i=>i.value).filter(v=>/^\\d\\d:\\d\\d$|^2026-|^20\\d\\d-/.test(v));
if(vals().length<2){const radio=[...document.querySelectorAll('input[type=radio]')][1]; radio.scrollIntoView({block:'center'}); (radio.closest('label')||radio.parentElement).click(); await S(1500); const al=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()==='Allow'); if(al){al.click(); await S(1500);} }
const di=[...document.querySelectorAll('input')].find(i=>/^20\\d\\d-/.test(i.value)); if(!document.querySelector('span.day.valid')){di.scrollIntoView({block:'center'}); di.click(); await S(800);}
const months=['January','February','March','April','May','June','July','August','September','October','November','December']; const want=months[+d.slice(5,7)-1];
for(let k=0;k<3&&document.querySelector('.month-title').textContent.trim()!==want;k++){document.querySelectorAll('.month-header-wrapper .arrow')[1].click(); await S(500);}
const day=[...document.querySelectorAll('span.day.valid')].find(e=>e.textContent.trim()===String(+d.slice(8))); if(!day) return 'DAY NOT VALID '+d; day.click(); await S(800);
const ti=[...document.querySelectorAll('input')].find(i=>/^\\d\\d:\\d\\d$/.test(i.value)); ti.click(); await S(800);
const pick=(cls,v)=>{const e=[...document.querySelectorAll('.tiktok-timepicker-option-text.'+cls)].find(x=>x.textContent.trim()===v); if(!e) return false; e.scrollIntoView({block:'center'}); e.click(); return true;};
const a=pick('tiktok-timepicker-left',t.slice(0,2)); await S(500); const b=pick('tiktok-timepicker-right',t.slice(3)); await S(600);
document.querySelector('[class*=scheduled-title]')?.click(); await S(400);
return 'sched set '+vals().join(' ')+' (want '+it.when+') h'+a+' m'+b;`;

// Read-only check of the form.
H.edl_chk = `const ed=document.querySelector('.public-DraftEditor-content'); const it=JSON.parse(localStorage.getItem('edl_tt'))[I];
const tags=[...ed.querySelectorAll('span.mention')].map(s=>s.textContent); const snd=/Lofi Study/.test(document.body.innerText.split('Photos')[0]||'');
return 'item '+I+' '+it.slot+' counter '+(document.body.innerText.match(/\\d+\\/4000/)||[''])[0]+' tags '+tags.join(' ')+(tags.length===it.tags.length?' OK':' TAGS MISMATCH')+' | loc '+document.querySelector('input[placeholder="Search locations"]').value+' | sound '+snd+' | sched '+[...document.querySelectorAll('input')].map(i=>i.value).filter(v=>/^\\d\\d:\\d\\d$|^20\\d\\d-/.test(v)).join(' ')+' | want '+it.when;`;

// Guarded submit: tags OK; NOW = IE location, scheduled = NO location; photo = sound set; schedule matches.
// Clicks Post or Schedule, confirms the "Continue to post?" dialog (content check still running).
H.edl_go = `const R=n=>new (Object.getPrototypeOf(async function(){}).constructor)('I',localStorage.getItem(n));
const it=JSON.parse(localStorage.getItem('edl_tt'))[I]; const c=await R('edl_chk')(I); let ok=c.includes(' OK | ');
if(it.when==='now') ok=ok&&c.includes('loc IE University - IE Tower |'); else ok=ok&&c.includes('loc  |');
if(document.querySelector('input[placeholder="Add a catchy title"]')) ok=ok&&c.includes('sound true');
if(it.when!=='now'){const w=it.when.split(' '); ok=ok&&c.includes('sched '+w[1]+' '+w[0]);}
if(!ok) return 'NOT POSTED: '+c; const label=it.when==='now'?'Post':'Schedule';
const b=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()===label); if(!b) return 'NO BUTTON '+label+' | '+c;
b.click(); await new Promise(r=>setTimeout(r,3000)); let dlg='';
const pn=[...document.querySelectorAll('button')].find(b=>b.innerText.trim()==='Post now'); if(pn&&/Continue to post/.test(document.body.innerText)){pn.click(); dlg=' (confirmed Continue to post)';}
await new Promise(r=>setTimeout(r,6000)); return 'CLICKED '+label+dlg+' -> '+location.pathname+' | '+c;`;

// Like + save on a PHOTO post page (tiktok.com/@edlintics/photo/<id>), run right after navigate.
// Finds the post by its caption, so it never touches the next post in the feed.
H.edl_eng = `const it=JSON.parse(localStorage.getItem('edl_tt'))[I]; const key=it.body.slice(0,30); const S=ms=>new Promise(r=>setTimeout(r,ms));
for(let t=0;t<10&&![...document.querySelectorAll('[data-e2e=like-icon]')].length;t++) await S(500);
let box=null; for(const l of document.querySelectorAll('[data-e2e=like-icon]')){let a=l; while(a&&a!==document.body){a=a.parentElement; if(a.querySelectorAll('[data-e2e=like-icon]').length>1) break; if((a.innerText||'').includes(key)){box=a;break;}} if(box) break;}
if(!box) return 'POST BOX NOT FOUND '+it.slot;
const like=box.querySelector('[data-e2e=like-icon]'), fav=box.querySelector('[data-e2e=favorite-icon]'); const lab=e=>(e.getAttribute('aria-label')||'').replace(/\\s+/g,' ');
const lb=like.getAttribute('aria-pressed'), fb=lab(fav);
if(lb==='false'){like.click(); await S(1500);} if(/^Add to Favou?rites/.test(fb)){fav.click(); await S(1500);}
return it.slot+' like '+lb+'->'+like.getAttribute('aria-pressed')+' ('+lab(like)+') | fav ['+fb+'] -> ['+lab(fav)+']';`;

Object.entries(H).forEach(([k, v]) => localStorage.setItem(k, v));
'stored ' + Object.keys(H).join(', ');
