import json, urllib.parse, urllib.request
from pathlib import Path
import cairosvg
from PIL import Image
from io import BytesIO
UA='SolaAnalyse/1.0 (contact@example.com)'
logos=Path('logos'); logos.mkdir(exist_ok=True)
items={
 'AP':('Labour_Party_(Norway)','Arbeiderpartiet logo'),
 'H':('Høyre','Høyre logo'),
 'FrP':('Progress_Party_(Norway)','Fremskrittspartiet logo'),
 'MDG':('Green_Party_(Norway)','Miljøpartiet De Grønne logo'),
 'INP':('Industry_and_Business_Party','Industri- og Næringspartiet logo'),
}
def get(url):
 r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=30)
 return r.read(),r.headers.get('Content-Type',''),r.geturl()
def save(abbr,raw,ct,url):
 out=logos/(abbr+'.png'); svg='svg' in ct.lower() or '.svg' in urllib.parse.urlparse(url).path.lower() or raw.lstrip().startswith(b'<svg')
 if svg: cairosvg.svg2png(bytestring=raw,write_to=str(out),output_width=500); return 'PNG (SVG rasterized)'
 with Image.open(BytesIO(raw)) as im: im.convert('RGBA').save(out,'PNG')
 return 'PNG (raster converted)'
def api_image(title):
 q=urllib.parse.urlencode({'action':'query','format':'json','prop':'pageimages','piprop':'original|thumbnail','pithumbsize':'500','titles':title})
 data,_,_=get('https://en.wikipedia.org/w/api.php?'+q); pages=json.loads(data)['query']['pages']; p=next(iter(pages.values()))
 return p.get('original',{}).get('source') or p.get('thumbnail',{}).get('source')
def commons_image(search):
 q=urllib.parse.urlencode({'action':'query','format':'json','generator':'search','gsrsearch':search,'gsrnamespace':'6','gsrlimit':'10','prop':'imageinfo','iiprop':'url','iiurlwidth':'500'})
 data,_,_=get('https://commons.wikimedia.org/w/api.php?'+q); pages=json.loads(data).get('query',{}).get('pages',{})
 for p in pages.values():
  u=(p.get('imageinfo') or [{}])[0].get('thumburl') or (p.get('imageinfo') or [{}])[0].get('url')
  if u: return u
for abbr,(title,search) in items.items():
 method='failed'; fmt='-'
 for label, fn in [('api',lambda:api_image(title)),('commons',lambda:commons_image(search))]:
  try:
   u=fn()
   if u:
    raw,ct,final=get(u); fmt=save(abbr,raw,ct,final); method=label; break
  except Exception as e: err=str(e)
 print(f'{abbr:4} | {method:7} | {fmt}')
