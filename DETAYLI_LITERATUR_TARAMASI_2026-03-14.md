# İlaç Etkileşim Uyarı Sistemi İçin Detaylı Literatür Taraması

**Tarih:** 14 Mart 2026
**Proje bağlamı:** DrugBank/Kaggle DDI + TWOSIDES + ileride DDInter doğrulaması + açıklanabilir ve ürünleşebilir bir uyarı sistemi
**Amaç:** Projeyi güncel literatüre göre konumlandırmak, güçlü ve zayıf yanları belirlemek, özgünleşme ve iyileştirme fırsatlarını somutlaştırmak

## 1. Kapsam ve Yöntem

Bu rapor, senin paylaştığın üç arama yönünü temel aldı:

- Web of Science
- arXiv
- Google Scholar

Ancak önemli bir metodolojik not var:

- Web of Science özet sayfaları ve Google Scholar sonuç sayfaları indeks/arama kapılarıdır; bunlar doğrudan akademik birincil kaynak gibi kullanılmaya uygun değildir.
- Bu nedenle bu raporda, o arama kapılarından ulaşılabilecek **birincil kaynaklar** kullanıldı:
  - PubMed
  - Nature / npj
  - Oxford Academic
  - ACS
  - Springer
  - Science / PNAS / PMC
  - NLM resmi teknik kaynakları
  - arXiv tabanlı güncel benchmark/dataset kayıtları

Kullandığım genişletilmiş anahtar kelimeler:

- `drug-drug interaction prediction`
- `emerging DDI prediction`
- `distribution shift drug interaction`
- `DDI severity classification`
- `DrugBank 6.0`
- `DDInter 2.0`
- `TWOSIDES`
- `higher-order drug-drug interactions`
- `DDI explainability`
- `DDI large language models`
- `RxNorm drug normalization`

## 2. Repo Bağlamından Çıkan Proje Konumu

Repo incelemesine göre projenin şu omurgası var:

- Veri kaynağı olarak DrugBank türevi Kaggle DDI kullanılıyor.
- Yan etki/risk zenginleştirmesi için TWOSIDES kullanılıyor.
- DDInter doğrulama kaynağı olarak düşünülmüş.
- `SCRUM-4` kapsamında DrugBank vocabulary ile ilaç adı standardizasyonu hedefleniyor.
- Ürün hedefi yalnızca model eğitmek değil; FastAPI + frontend ile kullanıcıya uyarı veren bir sistem üretmek.

Bu nokta çok önemli: Literatürdeki birçok çalışma yalnızca `prediction benchmark` iken, sizin projeniz potansiyel olarak `clinical-style decision support prototype` yönüne gidiyor. Bu, doğru yönetilirse sizi sıradan bir akademik denemeden ayırabilir.

## 3. 2026'dan Geriye Doğru Literatür Haritası

## 3.1. 2026: Literatürün Şu An Geldiği Yer

### 3.1.1. Klinik uygulanabilirlik, açıklanabilirlik ve genellenebilirlik artık merkezde

Lu ve arkadaşlarının **npj Digital Medicine** dergisinde 29 Ocak 2026'da yayımlanan derleme makalesi, alanın yeni yönünü çok net özetliyor: yalnızca yüksek skor üreten model yetmiyor; modelin klinik iş akışına entegre olması, yorumlanabilir olması ve yeni senaryolara genellenebilmesi gerekiyor.

Bu makaleden proje için çıkan en önemli dersler:

- DDI problemi sadece modelleme problemi değil, klinik karar desteği problemidir.
- Yorumlanabilirlik artık "ekstra özellik" değil, klinik güven için zorunlu katmandır.
- Veri heterojenliği büyüdükçe model karmaşıklığı artıyor; ama bu artış otomatik olarak klinik değer üretmiyor.

Bu sizin proje için çok iyi haber, çünkü siz zaten:

- açıklama metni,
- risk seviyesi,
- kullanıcıya gösterilebilir uyarı,
- veri standardizasyonu

gibi ürünleşmeye yakın bileşenleri düşünüyorsunuz.

### 3.1.2. Çok karmaşık model her zaman kazanmaz

