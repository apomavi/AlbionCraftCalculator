İş adı:
PostgreSQL ana yoluna geçiş ve ortak log writer doğrulaması

Amaç:
Bu request, önceki PostgreSQL primary + ortak log writer çalışmasının CrewAI ajanları ile doğrulanması içindir.

Kontrol et:
1. İstenen iş gerçekten yapılmış mı
2. Konu dışına çıkılmış mı
3. Resmi AODP path dışında endpoint var mı
4. Append-only kayıt mantığı bozulmuş mu
5. PostgreSQL ana yoluna ters bir şey var mı
6. Test yeterli mi
7. Riskli ama gizlenmiş bir nokta var mı

Çıktı formatı:
- Correct
- Wrong
- Risky
- Required Fixes

Kurallar:
- sadece denetim yap
- kod yazma
- dosya değiştirme
- mevcut repo durumunu değerlendir