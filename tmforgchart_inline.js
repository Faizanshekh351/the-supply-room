

const $=id=>document.getElementById(id);

const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

const fmt=n=>Number(n||0).toLocaleString("en-US");

const xUrl=h=>"https://x.com/"+encodeURIComponent(h);

const FUNDN=["Argon","Bogle","Smaug","Midas","Vladd"], FUNDC=["#5b8ac2","#57a671","#c97258","#d19a19","#977bc4"];

const SIZE=r=>r>=6?"l":r>=3?"m":"s", CAP=[260,200,160,140,120,999,999,999];

let D=null, off=new Set(), meKey="";



function pic(url){ return url?url.replace(/_normal(\.\w+)$/,"_bigger$1"):""; }

function img(p,cls){ return p.a?'<img src="'+esc(pic(p.a))+'" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">':""; }



function render(){

  const d=D, byR=d.titles.map(()=>[]);

  for(const p of d.staff) byR[p.r].push(p);

  const n=d.staff.length;

  let html='<div class="chair"><div class="fl-meta"><div class="fl-no">PENTHOUSE · SEAT 0</div><div class="fl-title">The Chairman</div><div class="fl-n">belongs to the building</div></div>'

    +'<div class="fl-desks"><a class="desk" href="'+xUrl(d.chairman.h)+'" target="_blank" rel="noopener">'+(d.chairman.a?'<img src="'+esc(pic(d.chairman.a))+'" alt="" referrerpolicy="no-referrer">':"")+'</a>'

    +'<div class="who"><b>@'+esc(d.chairman.h)+'</b>never ranked, never for sale</div></div></div>';

  for(let r=7;r>=0;r--){

    const list=byR[r], fl=d.floors[r], sz=SIZE(r);

    const pct=n?Math.max(1,Math.round(list.length/n*100)):0;

    html+='<div class="floor"><div class="fl-meta"><div class="fl-no">FLOOR '+(r+1)+'</div><div class="fl-title">'+esc(d.titles[r])+'</div>'

      +'<div class="fl-n">'+fmt(list.length)+(list.length===1?" desk":" desks")+(n?" · "+pct+"%":"")+'</div></div><div class="fl-desks">';

    if(!list.length) html+='<div class="empty">Vacant.</div>';

    const show=list.slice(0,CAP[r]);

    for(const p of show){

      const k=p.h.toLowerCase(), cls="desk s-"+sz+(off.size&&off.has(p.f)?" dim":"")+(k===meKey?" me":"");

      const tile='<a class="'+cls+'" style="--c:'+FUNDC[p.f]+'" href="'+xUrl(p.h)+'" target="_blank" rel="noopener" data-k="'+esc(k)+'">'+img(p)+'</a>';

      html+=sz==="l"?'<div class="cap">'+tile+'<span>@'+esc(p.h)+'</span></div>':tile;

    }

    if(list.length>show.length) html+='<span class="more">and '+fmt(list.length-show.length)+' more on this floor</span>';

    html+='</div></div>';

  }

  $("building").innerHTML=html;

}



function renderDepts(){

  $("depts").innerHTML=FUNDN.map((f,i)=>'<button class="dept'+(off.size&&off.has(i)?" off":"")+'" data-f="'+i+'"><i style="background:'+FUNDC[i]+'"></i>The '+f+' Fund</button>').join("");

}

$("depts").addEventListener("click",ev=>{

  const b=ev.target.closest(".dept"); if(!b)return; const f=+b.dataset.f;

  // first click isolates a department; clicking it again shows everyone

  if(off.size===4&&!off.has(f)) off=new Set(); else off=new Set([0,1,2,3,4].filter(x=>x!==f));

  renderDepts(); render();

});



/* hover card */

const tip=$("tip");

$("building").addEventListener("mousemove",ev=>{

  const a=ev.target.closest(".desk[data-k]"); if(!a){tip.style.display="none";return;}

  const p=D.staff.find(x=>x.h.toLowerCase()===a.dataset.k); if(!p)return;

  tip.innerHTML='<div class="t1">@'+esc(p.h)+'</div><div class="t2">'+esc(D.titles[p.r])+', The '+FUNDN[p.f]+' Fund</div>'

    +'<div class="t3">No. '+String(p.no).padStart(4,"0")+' · '+fmt(p.s)+' pts · '+p.p+' posts</div>';

  tip.style.display="block";

  const x=Math.min(ev.clientX+14,innerWidth-230), y=Math.min(ev.clientY+14,innerHeight-90);

  tip.style.left=x+"px"; tip.style.top=y+"px";

});

