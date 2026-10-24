# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Komut sistemi ve kayıt deseni (registry pattern)

import functools

# Kayıtlı komutların tutulduğu sözlük: {komut_adi: (fonksiyon, aciklama)}
KOMUTLAR = {}


def komut(ad: str, aciklama: str = ""):
    """Fonksiyonu (fonksiyon, aciklama) şeklinde KOMUTLAR sözlüğüne kaydeder."""
    # Aynı komut iki kez tanımlanırsa tanım anında hata veriyoruz
    if ad in KOMUTLAR:
        raise ValueError(f"'{ad}' adlı komut zaten kayıtlı!")

    def dekorator(fonksiyon):
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' adlı komut zaten kayıtlı!")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        # Fonksiyonu değiştirmeden döndürüyoruz
        return fonksiyon

    return dekorator


@komut("yardim", "komutları listeler")
def yardim(durum: dict) -> str:
    """Kayıtlı komutları ve açıklamalarını alfabetik sırayla listeler."""
    satirlar = []
    # Komutları alfabetik sırayla yazdırıyoruz
    for ad in sorted(KOMUTLAR.keys()):
        _, aciklama = KOMUTLAR[ad]
        satirlar.append(f"{ad} {aciklama}".rstrip())
    return "\n".join(satirlar)


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: dict) -> str:
    """Oyuncunun envanterindeki eşyaları gösterir."""
    credits = durum.get("credits", False)
    engines = durum.get("engines", False)
    copilot = durum.get("copilot", False)

    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiper motor")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return "Envanteriniz boş."
    return "Sende: " + ", ".join(esyalar)


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: dict) -> str:
    """Mevcut konumdan gidilebilecek gezegenleri virgülle ayrılmış olarak döndürür."""
    konum = durum.get("konum", "")
    baglantilar = durum.get("baglantilar", {})
    gidebilecekler = baglantilar.get(konum, [])
    if not gidebilecekler:
        return "Gidilebilecek gezegen yok."
    return ", ".join(gidebilecekler)