Gil-Sorribes ve Molina'nın 19 Şubat 2026 tarihli **Journal of Cheminformatics** makalesi özellikle önemli. Çalışma, giderek daha karmaşık GNN/Transformer tabanlı sistemlerin her koşulda anlamlı üstünlük getirmediğini gösteriyor. Leak-proof DrugBank split'lerinde Morgan fingerprint + sığ sınıflandırıcıların çok daha karmaşık sistemleri yakalayabildiği veya geçebildiği; asıl kırılmanın out-of-distribution ve scaffold tabanlı daha zor senaryolarda ortaya çıktığı gösteriliyor.

Bu makaleden senin proje için çok kritik sonuçlar çıkıyor:

- İlk üretimsel baseline için XGBoost / Random Forest / sığ DNN seçmek yanlış değil.
- Veri standardizasyonu ve split tasarımı, model kompleksliğinden daha kritik olabilir.
- "Basit ama güvenilir ve açıklanabilir" yaklaşımı güncel literatür tarafından destekleniyor.

Bu, düşük modellerle yaptığın önceki denemelerin yetersiz hissettirmiş olmasını da açıklıyor olabilir: sorun model boyutu değil, veri kontratı ve deney tasarımı da olabilir.

## 3.2. 2025: En Güçlü Tema Dağılımı

### 3.2.1. DDI-Ben: gerçek hayata yakın değerlendirme ihtiyacı

Shen ve arkadaşlarının 14 Ekim 2025 tarihli **Bioinformatics** makalesi olan **DDI-Ben**, yeni ilaçlar geldiğinde model performansının ciddi düştüğünü gösteren çok önemli bir benchmark çerçevesi sunuyor. Ana mesaj şu:

- Rastgele train/test split, gerçek dünyayı iyi temsil etmiyor.
- Bilinen ilaçlar ile görülmemiş/yeni ilaçlar arasında dağılım kayması var.
- Var olan birçok yöntem bu dağılım kayması altında ciddi performans kaybediyor.

Bu sizin proje açısından şu anlama geliyor:

- Eğer yalnızca klasik random split yaparsanız, model gerçekte olduğundan daha iyi görünebilir.
- Projeyi güçlendirmek için en az iki değerlendirme senaryosu kurmalısınız:
  - random split
  - unseen-drug veya emerging-drug split

Bu öneri, projeyi literatüre göre bir anda daha ciddi hale getirir.

### 3.2.2. Yönlülük ve serbest metin açıklamalarının yapısallaştırılması artık önemli

Feng ve Huang'ın 2025 tarihli **Journal of Biomedical Informatics** makalesi, serbest metin DDI açıklamalarını GPT-4o ile yapılandırılmış tripletlere dönüştürüp yönlülüğü modele dahil ediyor. Aynı çalışma, sınıf dengesizliğini SMOTE ile ele alıyor.

Bu makaleden sizin proje için çıkan güçlü dersler:

- DrugBank açıklama cümlelerini sadece düz metin olarak bırakmak yerine yapısallaştırmak çok değerli.
- `A ilacı B'nin metabolizmasını artırır/azaltır` gibi yönlü ilişkiler klinik olarak daha anlamlıdır.
- Senin `increase / decrease / risk / contraindication` label yaklaşımın doğru yöne bakıyor, ama daha ince granüler hale getirilebilir.

Bu yüzden projenin mevcut label planı literatürle uyumlu, fakat şu an hâlâ nispeten kaba bir seviye:

- `increase`
- `decrease`
- `risk`
- `contraindication`

Bir sonraki olgunluk seviyesi ise şu olur:

- mekanizma ailesi
- yönlülük
- etki alanı
- şiddet/risk seviyesi

### 3.2.3. Sınıf dengesizliği artık merkezi bir konu

Xie ve arkadaşlarının **DDintensity** çalışması (2025, *Artificial Intelligence in Medicine*), özellikle risk seviyesi sınıflarındaki dengesizliğe odaklanıyor. Çalışmada DDInter üzerinden risk seviyesi verisi kullanılıyor ve BioGPT tabanlı embedding'lerin bu tip problemde iyi performans verdiği gösteriliyor.

Bu sizin proje için iki açıdan çok önemli:

