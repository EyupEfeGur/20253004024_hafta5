# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Galaksiyi veri dosyasindan kurma

import json
import os

try:
    from uzay_oyunu.dekoratorler import log_cagri
except ModuleNotFoundError:
    from dekoratorler import log_cagri


@log_cagri
def galaksi_kur(gezegenler: list, baglantilar: dict, baslangic: str, **kwargs) -> dict:
    """Galaksi haritasını ve başlangıç durumunu kurar."""
    # Başlangıç gezegeni listede yoksa hata fırlatıyoruz
    if baslangic not in gezegenler:
        raise ValueError(
            f"Başlangıç gezegeni '{baslangic}' gezegenler listesinde bulunamadı!"
        )

    # Yakıt verilmediyse varsayılan olarak 50 alıyoruz
    yakit = kwargs.get("yakit", 50)

    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": yakit,
    }


def veri_yukle(dosya_adi: str = "galaksi.json") -> dict:
    """JSON veri dosyasını okuyup galaksiyi kurar."""
    klasor = os.path.dirname(os.path.abspath(__file__))
    tam_yol = os.path.join(klasor, dosya_adi)

    with open(tam_yol, "r", encoding="utf-8") as dosya:
        veri = json.load(dosya)

    return galaksi_kur(**veri)
