# -*- coding: utf-8 -*-
"""Build per-locale index.html files from _template.html + _strings.py.

Reads the template, performs string substitution per locale, writes to
{lang_subdir}/index.html. Also updates the root index.html (en-US) and
sitemap.xml.

Usage: python _build.py
"""
import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).parent

# (lang_code, subdir, hreflang) — subdir empty means root (en).
LOCALES = [
    ("en",    "",        "en"),
    ("ja",    "ja",      "ja"),
    ("ko",    "ko",      "ko"),
    ("zh-CN", "zh-CN",   "zh-CN"),
    ("zh-TW", "zh-TW",   "zh-TW"),
    ("es",    "es",      "es"),
    ("pt",    "pt-BR",   "pt-BR"),
    ("fr",    "fr",      "fr"),
    ("de",    "de",      "de"),
    ("ru",    "ru",      "ru"),
    ("ar",    "ar",      "ar"),
    ("hi",    "hi",      "hi"),
]

LANG_NAMES = {
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文",
    "es": "Español",
    "pt-BR": "Português (BR)",
    "fr": "Français",
    "de": "Deutsch",
    "ru": "Русский",
    "ar": "العربية",
    "hi": "हिन्दी",
}

BASE_URL = "https://sakuradevjp.github.io/notikeep-notes"


def url_for(subdir: str) -> str:
    return f"{BASE_URL}/" if subdir == "" else f"{BASE_URL}/{subdir}/"


def hreflang_block() -> str:
    lines = []
    for _, subdir, hreflang in LOCALES:
        lines.append(f'<link rel="alternate" hreflang="{hreflang}" href="{url_for(subdir)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/">')
    return "\n".join(lines)


def lang_switcher(current_subdir: str) -> str:
    """A small inline language switcher rendered at the very top of the body."""
    parts = []
    for _, subdir, hreflang in LOCALES:
        url = url_for(subdir)
        name = LANG_NAMES[hreflang]
        if subdir == current_subdir:
            parts.append(f'<strong>{name}</strong>')
        else:
            parts.append(f'<a href="{url}">{name}</a>')
    return ' · '.join(parts)


def build():
    from _strings import STRINGS
    import shutil

    template = (ROOT / "_template.html").read_text(encoding="utf-8")

    # Copy per-locale screenshots from store_screenshots into assets/{lang}/
    src_root = ROOT.parent / "notikeep" / "store_screenshots"
    if src_root.exists():
        for lang_key, _, _ in LOCALES:
            dst = ROOT / "assets" / lang_key
            dst.mkdir(parents=True, exist_ok=True)
            mapping = {
                "1.png": "main.png",   # Keep every notification (hero)
                "2.png": "swipe.png",  # Swipe to organize (step 3)
                "3.png": "imt-phone.png",  # Image timeline screen (IMT 3D inner)
                "8.png": "bell.png",   # Control sounds (step 2)
            }
            lang_src = src_root / lang_key
            for src_name, dst_name in mapping.items():
                src = lang_src / src_name
                if src.exists():
                    shutil.copy2(src, dst / dst_name)
            yt_src = src_root / "yt_v2" / f"{lang_key}.png"
            if yt_src.exists():
                shutil.copy2(yt_src, dst / "yt.png")

    for lang_key, subdir, hreflang in LOCALES:
        if lang_key not in STRINGS:
            print(f"WARN: no strings for {lang_key}, skipping")
            continue

        s = dict(STRINGS[lang_key])
        s["LANG_ATTR"] = hreflang
        if hreflang == "ar":
            s["DIR_ATTR"] = ' dir="rtl"'
        else:
            s["DIR_ATTR"] = ""
        s["HREFLANG_LINKS"] = hreflang_block()
        s["LANG_SWITCHER"] = lang_switcher(subdir)
        s["CANONICAL_URL"] = url_for(subdir)

        # Asset base path: relative from the index.html location
        # Root (en): assets/en/X.png
        # subdir (ja, ko, etc.): ../assets/ja/X.png
        if subdir == "":
            s["ASSET_BASE"] = f"assets/{lang_key}/"
        else:
            s["ASSET_BASE"] = f"../assets/{lang_key}/"
        # og:image needs an absolute URL for crawlers
        s["OG_IMAGE_URL"] = f"{BASE_URL}/assets/{lang_key}/main.png"

        out = template
        for k, v in s.items():
            placeholder = f"{{{{{k}}}}}"
            out = out.replace(placeholder, v)

        # Sanity: warn on any unsubstituted placeholders
        leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", out)
        if leftover:
            print(f"  ! {lang_key}: unsubstituted: {set(leftover)}")

        # Write file
        if subdir == "":
            target = ROOT / "index.html"
        else:
            (ROOT / subdir).mkdir(exist_ok=True)
            target = ROOT / subdir / "index.html"
        target.write_text(out, encoding="utf-8")
        print(f"  wrote {target.relative_to(ROOT)} ({len(out)} chars)")

    # Build sitemap
    write_sitemap()


def write_sitemap():
    today = "2026-04-25"
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    for _, subdir, hreflang in LOCALES:
        priority = "1.0" if subdir == "" else "0.8"
        lines.append("  <url>")
        lines.append(f"    <loc>{url_for(subdir)}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        for _, sub_inner, hl_inner in LOCALES:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{hl_inner}" href="{url_for(sub_inner)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote sitemap.xml ({len(LOCALES)} URLs)")


if __name__ == "__main__":
    build()
