# Bitirme Projesi Teklifi
## Makine Öğrenmesi ile İlaç-İlaç Etkileşim Tahmin ve Uyarı Sistemi

### Proje Amacı

Birden fazla ilaç kullanan hastaların karşılaşabileceği ilaç-ilaç etkileşimlerini (Drug-Drug Interaction — DDI) makine öğrenmesi yöntemleri ile tahmin eden ve kullanıcıyı uyaran bir karar destek sistemi geliştirilmesi amaçlanmaktadır.

Sistem, kullanıcının girdiği iki veya daha fazla ilaç arasındaki olası etkileşimleri tespit edecek, etkileşim türünü sınıflandıracak ve risk seviyesini belirleyerek kullanıcıya anlaşılır bir uyarı sunacaktır.

### Problemin Önemi

Polifarmasi (çoklu ilaç kullanımı) özellikle yaşlı ve kronik hastalığı olan bireylerde yaygın bir durumdur. Dünya Sağlık Örgütü verilerine göre, hastaneye yatışların önemli bir bölümü ilaç etkileşimlerinden kaynaklanan advers (istenmeyen) etkilerden kaynaklanmaktadır. Bu projede geliştirilecek sistem, sağlık profesyonellerine ve hastalara karar desteği sağlayarak bu riski azaltmayı hedeflemektedir.

### Veri Kaynakları

Proje kapsamında aşağıdaki açık erişimli ve ücretsiz veri setleri kullanılacaktır:

1. **DrugBank DDI Veri Seti (Kaggle):** 191.541 ilaç etkileşim kaydı, 1.701 benzersiz ilaç. Her kayıt ilaç çifti ve etkileşim açıklamasını içermektedir. (Kaynak: TDCommons / DrugBank)

2. **TWOSIDES (Tatonetti Lab, Columbia University):** FDA'nın Adverse Event Reporting System'ından (FAERS) elde edilen 3.300+ ilaç ve 63.000 kombinasyona ait yan etki verileri. İstatistiksel anlamlılık gösteren PRR (Proportional Reporting Ratio) risk skorlarını içermektedir.

### Yöntem

- **Veri Ön İşleme:** Etkileşim açıklamalarından NLP yöntemleri ile etkileşim türü etiketi çıkarılması (artırma / azaltma / kontrendikasyon / risk)
- **Öznitelik Mühendisliği:** İlaç çiftlerinden öznitelik vektörlerinin oluşturulması
- **Model Eğitimi:** XGBoost ve/veya Random Forest ile etkileşim tahmini
- **Değerlendirme:** Accuracy, F1-Score, Precision, Recall metrikleri ile model performansının ölçülmesi
- **Web Arayüzü:** FastAPI (Backend) ve modern bir frontend (React veya düz HTML/JS) ile kullanıcı dostu bir uyarı sistemi arayüzü

### Beklenen Çıktılar

1. Eğitilmiş bir ML modeli (etkileşim tahmini + risk sınıflandırması)
2. Web tabanlı kullanıcı arayüzü (ilaç adı girişi → etkileşim uyarısı)
3. Performans analiz raporu (model karşılaştırmaları)

### Zaman Planı

| Dönem | Çalışma |
|-------|---------|
| Şubat — Mart | Veri ön işleme, temizleme, öznitelik çıkarımı |
| Mart — Nisan | Model eğitimi ve optimizasyonu |
| Nisan — Mayıs | Web arayüzü geliştirme ve entegrasyon |
| Mayıs — Haziran | Test, doğrulama, rapor ve sunum hazırlığı |

---

*Bu proje, yazılım mühendisliği ve veri bilimi disiplinlerini birleştiren, gerçek dünya verilerine dayalı, uygulanabilir bir çözüm sunmayı hedeflemektedir.*
