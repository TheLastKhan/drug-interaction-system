# 📅 İlaç Etkileşim Uyarı Sistemi — 5 Haftalık Proje Takvimi

**Başlangıç:** 3 Mart 2026  
**Bitiş:** 6 Nisan 2026  
**Ekip:** 3 kişi  

> **Not:** Veri seti araştırması, proje yapısı kurulumu ve keşifsel veri analizi (EDA) zaten tamamlanmıştır. Bu takvim kalan geliştirme sürecini kapsar.

---

## 👥 Rol Dağılımı

| Kısaltma | Rol | Sorumluluk Alanı |
|----------|-----|------------------|
| **ML** | Makine Öğrenmesi | Veri işleme, model eğitimi, optimizasyon |
| **BE** | Backend | FastAPI, veritabanı, model servisi |
| **FE** | Frontend | Web arayüzü, görselleştirme, UX |

---

## 🗓️ Hafta 1 — Veri Hazırlama & Feature Engineering
**📆 3–9 Mart 2026**

### Hedefler
Veri setlerini birleştirmek, temizlemek ve ML modeline girdi olacak feature'ları oluşturmak.

### Görevler

| # | Görev | Sorumlu | Çıktı |
|---|-------|---------|-------|
| 1.1 | Kaggle DDI + TWOSIDES veri birleştirme (ortak ilaçlar üzerinden) | ML | `data/processed/merged_ddi.csv` |
| 1.2 | Etkileşim açıklamalarından NLP ile label çıkarma (increase / decrease / risk / contraindication) | ML | `data/processed/labeled_interactions.csv` |
| 1.3 | Label dağılımı analizi ve dengesizlik kontrolü | ML | Analiz raporu |
| 1.4 | DrugBank Vocabulary indirme (Open Data, ücretsiz) → ilaç isim standardizasyonu | ML + BE | `data/raw/drugbank_vocabulary.csv` |
| 1.5 | EDA görselleştirmelerini tamamlama (plotlar, grafikler) | FE | `notebooks/01_eda_visualizations.ipynb` |
| 1.6 | Backend proje altyapısını kurma (FastAPI boilerplate, proje yapısı) | BE | `src/api/` dizini |
| 1.7 | Frontend teknoloji seçimi ve proje oluşturma | FE | `frontend/` dizini |

### Hafta Sonu Kontrol Noktası ✅
- [ ] Birleştirilmiş veri seti hazır mı?
- [ ] Label'lar başarıyla çıkarıldı mı?
- [ ] Backend ve frontend iskeletleri çalışıyor mu?

---

## 🗓️ Hafta 2 — Model Geliştirme (Baseline)
**📆 10–16 Mart 2026**

### Hedefler
İlk ML modelini eğitmek, baseline performans metriklerini elde etmek.

### Görevler

| # | Görev | Sorumlu | Çıktı |
|---|-------|---------|-------|
| 2.1 | Feature engineering: TF-IDF veya Word2Vec ile etkileşim açıklamalarından feature çıkarma | ML | `src/feature_engineering.py` |
| 2.2 | Train/test split (%80/%20 stratified) | ML | Bölünmüş veri setleri |
| 2.3 | XGBoost baseline modeli eğitimi | ML | `models/xgboost_baseline.pkl` |
| 2.4 | Random Forest modeli eğitimi (karşılaştırma için) | ML | `models/random_forest.pkl` |
| 2.5 | Model değerlendirme: Accuracy, F1-Score, Precision, Recall, Confusion Matrix | ML | `reports/model_comparison.md` |
| 2.6 | API endpoint tasarımı (route yapısı, request/response şemaları) | BE | API dokümantasyonu |
| 2.7 | Frontend ana sayfa ve ilaç giriş formu tasarımı (UI/UX mockup) | FE | Figma/HTML prototipi |

### Hafta Sonu Kontrol Noktası ✅
- [ ] En az 1 model çalışır durumda mı?
- [ ] Baseline metrikler raporlandı mı?
- [ ] API endpoint yapısı belirlendi mi?

---

## 🗓️ Hafta 3 — Model Optimizasyonu & API Geliştirme
**📆 17–23 Mart 2026**

### Hedefler
Modeli iyileştirmek, API'yi çalışır hale getirmek, frontend'i backend'e bağlamak.

### Görevler

| # | Görev | Sorumlu | Çıktı |
|---|-------|---------|-------|
| 3.1 | Hyperparameter tuning (GridSearch / RandomSearch) | ML | Optimize edilmiş model |
| 3.2 | Cross-validation (5-fold) ile model güvenilirliğini doğrulama | ML | CV sonuçları |
| 3.3 | (Opsiyonel) SMILES/fingerprint tabanlı ek feature'lar ekleme | ML | Güncellenmiş feature seti |
| 3.4 | DDInter veri seti ile model çıktısını doğrulama | ML | Doğrulama raporu |
| 3.5 | FastAPI endpoint'lerini kodlama: `/predict`, `/drug-info`, `/health` | BE | Çalışan API |
| 3.6 | Model'i API'ye entegre etme (model yükleme + tahmin servisi) | BE + ML | `src/api/predict.py` |
| 3.7 | Frontend → Backend API bağlantısı (fetch/axios ile) | FE + BE | Çalışan iletişim |
| 3.8 | İlaç ismi autocomplete özelliği (1.701 ilaç listesinden) | FE | Autocomplete componenti |

