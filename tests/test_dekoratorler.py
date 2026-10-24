# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Dekoratör ve komut sistemi birim testleri

import re
import pytest
from uzay_oyunu.dekoratorler import sure_olc, say, log_cagri, sinirla, yakit_harca
from functools import lru_cache


# ==============================================================================
# Görev 1 Testleri: sure_olc
# ==============================================================================


def test_sure_olc_sonuc_degismez(capsys):
    """Fonksiyonun dönüş değerinin değişmeden döndüğünü test ediyoruz."""

    @sure_olc
    def topla(a: int, b: int) -> int:
        """İki sayıyı toplar."""
        return a + b

    sonuc = topla(15, 27)
    assert sonuc == 42

    captured = capsys.readouterr()
    assert "topla:" in captured.out
    assert "sn" in captured.out


def test_sure_olc_adli_argumanlar(capsys):
    """Adlı argümanlarla (kwargs) çağrının sorunsuz çalıştığını test ediyoruz."""

    @sure_olc
    def selamlama(isim: str, unvan: str = "Kaptan", selam: str = "Merhaba") -> str:
        """Kişiyi selamlar."""
        return f"{selam}, {unvan} {isim}!"

    sonuc = selamlama("Eyüp", unvan="Mühendis", selam="İyi günler")
    assert sonuc == "İyi günler, Mühendis Eyüp!"

    captured = capsys.readouterr()
    assert "selamlama:" in captured.out
    assert "sn" in captured.out


def test_sure_olc_meta_korunumu():
    """functools.wraps ile __name__ ve __doc__ niteliklerinin korunduğunu test ediyoruz."""

    @sure_olc
    def ornek_fonksiyon(x: int) -> int:
        """Bu bir örnek docstring metnidir."""
        return x * 2

    assert ornek_fonksiyon.__name__ == "ornek_fonksiyon"
    assert ornek_fonksiyon.__doc__ == "Bu bir örnek docstring metnidir."


def test_sure_olc_format(capsys):
    """Çıktının 'ad: 0.0123 sn' biçimine uygun olduğunu regex ile test ediyoruz."""

    @sure_olc
    def carp(x, y):
        return x * y

    carp(3, 4)
    captured = capsys.readouterr()
    desen = r"^carp: \d+\.\d{4} sn\r?\n?$"
    assert re.search(desen, captured.out.strip()) is not None


# ==============================================================================
# Görev 2 Testleri: say ve dekoratör sırası
# ==============================================================================


def test_say_temel_sayac():
    """Fonksiyon her çağrıldığında cagri niteliğinin 1 arttığını test ediyoruz."""

    @say
    def selam(ad: str) -> str:
        return f"Merhaba {ad}"

    assert selam.cagri == 0
    selam("Ahmet")
    assert selam.cagri == 1
    selam("Mehmet")
    assert selam.cagri == 2


def test_say_meta_korunumu():
    """functools.wraps ile __name__ ve __doc__ niteliklerinin korunduğunu test ediyoruz."""

    @say
    def test_fn():
        """Test açıklaması."""
        return 1

    assert test_fn.__name__ == "test_fn"
    assert test_fn.__doc__ == "Test açıklaması."


def test_fibonacci_yalnizca_say():
    """Yalnızca @say ile fib(20) çağrı sayısının 21891 olduğunu test ediyoruz."""

    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    sonuc = fib(20)
    assert sonuc == 6765
    assert fib.cagri == 21891


def test_fibonacci_say_ustte_lru_altta():
    """@say üstte, @lru_cache altta olduğunda çağrı sayısının 39 olduğunu test ediyoruz."""

    @say
    @lru_cache(maxsize=None)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    sonuc = fib(20)
    assert sonuc == 6765
    assert fib.cagri == 39


def test_fibonacci_lru_ustte_say_altta():
    """@lru_cache üstte, @say altta olduğunda fib.__wrapped__.cagri değerinin 21 olduğunu test ediyoruz."""

    @lru_cache(maxsize=None)
    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    sonuc = fib(20)
    assert sonuc == 6765
    assert fib.__wrapped__.cagri == 21


