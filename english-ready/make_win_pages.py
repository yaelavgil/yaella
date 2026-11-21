#!/usr/bin/env python3
"""The win link a kid sends (w.html?i=CODE) shows its WhatsApp preview from static tags:
WhatsApp never runs the page's script, so one page cannot say who won. So every kid gets
their own copy, w-<slug>.html, whose preview picture says "<name> won!".

Run after adding a kid (and keep WIN_PAGES in index.html in step):
    python3 english-ready/make_win_pages.py
Needs Google Chrome (headless) and Pillow. Pictures come from og-src/win.html.
"""
import pathlib, re, subprocess, tempfile, urllib.parse
from PIL import Image

D = pathlib.Path(__file__).resolve().parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
BASE = 'https://yaelavgil.github.io/yaella/english-ready/'
V = '4'  # bump to make WhatsApp fetch the pictures again
# slug, first name as the kid sees it, 'f' or 'm' (זכתה / זכה)
KIDS = [('gur', 'גור', 'm'), ('dani', 'דני', 'f'), ('lili', 'לילי', 'f')]


def shot(query, out):
    with tempfile.TemporaryDirectory() as t:
        png = pathlib.Path(t) / 'x.png'
        url = (D / 'og-src' / 'win.html').as_uri() + ('?' + urllib.parse.urlencode(query) if query else '')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1200,630',
                        '--virtual-time-budget=4000', f'--screenshot={png}', url], check=True, capture_output=True)
        Image.open(png).convert('RGB').save(out, quality=88)


def main():
    src = (D / 'w.html').read_text()
    for slug, name, g in KIDS:
        won = 'זכתה' if g == 'f' else 'זכה'
        title = f'🎡 {name} {won} בגלגל ההפתעות!'
        img = f'{BASE}og-win-{slug}.jpg?v={V}'
        s = src
        s = re.sub(r'<title>[^<]*</title>', f'<title>{title} · מאסטר אנגלית</title>', s, count=1)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\g<1>{title}', s, count=1)
        s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', rf'\g<1>{title}', s, count=1)
        s = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*', rf'\g<1>{img}', s)
        s = re.sub(r'(<meta property="og:url" content=")[^"]*', rf'\g<1>{BASE}w-{slug}.html', s, count=1)
        s = s.replace('לחצו כדי לראות מה הפרס.', f'לחצו כדי לראות במה {won}.')
        s = s.replace('so the preview is the same for every win.', f'this copy is made by make_win_pages.py for one kid ({slug}); edit w.html, not this file.')
        (D / f'w-{slug}.html').write_text(s)
        shot({'n': name, 'v': g}, D / f'og-win-{slug}.jpg')
        print('ok', slug)


if __name__ == '__main__':
    main()
