## Albion Online Veri Araştırma Raporu

### Research Headings

1.  **AODP Resmi API ve Developer Sayfası:**
    *   Mevcut API endpoint'leri ve sundukları veri türleri.
    *   API kullanım limitleri ve kimlik doğrulama yöntemleri.
    *   Developer dokümantasyonunda belirtilen kritik bilgiler.
    *   **Kullanım Alanı:** Market verileri, eşya bilgileri, zanaat ve rafine tarifleri.

2.  **AODP Item/Identifier Yapısı:**
    *   Eşyaların benzersiz tanımlayıcıları (IDs) ve bu tanımlayıcıların API ile ilişkisi.
    *   Eşyaların kategorizasyonu, seviyeleri, özelliklerindeki tutarlılık.
    *   **Kullanım Alanı:** Eşya takibi, fiyatlandırma, zanaat ve rafine girdileri.

3.  **ao-bin-dumps GitHub Repoları:**
    *   [https://github.com/brodyle/ao-bin-dumps](https://github.com/brodyle/ao-bin-dumps)
    *   Oyunun statik verilerini (eşya bilgileri, tarifler, statlar vb.) barındıran depoların incelenmesi.
    *   Bu depolardaki verilerin güncelliği ve AODP API verileriyle karşılaştırılması.
    *   **Kullanım Alanı:** Zanaat ve rafine tariflerinin detayları, eşya özellikleri.

4.  **Şehir Bonusları (City Bonuses):**
    *   Her şehrin sunduğu spesifik üretim, rafine veya ticaret bonuslarının tespiti.
    *   Bu bonusların fiyatlandırma ve kar marjlarına etkisi.
    *   **Kullanım Alanı:** Rafine ve zanaat verimliliği, taşıma maliyetleri.

5.  **Focus Sistemi:**
    *   Focus'un zanaat ve rafine üzerindeki etkileri, oranları ve maliyetleri.
    *   Focus kullanımı ile elde edilen verim artışının hesaplanması.
    *   **Kullanım Alanı:** Zanaat ve rafine karlılık analizleri.

6.  **Premium Etkileri:**
    *   Premium aboneliğin zanaat, rafine, üretim ve pazar işlemlerine olan etkileri (vergiler, bonuslar vb.).
    *   **Kullanım Alanı:** Tüm ekonomik hesaplamalarda Premium durumu değişkeni.

7.  **Pazar Verileri (Market Tax, Setup Fee, Satış Vergileri):**
    *   Her şehirdeki pazar vergisi oranları.
    *   Eşya satışına uygulanan işlem ücretleri (setup fee).
    *   Pazar manipülasyonu ve flip stratejileri için bu verilerin önemi.
    *   **Kullanım Alanı:** Market flip, kar marjı hesaplamaları.

8.  **Zanaat (Craft) ve Rafine (Refine) Tarif Kaynakları:**
    *   Resmi API ve GitHub depolarından elde edilecek zanaat/rafine tarif girdileri ve çıktıları.
    *   Gerekli hammaddeler, işleme istasyonları ve uzmanlık seviyeleri.
    *   **Kullanım Alanı:** Üretim maliyeti ve kar marjı hesaplamaları.

9.  **Taşıma (Transport) İçin Gerekli Veri Alanları:**
    *   Eşya ağırlığı, hacmi (varsa), kırılganlık durumu.
    *   Farklı şehirler arası taşıma maliyetleri (yol, risk vb.).
    *   **Kullanım Alanı:** Lojistik ve taşıma maliyeti hesaplamaları.

10. **Kara Borsa (Black Market) Veri Durumu:**
    *   Kara borsa talebi ve fiyatlandırması için resmi olarak sunulan bir API veya veri kaynağı olup olmadığı.
    *   Kara borsanın oyun içi dinamiklerinin ve veri erişilebilirliğinin tespiti.
    *   **Kullanım Alanı:** Kara borsa alım/satım karlılığı.

11. **Statik Veriler:**
    *   Zanaat/rafine tarifleri, eşya özellikleri, şehir bonusları (değişkenlik az ise), temel oyun mekanikleri.
    *   **Kullanım Alanı:** Veritabanında saklanacak, nadiren güncellenen bilgiler.

12. **Canlı Veriler:**
    *   Güncel pazar fiyatları, eşya arz/talep durumu, oyuncu sayıları (varsa).
    *   **Kullanım Alanı:** Gerçek zamanlı analiz ve tahminler için API'den çekilecek veriler.

13. **Kullanıcıdan Alınacak Veriler:**
    *   Oyuncu adı, şehir tercihleri, Premium durumu, mevcut Focus miktarı.
    *   **Kullanım Alanı:** Kişiselleştirilmiş analizler ve hesaplamalar.

### Approval Needed

1.  **AODP API Erişim Politikası:** Ücretsiz erişimin yeterli olup olmadığı veya ücretli katmanlar için bütçe gerekliliği.
2.  **GitHub Depolarının Güvenilirliği ve Güncelliği:** `ao-bin-dumps` gibi depoların verilerinin ne ölçüde güvenilir ve güncel kabul edileceği konusunda bir standarta karar verilmesi.
3.  **Kara Borsa Veri Erişimi:** Kara borsa için veriye ulaşımın kısıtlı veya imkansız olması durumunda, bu alanın analiz kapsamından çıkarılıp çıkarılmayacağına karar verilmesi.

### Next Task

GitHub depolarındaki (ao-bin-dumps) statik oyun verilerinin (eşya, zanaat, rafine tarifleri) ilk incelenmesi ve AODP API'sinden çekilebilecek canlı pazar verisi formatının belirlenmesi.