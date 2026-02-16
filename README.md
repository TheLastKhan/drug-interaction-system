# İlaç Etkileşim Uyarı Sistemi (Drug Interaction Warning System)

Makine öğrenmesi ile ilaç-ilaç etkileşimlerini tahmin eden ve kullanıcıyı uyaran bir sistem.

## Veri Kaynakları
- **Kaggle DDI (MGhobashy)** — DrugBank'tan türetilmiş 191K etkileşim kaydı
- **TWOSIDES** — FDA Adverse Event Reporting System'dan 3,300+ ilaç, 63,000 kombinasyon
- **DDInter** — Risk seviyeli etkileşim veritabanı

## Kurulum
```bash
pip install -r requirements.txt
```

## Proje Yapısı
```
drug-interaction-system/
├── data/raw/           # Ham veri setleri
├── data/processed/     # Temizlenmiş veri
├── notebooks/          # Jupyter EDA notebook'ları
├── src/                # Kaynak kod
└── requirements.txt
```
