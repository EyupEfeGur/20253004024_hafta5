# Ad : Eyüp Efe
# Soyad : GÜR
# Numara : 20253004024
# Bölüm : Bilişim Sistemleri ve Teknolojileri

# Dekoratör ve komut sistemi birim testleri

import re
import pytest
from uzay_oyunu.dekoratorler import sure_olc


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
