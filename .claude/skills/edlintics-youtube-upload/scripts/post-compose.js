// Step P1. Run on https://www.youtube.com/channel/UCUx_KFGdEVdBoKvCS3BxYRA/posts right after navigating.
// Replace __I__ with the item index. Needs localStorage 'edl_items' (made by build_items.py, step P0).
// Installs a fetch hook so step P2 can read the real create_post status, types the caption,
// opens the image dropzone and labels its file input YT_DROPZONE_INPUT for find + file_upload.
window.__cp=[];const of=window.fetch;window.fetch=async function(...a){const res=await of.apply(this,a);try{const u=(a[0]&&a[0].url)||String(a[0]);if(u.includes('create_post')){window.__cp.push(res.status);if(res.status!==200)res.clone().text().then(t=>window.__cp.push(t.slice(0,300)));}}catch(e){}return res;};
const I=__I__;const it=JSON.parse(localStorage.getItem('edl_items'))[I];
let w=0;while(!document.querySelector('#commentbox-placeholder')&&w<20){await new Promise(r=>setTimeout(r,500));w++;}
document.querySelector('#commentbox-placeholder')?.click();await new Promise(r=>setTimeout(r,1000));
const ed=[...document.querySelectorAll('[contenteditable=true]')].find(e=>e.offsetParent);
if(!ed){'noeditor'}else{ed.focus();document.execCommand('insertText',false,it.text);
const btn=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/^\s*Image\s*$/.test(b.innerText));btn&&btn.click();
await new Promise(r=>setTimeout(r,1200));const i=document.querySelector('#dropzone input[type=file]');i&&i.setAttribute('aria-label','YT_DROPZONE_INPUT');
'item '+I+' len '+ed.innerText.length+'/'+it.text.length+' img '+!!i}
