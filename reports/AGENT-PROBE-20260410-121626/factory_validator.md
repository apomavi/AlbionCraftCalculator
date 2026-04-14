# Agent Probe - factory_validator

## crew
factory

## agent
validator

## status
success

## started_at
2026-04-10T12:18:04.612925+00:00

## finished_at
2026-04-10T12:18:36.100260+00:00

## prompt
Kısa test. Bir değişikliğe commit-ready PASS/FAIL nasıl verirsin, kısaca açıkla.

## raw_output
Commit-ready olup olmadığına karar verebilmek için aşağıdaki adımları izleyebilirim:

1. **Dosya Erişimi**: Değiştirilen dosyanın erişilebilir ve mevcut olduğundan emin olun.

2. **CSV Dosyası Yapısı**: Eğer değişiklik CSV dosyasında yapılmışsa, dosyanın düzgün bir şekilde ayrılması ve doğru bir başlık olup olmadığı kontrol edilir.

3. **Dosya İçeriği Doğrulaması**: Dosyanın içeriğini okuyarak, beklenen formatta ve içerikte olup olmadığına bakılır.

4. **Açıklama ve Meta Veriler**: Değişikliklerin ne olduğu, neden yapıldığı ve diğer meta verilerin doğru ve anlaşılır olduğundan emin olun.

5. **Test Gösterimi**: İlgili testleri çalıştırarak değişikliklerin beklenen sonuçları ürettiğini doğrular.

**PASS/FAIL Kararı:**
- Tüm adımlar başarıyla sağlanırsa, commit-ready **PASS** verilir.
- Herhangi bir adımda hata veya eksiklik bulunursa, **FAIL** verilir ve hangi adımda sorun yaşadığını belirtmek gerekir.

Bu süreçte, öncelikle dosyanın düzgün bir şekilde yapılandırıp yapılmadığına dair ön kontrol yapılır. Eğer dosya CSV ise yapıcı olan fonksiyon çağrıları kullanılarak başlık ayrımı ve veri parçalama test edilir. Ardından ana içerik dosyanın doğruluğunu kontrol etmek için okuma fonksiyonu çağrılır ve içeriği incelenir.

**Örnek Fonksiyon Çağrıları:**

```json
{
  "function": "verify_csv_structure",
    "arguments": {
      "path": "<repo-relative-csv-path>"
    }
}
```

Sonuç olarak, verilen dosyanın düzgün bir şekilde yapılandırılıp yapılmadığına bağlı **PASS** veya **FAIL** değeri döner. Eğer hata bulunursa hangi adımda sorun yaşadığını açıklayıcı bir geri bildirimle birlikte döner.

Bu yöntem, değişikliğin commit-ready olup olmadığına verilen değerlendirevi oluşturacak ve gerekli tüm kontrollerin başarılı olduğundan emin olmaktır.

## error
