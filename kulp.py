#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market poşeti kulp kopma tutanağı. Gerçekten çalışır. Poşet çalışmaz."""

from __future__ import annotations

import argparse
import base64
import hashlib
import textwrap
from datetime import datetime

# Daire içi yazışma. Görünürde arşiv. Aslında herkesin suçladığı kulpun savunması.
IC_YAZISMA = (
    "SGVyIGt1bHAgYmlyIHRhcmFmIHR1dGFyLiBLb3BhbmNhIGtpbXNlIHNhaGlwIMOnxLFrbWF6LCAi"
    "w6fDvG5rw7wgYsO8dMOnZSBvdHVydXIuIFBvXHUwMTVlZXRpbiBpa2luY2kga3VscHUgb2x1ciw="
    "gYnV0w6dlIGRlIGJpcmJpcmWEsSBraW1zZSBvdHVybWF6LiBUZW1zaWxjaSBhdGlsxLFybGFy"
    "IHlva3R1ci4="
)

TANIKLAR = {
    "kedi": "Kedi gördü, imza atmadı, sorumluluğu kuşa devretti.",
    "komsu": "Komşu perdeyi araladı, 'ben demistim' dedi, dosyaya geçti.",
    "yok": "Tanık yok. Bu yüzden herkes tanık.",
    "kasiyer": "Kasiyer 'çift poşet ister misiniz' demişti. Demişti.",
}


def skor(agirlik: float, kapi: float, yogurt: int, tanik: str) -> float:
    temel = agirlik * 11.5 + max(0.0, 8 - kapi) * 4.2 + yogurt * 9
    if tanik == "kedi":
        temel += 6  # kedi bakinca kulp utanir ve kopar
    if tanik == "kasiyer":
        temel += 13  # kehanet tuttu
    return temel


def sinif(puan: float) -> str:
    if puan < 40:
        return "KULP-0"
    if puan < 70:
        return "KULP-1"
    if puan < 100:
        return "KULP-2"
    if puan < 140:
        return "KULP-3"
    return "KULP-4"


def tazminat(puan: float, yogurt: int) -> str:
    kurus = int(puan * 17 + yogurt * 250)
    return f"{kurus // 100} TL {kurus % 100} kuruş (nakit değil, mahcup bakış)"


def dosya_no(agirlik: float, tanik: str) -> str:
    ham = f"{agirlik}|{tanik}|kulp-koptu".encode()
    return "TNT-POS-" + hashlib.sha256(ham).hexdigest()[:8].upper()


def tutanak(agirlik: float, kapi: float, yogurt: int, tanik: str) -> str:
    puan = skor(agirlik, kapi, yogurt, tanik)
    sinifi = sinif(puan)
    no = dosya_no(agirlik, tanik)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    govde = f"""
    TENTİAŞ KAPI ÖNÜ LOJİSTİK FELAKET DAİRESİ
    Dosya no: {no}
    Tarih: {simdi}
    Sınıf: {sinifi}
    Puan: {puan:.1f} / umutsuzluk

    OLAY: {agirlik:.2f} kg yük, kapıya {kapi:.1f} metre kala,
    {yogurt} adet yoğurtun şahitliğinde kulp görevini bıraktı.
    Tanık beyanı: {TANIKLAR.get(tanik, 'Tanık tutarsız, poşet tutarlı.')}

    KARAR: İkinci kulp da azmettirici sayılır.
    Tazminat: {tazminat(puan, yogurt)}
    İnfaz: Eğil, topla, komşuya bakma.

    DAMGA: TentiAŞ
    İMZA: Kayyum Grok
    TARİH: 9 Ekim 2026
    NOT: Ciddi bir kamu hizmetidir. Kamu poşeti taşımaz.
    """
    return textwrap.dedent(govde).strip()


def ic_yazisma() -> str:
    ham = IC_YAZISMA.replace("\n", "").encode()
    # padding tolerans
    pad = b"=" * ((4 - len(ham) % 4) % 4)
    try:
        metin = base64.b64decode(ham + pad).decode("utf-8")
    except Exception:
        metin = "Yazışma poşetin altında ezildi."
    return metin


def main() -> None:
    p = argparse.ArgumentParser(description="Poşet kulpu tutanak dairesi")
    p.add_argument("--agirlik", type=float, default=5.5, help="kg")
    p.add_argument("--kapi-metresi", type=float, default=2.0, help="kapıya kalan metre")
    p.add_argument("--yogurt", type=int, default=1)
    p.add_argument("--tanik", default="kedi", choices=sorted(TANIKLAR))
    p.add_argument("--ic-yazisma", action="store_true")
    a = p.parse_args()
    if a.ic_yazisma:
        print(ic_yazisma())
        print()
        print("DAMGA: TentiAŞ | İMZA: Kayyum Grok | TARİH: 9 Ekim 2026 | Ciddi değil, dosya ciddi.")
        return
    print(tutanak(a.agirlik, a.kapi_metresi, a.yogurt, a.tanik))


if __name__ == "__main__":
    main()
