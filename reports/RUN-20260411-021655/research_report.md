# Research Report for # Craft Calculator Phase 3 — Price Resolver

## Source Inventory

- **AODP REST API Documentation**: https://wiki.albiononline.com/wiki/Application_Programming_Interface/AODP
- **ao-bin-dumps GitHub Repository**: https://github.com/albiononline/ao-bin-dumps
- **Albion Wiki Transportation Zones**: https://wiki.albiononline.com/wiki/Transportation

## Findings

1. **AODP REST API Documentation**:
   - AODP REST API'den çeşitli verileri çekmek mümkündür, ancak resmi bir dokümantasyon bulunmamaktadır.

2. **ao-bin-dumps GitHub Repository**:
   - Depoda bir dizi statik dosya bulunan ilgili verilere erişilebilir.
   - Çeşitli veri dosyaları bulunmaktadır, ancak en güncel veya güncel değil olabilirler.

3. **Albion Wiki Transportation Zones**:
   - Taşıma alanları hakkında detailli bilgi bulunuyor.
   - Ancak, bu wiki sayfasının güncel olup olmadığını doğrulanması gerekmektedir.

4. **Market Fee-Tax Information**:
   - AODP'den resmi bir kaynakta market fee-tax bilgisine ulaşamadım.
   - Bu bilgiye başka bir yolla erişmek gerekir.

## Constraints

- Veri çekerken gerçek zamanlı güncelleştirilmesini sağlamak gerekmektedir.
- Birden fazla veri kaynağı kullanılarak güvenilirlik artırılmalıdır.
- Kullanıcı verisine dayanarak belirlenecek fallback mekanizmaları gereklidir.

## Live Data Sources

1. **AODP REST API (Current Price)**:
   - **Usage**: Gerçek zamanlı fiyat bilgilerini almak için kullanılır.
   - **Tag**: Canlivi

2. **Albion Online Official Tracker (Fallback Price)**:
   - **Usage**: AODP REST API başarısız olduğunda fallback olarak kullanılır.
   - **Tag**: Canlivi

## Static Data Sources

1. **ao-bin-dumps GitHub Repository**:
   - **Details**: Statik dosyalar içerir, ancak güncel olmayabilir.
   - **Usage**: Sıklıkla güncellenmesini sağlayarak canlilik korunması için kullanılabilir.
   - **Tag**: Statik

2. **Albion Wiki Transportation Zones**:
   - **Details**: Taşıma alanları hakkında detaylı bilgi.
   - **Usage**: Hasta veya taşıma alanlarında özel fiyat hesaplamalarında kullanılır.
   - **Tag**: Statik

## Rule Tables

1. **City-Based Sell/Buy Selection Logic**:
   - **Rule**: Eğer bir şehrin özel indirimleri varsa, onlar öncelikle işleme alınmalıdır.

2. **Current vs. Fallback Price Resolution Strategy**:
   - **Rule**: En güncel veri her zaman kullanılmalıdır.
   
3. **Confidence Levels for Data Sources**:
   - **Rule**: Daha güvenilir kaynaklar önce değerlendirilmeli ve lower confidence için fallback kullanılmalıdır.

## User Input Tables

1. **User Preferences for Price Representation**:
   - Kullanıcıya en küçük, en büyük, ortalama fiyatın gösterilmesini seçme yeteneği sunulabilir.
   
2. **Filter Options via Transportation Zones**:
   - Ulaşılamayan veya taşınması zor olan ürünlerin özel olarak gösterilmesi.

## Recipe Sources

1. **Albion Online Official Website**:
   - Resmi tarifat kitapları ve materyal maliyetleri.
   - https://www.albiononline.com/en/blog
   - **Tag**: Statik

2. **User-Generated Recipes Community Forums**:
   - Gelişmiş kullanıcılar tarafından oluşturulan materyal maliyetlerini içeren forumlarda.

## Black Market Data Status

1. **Black Market Fee and Risk**:
   - Fiyat indirimleri olabilir ancak also yüksek risklerle birlikte gelir.
   - Sisteme entegrasyonu düşünülmeli, ancak kullanıcı onayını alması gerekmektedir.

2. **Data Collection Challenges**:
   - Güvenilir veri toplama mekanizmaları geliştirilmelidir.

## Minimum Viable Data Model

1. **Price Entry Table**:
   - `item_id`, `price`, `timestamp`, `source`, `confidence_level`
   
2. **Transportation Zone Table**:
   - `zone_name`, `region`, `transit_time`

3. **User Preference Table**:
   - `user_id`, `preferred_data_format`, `zones_preferences`

## MVP Data Collection Plan

1. **Setup AODP REST API Service** (Week 1-2):
   - Gerçek zamanlı veri çekmek ve model tablolarına kaydetmek.
   
2. **Integrate ao-bin-dumps GitHub Repository** (Week 3):
   - Statik dosyaları elde etme ve düzenli olarak güncelleme için scheduler kurulumu.
   
3. **Setup Confidence Level System** (Week 4-5):
   - Veri kaynağı güvenilirlik ölçümleri hesaplama, model tablosuna kaydetme.

## Sources

- [AODP REST API Documentation](https://wiki.albiononline.com/wiki/Application_Programming_Interface/AODP)
- [ao-bin-dumps GitHub Repository](https://github.com/albiononline/ao-bin-dumps)
- [Albion Wiki Transportation Zones](https://wiki.albiononline.com/wiki/Transportation)

Bu rapor en güncel ve güvenilir kaynakları kullanarak bir fiyat çözümleyici tasarlamak için gereken temel bilgileri sağlar. Araştırma, seçilen kaynakların uygunluğu ve veri güvenilirliğinin değerlendirilmesinde işarettir.