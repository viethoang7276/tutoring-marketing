// Step P2 for posts that go out immediately (old posts). Replace __N__ with the number of slides.
const N=__N__;const S=ms=>new Promise(r=>setTimeout(r,ms));
const cnt=()=>performance.getEntriesByType('resource').filter(e=>e.name.includes('upload_protocol=resumable')).length;
let t=0;while(cnt()<N&&t<60){await S(1000);t++;}await S(1500);
const p=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='Post');
if(p.length!==1){'post buttons '+p.length}else{p[0].click();let k=0;while(!window.__cp.length&&k<30){await S(500);k++;}await S(1500);'uploads '+cnt()+' result '+JSON.stringify(window.__cp).slice(0,80)}
