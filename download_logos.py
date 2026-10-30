import json
import urllib.request
import urllib.parse
from pathlib import Path
import cairosvg
from PIL import Image
from io import BytesIO

logos = Path('logos')
logos.mkdir(exist_ok=True)
items = [
    ('AP', 'Labour_Party_(Norway)'),
    ('H', 'H%C3%B8yre'),
    ('FrP', 'Progress_Party_(Norway)'),
    ('SV', 'Socialist_Left_Party'),
    ('KrF', 'Christian_Democratic_Party_(Norway)'),
    ('V', 'Liberal_Party_(Norway)'),
    ('MDG', 'Green_Party_(Norway)'),
    ('INP', 'Industry_and_Business_Party'),
]
for abbr, title in items:
    try:
        api = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + title
        req = urllib.request.Request(api, headers={'User-Agent': 'SolaAnalyse/1.0 (contact@example.com)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
        source = (data.get('originalimage') or {}).get('source') or (data.get('thumbnail') or {}).get('source')
        if not source:
            raise RuntimeError('No image source in API response')
        req = urllib.request.Request(source, headers={'User-Agent': 'SolaAnalyse/1.0 (contact@example.com)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            content_type = response.headers.get('Content-Type', '')
        path = urllib.parse.urlparse(source).path.lower()
        is_svg = path.endswith('.svg') or 'svg' in content_type.lower() or raw.lstrip().startswith(b'<svg')
        target = logos / (abbr + '.png')
        if is_svg:
            cairosvg.svg2png(bytestring=raw, write_to=str(target), output_width=400)
            fmt = 'SVG -> PNG'
        else:
            with Image.open(BytesIO(raw)) as image:
                image.convert('RGBA').save(target, 'PNG')
            fmt = content_type or 'raster image'
        print(f'{abbr}: success ({fmt}) -> {target}')
    except Exception as exc:
        print(f'{abbr}: FAILED: {exc}')
