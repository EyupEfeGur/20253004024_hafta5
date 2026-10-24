# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Saf fonksiyonlar ve uzay seyahati

try:
    from uzay_oyunu.dekoratorler import log_cagri
except ModuleNotFoundError:
    from dekoratorler import log_cagri


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Eşyaların durumuna göre envanter metnini döndürür."""
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiper motor")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return "Sende: " + ", ".join(esyalar)


@log_cagri
def hedef_menusu(hedefler: list) -> str:
    """Gidilebilecek hedefleri numaralandırarak menü olarak döndürür."""
    satirlar = ["Nereye gitmek istersin?"]
    for i, hedef in enumerate(hedefler, 1):
        satirlar.append(f"[{i}] {hedef}")
    return "\n".join(satirlar)


def travel():
    """Uzay oyunu seyahat fonksiyonu."""
    try:
        from uzay_oyunu.araclar import hamle_sayaci
        from uzay_oyunu.galaksi import veri_yukle
        from uzay_oyunu.akis import yakit_gostergesi
        from uzay_oyunu.komutlar import KOMUTLAR
    except ModuleNotFoundError:
        from araclar import hamle_sayaci
        from galaksi import veri_yukle
        from akis import yakit_gostergesi
        from komutlar import KOMUTLAR

    galaksi = veri_yukle()
    if not galaksi:
        return

    sayac = hamle_sayaci()
    toplam_hamle = 0

    envanter = envanter_metni(True, False, True)
    if envanter:
        print(envanter)

    planet = galaksi.get("konum", "dünya")
    yakit = galaksi.get("yakit", 100)
    # Her yolculuk için gösterge üreteci oluşturuyoruz
    gosterge = yakit_gostergesi(yakit, 5)

    durum = {
        "konum": planet,
        "baglantilar": galaksi.get("baglantilar", {}),
        "credits": True,
        "engines": False,
        "copilot": True,
    }

    while True:
        destinations = galaksi["baglantilar"].get(planet, [])

        if not destinations:
            print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
            break

        print(f"\nŞu anki konum: {planet}")
        print(hedef_menusu(destinations))

        secim = input("Seçiminiz (Çıkış için q): ")
        if secim.lower() == "q":
            print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
            break

        # Komut sistemi: Eğer oyuncunun girdisi bir komut adıysa çalıştır ve menüyü tekrar göster
        girdi = secim.strip()
        if girdi in KOMUTLAR:
            komut_fonksiyonu, _ = KOMUTLAR[girdi]
            sonuc = komut_fonksiyonu(durum)
            if sonuc:
                print(sonuc)
            continue

        try:
            index = int(secim) - 1
            if 0 <= index < len(destinations):
                planet = destinations[index]
                durum["konum"] = planet
                toplam_hamle = sayac()
                try:
                    yakit = next(gosterge)
                except StopIteration:
                    print("Yakıtın bitti, uzayda sürükleniyorsun…")
                    break
            else:
                print("Geçersiz seçim!")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")


if __name__ == "__main__":
    travel()
