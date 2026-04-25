# -*- coding: utf-8 -*-
"""Replace misleading 'Encrypted backup' wording with accurate phrasing.

The actual NotiKeep backup is a plain ZIP — calling it 'encrypted' is
incorrect. Replaces with locale-appropriate 'backup with images' wording.
Also strips the locale-specific 'encrypted ZIP' / 'encrypted backup'
mentions from FAQ4_A and FAQ7_A.

Targets two files:
  notikeep-notes/_strings.py
  notikeep/store_screenshots/translations.py
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FILES = [
    Path(r"C:\Users\ryo_d\notikeep-notes\_strings.py"),
    Path(r"C:\Users\ryo_d\notikeep\store_screenshots\translations.py"),
]

# (find, replace) pairs. Order matters — longer phrases first to avoid partial.
REPLACEMENTS = [
    # English
    ("encrypted ZIP", "ZIP archive"),
    ("encrypted backup", "backup"),
    ("Encrypted backup &amp; restore", "Backup &amp; restore"),
    ("Encrypted backup with images", "Backup with images"),
    ("Encrypted backup", "Backup with images"),
    # Japanese
    ("暗号化ZIP", "ZIP"),
    ("暗号化バックアップ＆復元", "バックアップ＆復元"),
    ("暗号化バックアップ（画像付き）", "バックアップ（画像付き）"),
    ("暗号化バックアップ", "画像付きバックアップ"),
    # Korean
    ("암호화 ZIP", "ZIP"),
    ("암호화 백업 & 복원", "백업 & 복원"),
    ("이미지 포함 암호화 백업", "이미지 포함 백업"),
    ("암호화 백업", "이미지 포함 백업"),
    # zh-CN
    ("加密 ZIP", "ZIP"),
    ("加密备份 & 恢复", "备份 & 恢复"),
    ("含图片的加密备份", "含图片备份"),
    ("加密备份", "含图片备份"),
    # zh-TW
    ("加密 ZIP", "ZIP"),
    ("加密備份 & 還原", "備份 & 還原"),
    ("含圖片的加密備份", "含圖片備份"),
    ("加密備份", "含圖片備份"),
    # Spanish
    ("ZIP cifrado", "ZIP"),
    ("Copia de seguridad y restauración cifradas", "Copia de seguridad y restauración"),
    ("copia cifrada con imágenes", "copia con imágenes"),
    ("copia cifrada", "copia"),
    ("Copia cifrada con imágenes", "Copia con imágenes"),
    ("Copia de seguridad cifrada", "Copia de seguridad con imágenes"),
    # Portuguese
    ("ZIP criptografado", "ZIP"),
    ("Backup & restauração criptografados", "Backup & restauração"),
    ("Backup criptografado com imagens", "Backup com imagens"),
    ("Backup criptografado", "Backup com imagens"),
    ("backup criptografado", "backup"),
    # French
    ("ZIP chiffré", "ZIP"),
    ("Sauvegarde et restauration chiffrées", "Sauvegarde et restauration"),
    ("Sauvegarde chiffrée avec images", "Sauvegarde avec images"),
    ("Sauvegarde chiffrée", "Sauvegarde avec images"),
    ("sauvegarde chiffrée", "sauvegarde"),
    # German
    ("verschlüsseltes ZIP", "ZIP"),
    ("Verschlüsseltes ZIP", "ZIP"),
    ("Verschlüsselte Sicherung & Wiederherstellung", "Sicherung & Wiederherstellung"),
    ("Verschlüsselte Sicherung mit Bildern", "Sicherung mit Bildern"),
    ("Verschlüsselte Sicherung", "Sicherung mit Bildern"),
    ("verschlüsselte Sicherung", "Sicherung"),
    # Russian
    ("зашифрованный ZIP", "ZIP"),
    ("Зашифрованный ZIP", "ZIP"),
    ("Зашифрованная резервная копия и восстановление", "Резервная копия и восстановление"),
    ("Зашифрованные резервные копии и восстановление", "Резервные копии и восстановление"),
    ("Зашифрованная копия с изображениями", "Копия с изображениями"),
    ("Зашифрованная резервная копия", "Резервная копия с изображениями"),
    ("зашифрованную резервную копию", "резервную копию"),
    # Arabic
    ("ZIP مشفّر", "ZIP"),
    ("ZIP مشفّرًا", "ZIP"),
    ("النسخ الاحتياطي والاستعادة المشفّرة", "النسخ الاحتياطي والاستعادة"),
    ("نسخة احتياطية مشفّرة بالصور", "نسخة احتياطية بالصور"),
    ("نسخة احتياطية مشفّرة", "نسخة احتياطية"),
    # Hindi
    ("एन्क्रिप्टेड ZIP", "ZIP"),
    ("एन्क्रिप्टेड बैकअप और पुनर्स्थापन", "बैकअप और पुनर्स्थापन"),
    ("छवि सहित एन्क्रिप्टेड बैकअप", "छवियों सहित बैकअप"),
    ("एन्क्रिप्टेड बैकअप", "छवियों सहित बैकअप"),
]


def main():
    for fp in FILES:
        text = fp.read_text(encoding="utf-8")
        original = text
        for find, repl in REPLACEMENTS:
            text = text.replace(find, repl)
        if text != original:
            count = sum(1 for f, _ in REPLACEMENTS if f in original)
            fp.write_text(text, encoding="utf-8")
            print(f"updated {fp.name} ({count} unique terms found)")
        else:
            print(f"no changes in {fp.name}")


if __name__ == "__main__":
    main()
