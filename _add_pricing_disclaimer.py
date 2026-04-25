# -*- coding: utf-8 -*-
"""Add PRICING_DISCLAIMER key to each locale in _strings.py.

Inserts after PRICE_NOTE_LIFETIME line.
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DISCLAIMERS = {
    "en":    "Prices shown are in USD. Google Play displays the equivalent in your local currency at checkout.",
    "ja":    "表示価格はUSDです。Google Playの購入画面では現地通貨に換算されて表示されます。",
    "ko":    "표시된 가격은 USD 기준입니다. Google Play 결제 화면에서는 현지 통화로 환산되어 표시됩니다.",
    "zh-CN": "显示价格为美元。Google Play 结账时会按当地货币换算显示。",
    "zh-TW": "顯示價格為美元。Google Play 結帳時會按當地貨幣換算顯示。",
    "es":    "Los precios se muestran en USD. Google Play muestra el equivalente en tu moneda local en el momento de pagar.",
    "pt":    "Preços exibidos em USD. O Google Play mostra o equivalente em sua moeda local no momento da compra.",
    "fr":    "Tarifs en USD. Google Play affiche l'équivalent dans votre devise locale au moment du paiement.",
    "de":    "Preise in USD. Google Play zeigt den Gegenwert in deiner Lokalwährung bei der Bezahlung.",
    "ru":    "Цены указаны в USD. Google Play отображает эквивалент в вашей локальной валюте при оплате.",
    "ar":    "الأسعار المعروضة بالدولار الأمريكي. يعرض Google Play المعادل بعملتك المحلية عند الدفع.",
    "hi":    "दिखाई गई कीमतें USD में हैं। Google Play चेकआउट के समय आपकी स्थानीय मुद्रा में समतुल्य राशि दिखाता है।",
}

PATH = Path(r"C:\Users\ryo_d\notikeep-notes\_strings.py")


def main():
    text = PATH.read_text(encoding="utf-8")
    for lang_key, disclaimer in DISCLAIMERS.items():
        # Find the locale block and insert after PRICE_NOTE_LIFETIME
        # Find the marker and append our new line right after.
        marker = '"PRICE_NOTE_LIFETIME":'
        if f'"{lang_key}":' not in text:
            print(f"  ! {lang_key}: locale not found")
            continue
        # Locate the locale block start
        start = text.index(f'"{lang_key}":')
        # Locate the next occurrence of PRICE_NOTE_LIFETIME after start
        idx = text.index(marker, start)
        # Find end of that line (the closing comma+newline)
        end_of_line = text.index("\n", idx)
        # The next line should be where we insert
        new_line = f'    "PRICING_DISCLAIMER": {disclaimer!r},\n'
        # Use repr but ensure unicode is preserved in output (use json.dumps for safe quoting)
        import json
        new_line = f'    "PRICING_DISCLAIMER": {json.dumps(disclaimer, ensure_ascii=False)},\n'
        # Skip if PRICING_DISCLAIMER already present in this locale's block
        next_close = text.index('\n},\n', idx)
        block = text[start:next_close]
        if '"PRICING_DISCLAIMER"' in block:
            print(f"  - {lang_key}: already has PRICING_DISCLAIMER")
            continue
        text = text[:end_of_line + 1] + new_line + text[end_of_line + 1:]
        print(f"  + {lang_key}: added")

    PATH.write_text(text, encoding="utf-8")
    print(f"\nSaved {PATH}")


if __name__ == "__main__":
    main()
