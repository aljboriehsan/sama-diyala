const {chromium}=require('playwright');
(async()=>{
  const [src,dx]=process.argv.slice(2);
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:4});
  await p.goto('file://'+src); await p.waitForFunction(()=>document.body.dataset.ready==='1');
  if(dx) await p.addStyleTag({content:`:root{--kick-dx:${dx}px}`});
  // ink right edges via canvas-free approach: render each element alone
  const edge=async(sel)=>{
    await p.addStyleTag({content:`.ad *{visibility:hidden!important} .ad{background:#000!important} ${sel},${sel} *{visibility:visible!important;color:#fff!important}`});
    await p.waitForTimeout(100);
    const box=await p.evaluate(s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left,r.top,r.width,r.height]},sel);
    const buf=await p.screenshot({clip:{x:box[0]-4,y:box[1]-4,width:box[2]+8,height:box[3]+8}});
    await p.evaluate(()=>{document.querySelectorAll('style').forEach((s,i,a)=>{if(i===a.length-1)s.remove()})});
    return {buf,left:box[0]-4};
  };
  const fs=require('fs'); const a=await edge('.kicker'); const c=await edge('.price .from');
  fs.writeFileSync('/tmp/claude-0/-home-user-sama-diyala/ac5234ca-4a29-5f40-9e89-18987c0271f8/scratchpad/bp/k.png',a.buf);
  fs.writeFileSync('/tmp/claude-0/-home-user-sama-diyala/ac5234ca-4a29-5f40-9e89-18987c0271f8/scratchpad/bp/f.png',c.buf);
  console.log(a.left,c.left); await b.close();
})();
