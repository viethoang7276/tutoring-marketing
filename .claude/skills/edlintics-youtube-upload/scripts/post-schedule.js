// Step P2. Run after file_upload of ALL slides in one call. Replace __I__.
// Waits until every image finished uploading (2 requests per image, counts the resumable ones),
// opens Post ▾ › Schedule post, types the date, picks the time, checks both, clicks Schedule
// and returns the create_post HTTP status. Only [200] is a success. [429] = rate limit (see SKILL.md).
// For "post now" (old posts), use post-now.js instead.
const I=__I__;const it=JSON.parse(localStorage.getItem('edl_items'))[I];const S=ms=>new Promise(r=>setTimeout(r,ms));
const cnt=()=>performance.getEntriesByType('resource').filter(e=>e.name.includes('upload_protocol=resumable')).length;
let t=0;while(cnt()<it.n&&t<90){await S(1000);t++;}await S(1000);
const leaf=(re)=>[...document.querySelectorAll('*')].filter(e=>e.childElementCount===0&&re.test(e.textContent.trim()));
const a=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.getAttribute('aria-label')==='Action menu');a[0].scrollIntoView({block:'center'});a[0].click();await S(800);
leaf(/^Schedule post$/).find(e=>e.offsetParent).click();await S(1200);
document.querySelector('#date-label-text').click();await S(800);
const tb=[...document.querySelectorAll('input#textbox')].find(i=>i.offsetParent&&/20\d\d/.test(i.value));tb.focus();tb.select();document.execCommand('insertText',false,it.date);
tb.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));await S(800);
tb.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',code:'Escape',keyCode:27,bubbles:true}));await S(600);
const tl=leaf(/^\d{1,2}:\d\d\s*[AP]M$/).find(e=>e.offsetParent&&!e.closest('tp-yt-paper-listbox'));tl.click();await S(800);
const ti=leaf(new RegExp('^'+it.time+'\\s*'+it.ap+'$')).find(e=>e.closest('tp-yt-paper-listbox'));ti.scrollIntoView({block:'center'});ti.click();await S(800);
const dl=document.querySelector('#date-label-text').textContent.trim();
const tl2=leaf(/^\d{1,2}:\d\d\s*[AP]M$/).find(e=>e.offsetParent&&!e.closest('tp-yt-paper-listbox')).textContent.trim().replace(/\s/g,' ');
if(dl!==it.date||tl2!==it.time+' '+it.ap){'MISMATCH '+dl+' '+tl2}else{
const sb=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='Schedule');sb[0].click();
let k=0;while(!window.__cp.length&&k<30){await S(500);k++;}await S(2000);
'item '+I+' uploads '+cnt()+' sched '+dl+' '+tl2+' result '+JSON.stringify(window.__cp).slice(0,80)}