1. `SCRUM-2` ve sonraki modelleme adımlarında sınıf dengesizliği mutlaka izlenmeli.
2. Risk seviyesi tahmini istiyorsanız DDInter doğrulaması "opsiyonel ekstra" değil, proje kalitesini ciddi artıran bir katman.

### 3.2.4. Küçük ama alan-özel dil modelleri de güçlü olabilir

Ibrahim ve arkadaşlarının 2025 tarihli **D3** makalesi, yaklaşık 70 milyon parametreli küçük bir modelin, çok daha büyük LLM'lerle DDI tahmini üzerinde rekabet edebildiğini gösteriyor.

Bunun proje açısından anlamı şu:

- Her yerde büyük LLM zorunlu değil.
- Alan-özel, görev-özel, daha hafif çözümler hem maliyet hem deploy açısından avantajlı olabilir.
- Sizdeki ürün hedefi düşünüldüğünde bu daha da değerli.

Yani nihai sistemde LLM'i doğrudan son karar verici yapmaktan ziyade:

- etiketleme yardımı,
- açıklama üretimi,
- mekanizma özetleme,
- serbest metin yapılandırma

gibi yardımcı rollerde kullanmak daha sağlam bir strateji olur.

### 3.2.5. Biyomedikal literatürden metin embedding ile açıklanabilir DDI tahmini

Jung ve Yoo'nun 2025 tarihli **Computers in Biology and Medicine** makalesi, biyomedikal literatür tabanlı metin embedding ile 164 DDI tipi üzerinde güçlü sonuçlar gösteriyor. Hiyerarşik attention sayesinde modelin hangi cümleleri önemsediği de kısmen izlenebiliyor.

Bu, sizin proje için çok kritik çünkü sizde zaten metin merkezli bir damar var:

- DrugBank interaction description
- açıklama tabanlı label çıkarma
- kullanıcıya açıklanabilir sonuç dönme ihtiyacı

Yani literatür açıkça şunu söylüyor:

- Metin sadece "yan veri" değil, doğrudan ana bilgi kaynağı olabilir.

### 3.2.6. DDInter 2.0 artık çok daha güçlü bir doğrulama ve ürün kaynağı

Tian ve arkadaşlarının **DDInter 2.0** makalesi (Nucleic Acids Research, 2025), veritabanının 2310 ilaç, 302,516 DDI kaydı ve 8398 yüksek kaliteli mekanizma/yönetim açıklamasına ulaştığını gösteriyor. Ayrıca:

- drug-food interaction
- drug-disease interaction
- therapeutic duplication

katmanları da eklenmiş durumda.

Bu kaynak size üç büyük avantaj sunabilir:

1. **Doğrulama:** Modelinizin bazı çıktılarını DDInter ile çapraz kontrol edebilirsiniz.
2. **Risk seviyesi:** mild / moderate / severe tarzı daha klinik bir risk katmanı kurabilirsiniz.
3. **Arayüz tasarımı:** DDInter 2.0'ın filtreleme mantığı ve alert-fatigue azaltma yaklaşımı, kendi frontend/backend tasarımınıza ilham verebilir.

Özellikle şu detay önemli:

- DDInter 2.0, bilinmeyen mekanizmalı bazı etkileşimleri dışarıda bırakarak alert fatigue'i azaltmayı hedefliyor.

Bu, sizin sistem için çok güçlü bir ürün ilkesi olabilir:

- Her interaction'ı aynı sertlikte göstermemek
- Belirsizlik / güven seviyesi göstermek
- Klinik olarak daha anlamlı filtreleme sunmak

### 3.2.7. Çoklu ilaç kombinasyonları (2+ ilaç) literatürde ayrı bir frontier

2025 tarihli **HODDI** veri seti çalışması, TWOSIDES gibi kaynakların çoğunlukla ikili etkileşimlere odaklandığını; oysa gerçek hayatta daha yüksek dereceli kombinasyonların kritik olduğunu vurguluyor.

Bu, sizin sprint planınızdaki `2+ ilaç kombinasyonu` maddesi için çok değerli:

- Çoklu ilaç desteği literatürde gerçekten güncel bir problem.
- Ama bunu doğrudan mevcut pairwise modelin üzerine "kolay ek özellik" gibi koymak yeterli olmayabilir.
- Pairwise ve higher-order problem ayrımını net yapmak gerekir.