$("building").addEventListener("mouseleave",()=>tip.style.display="none");



function renderMemo(){

  const up=D.staff.filter(p=>p.up!=null).sort((a,b)=>b.r-a.r||b.s-a.s).slice(0,10);

  const hires=D.staff.filter(p=>p.hire).sort((a,b)=>b.s-a.s).slice(0,10);

  const row=(p,m)=>'<div class="row" style="--c:'+FUNDC[p.f]+'">'+(p.a?'<img src="'+esc(p.a)+'" alt="" referrerpolicy="no-referrer" onerror="this.remove()">':'<img alt="">')

    +'<a class="h" href="'+xUrl(p.h)+'" target="_blank" rel="noopener">@'+esc(p.h)+'</a><span class="m">'+m+'</span></div>';

  let h="";

  if(up.length) h+='<h4>promoted</h4>'+up.map(p=>row(p,esc(D.titles[p.up])+' → <b>'+esc(D.titles[p.r])+'</b>')).join("");

  if(hires.length) h+='<h4>new hires</h4>'+hires.map(p=>row(p,esc(D.titles[p.r]))).join("");

  $("memo").innerHTML=h||'<div class="empty">Nothing filed yet today.</div>';

}

function renderLadder(){

  $("ladder").innerHTML=D.titles.map((t,r)=>({t,r})).reverse().map(({t,r})=>'<tr><td>'+(r+1)+' · '+esc(t)+'</td><td>'+fmt(D.floors[r].n)+'</td></tr>').join("");

}



/* personnel file */

function nextFloor(p){

  if(p.r>=7) return null;

  const above=D.staff.filter(x=>x.r===p.r+1); if(!above.length) return null;

  return { title:D.titles[p.r+1], pts:Math.max(1,Math.min(...above.map(x=>x.s))-p.s) };

}

let cur=null;

function openFile(raw){

  const k=raw.trim().replace(/^@+/,"").toLowerCase(); if(!k)return;

  if(!D){ $("file").style.display="none"; $("miss").style.display="block"; $("miss").textContent="The files are still loading. Try again in a moment."; return; }

  const p=D.staff.find(x=>x.h.toLowerCase()===k);

  meKey=p?k:""; render();

  if(!p){ $("file").style.display="none"; $("miss").style.display="block";

    $("miss").innerHTML="No file under @"+esc(k)+" yet. Post about @TheMutualFun and HR opens one within a couple of minutes. Already posted? <button class=\"btn ghost\" id=\"recheck\" style=\"margin-left:8px\">Check X again</button>";

    $("recheck").onclick=async()=>{ const b=$("recheck"); b.disabled=true; b.textContent="Checking X…";

      const r=await fetch("/api/backfill?handle="+encodeURIComponent(k)).then(r=>r.json()).catch(()=>null);

      if(r&&r.ok&&r.stored>0){ await load(); openFile(k); return; }

      b.textContent=r&&r.error==="wait"?"Checked recently, try in 30 min":r&&r.error==="busy"?"Daily check limit reached, try tomorrow":"Nothing found yet"; }; return; }

  cur=p; $("miss").style.display="none";

  const rank=D.staff.indexOf(p)+1, nx=nextFloor(p), since=new Date(p.since).toLocaleDateString("en-US",{month:"short",day:"numeric"});

  $("file").style.display="block";

  $("file").innerHTML='<div class="hd" style="--c:'+FUNDC[p.f]+'">'+(p.a?'<img src="'+esc(pic(p.a))+'" alt="" referrerpolicy="no-referrer">':"")

    +'<div><div class="no">EMPLOYEE No. '+String(p.no).padStart(4,"0")+'</div><div class="h">@'+esc(p.h)+'</div></div></div>'

    +'<dl><dt>Title</dt><dd class="t">'+esc(D.titles[p.r])+'</dd>'

    +'<dt>Department</dt><dd class="t" style="color:'+FUNDC[p.f]+'">The '+FUNDN[p.f]+' Fund</dd>'

    +'<dt>On the floor since</dt><dd>'+since+'</dd>'

    +'<dt>Posts on file</dt><dd>'+p.p+' over '+p.d+(p.d===1?" day":" days")+'</dd>'

    +'<dt>Review score</dt><dd>'+fmt(p.s)+' pts · #'+fmt(rank)+' of '+fmt(D.staff.length)+'</dd>'

    +'<dt>Next floor</dt><dd>'+(nx?esc(nx.title)+', '+fmt(nx.pts)+' pts away':"top of the building")+'</dd></dl>'

    +'<div class="acts"><button class="btn" id="cert">Issue my certificate</button>'

    +'<button class="btn ghost" id="find">Show me in the building</button>'

    +'<button class="btn ghost" id="recount" title="Posts missing? We re-read your timeline.">Recount my posts</button></div>';

  $("cert").onclick=issue;

  $("recount").onclick=async()=>{ const b=$("recount"); b.disabled=true; b.textContent="Reading your timeline…";

    const r=await fetch("/api/backfill?handle="+encodeURIComponent(p.h)).then(r=>r.json()).catch(()=>null);

    if(r&&r.ok){ await load(); const q=D.staff.find(x=>x.h.toLowerCase()===p.h.toLowerCase()); const was=p.p, now=q?q.p:was; openFile(p.h); const m=$("recount"); if(m){ m.disabled=true; m.textContent=now>was?("+"+(now-was)+" found"):"Up to date"; } return; }

    b.textContent=r&&r.error==="wait"?"Checked recently, try in 30 min":r&&r.error==="busy"?"Daily check limit reached, try tomorrow":"Could not check"; };

  $("find").onclick=()=>{ const el=document.querySelector('.desk.me'); if(el) el.scrollIntoView({behavior:"smooth",block:"center"}); };

}

