#!/usr/bin/env python3
import json, re, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'catalog' / 'robot-config.json'
OUTPUT = ROOT / 'catalog' / 'robot-catalog.json'

UA = 'GuiaNaturalNaturaCatalogBot/1.0 (GitHub Actions)'

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

def wiki_summary(term):
    title = urllib.parse.quote(term.replace(' ', '_'), safe='')
    url = f'https://pt.wikipedia.org/api/rest_v1/page/summary/{title}'
    try:
        data = get_json(url)
        if data.get('type') == 'standard':
            return data
    except Exception:
        pass
    return None

def commons_image(term):
    q = urllib.parse.quote(f'{term} plant', safe='')
    api = ('https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search'
           f'&gsrsearch={q}&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url%7Cextmetadata'
           '&iiurlwidth=900')
    try:
        data = get_json(api)
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            info = (page.get('imageinfo') or [{}])[0]
            url = info.get('thumburl') or info.get('url')
            if not url:
                continue
            meta = info.get('extmetadata', {})
            license_name = (meta.get('LicenseShortName') or {}).get('value', '')
            artist = re.sub('<[^>]+>', '', (meta.get('Artist') or {}).get('value', ''))
            return {
                'imageUrl': url,
                'imageSourceUrl': 'https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=' + urllib.parse.quote(term),
                'imageLicense': license_name,
                'imageAuthor': artist
            }
    except Exception:
        pass
    return {}

def slug(s):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower().strip())
    return s.strip('-')

def main():
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    old = {}
    if OUTPUT.exists():
        try:
            old = {x['id']: x for x in json.loads(OUTPUT.read_text(encoding='utf-8')).get('items', [])}
        except Exception:
            old = {}

    items = []
    seen = set()
    max_items = int(cfg.get('maxItemsPerRun', 12))

    for category, terms in cfg.get('categories', {}).items():
        for term in terms:
            key = slug(term)
            if key in seen or len(items) >= max_items:
                continue
            seen.add(key)
            sid = 'bot-' + key
            if sid in old:
                item = old[sid]
                item['category'] = category
                items.append(item)
                continue

            summary = wiki_summary(term)
            if not summary:
                continue
            image = commons_image(term)
            name = summary.get('title') or term.title()
            item = {
                'id': sid,
                'name': name,
                'popularName': term.title(),
                'scientificName': '',
                'category': category,
                'usageType': 'Informativo; confirmar se o produto é para uso oral ou externo antes de utilizar',
                'description': summary.get('extract', ''),
                'purpose': 'Informação botânica e usos tradicionalmente descritos na fonte. Não constitui indicação de tratamento.',
                'usage': 'Consultar a fonte oficial e a embalagem do produto antes de qualquer uso.',
                'ingestion': 'Não informado automaticamente. Não ingerir com base apenas nesta página.',
                'ingestible': False,
                'ingredients': '',
                'contraindications': 'Não informado automaticamente; consultar fonte oficial e orientação profissional quando aplicável.',
                'adverseReactions': 'Não informado automaticamente.',
                'targetAudience': 'Informativo para público geral.',
                'warnings': 'Cadastro automático para revisão. Não substitui orientação profissional nem comprovação de eficácia ou segurança.',
                'imageUrl': image.get('imageUrl', ''),
                'imageSourceUrl': image.get('imageSourceUrl', ''),
                'imageLicense': image.get('imageLicense', ''),
                'imageAuthor': image.get('imageAuthor', ''),
                'source': 'Wikimedia Commons / Wikipédia em português',
                'sourceUrl': summary.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'updatedAt': datetime.now(timezone.utc).isoformat(),
                'status': 'draft',
                'autoCollected': True
            }
            items.append(item)

    # Preserve all previously collected items, then replace/update current batch.
    merged = dict(old)
    for item in items:
        merged[item['id']] = item

    payload = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'items': list(merged.values())
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Robô: {len(items)} itens processados; {len(merged)} itens no catálogo automático.')

if __name__ == '__main__':
    main()