Kısa sonuç:

- Çoklu ilaç desteği iyi bir özgünlük alanı.
- Ama bunu ayrı araştırma fazı gibi konumlandırmak daha doğru olur.

### 3.2.8. LLM'ler umut verici ama şu an güvenilir nihai hakem değiller

2025 sonu ve 2024 literatüründe LLM kullanan DDI çalışmalarında ikili bir tablo var:

- Bazı dar görevlerde çok iyi performans var.
- Ama daha karmaşık çoklu ilaç akıl yürütmesinde ve risk derecelendirmesinde tutarlılık sorunu sürüyor.

Özellikle iki önemli bulgu var:

- `Drug-drug interaction identification using large language models` ön baskısı, görev karmaşıklığı arttıkça self-consistency'nin düştüğünü gösteriyor.
- OTC/herbal risk sınıflandırması üzerine çalışma, GPT tabanlı modellerin hazır şekilde risk puanlama için güvenilir olmadığını gösteriyor.

Bu nedenle önerim çok net:

- LLM'i **yardımcı bilgi çıkarıcı** olarak kullan
- Nihai risk kararını **referans veri + klasik model + kural** hibritiyle ver

Bu yaklaşım hem daha güvenli, hem ürün açısından daha savunulabilir.

## 3.3. 2024: Veri tabanları, yorumlanabilirlik ve görev sınıfları netleşiyor

### 3.3.1. DrugBank 6.0 veri büyüklüğünü dramatik biçimde artırdı

Knox ve arkadaşlarının **DrugBank 6.0** makalesi (Nucleic Acids Research, 2024), DrugBank'in artık çok daha geniş kapsamlı bir bilgi tabanına dönüştüğünü gösteriyor. Makalede:

- DDI sayısının 365,984'ten 1,413,413'e çıktığı
- drug-food interaction sayısının ciddi arttığı
- açık erişimli `DrugBank Vocabulary` setinin bulunduğu

belirtiliyor.

Bu, `SCRUM-4 vocabulary` işinin neden stratejik olduğunu doğruluyor:

- İlaç isim standardizasyonu literatürde yan görev değil, veri entegrasyonunun temelidir.
- DrugBank vocabulary'yi iyi kullanmak, Kaggle DDI ve TWOSIDES eşleştirmesini güçlendirir.

### 3.3.2. Alanın genel taksonomisi artık daha net

Zhang ve arkadaşlarının **Application of Artificial Intelligence in Drug-Drug Interactions Prediction: A Review** makalesi, DDI tahminini üç ana sınıfa ayırıyor:

- undirected DDI prediction
- DDI event prediction
- asymmetric DDI prediction

Bu sınıflandırmayı sizin projeye çevirirsek:

- Şu anki temel planınız `event/risk-oriented` bir hatta daha yakın.
- Eğer yönlülüğü eklerseniz `asymmetric DDI prediction` çizgisine yaklaşmış olursunuz.

Bu, proje sunumunda kullanılabilecek çok güzel bir akademik çerçeve sağlar.

### 3.3.3. Knowledge graph tabanlı açıklanabilirlik güçlü rakiplerden biri

Wang ve arkadaşlarının **KnowDDI** makalesi (Communications Medicine, 2024), knowledge graph ve knowledge subgraph mantığıyla hem güçlü performans hem de açıklanabilir reasoning path üretmeye çalışıyor.

Bu makalenin önemi:

- Sadece tahmin değil, `neden` sorusuna da cevap vermeye çalışıyor.
- Veri seyrek olduğunda dış bilgi grafikleri yardımcı olabiliyor.

Sizin proje açısından çıkarım:

- Eğer ileride projeyi büyütmek isterseniz; targets, enzymes, transporters, pathways gibi DrugBank alanları knowledge-graph benzeri ikinci faz için çok iyi aday.
- Ama ilk fazda bunu zorunlu yapmak gerekmez.

## 3.4. Tarihsel omurga: bugünkü alanı kuran eski ama kritik çalışmalar

### 3.4.1. DeepDDI (2018)

