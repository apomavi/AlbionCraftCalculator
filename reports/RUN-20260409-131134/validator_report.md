- Verdict: PARTIAL

- Correct Claims:
    - Source Inventory listesi genel olarak doğru ve ilgili kaynakları içeriyor.
    - Live Data Sources bölümünde AODP API'nin pazar ve eşya verileri için kullanılabileceği doğru.
    - Static Data Sources bölümünde `ao-bin-dumps`'ın eşya tanımları ve temel tarif yapısı için kullanıldığı doğru.
    - Rule Tables başlığı altında şehir bonusları, pazar ücretleri, focus ve premium etkilerinin statik veri olarak sınıflandırılması doğru.
    - User Input Tables başlığı altında oyuncu bilgileri, mevcut kaynaklar, hedeflenen eşya ve focus miktarının kullanıcı girdisi olarak alınması gerektiği doğru.
    - Recipe Sources bölümünde hem AODP API'nin canlı veriler hem de `ao-bin-dumps`'ın statik yapı için kullanılabileceği doğru.
    - Black Market Data Status bölümünde resmi veri kaynağı olmadığı ve dolaylı/manuel erişim gerektiği tespiti doğru.
    - Minimum Viable Data Model'deki tablolar (Items, Recipes, CityMarketPrices, CityBonuses, MarketFees, PlayerInfo) MVP için uygun görünüyor.
    - MVP Data Collection Plan'deki adımlar genel olarak mantıklı ve kaynakları doğru kullanıyor.
    - Kaynaklar listesi (AODP API, ao-bin-dumps, Albion Wiki) doğru ve linkleri mevcut.

- Wrong Claims:
    - **Live Data Sources - Item Data:** "Eşyaların güncel statları, seviyeleri, ağırlıkları." olarak belirtilmiş. Ağırlık (`weight`) gibi bazı temel eşya özellikleri `ao-bin-dumps` gibi statik kaynaklarda bulunur ve oyun güncellemeleriyle sık değişmez. Bu, "Canlı/Statik - Oyun güncellemeleriyle değişir" olarak genelleştirilemez. Bazı temel özellikler statiktir.
    - **Live Data Sources - Crafting/Refining Recipes:** "Canlı/Statik - Oyun güncellemeleriyle değişir" ifadesi biraz kafa karıştırıcı. API'den çekilen veriler günceldir (yani "canlı" olarak görülebilir), ancak tarifin kendisi (hangi girdiden ne kadar çıkacağı) genellikle oyun güncellemelerinde değişir. Bu ayrım netleştirilmeli. `ao-bin-dumps` statik tarif yapısını verirken, API güncel çıktıları verebilir.
    - **Static Data Sources - Item Definitions:** "Eşyaların ID'leri, isimleri, türleri, temel özellikleri ve ikonları." listelenmiş. Ağırlık (`weight`) gibi bazı temel özellikler buraya da eklenebilir ve `ao-bin-dumps`'tan gelir.
    - **MVP Data Collection Plan - 2. Şehir ve Pazar Kuralları:** "Albion Wiki ve oyun içi gözlemlerle şehir bonuslarını, pazar vergilerini ve işlem ücretlerini belirle." denmiş. Bu bilgiler hem Wiki'de hem de API'de (pazar vergileri ve ücretleri için) bulunabilir. Sadece "oyun içi gözlem"e sınırlı kalmak yerine resmi veri kaynaklarına öncelik verilmeli.

- Unverified Claims:
    - **AODP API - Item Data:** API'nin "güncel statlar" olarak tam olarak neleri içerdiği, ağırlık gibi bilgileri içerip içermediği ve bunların ne sıklıkla güncellendiği tam olarak doğrulanmalı.
    - **AODP API - Crafting/Refining Recipes:** API'nin sadece girdi/çıktı oranlarını mı yoksa tüm tarif yapısını mı çektiği netleştirilmeli.
    - **MVP Data Collection Plan - 5. Kara Borsa Verisi (Manuel Giriş):** "Tahmini alım/satım fiyatları veya kar marjı bilgisi alma opsiyonu"nun nasıl bir mekanizma ile olacağı (örneğin, kullanıcının bir aralık girmesi mi, tek bir değer mi?) belirtilmemiş. Bu, "kullanıcı girdisi" kategorisiyle örtüşüyor ancak detaylandırılmalı.

- Required Fixes:
    - **Live Data Sources:** "Item Data" bölümündeki eşya özelliklerinin statik mi yoksa canlı mı olduğu ayrımı daha net yapılmalı. Ağırlık gibi statik özellikler için `ao-bin-dumps`'a atıfta bulunulmalı.
    - **Live Data Sources:** "Crafting/Refining Recipes" bölümündeki "Canlı/Statik" ifadesi netleştirilmeli. API'den çekilen verinin "güncel çıktı" olduğu, tarifin "temel yapısının" ise statik olduğu vurgulanmalı.
    - **Static Data Sources:** "Item Definitions" listesine, `ao-bin-dumps`'tan elde edilebilecek statik özellikler (örneğin, ağırlık) eklenmeli.
    - **MVP Data Collection Plan:** "Şehir ve Pazar Kuralları" bölümünde, bu verilerin sadece "oyun içi gözlem" ile değil, API ve Wiki gibi resmi kaynaklardan da alınabileceği belirtilmeli ve bu kaynaklara öncelik verildiği vurgulanmalı.
    - **MVP Data Collection Plan:** "Kara Borsa Verisi (Manuel Giriş)" bölümündeki kullanıcı girdisi mekanizmasının nasıl olacağı hakkında daha fazla detay (örneğin, veri formatı) eklenebilir, ancak bu bir MVP için şart olmayabilir. Mevcut haliyle "kullanıcı girdisi" olması yeterli.
    - **API Endpoints:** Tüm API kullanımları için somut endpoint örnekleri veya dokümantasyon linki eklenmesi, belirsizliği azaltacaktır. Rapor, "AODP API" genelinde konuşuyor ancak spesifik endpointler belirtilmemiş.
    - **NATS:** Raporun hiçbir yerinde NATS (Neural Autoregressive Sequence models) ile ilgili bir referans veya kullanım amacı bulunmamaktadır. Bu durum, "Wrong Claims" veya "Unverified Claims" altına "Irrelevant Section" olarak işaretlenmeli veya tamamen kaldırılmalıdır. Eğer NATS'ın dolaylı bir kullanımı varsa (örneğin, fiyat tahmini için bir ML modeli), bunun açıkça belirtilmesi gerekir. Şu anki haliyle listede yeri yok.
    - **Item Mapping:** `ao-bin-dumps` ve AODP API arasındaki eşya ID eşleştirmesi (item mapping) hakkında bilgi yok. `ao-bin-dumps`'tan alınan ID'lerin AODP API'sinde nasıl kullanılacağı veya tam tersi gibi durumlar belirsiz. Bu, MVP için kritik olabilir. "Unverified Claims" altına eklenebilir.
    - **Black Market:** "Kara borsa için gerçekten var olan veri ve olmayan veri" bölümü (Raporun 7. maddesi) genel olarak doğru olsa da, MVP planındaki manuel giriş yöntemiyle nasıl entegre olacağı daha net ifade edilebilir.