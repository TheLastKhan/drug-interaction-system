# 💊 İlaç Etkileşim Uyarı Sistemi — Proje Özet Raporu
**Tarih:** 16 Şubat 2026  
**Durum:** Veri seti analizi tamamlandı, ML modeli aşamasına hazır

---

## 📌 Proje Nedir?
Kullanıcıların aldığı ilaçların birbirleriyle etkileşimini (drug-drug interaction) tespit eden,
risk seviyesini gösteren ve uyarı veren bir makine öğrenmesi projesi.

**Kullanım senaryosu:** Kullanıcı 2 ilaç adı girer → Sistem etkileşim riskini gösterir

---

## 📊 Kullanılacak Veri Setleri

### 1. Kaggle DDI (Ana Veri Seti) ✅ İNDİRİLDİ VE ANALİZ EDİLDİ
- **Kaynak:** https://www.kaggle.com/datasets/mghobashy/drug-drug-interactions
- **Lisans:** Apache 2.0 (ücretsiz)
- **Boyut:** 22 MB
- **İçerik:** DrugBank veritabanından türetilmiş ilaç-ilaç etkileşimleri

| Metrik | Değer |
|--------|-------|
| Toplam etkileşim kaydı | 191,541 |
| Benzersiz ilaç sayısı | 1,701 |
| Benzersiz ilaç çifti | 191,135 |
| Sütunlar | Drug 1, Drug 2, Interaction Description |
| Null/eksik değer | 0 (sıfır) |

**Etkileşim Türleri (Anahtar Kelime Analizi):**
- %67.8 → "increase" (bir ilacın etkisini artırma)
- %32.0 → "decrease" (bir ilacın etkisini azaltma)
- %32.1 → "risk" (risk artışı)
- %31.8 → "adverse" (yan etki)
- %20.5 → "metabolism" (metabolizma etkisi)
- %18.3 → "serum concentration" (kan seviyesi değişimi)

**En Çok Etkileşime Giren 10 İlaç:**
1. Phenobarbital — 858 etkileşim
2. Pentobarbital — 820
3. Carbamazepine — 800
4. Primidone — 765
5. Phenytoin — 752
6. Rifampicin — 736
7. Fosphenytoin — 734
8. Rifapentine — 704
9. Rifabutin — 625
10. Dabrafenib — 615

**Örnek Veri:**
```
Drug 1: Trioxsalen
Drug 2: Verteporfin
Interaction: "Trioxsalen may increase the photosensitizing activities of Verteporfin."
```

---

### 2. TWOSIDES (Zenginleştirme Verisi) ✅ İNDİRİLDİ VE ANALİZ EDİLDİ
- **Kaynak:** https://tatonettilab.org/offsides/
- **Lisans:** Akademik kullanım, ücretsiz
- **Boyut:** 738 MB (sıkıştırılmış)
- **İçerik:** FDA Adverse Event Reporting System'dan ilaç çifti + yan etki verileri

| Metrik | Değer (500K satırlık örneklem) |
|--------|------|
| Benzersiz ilaç | 1,145 |
| Benzersiz yan etki/koşul | 7,836 |
| Sütun sayısı | 13 |
| PRR (risk skoru) ortalaması | 7.02 |
| PRR medyanı | 5.0 |
| PRR max | 960.0 |

**TWOSIDES Sütunları:**
- drug_1_concept_name, drug_2_concept_name (ilaç isimleri)
- condition_concept_name (yan etki adı, ör: Nausea, Headache)
- PRR (Proportional Reporting Ratio — risk skoru)
- A, B, C, D (istatistiksel sayılar)
- mean_reporting_frequency

**En Sık Yan Etkiler:**
1. Nausea (Bulantı) — 1,893
2. Diarrhoea (İshal) — 1,842
3. Dyspnoea (Nefes Darlığı) — 1,835
4. Vomiting (Kusma) — 1,776
5. Fatigue (Yorgunluk) — 1,719

**En Çok Etkileşen İlaçlar (TWOSIDES):**
1. Aspirin — 16,394
2. Oxycodone — 9,828
3. Amlodipine — 9,653
4. Lisinopril — 8,221
5. Warfarin — 5,881

---

### 3. DDInter (Doğrulama Verisi) ⏳ HENÜZ İNDİRİLMEDİ
- **Kaynak:** https://ddinter.scbdd.com/
- **İçerik:** ATC kodlarına göre kategorize edilmiş DDI'lar + risk seviyeleri
- **Kullanım:** Model çıktısını doğrulamak için referans

---

## ❌ Elenen Veri Setleri
| Veri Seti | Neden Elendi |
|-----------|-------------|
| ujjwalaggarwal402 Medicine | Sentetik veri, etkileşim bilgisi yok |
| snowyowl22 Pharmacy | Sadece 2.9 KB, eczane yönetim verisi |
| hugoya DDI | Dokümantasyonu yok, güvenilirliği belirsiz |

---

## 🛠️ Teknik Detaylar

**Proje Dizini:** `drug-interaction-system/`
```
drug-interaction-system/
├── data/raw/
│   ├── db_drug_interactions.csv   (22 MB - Kaggle DDI)
│   └── TWOSIDES.csv.gz            (738 MB - TWOSIDES)
├── data/processed/
│   ├── kaggle_ddi_stats.json      (analiz sonuçları)
│   └── twosides_stats.json        (analiz sonuçları)
├── src/
│   ├── analyze_kaggle_ddi.py
│   └── analyze_twosides.py
├── notebooks/
├── requirements.txt
└── README.md
```

**Gereksinimler:** Python 3.10+
```
pandas, numpy, matplotlib, seaborn, scikit-learn, kaggle, jupyter
```

---

## 📋 Yapılacaklar (Roadmap)

- [x] Veri seti araştırması ve seçimi
- [x] Proje yapısı oluşturma
- [x] Veri setlerini indirme
- [x] Keşifsel Veri Analizi (EDA)
- [ ] Grafik/görselleştirmeler
- [ ] İki veri setini birleştirme (ortak ilaçlar üzerinden)
- [ ] ML modeli için feature engineering
- [ ] Model eğitimi (XGBoost baseline)
- [ ] (Opsiyonel) GNN modeli ile karşılaştırma
- [ ] Web arayüzü (FastAPI + Frontend)
- [ ] Test ve doğrulama
- [ ] Proje raporu ve sunum

---

## 👥 Önerilen İş Bölümü (3 kişi)
| Kişi | Sorumluluk |
|------|-----------|
| Kişi 1 (ML) | Veri ön işleme, model eğitimi, optimizasyon |
| Kişi 2 (Backend) | FastAPI API, veritabanı, model entegrasyonu |
| Kişi 3 (Frontend) | Web arayüzü, görselleştirme, UX tasarımı |
