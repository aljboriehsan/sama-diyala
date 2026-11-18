// measures ink bounds (device px at scale 4) of logo, name, tagline with photo hidden
const {chromium}=require('playwright');
(async()=>{
  const [src,css]=process.argv.slice(2);
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:4});
  await p.goto('file://'+src); await p.waitForFunction(()=>document.body.dataset.ready==='1');
  await p.addStyleTag({content:'.photo,.shade-top,.shade-bot,.dest,.price,.perf,.foot,.stripes{visibility:hidden!important} .ad{background:#000!important} '+(css||'')});
  await p.waitForTimeout(150);
  const r=await p.evaluate(()=>{const g=id=>{const e=document.querySelector(id).getBoundingClientRect();return [e.left,e.top,e.right,e.bottom]};return {logo:g('.lockup img'),name:g('.lockup .name'),tag:g('#tag')}});
  const buf=await p.screenshot({clip:{x:0,y:0,width:1080,height:260}});
  require('fs').writeFileSync(process.env.OUT||'/dev/null',buf);
  console.log(JSON.stringify(r)); await b.close();
})();