Ryu ve arkadaşlarının **PNAS 2018** çalışması, DDI tahmininde hâlâ referans alınan dönüm noktalarından biri. 86 DDI tipini insan-okunur cümleler olarak üretmesi özellikle önemliydi.

Bu makalenin projenize etkisi:

- Sadece `interaction var/yok` demek yerine etkileşim tipini cümle seviyesinde açıklamak çok değerli.
- Sizin kullanıcıya açıklama dönen ürün hedefiniz, bu geleneğin daha pratik/ürünleşmiş versiyonuna dönüşebilir.

### 3.4.2. TWOSIDES'in kökeni (2012)

Tatonetti ve arkadaşlarının **Science Translational Medicine 2012** makalesi, TWOSIDES/Offsides hattının temelini kuruyor. FAERS tabanlı veri madenciliğiyle yeni yan etki ve etkileşimleri ayıklamaya çalışıyor; EMR ile bazı bulguları da doğruluyor.

Bu, sizin TWOSIDES kullanımınızı çok güçlü biçimde meşrulaştırıyor:

- TWOSIDES rastgele bir CSV değil.
- Alanın tarihsel olarak önemli kaynaklarından biri.
- Ama aynı zamanda observasyonel veri doğası gereği gürültü ve confounding riski taşıyor.

Dolayısıyla TWOSIDES'i:

- saf ground-truth gibi değil,
- risk zenginleştirici sinyal kaynağı gibi

kullanmak daha doğru olur.

## 4. Literatüre Göre Sizin Projenizin Güçlü Yanları

## 4.1. Veri seçimi genel olarak doğru

DrugBank/Kaggle + TWOSIDES + ileride DDInter doğrulaması kombinasyonu, literatürdeki en mantıklı hibritlerden biri:

- DrugBank açıklayıcı ve mekanistik
- TWOSIDES daha gerçek dünya yan etki/risk sinyali veriyor
- DDInter daha klinik risk ve yönetim yönü taşıyor

Bu üçlü, tek veri setine yaslanan projelere göre daha olgun bir mimari olabilir.

## 4.2. Açıklanabilir ürün hedefi büyük avantaj

Birçok makale yüksek skor gösterip orada bitiyor. Siz ise:

- açıklama,
- risk,
- uyarı,
- kullanıcı arayüzü,
- çoklu ilaç desteği

gibi ürün boyutlarını düşünüyorsunuz.

Bu, doğru uygulanırsa projenin özgün yanlarından biri olur.

## 4.3. SCRUM-4 işi stratejik bir iş

Drug name normalization sıradan bir temizlik işi gibi görünse de, aslında:

- merge kalitesini,
- label kalitesini,
- autocomplete kalitesini,
- kullanıcı giriş doğruluğunu,
- değerlendirme tutarlılığını

etkiliyor.

Yani senin üstlendiğin kısım gerçekten kritik.

## 4.4. Basit modelle başlama kararı literatürce destekleniyor

2026 ve 2025 literatürü gösteriyor ki:

- her zaman en büyük model en iyi strateji değil
- açıklanabilir ve veri-disiplini güçlü baseline çoğu zaman daha iyi başlangıç

Bu nedenle:

- XGBoost
- Random Forest
- metin tabanlı feature engineering
- risk skoru ve label mühendisliği

hala gayet mantıklı bir çekirdek.

## 5. Literatüre Göre Zayıf veya Riskli Yanlar

## 5.1. Şu anki label şeması klinik olarak biraz kaba kalabilir

`increase / decrease / risk / contraindication` iyi bir başlangıç ama yeterince ince değil.

Eksik kalabilecek boyutlar:

- mekanizma tipi
- farmakokinetik / farmakodinamik ayrımı
- yönlülük
- şiddet
- yönetim önerisi

## 5.2. Veri sızıntısı ve değerlendirme yanılgısı riski yüksek

DDI-Ben ışığında en büyük risklerden biri bu:

- random split ile yüksek görünen performans
- unseen-drug senaryosunda sert düşüş

Bu, proje raporunda ele alınmazsa model olduğundan daha güçlü sanılabilir.

## 5.3. TWOSIDES merge çıktısı tekrar üretme riski taşıyor

