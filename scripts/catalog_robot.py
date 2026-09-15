#!/usr/bin/env python3
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'catalog' / 'robot-config.json'
OUTPUT = ROOT / 'catalog' / 'robot-catalog.json'
UA = 'GuiaNaturalNaturaCatalogBot/2.0 (GitHub Actions; CBPM Fiocruz primary source)'
CBPM_URL = 'https://cbpm.fiocruz.br/catalogue'


def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')


def post_form(url, data):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')


def clean_text(value):
    value = re.sub(r'<[^>]+>', ' ', value)
    value = html.unescape(value)
    return re.sub(r'\s+', ' ', value).strip()


def cbpm_search(scientific_name):
    """Consulta o catálogo oficial da CBPM por gênero + epíteto e extrai registros botânicos."""
    parts = scientific_name.replace('×', ' ').split()
    if len(parts) < 2:
        return []
    genus, epithet = parts[0], parts[1]
    try:
        raw = post_form(CBPM_URL, {
            'catalognumber': '', 'family': '', 'genus': genus, 'species': epithet,
            'country': '', 'stateprovince': '', 'collector': '',
            'monthcollected': '', 'yearcollected': ''
        })
    except Exception as exc:
        print(f'CBPM indisponível para {scientific_name}: {exc}')
        return []

    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', raw, flags=re.I | re.S)
    records = []
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, flags=re.I | re.S)
        values = [clean_text(c) for c in cells]
        if len(values) < 6 or not values[0].startswith('CBPM '):
            continue
        records.append({
            'catalogNumber': values[0],
            'family': values[1],
            'scientificName': values[2],
            'collector': values[3],
            'collectionDate': values[4],
            'locality': values[5],
            'sourceUrl': CBPM_URL
        })
    return records


def commons_image(term):
    q = urllib.parse.quote(term, safe='')
    api = ('https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search'
           f'&gsrsearch={q}&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url%7Cextmetadata'
           '&iiurlwidth=900')
    try:
        data = json.loads(get_text(api))
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

    if not cfg.get('enabled', True):
        print('Robô desativado.')
        return

    items = []
    seen = set()
    max_items = int(cfg.get('maxItemsPerRun', 20))
    scientific_map = cfg.get('scientificNames', {})

    for category, terms in cfg.get('categories', {}).items():
        for term in terms:
            key = slug(term)
            if key in seen or len(items) >= max_items:
                continue
            seen.add(key)
            sid = 'bot-' + key
            scientific = scientific_map.get(term, '').strip()
            if not scientific:
                print(f'Sem nome científico configurado para: {term}')
                continue

            records = cbpm_search(scientific)
            if not records:
                print(f'Sem registro na CBPM para: {term} ({scientific})')
                continue

            primary = next((r for r in records if r.get('scientificName', '').lower() == scientific.lower()), records[0])
            image = commons_image(term)
            previous = old.get(sid, {})
            item = {
                'id': sid,
                'name': term.title(),
                'popularName': term.title(),
                'scientificName': primary.get('scientificName') or scientific,
                'family': primary.get('family', ''),
                'category': category,
                'usageType': 'Informativo; confirmar se o produto é para uso oral ou externo antes de utilizar',
                'description': f"Registro botânico encontrado no catálogo da Coleção Botânica de Plantas Medicinais (CBPM/Fiocruz). Família: {primary.get('family', '')}.",
                'purpose': 'Informação botânica e rastreabilidade da espécie. Não constitui indicação de tratamento.',
                'usage': 'Consultar fonte oficial e embalagem do produto antes de qualquer uso.',
                'ingestion': 'Não informado automaticamente. Não ingerir com base apenas nesta página.',
                'ingestible': False,
                'ingredients': '',
                'contraindications': 'Não informado pela consulta automática; verificar fontes sanitárias oficiais antes de orientar uso.',
                'adverseReactions': 'Não informado pela consulta automática.',
                'targetAudience': 'Informativo para público geral.',
                'warnings': 'Cadastro automático para revisão. A presença no acervo botânico não comprova eficácia, segurança ou indicação terapêutica.',
                'cbpmRecords': records[:10],
                'cbpmCatalogNumber': primary.get('catalogNumber', ''),
                'cbpmCollector': primary.get('collector', ''),
                'cbpmCollectionDate': primary.get('collectionDate', ''),
                'cbpmLocality': primary.get('locality', ''),
                'imageUrl': image.get('imageUrl', previous.get('imageUrl', '')),
                'imageSourceUrl': image.get('imageSourceUrl', previous.get('imageSourceUrl', '')),
                'imageLicense': image.get('imageLicense', previous.get('imageLicense', '')),
                'imageAuthor': image.get('imageAuthor', previous.get('imageAuthor', '')),
                'source': 'Coleção Botânica de Plantas Medicinais (CBPM) / Fiocruz',
                'sourceUrl': CBPM_URL,
                'updatedAt': datetime.now(timezone.utc).isoformat(),
                'status': 'draft',
                'autoCollected': True,
                'primarySource': 'CBPM/Fiocruz'
            }
            items.append(item)
            print(f'CBPM: {term} -> {primary.get("scientificName")} | {len(records)} registro(s)')

    merged = dict(old)
    for item in items:
        merged[item['id']] = item

    payload = {'generatedAt': datetime.now(timezone.utc).isoformat(), 'items': list(merged.values())}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Robô CBPM: {len(items)} itens processados; {len(merged)} itens no catálogo automático.')


if __name__ == '__main__':
    main()
