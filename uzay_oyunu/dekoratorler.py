# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Dekoratör fonksiyonları ve süre/çağrı ölçümleri

import functools
import time


def sure_olc(fonksiyon):
    """Fonksiyonun çalışma süresini time.perf_counter() ile ölçüp ekrana yazdırır."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        # Başlangıç zamanını hassas sayaçla alıyoruz
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        gecen_sure = bitis - baslangic
        # İstenen "ad: 0.0123 sn" formatında yazdırıyoruz
        print(f"{fonksiyon.__name__}: {gecen_sure:.4f} sn")
        return sonuc

    return sarmalayici


def say(fonksiyon):
    """Fonksiyonun çağrı sayısını 'cagri' niteliğinde sayar."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        # Fonksiyon her çağrıldığında sayacı 1 artırıyoruz
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    # Başlangıçta sayacı sıfırlıyoruz
    sarmalayici.cagri = 0
    return sarmalayici


def log_cagri(fonksiyon):
    """Her çağrıdan önce fonksiyonu ve parametrelerini, sonra dönüş değerini yazdırır."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        # Konumsal ve varsa isimli argümanları formatlıyoruz
        arg_parcalari = [repr(a) for a in args]
        arg_parcalari.extend([f"{k}={v!r}" for k, v in kwargs.items()])
        arg_metni = ", ".join(arg_parcalari)
        print(f"-> {fonksiyon.__name__}({arg_metni})")

        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {sonuc!r}")
        return sonuc

    return sarmalayici


def sinirla(alt: int | float, ust: int | float):
    """Fonksiyonun ilk argümanının [alt, ust] aralığında olmasını kontrol eder."""

    def dekorator(fonksiyon):
        @functools.wraps(fonksiyon)
        def sarmalayici(*args, **kwargs):
            deger = None
            if args:
                deger = args[0]
            elif kwargs:
                deger = next(iter(kwargs.values()))

            # Değer aralık dışındaysa ValueError fırlatıyoruz
            if deger is not None:
                if deger < alt or deger > ust:
                    raise ValueError(
                        f"{fonksiyon.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                    )

            return fonksiyon(*args, **kwargs)

        return sarmalayici

    return dekorator


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    """Belirtilen miktar kadar yakıt harcar ve kalan yakıtı (100 - miktar) döndürür."""
    return 100 - miktar


def hafiza(maxsize=None):
    """functools.lru_cache kullanmadan, closure içindeki sözlükle çalışan önbellek dekoratörü."""

    def dekorator(fonksiyon):
        # Closure içinde önbellek sözlüğünü tutuyoruz
        onbellek = {}

        @functools.wraps(fonksiyon)
        def sarmalayici(*args, **kwargs):
            anahtar = (args, tuple(sorted(kwargs.items())))

            if anahtar in onbellek:
                # LRU mantığı: erişilen elemanı sözlükten çıkarıp en sona ekliyoruz
                sonuc = onbellek.pop(anahtar)
                onbellek[anahtar] = sonuc
                return sonuc

            sonuc = fonksiyon(*args, **kwargs)

            # Limit varsa ve dolduysa en eski kaydı siliyoruz
            if maxsize is not None and maxsize > 0:
                if len(onbellek) >= maxsize:
                    en_eski = next(iter(onbellek))
                    del onbellek[en_eski]
                onbellek[anahtar] = sonuc
            elif maxsize is None:
                onbellek[anahtar] = sonuc

            return sonuc

        sarmalayici.onbellek = onbellek
        return sarmalayici

    return dekorator


if __name__ == "__main__":
    # Hafta 4'teki önbelleksiz rota sayacına uygulayarak adim=20 için süreyi ölçüyoruz:
    try:
        from uzay_oyunu.galaksi import veri_yukle
    except ModuleNotFoundError:
        from galaksi import veri_yukle

    galaksi = veri_yukle()
    baglantilar = galaksi["baglantilar"]

    def rota_sayaci_onbelleksiz(baglanti_haritasi: dict):
        """Önbelleksiz özyinelemeli rota sayacı."""

        def rota_sayisi(gezegen: str, adim: int) -> int:
            if adim == 0:
                return 1
            komsular = baglanti_haritasi.get(gezegen, [])
            if not komsular:
                return 0
            return sum(rota_sayisi(k, adim - 1) for k in komsular)

        return rota_sayisi

    onbelleksiz_sayac = rota_sayaci_onbelleksiz(baglantilar)

    @sure_olc
    def rota_hesapla(gezegen: str, adim: int) -> int:
        """Belirtilen gezegen ve adım için rota sayısını hesaplar."""
        return onbelleksiz_sayac(gezegen, adim)

    print("--- Görev 1: Önbelleksiz Rota Sayacı Ölçümü (adim=20) ---")
    sonuc = rota_hesapla("dünya", 20)
    print(f"Hesaplanan rota sayısı: {sonuc}")
