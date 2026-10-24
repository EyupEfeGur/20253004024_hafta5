# Python İle Programlama - Hafta 5 Lab Ödevi

**Ad :** Eyüp Efe  
**Soyad :** GÜR  
**Numara :** 20253004024  
**Bölüm :** Bilişim Sistemleri ve Teknolojileri  
**Ders :** İleri Python Programlama  
**Öğretim Üyesi :** Dr. Öğr. Üyesi Murat Emeç  
**GitHub Deposu :** https://github.com/EyupEfeGur/20253004024_hafta5  

---

### Açıklama
Bu laboratuvar ödevinde uzay oyunu projesine dekoratörler (decorators) ve dekoratörlerle çalışan bir komut sistemi eklenmiştir. Fonksiyonların çalışma süresini ölçen `sure_olc`, çağrı sayısını sayan `say`, argümanları ve dönüş değerini loglayan `log_cagri`, argüman sınırlarını kontrol eden `@sinirla(alt, ust)` ve closure tabanlı çalışan LRU önbellek dekoratörü `hafiza` yazılmıştır. Ayrıca `komutlar.py` modülü içinde kayıt deseni (registry pattern) ile `yardim`, `envanter` ve `harita` komutları tanımlanıp `travel()` seyahat döngüsüne entegre edilmiştir.

---

### Görev 1: Önbelleksiz Rota Sayacı Süre Ölçümü (adim=20)

Hafta 4'teki önbelleksiz rota sayacına `@sure_olc` dekoratörü uygulanarak Dünya gezegeninden 20 adım yolculuk yapan rota sayısı ve süresi ölçülmüştür:

- **Hesaplanan Rota Sayısı:** 22.456.663
- **Çalışma Süresi:** 8.3312 sn
- **Konsol Çıktısı:** `rota_hesapla: 8.3312 sn`

---

### Görev 2: Fibonacci Çağrı Sayacı ve Dekoratör Sırası Özet

Özyinelemeli `fib(20)` için yapılan ölçümler:
- **Yalnızca @say :** 21891 çağrı
- **@say üstte, @lru_cache altta :** 39 çağrı
- **@lru_cache üstte, @say altta :** 21 çağrı (`fib.__wrapped__.cagri` ile)

> Sonuçların nedenleri, çağrı sırası mantığı ve `__wrapped__` niteliğinin açıklaması `dekorator_sirasi.md` dosyasında detaylandırılmıştır.

---

### Testler

Tüm testler `uv run pytest` komutu ile çalıştırılmaktadır. Hafta 4'ten gelen 30 test ve bu hafta eklenen 27 test olmak üzere toplam 57 birim test başarıyla geçmektedir.
