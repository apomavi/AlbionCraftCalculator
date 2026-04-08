## Validator Raporu

### Verdict
PARTIAL

### Correct Claims

*   AODP'nin market verileri için aşağıdaki REST API endpoint'lerini sunduğu iddiası doğrudur:
    *   `/api/v2/stats/History/{item_id_list}`
    *   `/api/v2/stats/Prices/{item_id_list}`
    *   `/api/v2/stats/data/{item_id_list}`
    *   `/api/v2/stats/average-prices`
*   `https://www.albion-online-data.com/items.json` ve `https://www.albion-online-data.com/items.txt` dosyalarının item ID, isim ve diğer meta verilerini içerdiği ve item eşlemesi için kullanılabileceği iddiası doğrudur.
*   Albion Online Data Project'in resmi sayfalarında veya API belgelerinde harici geliştiricilerin kullanabileceği NATS topic listeleri veya doğrudan NATS entegrasyonu hakkında resmi bir bilginin bulunmadığı iddiası doğrudur.
*   Hesaplama motoru için Item Verileri (ID, Name, Tier, Enchantment) ve Pazar Verileri (City, Sell/Buy Price Min/Max, Timestamp, Amount) alanlarının AODP REST API'si üzerinden sağlanabileceği iddiası doğrudur.
*   AODP API'sinde doğrudan recipe verileri, taşıma maliyetleri ve crafting/refining ücretleri sunan bir endpoint bulunmadığı iddiası doğrudur ve bu veriler için harici bir kaynağa ihtiyaç duyulacağı tespiti geçerlidir.

### Wrong Claims

*   **REST Endpoints - `/api/v2/stats/Charts/{item_id_list}.{quality}`:** Raporda belirtilen `/api/v2/stats/Charts/{item_id_list}.{quality}` endpoint'i hatalıdır. Swagger UI ve API belgelerine göre `quality` parametresi path içinde değil, bir sorgu parametresi (`query parameter`) olarak kullanılmaktadır. Doğrusu: `/api/v2/stats/Charts/{item_id_list}?quality={quality}`.
*   **Black Market Data Status:** "Black Market'e özel ... doğrudan fiyat veya talep verilerini çeken belirli bir endpoint bulunmamaktadır." ve "...ayrı bir kategori veya filtrelenebilir bir alan olarak açıkça belirtilmemiştir." iddiaları yanlıştır. AODP API'sinde `/api/v2/stats/Prices` gibi endpoint'lerde `locations` parametresi için "Black Market" değeri kullanılabilir ve bu sayede Black Market verilerine erişilebilir. Bu, Black Market verilerinin filtrelenebilir bir alan olarak mevcut olduğunu gösterir.

### Unverified Claims
Yok.

### Required Fixes

1.  **REST Endpoints:** `/api/v2/stats/Charts/{item_id_list}.{quality}` endpoint tanımı, `quality` parametresinin bir sorgu parametresi olduğunu belirtecek şekilde düzeltilmelidir (örn: `/api/v2/stats/Charts/{item_id_list}?quality={quality}`).
2.  **Black Market Data Status:** Black Market verilerine, pazar verisi endpoint'lerinde `locations=Black%20Market` parametresi kullanılarak erişilebildiği bilgisi rapora eklenmelidir. Bu durum, Black Market verilerinin mevcut pazar verileri içinde filtrelenebilir bir kategori olduğunu açıkça belirtir.