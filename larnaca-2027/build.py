#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה את index.html של larnaca-2027 מתוך גוף הארטיפקט.

הדף חי בשני מקומות מאותו מקור אחד:
  • ארטיפקט פרטי  — https://claude.ai/artifact/7zd4VAYxDE36yeCkNm1Akn  (שם יש DB ל-RSVP)
  • גיטהאב פייג׳ס — https://yaelavgil.github.io/yaella/larnaca-2027/   (שם ה-RSVP נופל להעתקה לוואטסאפ)

שימוש:  python3 build.py <נתיב לקובץ הגוף>
הגוף הוא הקובץ שמתפרסם כארטיפקט: בלי doctype/head, עם <title> ו-<style> בראשו.
"""
import re
import sys
import pathlib

SRC = sys.argv[1] if len(sys.argv) > 1 else None
if not SRC:
    sys.exit('שימוש: python3 build.py <נתיב לקובץ הגוף של הארטיפקט>')

body = pathlib.Path(SRC).read_text(encoding='utf-8')

body = body.replace('<title>לרנקה 2027</title>\n', '', 1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '', 1)

links = re.findall(r'<link rel="pre[^>]*>|<link rel="stylesheet"[^>]*>', body)
for l in links:
    body = body.replace(l + '\n', '', 1)

m = re.search(r'<style>.*?</style>\n', body, re.S)
if not m:
    sys.exit('לא נמצא בלוק <style> בקובץ המקור')
style = m.group(0)
body = body.replace(style, '', 1)

HEAD = '''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>רובי ויליאמס · לרנקה 2027</title>
<meta name="description" content="24 ביולי 2027, לרנקה. שעה טיסה מהבית, סוף שבוע אחד. כל הפרטים, המחירים והמלונות — ואפשר לסמן מי בא.">
<meta name="theme-color" content="#09090b">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="לרנקה 2027">
<meta property="og:title" content="רובי ויליאמס · לרנקה · 24.7.2027">
<meta property="og:description" content="₪181 בדשא | ₪449 לגולדן רינג. שעה טיסה מהבית, סוף שבוע אחד, 28,000 איש. כל הפרטים, המחירים והמלונות — ואפשר לסמן מי בא.">
<meta property="og:image" content="https://yaelavgil.github.io/yaella/larnaca-2027/og4.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="רובי ויליאמס בלרנקה, 24 ביולי 2027">
<meta property="og:url" content="https://yaelavgil.github.io/yaella/larnaca-2027/">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Heebo:wght@300;400;500;700;900&display=swap">
<style>
*{box-sizing:border-box}
html,body{background:#09090b}
img{display:block; max-width:100%}
[hidden]{display:none !important}
</style>
''' + style + '''</head>
<body>
'''

out = HEAD + body.lstrip('\n') + '\n</body>\n</html>\n'
dest = pathlib.Path(__file__).parent / 'index.html'
dest.write_text(out, encoding='utf-8')
print('נכתב', dest, len(out), 'תווים ·', len(links), 'קישורי פונט הועברו ל-head')