Repo örnekleri gösteriyor ki aynı ilaç çifti farklı yan etkiler nedeniyle çok sayıda satırda tekrar ediyor. Bu durum:

- etiket dağılımını çarpıtabilir
- veri dengesizliğini büyütebilir
- train/test leakage riskini artırabilir

Bu konu mutlaka dikkatle ele alınmalı.

## 5.4. Standardizasyon katmanı henüz resmi veri kontratına dönüşmemiş

`src/build_vocabulary.py` iyi bir başlangıç ama tek başına yeterli değil. Literatüre göre güçlü bir standardizasyon katmanı şunları içermeli:

- canonical ID
- synonym listesi
- normalize form
- kaynak veri ismi
- eşleşme güven seviyesi
- belirsiz eşleşme işaretleri

## 5.5. Çoklu ilaç desteği için erken genelleme riski var

Pairwise modelden doğrudan 3+ ilaç dünyasına atlamak cazip ama yanıltıcı olabilir. HODDI ve ilgili çalışmalar, bunun ayrı bir problem olduğunu gösteriyor.

## 6. Benzer Proje Kümeleri ve Sizden Farkları

## 6.1. Curated interaction checker sistemleri

Örnekler:

- DrugBank
- DDInter 2.0

Bu sistemler genellikle:

- yüksek güvenilir curated bilgi
- risk ve açıklama
- arama ve filtreleme

sunuyor; ama yeni/bilinmeyen etkileşimleri keşfetme tarafı zayıf.

Sizden farkları:

- Onlar bilgi tabanı ağırlıklı
- Siz öngörü + ürün hibriti kurabilirsiniz

## 6.2. Akademik prediction-only sistemleri

Örnekler:

- DeepDDI
- KnowDDI
- DDintensity
- D3

Bunlar çoğunlukla:

- model performansına odaklanıyor
- klinik arayüz veya karar desteği katmanını ikinci plana bırakıyor

Sizden farkları:

- Siz ürünleşmeye daha yakınsınız
- Ama onlar değerlendirme tasarımı ve metodolojik derinlikte daha güçlü olabiliyor

## 6.3. Benchmark ve review çalışmaları

Örnekler:

- DDI-Ben
- npj Digital Medicine 2026 review
- ACS/JCIM review

Bunlar size yöntem vermez; ama projeyi nasıl daha ciddi kurmanız gerektiğini söyler:

- daha iyi split
- daha iyi doğrulama
- daha iyi açıklanabilirlik
- daha iyi veri standardizasyonu

## 7. Projeyi Gerçekten Güçlendirecek Somut Öneriler

## 7.1. SCRUM-4'ü yalnızca "CSV temizliği" olarak bırakmayın

Bu işi şu ürüne dönüştürün:

- canonical vocabulary table
- synonym expansion table
- normalization function
- coverage audit report
- ambiguous alias list

Bu durumda `SCRUM-4`, projede altyapısal omurga olur.

## 7.2. İsim eşleşmesini sayısal olarak ölçün

Önerdiğim ölçümler:

- Kaggle ilaç adları içinde vocabulary ile eşleşen oran
- TWOSIDES ilaç adları içinde eşleşen oran
- normalize etmeden önce ve sonra eşleşme farkı
- birden fazla DrugBank ID'ye düşen alias sayısı
- hiç eşleşmeyen ilaç adı listesi

Bu ölçümler seni ekipte çok güçlü konuma getirir, çünkü herkesin işine yarar.

## 7.3. Evaluation protokolünü iki katmanlı kurun

En az şu iki senaryo olmalı:

- random split
- unseen-drug split

Eğer ileride yapısal özellikler eklerseniz üçüncü senaryo:

- scaffold/OOD split

## 7.4. Label yapısını hiyerarşik hale getirin

Uzun vadede şu yapı daha iyi olur:

- katman 1: etkileşim var mı
- katman 2: yönü ne
- katman 3: mekanizma ailesi ne
- katman 4: risk seviyesi ne

Bu hem klinik olarak daha anlamlı, hem raporlamada daha profesyonel olur.

## 7.5. DDInter 2.0'yı doğrulama ve kalibrasyon katmanına dönüştürün

DDInter'i sadece referans link gibi değil, şu işlerde kullanın:

