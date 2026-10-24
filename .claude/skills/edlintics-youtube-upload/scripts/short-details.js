// Step S1. Run in Studio after file_upload of the MP4 into YT_VIDEO_INPUT. Replace __TITLE__, __DESC__ (JSON strings) and __DATE__ ("Oct 28, 2026").
// Fills title + description, marks "not made for kids", clicks Next 3 times, opens Schedule,
// opens the date picker and types the date. Then press the REAL Return key (computer key "Return"):
// a synthetic Enter does not commit the Studio date.
const S=ms=>new Promise(r=>setTimeout(r,ms));let w=0;while(!document.querySelector('#title-textarea #textbox')&&w<30){await S(500);w++;}
const title=__TITLE__;const desc=__DESC__;const DATE='__DATE__';
const set=async(sel,txt)=>{const e=document.querySelector(sel);e.focus();document.execCommand('selectAll');document.execCommand('insertText',false,txt);await S(500);return e.innerText.length};
const a=await set('#title-textarea #textbox',title);const b=await set('#description-textarea #textbox',desc);
document.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click();await S(500);
for(let i=0;i<3;i++){document.querySelector('#next-button').click();await S(1500);}
document.querySelector('#second-container-expand-button').click();await S(1200);
document.querySelector('ytcp-visibility-scheduler ytcp-dropdown-trigger').click();await S(1000);
const di=[...document.querySelectorAll('input')].find(i=>i.offsetParent&&/^[A-Z][a-z]{2} \d{1,2}, 20\d\d$/.test(i.value));
di.focus();di.select();document.execCommand('insertText',false,DATE);'title '+a+' desc '+b+' date typed '+di.value
