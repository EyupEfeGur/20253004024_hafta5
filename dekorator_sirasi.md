# Dekoratör Sırası ve Fibonacci Çağrı Sayısı Analizi

**Ad :** Eyüp Efe  
**Soyad :** GÜR  
**Numara :** 20253004024  
**Bölüm :** Bilişim Sistemleri ve Teknolojileri  
**Ders :** İleri Python Programlama  
**Öğretim Üyesi :** Dr. Öğr. Üyesi Murat Emeç  
**GitHub Deposu :** https://github.com/EyupEfeGur/20253004024_hafta5  

---

### 1. Ölçülen Sonuçlar (fib(20))

Özyinelemeli (recursive) Fibonacci fonksiyonu üzerinde `@say` (çağrı sayacı) ve `functools.lru_cache` dekoratörleri 3 farklı sırada denenmiş ve `fib(20)` için çağrı sayıları ölçülmüştür:

1. **Yalnızca @say :** 21891
2. **@say üstte, @lru_cache altta :** 39
3. **@lru_cache üstte, @say altta :** 21 (sayaca `fib.__wrapped__.cagri` ile ulaşıldı)

---

### 2. Sonuçların Nedenleri ve Detaylı Açıklaması

#### Durum 1: Yalnızca @say (21891 Çağrı)
- **Neden bu sonuç çıktı?**  
  Herhangi bir önbellekleme (memoization) yapmadığımız için saf özyineleme çalışır. `fib(20)` hesaplanırken aynı alt problemler tekrar tekrar en baştan hesaplanır. Örneğin `fib(20)` için `fib(19)` ve `fib(18)` çağrılır; `fib(19)` da kendi içinde `fib(18)`'i tekrar hesaplar. Bu dallanma tabana kadar katlanarak büyür.
- **Matematiksel karşılığı:**  
  Taban durumları $fib(0)=0$ ve $fib(1)=1$ olan özyinelemeli Fibonacci fonksiyonunda toplam çağrı sayısı formülü $2 \cdot F(n+1) - 1$'dir.  
  $n=20$ için 21. Fibonacci sayısı $F(21) = 10946$ olduğundan:  
  $$2 \times 10946 - 1 = 21891$$  
  Bu yüzden `@say` tam olarak 21891 defa çağrılmıştır.

---

#### Durum 2: @say üstte, @lru_cache altta (39 Çağrı)
- **Neden bu sonuç çıktı?**  
  Python'da birden fazla dekoratör kullanıldığında fonksiyon çağrıları yukarıdan aşağıya (dıştan içe) doğru ilerler. `@say` en üstte olduğu için:  
  `fib = say(lru_cache(orijinal_fib))`  
  şeklinde sarılır.  
  Fonksiyonun içindeki `fib(n-1) + fib(n-2)` özyinelemeli çağrıları global isim alanındaki `fib` değişkenine bakar. Bu değişken de en dıştaki sarmalayıcı olan `@say` fonksiyonunu işaret eder.  
  Bu yüzden her özyinelemeli çağrıda istek **önce `@say` fonksiyonuna gelir**, sayaç 1 artar ve ardından çağrı alttaki `@lru_cache` katmanına aktarılır.  
  `@lru_cache` aranan değeri hafızasında bulsa bile (cache hit), `@say` en dışta kaldığı için çağrıyı çoktan saymış olur.
- **39 Sayısının Hesabı:**  
  $n=20$ için ilk ana çağrı yapılır (1 çağrı). Ardından $n=20$'den $n=2$'ye kadar olan 19 adımın her birinde fonksiyon sol ve sağ olmak üzere iki dala ayrılır ($n-1$ ve $n-2$). Sol dal derinlemesine inerken değerleri hesaplayıp önbelleğe yazar; sağ dal çağrıldığında `@say` yine tetiklenir ancak altındaki `@lru_cache` değeri önbellekten anında döner.  
  Böylece toplam çağrı sayısı:  
  $$1 + (19 \times 2) = 39$$  
  olur. Yani `@say`, hem önbellek ıskalarını (miss) hem de önbellek isabetlerini (hit) saymıştır.

---

#### Durum 3: @lru_cache üstte, @say altta (21 Çağrı)
- **Neden bu sonuç çıktı?**  
  Bu sefer dekoratör sırası tersinedir:  
  `fib = lru_cache(say(orijinal_fib))`  
  En dıştaki katman artık `@lru_cache` olmuştur. Özyinelemeli çağrılar yapıldığında istek doğrudan `@lru_cache` fonksiyonuna gider.  
  Eğer aranan sayı daha önce hesaplanmışsa (cache hit), `@lru_cache` alt katmandaki `@say` fonksiyonuna hiç uğramadan sonucu doğrudan döndürür.  
  `@say` fonksiyonu yalnızca önbellekte değer bulunamadığında (cache miss), yani yeni bir sayı gerçekten hesaplanması gerektiğinde çalıştırılır.
- **21 Sayısının Hesabı:**  
  $n=20$ için hesaplanması gereken benzersiz sayılar $0, 1, 2, \dots, 20$ olmak üzere toplam **21 tanedir**. Her biri sadece bir kez hesaplandığı için aradaki `@say` dekoratörü tam 21 defa çalışmıştır.

---

### 3. fib.__wrapped__.cagri Neden Kullanıldı?

Üçüncü durumda doğrudan `fib.cagri` yazarak sayaca ulaşamayız. Çünkü en dıştaki `fib` değişkeni `@lru_cache`'in döndürdüğü nesnedir ve bu nesnenin üzerinde `.cagri` niteliği tanımlı değildir.  
`functools.wraps`, sarmalanan asıl fonksiyona erişebilmemiz için `__wrapped__` niteliğini sağlar. `@lru_cache`'in sardığı iç fonksiyon bizim `@say` fonksiyonumuz olduğundan, `fib.__wrapped__.cagri` ifadesiyle içteki sayaca doğrudan ulaşabiliyoruz.
