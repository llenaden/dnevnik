#!/usr/bin/env python3
"""Собирает index.html из папки src/.

Запуск:  python3 build.py
Результат: index.html — одна самодостаточная страница (стили, скрипты и иконки внутри).
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"

def read(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")

body = (read("template.html")
        .replace("/*VEC*/", read("vec.js"))
        .replace("/*GLV*/", read("glv.js"))
        .replace("/*GL*/", read("glyphs.js"))
        .replace("/*ARTICLES*/", read("articles.js"))
        .replace("/*FOODS*/", read("foods.js")))

# title, favicon links and fonts move into <head>; the rest goes into <body>
head_part, rest = body.split("<style>", 1)
head_part = head_part.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")

page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="theme-color" content="#F7F7F7">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Дневник тела">
<link rel="manifest" href="manifest.webmanifest">
{head_part.strip()}
<style>html{{padding-top:env(safe-area-inset-top,0px)}}body{{margin:0}}</style>
</head>
<body>
<style>{rest}
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
print("index.html собран:", round(len(page.encode()) / 1024), "КБ")
