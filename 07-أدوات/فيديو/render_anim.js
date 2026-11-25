// Renders an animated HTML layer frame by frame (transparent PNGs) through window.seek(t).
// Usage: node render_anim.js <page.html> <out_dir> <seconds> [fps=30] [t1,t2,... = only these times, for checks]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
  const [src,out,secs,fps='30',only]=process.argv.slice(2);
  fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.resolve(src)); await p.waitForFunction(()=>document.body.dataset.ready==='1');
  const times=only?only.split(',').map(Number):[...Array(Math.round(+secs*+fps)).keys()].map(i=>i/+fps);
  for(const [i,t] of times.entries()){
    await p.evaluate(t=>window.seek(t),t);
    await p.screenshot({path:path.join(out,(only?'t'+t:String(i).padStart(4,'0'))+'.png'),omitBackground:true});
  }
  await b.close(); console.log('frames',times.length);
})();
