// Step S2. After the real Return key. Replace __DATE__ and __TIME__ ("7:00 PM").
// Sets the time, checks date + time, clicks Schedule, returns the Shorts link and the confirmation text.
// "nodialog" can still be a success: confirm in Studio › Content › Shorts (status "Scheduled").
const S=ms=>new Promise(r=>setTimeout(r,ms));const DATE='__DATE__',TIME='__TIME__';const N=s=>s.replace(/\s+/g,' ').trim();
const sc=document.querySelector('ytcp-visibility-scheduler');const ti=[...sc.querySelectorAll('input')].find(i=>i.offsetParent&&/^\d{1,2}:\d\d/.test(i.value));
ti.focus();ti.select();document.execCommand('insertText',false,TIME);ti.dispatchEvent(new Event('change',{bubbles:true}));ti.blur();await S(800);
const dl=N(sc.querySelector('ytcp-dropdown-trigger').innerText);const tv=N(ti.value);
if(!dl.includes(DATE)||tv!==TIME){'MISMATCH ['+dl+'] '+tv}else{
const link=[...document.querySelectorAll('a')].map(a=>a.href).find(h=>/youtube.com\/shorts|youtu.be/.test(h));
document.querySelector('#done-button').click();await S(5000);
const d=document.querySelector('ytcp-video-share-dialog, tp-yt-paper-dialog[opened]');link+' | '+(d?d.innerText.replace(/\n+/g,' | ').slice(0,140):'nodialog')}
