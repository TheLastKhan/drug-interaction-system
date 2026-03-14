# Proje İnceleme ve SCRUM-4 Çakışma Değerlendirmesi

**Tarih:** 14 Mart 2026
**Kapsam:** Repo durumu, `.md` dosyaları, mevcut veri çıktıları ve `SCRUM-4 DrugBank Vocabulary` işi için çakışma analizi

## İncelenen Ana Dosyalar

- `README.md`
- `PROJE_TAKVIMI_5HAFTA.md`
- `PROJE_OZET_RAPORU.md`
- `HOCAYA_PROJE_TANITIM.md`
- `LITERATUR_TARAMASI.md`
- `src/analyze_kaggle_ddi.py`
- `src/analyze_twosides.py`
- `src/build_vocabulary.py`

## Repo Durumu Özeti

- Aktif branch yalnızca `main`.
- Remote tarafta da yalnızca `origin/main` görünüyor.
- Git tarafından izlenmeyen tek kaynak kod dosyası `src/build_vocabulary.py`.
- `data/raw/` ve `data/processed/` altındaki büyük veri çıktıları `.gitignore` nedeniyle repoya girmiyor.
- Bu nedenle ekip içinde en büyük risk klasik Git merge çatışması değil, aynı ham/veri ara çıktıları üzerinde sessizce farklı işler yapılması.

## Projede Fiilen Görülen İlerleme

### Dokümantasyon tarafı

- Projenin amacı, veri kaynakları ve 5 haftalık plan net biçimde dokümante edilmiş.
- Mevcut `LITERATUR_TARAMASI.md` dosyası var, fakat daha kaynak-temelli ve güncel bir yeniden yazıma ihtiyaç duyuyordu.

### Kod tarafı

- `src/analyze_kaggle_ddi.py` ve `src/analyze_twosides.py` EDA/istatistik üretimi için yazılmış.
- `src/build_vocabulary.py` doğrudan `SCRUM-4` işine karşılık geliyor.

### Veri çıktıları

- `data/processed/drugbank_vocabulary_clean.csv` mevcut.
- Bu dosyada en az `55,487` satırlık normalize edilmiş isim varyantı bulunuyor.
- `data/processed/merged_drug_interactions.csv` mevcut.
- İlk 1000 satır örneğinde yalnızca 6 benzersiz ilaç çifti görülüyor; bu, `TWOSIDES` yan etki kayıtlarının aynı çift için birden fazla satır üretmesi nedeniyle merge çıktısında yoğun tekrar olduğunu gösteriyor.

## Sprint Maddelerine Göre Repo Eşlemesi

| Jira Maddesi | Beklenen Çıktı | Repodaki Kanıt | Yorum |
|---|---|---|---|
| `SCRUM-1` Kaggle DDI + TWOSIDES birleştirme | `data/processed/merged_ddi.csv` | `data/processed/merged_drug_interactions.csv` var | Büyük ihtimalle işin önemli kısmı yapılmış ama çıktı adı planla birebir aynı değil |
| `SCRUM-2` NLP ile label çıkarma | `data/processed/labeled_interactions.csv` | Bu adda dosya yok, ilgili script de görünmüyor | Repo seviyesinde tamamlanmış görünmüyor |
| `SCRUM-5` EDA görselleştirmeleri | `notebooks/01_eda_visualizations.ipynb` | `notebooks/` boş görünüyor | Repo seviyesinde görünür çıktı yok |
| `SCRUM-4` DrugBank Vocabulary indirme ve isim standardizasyonu | `data/raw/drugbank_vocabulary.csv` veya benzeri + standartlaştırma çıktısı | `data/raw/drugbank vocabulary.csv`, `src/build_vocabulary.py`, `data/processed/drugbank_vocabulary_clean.csv` | Bu iş için somut ilerleme var |

## SCRUM-4 Açısından Çakışma Riski

### Düşük riskli alanlar

- `src/build_vocabulary.py` şu an yalnızca yerel ve untracked; ekipte başka biri tarafından repoya alınmış paralel bir sürüm görünmüyor.
- `SCRUM-1`, `SCRUM-2` ve `SCRUM-5` için beklenen ana çıktılar repo üzerinde görünür değil.
- Bu yüzden senin `SCRUM-4` işini ayrı bir sözlük/normalizasyon katmanı olarak ilerletmen teknik olarak güvenli görünüyor.

### Orta riskli alanlar

- Vocabulary işi doğası gereği merge ve label çıkarma işlerini besleyen upstream bir katman.
- Yani doğrudan kod çatışması az olsa da, aynı ilaç adlarının nasıl normalize edileceği konusunda ekip kararı gerekebilir.
- Özellikle `Drug 1`, `Drug 2`, `drug_1_concept_name`, `drug_2_concept_name` eşleştirmelerinde hangi canonical name yaklaşımının seçileceği sonradan `SCRUM-1` ve `SCRUM-2` sonuçlarını etkileyebilir.

### Şu an en olası gerçek çakışma tipi

- Aynı dosyaya yazma çakışması değil
- Aynı alan için farklı isimlendirme/normalizasyon kuralı üretme çakışması
- Yani problem Git merge değil, veri kontratı çakışması

## Güvenli Çalışma Koridoru

`SCRUM-4` işini aşağıdaki sınırlar içinde yürütürsen ekip çakışması çok düşük olur:

1. Vocabulary katmanını ayrı tut:
   - `drugbank_id`
   - `common_name`
   - `name_variant`
   - `name_norm`

2. `merged_drug_interactions.csv` dosyasını şimdilik read-only kabul et.

3. Çıktılarını merge edilmiş veri üstüne yazmak yerine eşleştirme yardımcı çıktıları olarak üret:
   - örnek: `drug_name_mapping_audit.csv`
   - örnek: `vocabulary_match_report.md`

4. Eşleştirme mantığını açıkça dokümante et:
   - lower-case
   - accent removal
   - punctuation cleanup
   - synonym expansion
   - duplicate handling

5. Ambiguous alias durumlarını ayrıca listele.

## Somut Sonuç

14 Mart 2026 itibarıyla repo görünümüne göre:

- `SCRUM-4 vocabulary` işini alman mantıklı.
- Mevcut kanıta göre ekip arkadaşlarınla doğrudan dosya bazlı güçlü bir çakışma görünmüyor.
- En güçlü risk, teknik çatışmadan çok veri standardı kararlarının sessizce farklılaşması.
- Bu yüzden `SCRUM-4` işini "canonical vocabulary + normalization + coverage audit" olarak konumlandırman en güvenli yaklaşım olur.

## Benim Net Kararım

`SCRUM-4` üzerinde devam etmek için uygun bir alan var.

Ben olsam bu işi şu kapsamla sürdürürdüm:

- DrugBank vocabulary temizleme
- synonym tabanı oluşturma
- normalize edilmiş ilaç adı alanı üretme
- Kaggle ve TWOSIDES isimleri için kapsama/eşleşme raporu çıkarma
- merge dosyasını yeniden yazmadan, ek bir mapping katmanı üretme

Bu yaklaşım hem arkadaşlarınla çakışmayı azaltır, hem de projeye en fazla sistematik katkıyı sağlar.