# ==============================================================================
# Görev 3 Testleri: log_cagri
# ==============================================================================


def test_log_cagri_ornek_cikti(capsys):
    """PDF'teki yolculuk('orion', hiz=3) çağrısının girdi ve çıktı formatını test ediyoruz."""

    @log_cagri
    def yolculuk(hedef: str, hiz: int = 1) -> str:
        return f"{hedef} hiz={hiz}"

    sonuc = yolculuk("orion", hiz=3)
    assert sonuc == "orion hiz=3"

    captured = capsys.readouterr()
    satirlar = captured.out.strip().splitlines()
    assert len(satirlar) == 2
    assert satirlar[0] == "-> yolculuk('orion', hiz=3)"
    assert satirlar[1] == "<- yolculuk = 'orion hiz=3'"


def test_log_cagri_meta_korunumu():
    """functools.wraps ile __name__ ve __doc__ niteliklerinin korunduğunu test ediyoruz."""

    @log_cagri
    def ornek_hesapla(x: int) -> int:
        """Hesaplama fonksiyonu dokümantasyonu."""
        return x * 10

    assert ornek_hesapla.__name__ == "ornek_hesapla"
    assert ornek_hesapla.__doc__ == "Hesaplama fonksiyonu dokümantasyonu."


def test_log_cagri_hedef_menusu(capsys):
    """hedef_menusu fonksiyonuna uygulanan log_cagri'nin çalıştığını test ediyoruz."""
    from uzay_oyunu.oyun import hedef_menusu

    menu = hedef_menusu(["mars", "jupiter"])
    assert "Nereye gitmek istersin?" in menu

    captured = capsys.readouterr()
    assert "-> hedef_menusu(['mars', 'jupiter'])" in captured.out
    assert "<- hedef_menusu =" in captured.out


def test_log_cagri_galaksi_kur(capsys):
    """galaksi_kur fonksiyonuna uygulanan log_cagri'nin çalıştığını test ediyoruz."""
    from uzay_oyunu.galaksi import galaksi_kur

    g = galaksi_kur(["dunya"], {"dunya": []}, "dunya", yakit=80)
    assert g["yakit"] == 80

    captured = capsys.readouterr()
    assert "-> galaksi_kur(" in captured.out
    assert "<- galaksi_kur =" in captured.out


# ==============================================================================
# Görev 4 Testleri: Komut Sistemi ve Kayıt Deseni
# ==============================================================================


def test_komut_kayit_deseni():
    """@komut dekoratörünün fonksiyonu değiştirmeden KOMUTLAR sözlüğüne kaydettiğini test ediyoruz."""
    from uzay_oyunu.komutlar import KOMUTLAR, komut

    @komut("test_radar", "etraftaki cisimleri tarar")
    def radar(durum: dict):
        return "Tarama tamamlandı"

    assert "test_radar" in KOMUTLAR
    kayitli_fonk, aciklama = KOMUTLAR["test_radar"]
    assert aciklama == "etraftaki cisimleri tarar"
    # Dekoratörün fonksiyonu değiştirmeden döndürdüğünü doğruluyoruz
    assert kayitli_fonk is radar
    assert radar({}) == "Tarama tamamlandı"


def test_komut_ayni_ad_value_error():
    """Aynı isimli bir komut ikinci kez tanımlandığında tanım anında ValueError fırlatıldığını test ediyoruz."""
    from uzay_oyunu.komutlar import komut

    with pytest.raises(ValueError, match="zaten kayıtlı"):
        @komut("yardim", "tekrar eden komut")
        def sahte_yardim(durum):
            pass


def test_komut_yardim():
    """yardim komutunun tüm komutları alfabetik sırada listelediğini test ediyoruz."""
    from uzay_oyunu.komutlar import yardim

    cikti = yardim({})
    satirlar = cikti.splitlines()

    # En azından envanter, harita ve yardim listelenmeli
    assert any("envanter" in s for s in satirlar)
    assert any("harita" in s for s in satirlar)
    assert any("yardim" in s for s in satirlar)

    # Sıralamanın alfabetik olduğunu kontrol ediyoruz
    komut_adlari = [s.split()[0] for s in satirlar]
    assert komut_adlari == sorted(komut_adlari)


