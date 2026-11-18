const {chromium}=require('playwright');
(async()=>{
  const [src,out,w,h,scale]=process.argv.slice(2);
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+(scale||1)});
  await p.goto('file://'+src); await p.waitForFunction(()=>document.body.dataset.ready==='1',{timeout:15000});
  await p.waitForTimeout(200);
  console.log(await p.evaluate(()=>{const t=document.getElementById('tag'),l=document.getElementById('lockup');return [t.textContent,getComputedStyle(t).fontSize,t.getBoundingClientRect().width.toFixed(1),l.getBoundingClientRect().width.toFixed(1)].join(' | ')}));
  await p.screenshot({path:out}); await b.close();
})();