- severity/risk calibration
- known mechanism spot-check
- yönetim önerisi metni üretimi
- UI filtreleme mantığı

## 7.6. Nihai sistemde LLM'i yardımcı role koyun

Literatürün önerdiği güvenli kullanım şeması:

- serbest metinden triplet çıkarma
- açıklama özeti üretme
- mekanizma kategorileme
- literatür özetleme

Ama şu işlerde tek başına bırakmayın:

- nihai risk derecelendirme
- klinik kesin hüküm
- çoklu ilaç akıl yürütmesinde son karar

## 7.7. Açıklanabilirlik katmanını erken planlayın

Sizin ürününüzü farklılaştıracak çok önemli alan bu.

Önerilen açıklama bileşenleri:

- interaction description özeti
- eşleşen mekanizma etiketi
- PRR veya risk seviyesi gerekçesi
- feature importance / SHAP özeti
- veri kaynağı etiketi: DrugBank mi, TWOSIDES mı, DDInter mı

## 7.8. Alert fatigue'i ürün tasarımında ciddiye alın

DDInter 2.0'ın yaklaşımına benzer biçimde:

- severity filtresi
- güven seviyesi filtresi
- bilinmeyen mekanizmalı uyarıları ayrı gösterme
- yönetim önerisi olan etkileşimleri öne çıkarma

gibi arayüz kararları, projeyi gerçekten daha "kullanılabilir" yapar.

## 7.9. Çoklu ilaç desteğini ikinci faz olarak planlayın

İlk faz:

- pairwise güçlü sistem

İkinci faz:

- pairwise sonuçların kombinasyon analizi
- higher-order veri/dataset araştırması
- HODDI veya FAERS tabanlı genişletme

Bu ayrım projeyi daha kontrollü büyütür.

## 8. Benim Proje İçin Net Konumlandırmam

Bu proje, doğru ilerletilirse şu kategoriye oturabilir:

**"Açıklanabilir, veri-standardizasyonu güçlü, gerçek-dünya sinyali içeren, ürünleşebilir DDI karar destek prototipi."**

Bu konumlandırma bence çok güçlü çünkü:

- salt akademik benchmark değilsiniz
- salt bilgi tabanı kopyası da değilsiniz
- ML + standardization + risk + UI hibriti kuruyorsunuz

Ama bunun gerçekleşmesi için üç şey şart:

1. Veri standardizasyonunu ciddiye almak
2. Değerlendirme protokolünü gerçekçi kurmak
3. Açıklanabilirlik ve ürün kararlarını erken tasarlamak

## 9. SCRUM-4 İçin Benim Önerdiğim Mükemmel Kapsam

Senin elindeki vocabulary işi için ideal teslim seti şu olur:

### Teknik çıktı

- `drugbank_vocabulary_clean.csv`
- canonical name ve synonym tablosu
- normalize edici yardımcı fonksiyon
- Kaggle/TWOSIDES match audit çıktısı

### Analitik çıktı

- eşleşme kapsama oranı
- eşleşmeyen ilaç listesi
- ambiguous alias listesi
- en çok problem çıkaran isim varyantları

### Dokümantasyon çıktısı

- normalization kuralları
- hangi kolonun ne anlama geldiği
- merge pipeline için nasıl kullanılacağı
- hangi edge-case'lerin şimdilik dışarıda bırakıldığı

Bu teslim paketi, arkadaşların yaptığı işler bitmiş olsa bile onlara doğrudan fayda sağlar ve çakışma riskini düşürür.

## 10. Sonuç

14 Mart 2026 itibarıyla güncel literatürün ana mesajı şu:

- DDI alanı daha büyük model yarışından çok
- daha iyi veri,
- daha iyi değerlendirme,
- daha iyi açıklanabilirlik,
- daha iyi klinik entegrasyon

yönüne kayıyor.

Bu, sizin proje için çok avantajlı bir tablo.

Çünkü siz tam olarak şu kesişimde duruyorsunuz:

- veri standardizasyonu
- metin tabanlı açıklama çıkarımı
- risk katmanı
- kullanıcıya gösterilebilir uyarı

