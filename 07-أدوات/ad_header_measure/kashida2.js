const {chromium}=require('playwright');
(async()=>{
  const [src,target]=process.argv.slice(2);
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  await p.goto('file://'+src); await p.waitForFunction(()=>document.body.dataset.ready==='1');
  const r=await p.evaluate((target)=>{
    const c=document.createElement('canvas').getContext('2d'); c.font='500 20px Plex';
    const ink=t=>{const m=c.measureText(t);return m.actualBoundingBoxLeft+m.actualBoundingBoxRight};
    const words=[['الوكي','ل'],['الع','ام'],['للخط','وط'],['الجوي','ة'],['العراقي','ة']];  // stretch before the last joined letter
    const build=n=>words.map((w,i)=>w[0]+'ـ'.repeat(Math.floor(n/5)+(i<n%5?1:0))+w[1]).join(' ');
    let n=0; while(ink(build(n+1))<=target) n++;
    const t=build(n), w=ink(t), sp=(c.measureText(' ').width);
    return {n,t,w,rest:target-w,wordSpacing:(target-w)/4};
  },+target);
  console.log(JSON.stringify(r)); await b.close();
})();
