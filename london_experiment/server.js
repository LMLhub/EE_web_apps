'use strict';
const http=require('node:http'), fs=require('node:fs'), path=require('node:path');
const port=Number(process.env.PORT||4173);
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.ico':'image/x-icon'};
const allowed=new Set(['index.html','styles.css','engine.js','app.js']);
http.createServer((req,res)=>{
  let name;
  try{name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\//,'')||'index.html';}catch{res.writeHead(400);res.end();return;}
  if(!allowed.has(name)){res.writeHead(404);res.end('Not found');return;}
  fs.readFile(path.join(__dirname,name),(error,data)=>{if(error){res.writeHead(500);res.end('Unable to read file');return;}res.writeHead(200,{'Content-Type':types[path.extname(name)],'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(data);});
}).listen(port,'127.0.0.1',()=>console.log(`Boundary Experiment · http://127.0.0.1:${port}`));