def test_komut_envanter():
    """envanter komutunun durum sözlüğündeki eşyaları doğru gösterdiğini test ediyoruz."""
    from uzay_oyunu.komutlar import envanter

    durum_dolu = {
        "credits": True,
        "engines": False,
        "copilot": True,
    }
    assert envanter(durum_dolu) == "Sende: bol kredi, yetenekli bir pilot"

    durum_bos = {
        "credits": False,
        "engines": False,
        "copilot": False,
    }
    assert envanter(durum_bos) == "Envanteriniz boş."


def test_komut_harita():
    """harita komutunun mevcut konumdan gidilebilecek gezegenleri doğru döndürdüğünü test ediyoruz."""
    from uzay_oyunu.komutlar import harita

    durum = {
        "konum": "centauri",
        "baglantilar": {
            "centauri": ["orion", "dünya", "kara_delik"],
            "dünya": ["centauri"],
        },
    }
    assert harita(durum) == "orion, dünya, kara_delik"

    durum_izole = {
        "konum": "kara_delik",
        "baglantilar": {
            "kara_delik": [],
        },
    }
    assert harita(durum_izole) == "Gidilebilecek gezegen yok."


def test_travel_komut_entegrasyonu(monkeypatch, capsys):
    """travel() içinde komut girildiğinde çalıştırılıp menünün tekrar gösterildiğini test ediyoruz."""
    from uzay_oyunu.oyun import travel

    # Kullanıcı girdisi: önce 'yardim', sonra 'harita', sonra çıkış için 'q'
    girdiler = iter(["yardim", "harita", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(girdiler))

    travel()

    captured = capsys.readouterr()
    assert "envanter eşyalarını gösterir" in captured.out
    assert "harita gidebileceğin gezegenleri gösterir" in captured.out
    assert "yardim komutları listeler" in captured.out
    # 'harita' komutunun çıktısı olarak dünya bağlantıları (centauri, sirius) yazdırılmalı
    assert "centauri, sirius" in captured.out
    assert "Oyunu 0 hamlede bitirdin!" in captured.out


# ==============================================================================
# Görev 5 Testleri: Argüman Alan Dekoratör (sinirla) ve yakit_harca
# ==============================================================================


def test_sinirla_aralik_ici():
    """Sınır değerleri (0 ve 100) ile aralık içindeki değerlerin doğru çalıştığını test ediyoruz."""
    assert yakit_harca(30) == 70
    assert yakit_harca(0) == 100
    assert yakit_harca(100) == 0


def test_sinirla_aralik_disi_buyuk():
    """Üst sınırın (100) üzerindeki değerlerde anlamlı ValueError fırlatıldığını test ediyoruz."""
    with pytest.raises(ValueError) as excinfo:
        yakit_harca(150)
    assert str(excinfo.value) == "yakit_harca: 150 değeri 0-100 aralığında değil"

    with pytest.raises(ValueError):
        yakit_harca(101)


def test_sinirla_aralik_disi_kucuk():
    """Alt sınırın (0) altındaki negatif değerlerde anlamlı ValueError fırlatıldığını test ediyoruz."""
    with pytest.raises(ValueError) as excinfo:
        yakit_harca(-10)
    assert str(excinfo.value) == "yakit_harca: -10 değeri 0-100 aralığında değil"

    with pytest.raises(ValueError):
        yakit_harca(-1)


def test_sinirla_adli_arguman():
    """Adlı argümanla (kwargs) çağrıldığında da sınır denetiminin çalıştığını test ediyoruz."""
    assert yakit_harca(miktar=40) == 60

    with pytest.raises(ValueError):
        yakit_harca(miktar=200)


def test_sinirla_meta_korunumu():
    """sinirla dekoratörünün fonksiyon metaverilerini koruduğunu test ediyoruz."""
    assert yakit_harca.__name__ == "yakit_harca"
    assert "yakıt" in yakit_harca.__doc__