$("look").addEventListener("submit",ev=>{ ev.preventDefault(); openFile($("q").value); });



/* ================= the certificate =================

   1200x675, drawn in the browser like an engraved stock certificate. */

const loadImg=src=>new Promise(r=>{ const im=new Image(); im.onload=()=>r(im); im.onerror=()=>r(null); setTimeout(()=>r(null),4000); im.src=src; });

async function issue(){

  const p=cur; if(!p)return;

  const b=$("cert"); b.textContent="Engraving…";

  await Promise.all(['700 40px "Libre Caslon Text"','400 20px "Libre Caslon Text"','italic 400 20px "Libre Caslon Text"','400 20px "Source Serif 4"','italic 400 20px "Source Serif 4"','500 14px "IBM Plex Mono"'].map(f=>document.fonts.load(f).catch(()=>{})));

  const face=await loadImg("/api/avatar?h="+encodeURIComponent(p.h));

  const W=1200,H=675,c=document.createElement("canvas"); c.width=W; c.height=H; const g=c.getContext("2d");

  const PAPER="#f6efe3", INK="#211b14", MUTED="#6b5f4e", OX="#7a2e2e", GOLD="#b08a3c", F=FUNDC[p.f];

  const CAS='"Libre Caslon Text", Georgia, serif', SER='"Source Serif 4", Georgia, serif', MON='"IBM Plex Mono", Menlo, monospace';

  g.fillStyle=PAPER; g.fillRect(0,0,W,H);

  // paper grain

  for(let i=0;i<5200;i++){ g.fillStyle="rgba(120,95,60,"+(Math.random()*.05).toFixed(3)+")"; g.fillRect(Math.random()*W,Math.random()*H,1,1); }

  // engraved border: two rules and a guilloche band between them

  g.strokeStyle=OX; g.lineWidth=3; g.strokeRect(22,22,W-44,H-44);

  g.lineWidth=1; g.strokeRect(46,46,W-92,H-92);

  // guilloche band: two interleaved waves along each edge, between the rules

  g.strokeStyle="rgba(122,46,46,.5)"; g.lineWidth=.8;

  const wave=(horiz,fixed,from,to)=>{ for(const ph of [0,Math.PI]){ g.beginPath();

    for(let s=from;s<=to;s+=1.5){ const o=Math.sin(s/3+ph)*7; horiz?(s===from?g.moveTo(s,fixed+o):g.lineTo(s,fixed+o)):(s===from?g.moveTo(fixed+o,s):g.lineTo(fixed+o,s)); }

    g.stroke(); } };

  wave(true,34,48,W-48); wave(true,H-34,48,W-48); wave(false,34,48,H-48); wave(false,W-34,48,H-48);

  // corner rosettes in the department's color

  for(const [x,y] of [[34,34],[W-34,34],[34,H-34],[W-34,H-34]]){ g.beginPath(); g.arc(x,y,10,0,Math.PI*2); g.fillStyle=F; g.fill(); g.lineWidth=1.5; g.strokeStyle=OX; g.stroke(); }



  g.textAlign="center"; g.fillStyle=MUTED; g.font="400 15px "+SER;

  try{ g.letterSpacing="5px"; }catch(_){}

  g.fillText("THE MUTUAL FUN  ·  PERSONNEL DEPARTMENT",W/2,92);

  try{ g.letterSpacing="0px"; }catch(_){}

  g.fillStyle=INK; g.font="700 50px "+CAS; g.fillText("Certificate of Employment",W/2,150);

  g.strokeStyle=GOLD; g.lineWidth=1; g.beginPath(); g.moveTo(W/2-230,172); g.lineTo(W/2+230,172); g.stroke();



  // portrait in an oval, gold ring

  const ox=250, oy=360, rx=95, ry=118;

  g.save(); g.beginPath(); g.ellipse(ox,oy,rx,ry,0,0,Math.PI*2); g.fillStyle="#ede3cf"; g.fill(); g.clip();

  if(face){ const s=Math.max(rx*2/face.width,ry*2/face.height); g.drawImage(face,ox-face.width*s/2,oy-face.height*s/2,face.width*s,face.height*s); }

  else { g.fillStyle=MUTED; g.font="700 80px "+CAS; g.fillText(p.h[0].toUpperCase(),ox,oy+28); }

  g.restore();

  g.lineWidth=4; g.strokeStyle=GOLD; g.beginPath(); g.ellipse(ox,oy,rx+5,ry+5,0,0,Math.PI*2); g.stroke();

  g.lineWidth=1; g.strokeStyle=OX; g.beginPath(); g.ellipse(ox,oy,rx+11,ry+11,0,0,Math.PI*2); g.stroke();



  // the words

  const tx=720;

  g.fillStyle=MUTED; g.font="italic 400 22px "+SER; g.fillText("This certifies that",tx,238);

  g.fillStyle=INK; g.font="700 "+(p.h.length>12?44:52)+"px "+CAS; g.fillText("@"+p.h,tx,300);

  g.fillStyle=MUTED; g.font="italic 400 22px "+SER; g.fillText("holds the position of",tx,350);

  g.fillStyle=OX; g.font="700 "+(D.titles[p.r].length>14?38:44)+"px "+CAS; g.fillText(D.titles[p.r],tx,406);

  g.fillStyle=MUTED; g.font="italic 400 22px "+SER; g.fillText("in the department of",tx,452);

  g.fillStyle=F; g.font="700 34px "+CAS; g.fillText("The "+FUNDN[p.f]+" Fund",tx,496);



  // ledger line

  g.strokeStyle=GOLD; g.beginPath(); g.moveTo(90,526); g.lineTo(W-90,526); g.stroke();

  g.fillStyle=INK; g.font="500 15px "+MON;

  const issued=new Date().toLocaleDateString("en-GB",{day:"numeric",month:"short",year:"numeric"});

  g.fillText("EMPLOYEE No. "+String(p.no).padStart(4,"0")+"   ·   FLOOR "+(p.r+1)+" OF 8   ·   "+p.p+" POSTS ON FILE   ·   ISSUED "+issued.toUpperCase(),W/2,556);



  // signature line and seal, clear of the engraved border

  g.textAlign="left"; g.fillStyle=INK; g.font="italic 400 26px "+CAS; g.fillText("Personnel",108,592);

  g.strokeStyle=INK; g.lineWidth=.8; g.beginPath(); g.moveTo(104,601); g.lineTo(344,601); g.stroke();

  g.fillStyle=MUTED; g.font="400 13px "+SER; g.fillText("fan made, not affiliated with The Mutual Fun · "+location.host,104,619);

  const sx=W-160, sy=588;

  g.beginPath(); g.arc(sx,sy,36,0,Math.PI*2); g.fillStyle=OX; g.fill();

  g.beginPath(); g.arc(sx,sy,30,0,Math.PI*2); g.strokeStyle="rgba(246,239,227,.8)"; g.lineWidth=1.2; g.stroke();

  g.fillStyle=PAPER; g.textAlign="center"; g.font="700 9px "+CAS; g.fillText("UNOFFICIAL",sx,sy-1); g.font="400 10px "+SER; g.fillText("fan made",sx,sy+13);



  $("certimg").src=c.toDataURL("image/png"); $("modal").classList.add("on");

  b.textContent="Issue my certificate"; logCert("issued");

}

