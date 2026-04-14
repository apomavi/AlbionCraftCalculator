## Scope
`src/albion_factory/craftcalc/models.py` dosyasını güncelleme ve yeni modellerin (`PlayerProfile`, `LocationContext`) eklenmesi.

## Required Agents
- **researcher**: Gerekli değişikliklerin detaylı analizi ve uygun uygulama stratejisi belirleme.
- **data_collector**: Modelde kullanılacak verilerin toplanması ve doğrulanması.
- **coder**: Kodlama işlemini gerçekleştiren ve model güncellemelerini yapacak.
- **tester**: Yeni modellerin ve güncellenen modellerin test edilmesi ve hataların düzeltimi.
- **validator**: Son kodun kalitesini kontrol etme ve gereksinimleri karşılayıp karşılamadığı doğrulama.

## Constraints
- Mevcut alanların bozulmaması.
- Gerekliyse `pydantic.Field` kullanılarak varsayılan değerler belirlenmesi.

## Success Criteria
1. `PlayerProfile` ve `LocationContext` modellerinin başarıyla oluşturulması.
2. `CraftPricePoint` ve `CraftCalculationRequest` modellerinin güncellenmesi ve yeni alanların doğru bir şekilde eklenmesi.
3. Tüm kodun test edilip, hataların düzeltildiği ve gereksinimleri karşıladığı doğrulanması.

## Next Task
1. **researcher**: Gerekli değişikliklerin detaylı analizi yapın ve uygun uygulama stratejisi belirleyin.
2. **data_collector**: Modelde kullanılacak verileri toplayın ve doğrulayın.
3. **coder**: `PlayerProfile` ve `LocationContext` modellerini oluşturun ve mevcut modelleri güncelleyin (`CraftPricePoint`, `CraftCalculationRequest`).
4. **tester**: Yeni ve güncellenen modelleri test edin ve hataları düzeltin.
5. **validator**: Son kodu kontrol edin ve gereksinimleri karşılayıp karşılamadığı doğrulayın.

Bu adımlar tamamlandığında, `src/albion_factory/craftcalc/models.py` dosyası başarıyla güncellenecektir ve Phase 1 ve Phase 1.5 özelliklerini destekleyecek olacaktır.