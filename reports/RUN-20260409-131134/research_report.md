## Albion Online Ekonomi Veri Araştırması Raporu

### 1. Source Inventory

*   **Albion Online Data Project (AODP) API:** Oyun içi güncel pazar verileri, eşya bilgileri ve tarifler için birincil kaynak.
*   **ao-bin-dumps (GitHub):** Oyunun statik verilerini (eşya ID'leri, statlar, zanaat/rafine tarifleri) içeren, oyun güncellemeleriyle güncellenen bir depo.
*   **Albion Online Wiki:** Oyun mekanikleri, eşya detayları ve genel bilgiler için referans kaynak.
*   **Oyun İçi Gözlem / Kullanıcı Girdileri:** Kara borsa verileri gibi resmi olarak sunulmayan veriler için dolaylı bilgi kaynağı veya doğrudan kullanıcıdan alınacak veriler.

### 2. Live Data Sources

*   **AODP API - Market Data:** Belirli bir eşyanın farklı şehirlerdeki anlık satış fiyatları, arz ve talep miktarları. (Canlı)
    *   *Ne işe yarar:* Market flip, kar marjı ve fiyat trendleri analizi.
*   **AODP API - Item Data:** Eşyaların güncel statları, seviyeleri, ağırlıkları. (Canlı/Statik - Oyun güncellemeleriyle değişir)
    *   *Ne işe yarar:* Eşya bazlı üretim ve taşıma maliyetlerinin hesaplanması.
*   **AODP API - Crafting/Refining Recipes (Girdi/Çıktı Oranları):** Belirli bir eşyayı üretmek veya rafine etmek için gereken hammaddeler ve çıkan ürün miktarı. (Canlı/Statik - Oyun güncellemeleriyle değişir)
    *   *Ne işe yarar:* Üretim maliyetlerinin ve verimliliğin hesaplanması.

### 3. Static Data Sources

*   **ao-bin-dumps - Item Definitions:** Eşyaların ID'leri, isimleri, türleri, temel özellikleri ve ikonları. (Statik)
    *   *Ne işe yarar:* Eşyaların oyun içindeki temel tanımlayıcıları ve özellikleri.
*   **ao-bin-dumps - Crafting/Refining Recipes (Temel Tarif Yapısı):** Zanaat ve rafine işlemleri için gereken hammaddelerin listesi, kullanılan istasyon ve gerekli beceri seviyeleri. (Statik)
    *   *Ne işe yarar:* Üretim zincirlerinin ve temel tariflerin anlaşılması.
*   **Albion Wiki / Oyun İçi Kurallar:** Şehir bonusları, focus sistemi etkileri, premium avantajları, pazar vergileri ve işlem ücretleri gibi oyun mekaniklerinin detayları. (Statik)
    *   *Ne işe yarar:* Ekonomik hesaplamalarda kullanılacak kural ve bonusların belirlenmesi.

### 4. Rule Tables

*   **Şehir Bonusları Tablosu:** Her şehir için üretim, rafine veya ticaret bonuslarının yüzdesel değerleri. (Statik)
    *   *Ne işe yarar:* Belirli şehirlerdeki üretim/rafine karlılığını etkiler.
*   **Pazar Ücretleri Tablosu:** Şehir bazında satış vergisi (tax) ve kurulum ücreti (setup fee) oranları. (Statik)
    *   *Ne işe yarar:* Pazar işlemlerindeki maliyetleri belirler.
*   **Focus Etki Tablosu:** Focus kullanıldığında zanaat/rafine verimliliğindeki artış oranları ve Focus tüketim hızları. (Statik)
    *   *Ne işe yarar:* Focus'lu üretimin karlılığını hesaplar.
*   **Premium Etki Tablosu:** Premium aktifken uygulanan vergi indirimleri, üretim bonusları vb. oranlar. (Statik)
    *   *Ne işe yarar:* Premium oyuncular için ekonomik hesaplamaları ayarlar.

### 5. User Input Tables

*   **Oyuncu Bilgileri:** Oyuncu adı, seçtiği ana şehir, Premium durumu (aktif/pasif). (Kullanıcı Girdisi)
    *   *Ne işe yarar:* Kişiselleştirilmiş analizler ve Premium etkilerinin uygulanması.
*   **Mevcut Kaynaklar:** Oyuncunun elindeki hammadde miktarları ve maliyetleri. (Kullanıcı Girdisi)
    *   *Ne işe yarar:* Üretim planlaması ve mevcut stokla yapılabilecek işlemlerin belirlenmesi.
*   **Hedeflenen Ürün/Eşya:** Oyuncunun üretmek veya satmak istediği eşya. (Kullanıcı Girdisi)
    *   *Ne işe<bos>:* Analizlerin belirli bir eşyaya odaklanmasını sağlar.
*   **Focus Miktarı:** Oyuncunun kullanmak istediği Focus miktarı. (Kullanıcı Girdisi)
    *   *Ne işe yarar:* Focus'lu üretim karlılık hesaplamaları için girdi.

### 6. Recipe Sources

*   **AODP API:** Canlı ve güncel girdi/çıktı oranlarını çekmek için kullanılır. Özellikle oyun güncellemeleri sonrası kritik. (Canlı)
    *   *Ne işe yarar:* Güncel üretim ve rafine verimliliği.
*   **ao-bin-dumps (GitHub):** Eşyaların üretim ve rafine edilmesi için gereken temel hammaddeleri, kullanılan istasyonları ve statik tarif yapısını içerir. (Statik)
    *   *Ne işe yarar:* Tariflerin temel yapısını ve gereken girdileri öğrenme.

### 7. Black Market Data Status

*   **Veri Kaynağı:** Resmi bir AODP API'si veya kamuya açık bir veri deposu bulunmamaktadır. (Mevcut Değil)
*   **Erişim Yöntemi:** Kara borsa verileri için doğrudan veri çekme imkanı yok. Dolaylı analizler (oyuncu gözlemleri, belirli eşyaların kara borsadaki genel fiyat aralığı tahminleri) veya kullanıcıdan alınacak manuel girdiler ile sınırlı kalınabilir. (Dolaylı / Kullanıcı Girdisi)
    *   *Ne işe yarar:* Kara borsa alım/satım kararlılığını tahmin etmek zordur, manuel veri girişi gerektirir.

### 8. Minimum Viable Data Model

*   **Items:** item_id, name, type, weight, stackable (id, isim, tip, ağırlık, yığınlanabilirlik) - (Statik)
*   **Recipes:** recipe_id, output_item_id, input_item_id, input_amount, output_amount, crafting_station (tarife_id, çıktı_eşya_id, girdi_eşya_id, girdi_miktarı, çıktı_miktarı, üretim_istasyonu) - (Statik)
*   **CityMarketPrices:** city, item_id, buy_price, sell_price, timestamp (şehir, eşya_id, alış_fiyatı, satış_fiyatı, zaman damgası) - (Canlı)
*   **CityBonuses:** city, bonus_type, bonus_value (şehir, bonus_tipi, bonus_değeri) - (Statik)
*   **MarketFees:** city, tax_rate, setup_fee (şehir, vergi_oranı, kurulum_ücreti) - (Statik)
*   **PlayerInfo:** player_name, is_premium, current_city, focus_points (oyuncu_adı, premium_durumu, mevcut_şehir, focus_puanı) - (Kullanıcı Girdisi)

### 9. MVP Data Collection Plan

1.  **Statik Veri Çekimi (ao-bin-dumps):**
    *   `ao-bin-dumps` deposundan `items.json` ve `recipes.json` gibi dosyaları indir.
    *   Bu verileri kullanarak `Items` ve `Recipes` tablolarını oluştur.
    *   *Ne işe yarar:* Temel eşya ve tarif bilgilerini sisteme dahil etme.
2.  **Şehir ve Pazar Kuralları (Wiki/Oyun İçi Gözlem):**
    *   Albion Wiki ve oyun içi gözlemlerle şehir bonuslarını, pazar vergilerini ve işlem ücretlerini belirle.
    *   `CityBonuses` ve `MarketFees` tablolarını doldur.
    *   *Ne işe yarar:* Ekonomik kuralları ve maliyetleri sisteme entegre etme.
3.  **Canlı Pazar Verisi Erişimi (AODP API):**
    *   AODP API'sini kullanarak belirli şehirlerdeki eşyaların güncel alım/satım fiyatlarını çek.
    *   `CityMarketPrices` tablosunu anlık veya periyodik olarak güncelle.
    *   *Ne işe yarar:* Güncel piyasa koşullarını analiz edebilme.
4.  **Kullanıcı Girdisi Mekanizması:**
    *   Oyuncunun Premium durumunu, mevcut şehrini ve focus puanını girebileceği bir arayüz oluştur.
    *   *Ne işe yarar:* Kişiselleştirilmiş hesaplamalar için gerekli girdileri sağlama.
5.  **Kara Borsa Verisi (Manuel Giriş):**
    *   Kara borsa için doğrudan veri kaynağı olmadığından, kullanıcıdan manuel olarak tahmini alım/satım fiyatları veya kar marjı bilgisi alma opsiyonu ekle.
    *   *Ne işe yarar:* Sınırlı da olsa kara borsa analizine dahil edebilme.

### 10. Sources

*   **Albion Online Data Project (AODP) API:** [https://www.albion-online.com/en/data](https://www.albion-online.com/en/data) (Resmi - API dokümantasyonu gereklidir)
*   **ao-bin-dumps GitHub Repository:** [https://github.com/brodyle/ao-bin-dumps](https://github.com/brodyle/ao-bin-dumps) (GitHub)
*   **Albion Online Wiki:** [https://wiki.albiononline.com/wiki/Main_Page](https://wiki.albiononline.com/wiki/Main_Page) (Referans)