/* certificate ticker: every newly issued certificate shows up bottom-left for a few seconds */

let certSince=null; // set from the server clock on the first poll: only certificates issued after this page opened are announced

const NTF=[]; let unread=0;

function noteCert(handle){ NTF.unshift({handle,at:new Date()}); if(NTF.length>50) NTF.pop(); unread++; renderNtf(); }

function renderNtf(){ const n=$("bell-n"); n.hidden=!unread; n.textContent=unread>99?"99+":unread;

  const L=$("ntf-list"); if(!NTF.length){ L.innerHTML='<div class="ntf-empty">nothing yet. certificates issued while this page is open show up here.</div>'; return; }

  L.innerHTML=NTF.map(x=>'<div class="ntf-it"><img src="/api/avatar?h='+encodeURIComponent(x.handle)+'" alt="" onerror="this.remove()"><span><a href="'+xUrl(x.handle)+'" target="_blank" rel="noopener"><b>@'+esc(x.handle)+'</b></a> got a certificate</span><small>'+x.at.toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})+'</small></div>').join(""); }

$("bell").onclick=e=>{ e.stopPropagation(); const p=$("ntf"); p.classList.toggle("on"); if(p.classList.contains("on")){ unread=0; renderNtf(); } };

$("ntf-clear").onclick=()=>{ NTF.length=0; unread=0; renderNtf(); };

