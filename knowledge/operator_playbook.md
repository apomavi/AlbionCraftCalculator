# Operator Playbook

## Günlük Çalışma Akışı

1. Yeni request oluştur
   - `requests/REQ-xxxx.md`
   - Tek request = tek dosya

2. Plan al
   - Repo mevcut durumu okunur
   - Kısa plan çıkarılır

3. Onay ver
   - Uygulama öncesi kapsam onaylanır

4. Uygulat
   - Cline gerekli dosya değişikliklerini yapar
   - Gerekirse CrewAI yardımcı ajanları kullanılır

5. Reviewer kontrolü
   - Dış denetleyici AI veya insan reviewer çıktıyı kontrol eder
   - PASS/FAIL kararı verir

6. Commit
   - Reviewer onayından sonra commit hazırlanır
   - Commit mesajı anlamlı ve kapsamla uyumlu olur

## Operasyon Kuralları

- Tüm yeni işler `requests/REQ-xxxx.md` ile başlar
- Kalıcı çıktılar `reports/RUN-xxxx/` altında tutulur
- Commit öncesi dış reviewer kontrolü gerekir
- Aynı branch üzerinde tek implementer çalışır
