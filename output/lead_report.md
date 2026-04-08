# Albion Online Ekonomi Araştırma Planı

## Research Headings

1.  **AODP Resmi API Dokümantasyonu ve Entegrasyon Noktaları:**
    *   Mevcut ve gelecekteki veri çekme potansiyeli.
    *   Fiyatlandırma, pazar verileri, eşya bilgileri için kullanım.
    *   [Albion Online API](https://api.albiononline.com/)
2.  **AODP Developer Sayfası ve Geliştirici Kaynakları:**
    *   API erişim politikaları, kullanım limitleri.
    *   Geliştirici topluluğu, potansiyel destek.
3.  **AODP Eşya (Item) Yapısı ve Tanımlayıcıları (Identifiers):**
    *   Tüm eşyaların ID'leri, tipleri, özellikleri.
    *   Reçetelerde ve pazar listelemelerinde kullanılan benzersiz tanımlayıcılar.
4.  **`ao-bin-dumps` GitHub Deposu Analizi:**
    *   `item_definitions.json`: Eşya temel verileri (ID, isim, tip).
    *   `recipes.json`: Crafting ve refining reçeteleri (gerekli materyaller, çıktılar, üstatlık seviyeleri).
    *   `locations.json`: Şehirler, bölgeler ve potansiyel bonus alanları.
    *   [ao-bin-dumps](https://github.com/broderickhyman/ao-bin-dumps)
5.  **Şehir Bonusları (City Bonuses):**
    *   Her şehrin üretim, refining ve pazar üzerindeki etkileri.
    *   İlgili verilerin `locations.json` veya API'den çekilmesi.
6.  **Odak Sistemi (Focus System):**
    *   Odak kullanarak üretim verimliliğinin artırılması.
    *   Odak tüketimi ve verimlilik artış oranları.
7.  **Premium Etkileri:**
    *   Premium üyeliğin üretim, refining, pazar komisyonları ve diğer ekonomi modüllerine etkisi.
8.  **Pazar Vergileri ve Komisyonları:**
    *   Listeletme ücretleri (setup fee), satış vergileri (market tax).
    *   Şehir ve üstatlık seviyesine göre değişkenlik.
9.  **Crafting Reçeteleri Kaynakları:**
    *   `recipes.json` (ao-bin-dumps) üzerinden çekilecek temel veriler.
    *   Detaylı malzeme bilgileri için item tanımlayıcıları.
10. **Refining Reçeteleri Kaynakları:**
    *   `recipes.json` (ao-bin-dumps) üzerinden çekilecek temel veriler.
    *   Detaylı malzeme bilgileri için item tanımlayıcıları.
11. **Taşıma Veri Alanları:**
    *   Eşya ağırlığı, hacmi.
    *   Taşıyıcı kapasitesi (atlar, oyuncu, depolama).
    *   Bölgeler arası seyahat süreleri/maliyetleri.
12. **Black Market Veri Durumu:**
    *   Black Market'te işlem gören eşyalar (var mı?).
    *   Fiyatlandırma dinamikleri (varsa).
    *   API veya oyun içi gözlem gereksinimi.
    *   Resmi olarak dokümante edilmiş veri var mı? (Muhtemelen hayır).
13. **Statik Veri Alanları:**
    *   Eşya tanımları (ID, isim, tip, kategori, ağırlık).
    *   Craft/Refine reçeteleri (malzemeler, çıktılar, adımlar).
    *   Şehir bilgileri ve sabit bonusları.
    *   Temel oyun mekanikleri (premium etkileri, odak verimliliği).
14. **Canlı (Canlı Çekilmesi Gereken) Veri Alanları:**
    *   Güncel pazar fiyatları (satış ve alış).
    *   Güncel stok bilgileri (nerede ne kadar var).
    *   Black Market fiyatları (eğer tespit edilebilirse).
15. **Kullanıcıdan Alınması Gereken Veriler:**
    *   Oyuncunun sahip olduğu karakterin üstatlık seviyeleri.
    *   Oyuncunun sahip olduğu premium durumu.
    *   Oyuncunun kullanmak istediği odak miktarı.
    *   Oyuncunun depolama/taşıma kapasitesi.
    *   Black Market işlem tercihleri (eğer veri alınabilirse).

## Approval Needed

*   **`ao-bin-dumps` deposunun güvenilirliği ve güncelliği:** Bu depo, oyun dosyalarından çekilen verileri içerir. Verilerin ne sıklıkla güncellendiği ve oyun güncellemeleri ile ne kadar uyumlu olduğu kritik öneme sahiptir.
*   **Black Market veri toplama stratejisi:** Black Market'in resmi bir API desteği olmadığı için, veri toplama yönteminin (oyun içi manuel gözlem, bot ile takip vb.) oyunun kullanım koşullarına uygunluğu ve etkinliği hakkında onay alınmalıdır.
*   **Veri depolama ve erişim stratejisi:** Elde edilecek büyük veri setinin nasıl depolanacağı (veritabanı seçimi, schema tasarımı) ve nasıl erişileceği konusunda onay alınması gerekmektedir.

## Next Task

*   **`ao-bin-dumps` deposunun detaylı analizi ve `item_definitions.json`, `recipes.json`, `locations.json` dosyalarının çekilip incelenmesi.**