document.addEventListener("click",e=>{ if(!e.target.closest("#ntf")) $("ntf").classList.remove("on"); });

function toast(handle){ noteCert(handle); const box=$("toasts"); const el=document.createElement("div"); el.className="toast";

  el.innerHTML='<img src="/api/avatar?h='+encodeURIComponent(handle)+'" alt="" onerror="this.remove()"><a href="'+xUrl(handle)+'" target="_blank" rel="noopener"><b>@'+esc(handle)+'</b></a> just got their certificate.';

  box.appendChild(el); requestAnimationFrame(()=>el.classList.add("on")); setTimeout(()=>{ el.classList.remove("on"); setTimeout(()=>el.remove(),300); },5200); }

async function pollCerts(){ try{ const prime=!certSince; const j=await fetch("/api/certs?since="+encodeURIComponent(certSince||new Date().toISOString())).then(r=>r.json()); if(!j||!j.ok) return; certSince=j.now; if(prime) return;

  const items=j.items.slice().reverse().slice(-4); items.forEach((it,i)=>setTimeout(()=>toast(it.handle),i*900));

  if(items.length){ const n=Number(($("f-certs").textContent||"0").replace(/,/g,""))+items.length; $("f-certs").textContent=fmt(n); } }catch(_){} }

setInterval(pollCerts,12000); setTimeout(pollCerts,1500);

const logCert=action=>{ try{ fetch("/api/cert",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({h:cur.h,action})}); }catch(_){} };

$("dl").onclick=()=>{ logCert("downloaded"); const a=document.createElement("a"); a.download="tmf-certificate-"+cur.h+".png"; a.href=$("certimg").src; a.click(); };

$("share").onclick=()=>{ logCert("shared");

  const t="Got my desk at @TheMutualFun: "+D.titles[cur.r]+", The "+FUNDN[cur.f]+" Fund. Employee No. "+String(cur.no).padStart(4,"0")+".\n\nevery post about TMF puts you somewhere in the building. find your floor:\n"+location.origin;

  window.open("https://x.com/intent/post?text="+encodeURIComponent(t),"_blank","noopener");

};

$("close").onclick=()=>$("modal").classList.remove("on");

$("modal").addEventListener("click",ev=>{ if(ev.target.id==="modal") $("modal").classList.remove("on"); });



/* data */

let last=0;

async function load(){

  const j=await fetch("/api/board",{signal:AbortSignal.timeout(20000)}).then(r=>r.json()).catch(()=>null);

  if(!j||!j.ok){

    if(!D){ $("upd").textContent="the ledger room is slow, retrying…";

      $("building").innerHTML='<div class="floor"><div class="fl-meta"><div class="fl-no">one moment</div></div><div class="fl-desks"><div class="empty">The files are taking longer than usual to come up. Trying again in a few seconds.</div></div></div>';

      setTimeout(load,8000); }

    return;

  }

  D=j; last=Date.now();

  $("f-staff").textContent=fmt(j.totals.staff); $("f-posts").textContent=fmt(j.totals.posts);

  $("f-hires").textContent="+"+fmt(j.totals.hires); $("f-promos").textContent="+"+fmt(j.totals.promotions); $("f-certs").textContent=fmt((j.totals.certs||{}).issued||0);

  renderDepts(); render(); renderMemo(); renderLadder(); tick();

  const want=new URLSearchParams(location.search).get("h");

  if(want&&!cur){ $("q").value=want; openFile(want); }

  else if(cur) openFile(cur.h);

}

function tick(){ if(!last)return; const s=(Date.now()-last)/1000|0; $("upd").textContent="updated "+(s<10?"just now":s<60?s+"s ago":(s/60|0)+"m ago"); }

load(); setInterval(load,60000); setInterval(tick,5000);