### Hafta Sonu Kontrol Noktası ✅
- [ ] Optimize edilmiş model baseline'dan daha iyi mi?
- [ ] API'ye istek atıldığında doğru tahmin dönüyor mu?
- [ ] Frontend'den API'ye uçtan uca bağlantı çalışıyor mu?

---

## 🗓️ Hafta 4 — Entegrasyon & UI Tamamlama
**📆 24–30 Mart 2026**

### Hedefler
Tüm parçaları birleştirmek, kullanıcı deneyimini olgunlaştırmak, hataları gidermek.

### Görevler

| # | Görev | Sorumlu | Çıktı |
|---|-------|---------|-------|
| 4.1 | Sonuç sayfası tasarımı: etkileşim türü, risk seviyesi, açıklama gösterimi | FE | Sonuç sayfası UI |
| 4.2 | Risk seviyesi görselleştirme (renk kodlu: 🟢 düşük / 🟡 orta / 🔴 yüksek) | FE | Risk göstergesi componenti |
| 4.3 | Çoklu ilaç girişi desteği (2+ ilaç kombinasyonu) | BE + FE | Genişletilmiş form |
| 4.4 | Yan etki bilgisi gösterimi (TWOSIDES verisinden) | BE + FE | Yan etki paneli |
| 4.5 | Hata yönetimi: bilinmeyen ilaç, API hataları, edge case'ler | BE + FE | Error handling |
| 4.6 | Responsive tasarım (mobil uyumluluk) | FE | Responsive CSS |
| 4.7 | API rate limiting ve input validation | BE | Güvenlik katmanı |
| 4.8 | Uçtan uca (E2E) test senaryoları yazma | Herkes | Test dosyaları |

### Hafta Sonu Kontrol Noktası ✅
- [ ] Uygulama uçtan uca çalışıyor mu?
- [ ] Mobil ve desktop'ta düzgün görünüyor mu?
- [ ] Edge case'ler handle ediliyor mu?

---

## 🗓️ Hafta 5 — Test, Dokümantasyon & Sunum
**📆 31 Mart – 6 Nisan 2026**

### Hedefler
Son testleri yapmak, rapor ve sunumu hazırlamak, projeyi teslime hazır hale getirmek.

### Görevler

| # | Görev | Sorumlu | Çıktı |
|---|-------|---------|-------|
| 5.1 | Kapsamlı test: bilinen ilaç etkileşimleri ile doğrulama | Herkes | Test raporu |
| 5.2 | Performans testi (API yanıt süresi, model inference time) | BE | Performans raporu |
| 5.3 | Model performans raporu (final metrikler, grafikler, confusion matrix) | ML | `reports/final_model_report.md` |
| 5.4 | Proje raporu yazımı (giriş, yöntem, sonuçlar, tartışma) | Herkes | Proje raporu (PDF/Word) |
| 5.5 | Sunum slaytları hazırlama | Herkes | PowerPoint/Google Slides |
| 5.6 | Demo videosu kaydetme (opsiyonel) | FE | Demo video |
| 5.7 | GitHub README güncelleme (kurulum, kullanım, ekran görüntüleri) | BE | Güncel README.md |
| 5.8 | Kod temizliği, yorum ekleme, son push | Herkes | Temiz GitHub repo |

### Hafta Sonu Kontrol Noktası ✅
- [ ] Rapor tamamlandı mı?
- [ ] Sunum hazır mı?
- [ ] GitHub repo'su temiz ve güncel mi?
- [ ] Demo çalışıyor mu?

---

## 📊 Genel Zaman Çizelgesi

```
Hafta 1  ██████████████████████████░░░░  Veri Hazırlama & Feature Engineering
Hafta 2  ░░░░░██████████████████████░░░  Model Geliştirme (Baseline)
Hafta 3  ░░░░░░░░░██████████████████░░  Model Optimizasyonu & API
Hafta 4  ░░░░░░░░░░░░░░██████████████  Entegrasyon & UI Tamamlama
Hafta 5  ░░░░░░░░░░░░░░░░░░██████████  Test, Dokümantasyon & Sunum
         ─────────────────────────────
         ML ████  BE ████  FE ████  Herkes ████
```

---

## ⚠️ Riskler ve Önlemler

| Risk | Etki | Önlem |
|------|------|-------|
| Model performansı düşük kalabilir | Proje kalitesi düşer | Hafta 2'de birden fazla model dene, en iyisini seç |
| TWOSIDES verisi çok büyük | İşleme süresi uzar | Filtrelenmiş alt küme kullan (en sık ilaçlar) |
| İlaç isim eşleşme sorunu | Veri birleştirme başarısız olur | DrugBank Vocabulary ile standardizasyon yap |
| API yanıt süresi yavaş | Kullanıcı deneyimi kötü | Model cache + hafif model seç |
| Ekip üyesi gecikmeleri | Takvim kayar | Haftalık checkpoint toplantıları yap |

---

## 💡 Başarı Kriterleri

| Kriter | Hedef |
|--------|-------|
| Model accuracy | ≥ %85 |
| Model F1-score | ≥ %80 |
| API yanıt süresi | < 500ms |
| Desteklenen ilaç sayısı | 1.700+ |
| Web arayüzü | Responsive, kullanıcı dostu |
| Dokümantasyon | README + Proje raporu + Sunum |

---

*Son güncelleme: 27 Şubat 2026*
