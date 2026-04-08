# Albion Online Ekonomi Veri Araştırması Raporu

Bu rapor, Albion Online'daki craft, refine, market flip, taşıma, black market ve genel ekonomi odaklı veri araştırmasının sonuçlarını sunmaktadır. Amaç, AODP dahil olmak üzere tüm güçlü veri kaynaklarını bulmak ve sınıflandırmaktır.

---

## 1. Source Inventory

| Kaynak Adı                      | Tür      | Ne İşe Yarar                                                                                                                                                                                                                                                         | Link                                           |
| :------------------------------ | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| **Albion Online Data Project (AODP) API** | Resmi API | Canlı pazar fiyatları (alış/satış emirleri), altın fiyatları ve eşya bilgileri sağlar. Oyun sunucularına göre (Americas, Asia, Europe) ayrı endpointler sunar. | [https://www.albion-online-data.com/api/](https://www.albion-online-data.com/api/) |
| **AODP Developer Sayfası**      | Resmi Sayfa | API erişim politikaları, kullanım limitleri ve geliştirici topluluğu hakkında bilgi verir.                                                                                                                                                                    | [https://www.albion-online-data.com/](https://www.albion-online-data.com/) |
| **`ao-bin-dumps` GitHub Reposu**  | GitHub Deposu | Oyun dosyalarından çekilmiş statik veri dökümleri. Eşya tanımları, reçeteler, lokasyonlar gibi temel oyun verilerini içerir.                                                                                                                                  | [https://github.com/broderickhyman/ao-bin-dumps](https://github.com/broderickhyman/ao-bin-dumps) |
|   - `item_definitions.json`     | Dosya    | Eşyaların temel tanımlayıcıları (ID, isim, tip, kategori vb.).                                                                                                                                                                                               | -                                              |
|   - `recipes.json`              | Dosya    | Crafting ve refining reçeteleri (gerekli materyaller, çıktılar, üstatlık seviyeleri).                                                                                                                                                                     | -                                              |
|   - `locations.json`            | Dosya    | Şehirler, bölgeler ve onlara özel üretim/refining bonusları gibi lokasyon bazlı bilgiler.                                                                                                                                                                  | -                                              |
| **Albion Online Wiki**          | Resmi Wiki | Oyun mekanikleri, şehir bonusları, odak sistemi detayları, premium üyelik avantajları, pazar vergileri, eşya ağırlıkları ve Black Market'in işleyişi hakkında güvenilir bilgiler.                                                                          | [https://wiki.albiononline.com/wiki/Albion_Online_Wiki](https://wiki.albiononline.com/wiki/Albion_Online_Wiki) |

---

## 2. Live Data Sources

Canlı olarak çekilmesi gereken, sık değişen veriler:

*   **Pazar Fiyatları (Alış/Satış):**
    *   **Kaynak:** Albion Online Data Project (AODP) API
    *   **Ne İşe Yarar:** Belirli eşyaların, belirli şehirlerdeki anlık alış ve satış emir fiyatları. Market flipping ve üretim kârlılık hesaplamaları için kritik.
    *   **Veri Tipi:** Canlı
*   **Gold Fiyatı:**
    *   **Kaynak:** Albion Online Data Project (AODP) API
    *   **Ne İşe Yarar:** Oyun içi altın kurunun anlık değeri.
    *   **Veri Tipi:** Canlı

---

## 3. Static Data Sources

Genellikle sabit kalan veya nadiren güncellenen veriler:

*   **Eşya Tanımları:**
    *   **Kaynak:** `ao-bin-dumps` GitHub deposundaki `item_definitions.json`
    *   **Ne İşe Yarar:** Tüm eşyaların benzersiz ID'leri, adları, tipleri, kategorileri, tier'ları, enfeksiyon seviyeleri ve temel ağırlık bilgileri.
    *   **Veri Tipi:** Statik
*   **Crafting ve Refining Reçeteleri:**
    *   **Kaynak:** `ao-bin-dumps` GitHub deposundaki `recipes.json`
    *   **Ne İşe Yarar:** Bir eşyayı üretmek veya refine etmek için gerekli hammaddeler, miktarları, çıkan ürünler ve üretimde kullanılabilecek istasyonlar.
    *   **Veri Tipi:** Statik
*   **Şehir Bilgileri ve Üretim Bonusları:**
    *   **Kaynak:** `ao-bin-dumps` GitHub deposundaki `locations.json` ve Albion Online Wiki (Local Production Bonus)
    *   **Ne İşe Yarar:** Her şehrin kendine özgü refining ve crafting bonusları, kaynak dönüşüm oranları.
    *   **Veri Tipi:** Statik
*   **Temel Oyun Mekanikleri Katsayıları:**
    *   **Kaynak:** Albion Online Wiki (Premium, Crafting Focus, Resource return rate)
    *   **Ne İşe Yarar:** Premium üyeliğin getirdiği avantajlar (azaltılmış pazar vergisi, günlük odak puanı), odak kullanımı ile artan verimlilik oranları, genel kaynak dönüş oranları.
    *   **Veri Tipi:** Statik
*   **Pazar Vergileri ve İşlem Ücretleri (Temel):**
    *   **Kaynak:** Albion Online Wiki (Margin, Marketplace Setup Fee)
    *   **Ne İşe Yarar:** Pazar yerleştirme ücreti (setup fee) ve satış vergisi (market tax) temel oranları.
    *   **Veri Tipi:** Statik

---

## 4. Rule Tables

Oyun mekaniklerini ve ekonomi kurallarını tanımlayan veriler (çoğunlukla statik kaynaklardan türetilir):

*   **Şehir Üretim/Refining Bonusları Tablosu:**
    *   **Veri Alanları:** `CityID`, `CityName`, `RefineBonus` (Kaynak Tipi bazında), `CraftBonus` (Eşya Tipi bazında).
    *   **Açıklama:** Hangi şehrin hangi kaynakta veya eşya grubunda ne kadar bonus sağladığını gösterir.
*   **Odak Sistemi Verimlilik Hesaplama Kuralları:**
    *   **Veri Alanları:** `BaseFocusCost`, `FocusCostEfficiencyFormula`, `MasteryLevelContribution`, `PremiumFocusBonus`.
    *   **Açıklama:** Odak noktalarının üretim ve refining üzerindeki verimlilik artışını ve tüketimini hesaplamak için kullanılan formüller ve katsayılar.
*   **Premium Üyelik Etkileri Tablosu:**
    *   **Veri Alanları:** `PremiumStatus`, `MarketTaxReductionPercentage`, `DailyFocusGain`, `FameBonusPercentage`.
    *   **Açıklama:** Premium üyeliğin pazar vergisi indirimi, günlük odak kazanımı gibi faydaları.
*   **Pazar Yeri Vergi ve Ücret Kuralları:**
    *   **Veri Alanları:** `BaseSetupFeePercentage`, `BaseMarketTaxPercentage`, `PremiumTaxReductionPercentage`.
    *   **Açıklama:** Eşya listeletme ücreti ve satış vergisi oranları, Premium üyelere uygulanan indirimler. (Premium için %50 indirimli, yani non-premium %8, premium %4).
*   **Eşya Ağırlık ve Taşıma Kapasitesi Kuralları:**
    *   **Veri Alanları:** `ItemID`, `BaseWeight`, `InventoryCapacityFormula`, `MountCapacityBonus`, `BagCapacityBonus`.
    *   **Açıklama:** Eşyaların temel ağırlıkları, oyuncu ve bineklerin taşıma kapasitesi hesaplama mekanikleri.
*   **Kaynak Dönüşüm Oranları:**
    *   **Veri Alanları:** `BaseReturnRate`, `FocusReturnRateBonus`, `CityReturnRateBonus`.
    *   **Açıklama:** Üretim ve refining sırasında kaybedilen veya geri dönen kaynakların oranları.

---

## 5. User Input Tables

Kullanıcıdan alınması gereken dinamik veriler:

*   **Oyuncu Karakter Bilgileri:**
    *   **Veri Alanları:** `PlayerID`, `MasteryLevel` (her crafting/refining türü için), `PremiumStatus` (True/False), `AvailableFocusPoints`.
    *   **Açıklama:** Oyuncunun kendi üretim yetkinlik seviyeleri ve premium durumu, anlık odak puanı.
*   **Taşıma Tercihleri:**
    *   **Veri Alanları:** `PlayerID`, `SelectedMountCapacity`, `SelectedBagCapacity`, `DesiredMaxWeightPercentage`.
    *   **Açıklama:** Oyuncunun kullanacağı binek ve çanta bilgisi, hedeflediği maksimum ağırlık.
*   **Black Market İşlem Tercihleri:**
    *   **Veri Alanları:** `PlayerID`, `BlackMarketItemTargetPricePercentage` (eğer manuel hedef belirlenecekse), `AutoSellToBlackMarket` (True/False).
    *   **Açıklama:** Oyuncunun Black Market'e eşya satışı ile ilgili tercihleri (eğer bu modül geliştirilirse).

---

## 6. Recipe Sources

*   **Crafting Reçeteleri:**
    *   **Kaynak:** `ao-bin-dumps` GitHub deposundaki `recipes.json`
    *   **Yapı:** Her bir reçete için `craftingrequirements` (malzeme listesi), `craftingyield` (çıkan ürün ve miktarı), `craftresource` (hangi istasyonda üretildiği) gibi alanları içerir. Eşya ID'leri `item_definitions.json` ile eşleştirilmelidir.
    *   **Veri Tipi:** Statik
*   **Refining Reçeteleri:**
    *   **Kaynak:** `ao-bin-dumps` GitHub deposundaki `recipes.json`
    *   **Yapı:** Crafting reçeteleriyle benzer yapıdadır, ancak genellikle hammadde dönüşümüne odaklıdır.
    *   **Veri Tipi:** Statik

---

## 7. Black Market Data Status

*   **Gerçekten Var Olan Veri:** Black Market, Caerleon'da bulunan ve canavarlardan düşen ekipmanların oyuncular tarafından karşılandığı özel bir pazar yeridir. Oyunun ekonomisinin önemli bir parçasıdır. Fiyatlar, sistem tarafından belirlenen buy order'lar ile oluşur ve bu order'lar, oyuncuların Black Market'e sattığı eşyalarla karşılanır.
    *   **Kaynak:** Albion Online Wiki (Black Market), oyun içi gözlem.
    *   **Veri Tipi:** Canlı (fiyatlar), Statik (işleyiş mekaniği).
*   **Olmayan Veri (API Erişimi):** Black Market fiyatlarına doğrudan erişim sağlayan resmi bir API endpoint'i **bulunmamaktadır**. Bu nedenle, Black Market fiyatlarını programatik olarak çekmek mümkün değildir.
*   **Alternatif Veri Toplama:** Black Market fiyatlarını elde etmek için oyun içi manuel gözlem, topluluk destekli veri toplama (örn. oyuncuların fiyatları kaydetmesi) veya Sandbox Interactive'ın kullanım koşullarıyla çelişebilecek üçüncü taraf uygulamalar kullanılması gerekebilir. **Resmi API desteği olmadığından bu alandaki veri toplama stratejisi özel onay gerektirir.**

---

## 8. Minimum Viable Data Model

MVP için gerekli temel veri modeli:

*   **Item Tablosu:**
    *   `ItemID` (Primary Key)
    *   `ItemName`
    *   `ItemType`
    *   `ItemCategory`
    *   `Tier`
    *   `EnchantmentLevel`
    *   `BaseWeight`
*   **Location Tablosu (Cities):**
    *   `LocationID` (Primary Key)
    *   `LocationName`
    *   `Biome`
    *   `RefineBonus_Ore` (Diğer kaynaklar için de ayrı alanlar)
    *   `RefineBonus_Hide`
    *   `RefineBonus_Fiber`
    *   `RefineBonus_Wood`
    *   `RefineBonus_Stone`
    *   `CraftBonus_WeaponType` (Silah, Zırh, Alet vb. için ayrı alanlar)
    *   `CraftBonus_ArmorType`
*   **MarketPrice Tablosu (Canlı Veri):**
    *   `MarketPriceID` (Primary Key)
    *   `ItemID` (Foreign Key to Item Tablosu)
    *   `LocationID` (Foreign Key to Location Tablosu)
    *   `SellPriceMin`
    *   `SellPriceMax`
    *   `BuyPriceMin`
    *   `BuyPriceMax`
    *   `SellOrderCount`
    *   `BuyOrderCount`
    *   `Timestamp`
    *   `ItemQuality`
*   **Recipe Tablosu:**
    *   `RecipeID` (Primary Key)
    *   `OutputItemID` (Foreign Key to Item Tablosu)
    *   `OutputItemQuantity`
    *   `CraftingStation`
    *   `MasteryRequirement`
    *   `FocusCost` (Base)
*   **RecipeMaterial Tablosu (Recipe ve Item ilişkisi):**
    *   `RecipeMaterialID` (Primary Key)
    *   `RecipeID` (Foreign Key to Recipe Tablosu)
    *   `MaterialItemID` (Foreign Key to Item Tablosu)
    *   `MaterialQuantity`
*   **Rules Tablosu (Sabit Oyun Mekanikleri):**
    *   `RuleName` (örn. "BaseMarketTax", "PremiumTaxReduction")
    *   `RuleValue` (örn. 0.08, 0.50)
*   **PlayerSettings Tablosu (Kullanıcı Girişi):**
    *   `PlayerID` (Primary Key)
    *   `PremiumStatus` (Boolean)
    *   `CurrentFocusPoints`
    *   `MasteryLevel_CraftingType1`
    *   `MasteryLevel_RefiningType1`
    *   `EquippedMountCapacity`
    *   `EquippedBagCapacity`

---

## 9. MVP İçin Kesin Veri Toplama Planı

MVP (Minimum Viable Product) için aşağıdaki adımlar izlenecektir:

1.  **Statik Veri Toplama ve Depolama:**
    *   `ao-bin-dumps` GitHub deposundan `item_definitions.json`, `recipes.json` ve `locations.json` dosyaları indirilecektir.
    *   Bu JSON dosyaları parse edilecek ve Item, Location, Recipe ve RecipeMaterial tablolarına import edilecektir. Özellikle `locations.json` içindeki şehir bonusları Location tablosuna işlenecektir.
    *   Albion Online Wiki'den `Local Production Bonus`, `Crafting Focus`, `Premium`, `Margin` sayfaları incelenerek temel pazar vergileri, premium indirimleri, odak verimlilik formülleri ve eşya ağırlık/taşıma mekanikleri belirlenecek ve Rules tablosuna elle girilecektir.
2.  **Canlı Veri Toplama:**
    *   Albion Online Data Project (AODP) API'si kullanılarak belirli aralıklarla (örn. her 5-10 dakikada bir) popüler craft/refine ürünleri ve hammaddeleri için pazar fiyatları çekilecektir.
    *   API'den alınan fiyat verileri MarketPrice tablosuna zaman damgası ile birlikte kaydedilecektir. Hedeflenen sunucular (Americas, Asia, Europe) için ayrı ayrı veri çekimi yapılacaktır.
    *   API endpointleri:
        *   `/api/v2/stats/Prices/{item_id}?locations={location_id}` (Belirli bir eşyanın belirli bir lokasyondaki fiyatları)
3.  **Kullanıcı Girişi Mekanizması:**
    *   MVP arayüzünde oyuncunun Premium durumunu (Evet/Hayır), ilgili crafting/refining dallarındaki üstatlık seviyelerini ve kullanmak istediği odak miktarını girebileceği basit alanlar sağlanacaktır. Bu veriler PlayerSettings tablosuna kaydedilecektir.
4.  **Black Market Durumu Yönetimi:**
    *   MVP'de Black Market fiyatları için aktif bir API entegrasyonu olmayacaktır. Black Market'e satış kârlılık hesaplamaları, oyun içi gözlemlenen veya topluluk tarafından paylaşılan ortalama değerler üzerinden (kullanıcı girişi olarak alınabilir) bir tahminle yapılabilir. Bu konuda kullanıcı uyarılacak ve kesin veri olmadığı belirtilecektir.

---

## Sources

*   **Albion Online Data Project (AODP) API Documentation:** [https://www.albion-online-data.com/api/](https://www.albion-online-data.com/api/)
*   **Albion Online Data Project (AODP) Official Site:** [https://www.albion-online-data.com/](https://www.albion-online-data.com/)
*   **`ao-bin-dumps` GitHub Repository:** [https://github.com/broderickhyman/ao-bin-dumps](https://github.com/broderickhyman/ao-bin-dumps)
*   **Albion Online Wiki - Local Production Bonus:** [https://wiki.albiononline.com/wiki/Local_Production_Bonus](https://wiki.albiononline.com/wiki/Local_Production_Bonus)
*   **Albion Online Wiki - Crafting Focus:** [https://wiki.albiononline.com/wiki/Crafting_Focus](https://wiki.albiononline.com/wiki/Crafting_Focus)
*   **Albion Online Wiki - Premium:** [https://wiki.albiononline.com/wiki/Premium](https://wiki.albiononline.com/wiki/Premium)
*   **Albion Online Wiki - Margin (Marketplace Taxes):** [https://wiki.albiononline.com/wiki/Margin](https://wiki.albiononline.com/wiki/Margin)
*   **Albion Online Wiki - Weight and Burden:** [https://wiki.albiononline.com/wiki/Weight_and_Burden](https://wiki.albiononline.com/wiki/Weight_and_Burden)
*   **Albion Online Wiki - Black Market:** [https://wiki.albiononline.com/wiki/Black_Market](https://wiki.albiononline.com/wiki/Black_Market)