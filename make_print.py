"""Screenshots the mock at laptop / 27" sizes, then prints print.html to printout.pdf.
Run: python make_print.py   (needs Python playwright + Edge)"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
SHOTS = {  # name: (css width, css height, variant)
    'laptop': (1280, 800, 'today'),
    'monitor-today': (1920, 1080, 'today'),
    'monitor-wide': (1920, 1080, 'wide'),
}

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for name, (w, h, v) in SHOTS.items():
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto((ROOT / 'mock.html').as_uri() + f'?v={v}')
        pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready')
        pg.screenshot(path=str(ROOT / 'shots' / f'{name}.png'))
        pg.close()
    pg = b.new_page()
    pg.goto((ROOT / 'print.html').as_uri())
    pg.wait_for_load_state('networkidle')
    pg.pdf(path=str(ROOT / 'printout.pdf'), format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
    pg.set_viewport_size({'width': 794, 'height': 1123})
    pg.screenshot(path=str(ROOT / 'shots' / 'print-preview.png'), full_page=True)
    b.close()