Eğer `SCRUM-4` işini güçlü bir normalizasyon ve coverage audit katmanına çevirirseniz, bu proje sıradan bir sınıf projesinden daha derli toplu, daha akademik ve daha ürün-odaklı bir yapıya geçer.

## 11. Kaynaklar

1. Lu Y, Chen J, Fan N, et al. *Machine learning models for drug-drug interaction prediction from computational discovery to clinical application*. npj Digital Medicine, 29 January 2026. https://www.nature.com/articles/s41746-026-02400-3
2. Gil-Sorribes M, Molina A. *Addressing model overcomplexity in drug-drug interaction prediction with molecular fingerprints*. Journal of Cheminformatics, 19 February 2026. https://link.springer.com/article/10.1186/s13321-025-01128-8
3. Shen Z, Zhou M, Zhang Y, Yao Q. *Benchmarking drug-drug interaction prediction methods: a perspective of distribution changes*. Bioinformatics, 14 October 2025. https://academic.oup.com/bioinformatics/article/41/11/btaf569/8285831
4. Feng Q, Huang X. *Multi-feature machine learning for enhanced drug-drug interaction prediction*. Journal of Biomedical Informatics, 2025. https://pubmed.ncbi.nlm.nih.gov/41067296/
5. Xie W, Chen X, Huang L, et al. *DDintensity: Addressing imbalanced drug-drug interaction risk levels using pre-trained deep learning model embeddings*. Artificial Intelligence in Medicine, 2025. https://pubmed.ncbi.nlm.nih.gov/40617062/
6. Ibrahim A, Hosseini A, Ibrahim S, et al. *D3: A Small Language Model for Drug-Drug Interaction prediction and comparison with Large Language Models*. Machine Learning with Applications, 2025. https://www.sciencedirect.com/science/article/pii/S2666827025000416
7. Jung S, Yoo S. *Interpretable prediction of drug-drug interactions via text embedding in biomedical literature*. Computers in Biology and Medicine, 2025. https://pubmed.ncbi.nlm.nih.gov/39626457/
8. Tian Y, Yi J, Wang N, et al. *DDInter 2.0: an enhanced drug interaction resource with expanded data coverage, new interaction types, and improved user interface*. Nucleic Acids Research, 2025. https://pubmed.ncbi.nlm.nih.gov/39180399/
9. Knox C, Wilson M, Klinger CM, et al. *DrugBank 6.0: the DrugBank Knowledgebase for 2024*. Nucleic Acids Research, 2024. https://academic.oup.com/nar/article/52/D1/D1265/7416367
10. Zhang Y, Deng Z, Xu X, et al. *Application of Artificial Intelligence in Drug-Drug Interactions Prediction: A Review*. Journal of Chemical Information and Modeling, 2024. https://pubmed.ncbi.nlm.nih.gov/37458400/
11. Wang Y, Yang Z, Yao Q. *Accurate and interpretable drug-drug interaction prediction enabled by knowledge subgraph learning*. Communications Medicine, 2024. https://www.nature.com/articles/s43856-024-00486-y
12. Ryu JY, Kim HU, Lee SY. *Deep learning improves prediction of drug-drug and drug-food interactions*. PNAS, 2018. https://pubmed.ncbi.nlm.nih.gov/29666228/
13. Tatonetti NP, Ye PP, Daneshjou R, Altman RB. *Data-driven prediction of drug effects and interactions*. Science Translational Medicine, 2012. https://pubmed.ncbi.nlm.nih.gov/22422992/
14. Wang Z, Shi Y, Liu X, et al. *HODDI: A Dataset of High-Order Drug-Drug Interactions for Computational Pharmacovigilance*. arXiv, 2025. https://arxiv.org/abs/2502.06274
15. NLM. *RxNorm*. U.S. National Library of Medicine. https://www.nlm.nih.gov/research/umls/rxnorm/
16. Blotske K, Zhao X, Henry K, et al. *Drug-drug interaction identification using large language models*. Preprint indexed in PubMed, 2025. https://pubmed.ncbi.nlm.nih.gov/41503479/
17. *Risk stratification of potential drug interactions involving common over-the-counter medications and herbal supplements by a large language model*. 2024. https://pubmed.ncbi.nlm.nih.gov/39613295/
