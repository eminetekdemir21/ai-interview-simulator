"""Sirket Bazli Mulakat Modu icin sirket verisi. Frontend'deki
assets/app.js -> COMPANIES dizisiyle ayni id/isim setini kullanir, boylece
interview-setup.html'de secilen sirket id'si burada da karsilik bulur.

`style_hint`, Gemini'ye sirkete ozgu mulakat tarzini anlatmak icin
kullanilir (Gun 2'de gemini_client.py tarafindan promta eklenecek).
"""

COMPANIES = {
    "google": {"name": "Google", "focus": ["Algoritmalar", "Veri Yapilari", "System Design"], "style_hint": "Google mulakatlari algoritma/veri yapisi derinligi, karmasiklik analizi (Big-O) ve buyuk olcekli sistem tasarimina onem verir. Soru zor ve analitik olmali."},
    "microsoft": {"name": "Microsoft", "focus": ["C#", ".NET", "Azure", "OOP"], "style_hint": "Microsoft mulakatlari nesne yonelimli tasarim, .NET/C# ekosistemi ve bulut (Azure) bilgisine odaklanir."},
    "amazon": {"name": "Amazon", "focus": ["Leadership Principles", "Ownership", "Scalability"], "style_hint": "Amazon mulakatlari hem teknik derinlik hem de 'Leadership Principles' tarzinda davranissal/olcup-bicme sorulari icerir; olceklenebilirlik onemlidir."},
    "meta": {"name": "Meta", "focus": ["Coding", "Product Thinking", "System Design"], "style_hint": "Meta mulakatlari hizli ve temiz kod yazma, urun dusuncesi (product sense) ve sistem tasarimini birlikte degerlendirir."},
    "apple": {"name": "Apple", "focus": ["Swift", "System Design", "Detay Odagi"], "style_hint": "Apple mulakatlari detaylara verilen onem, kullanici deneyimine etkisi olan muhendislik kararlari ve titizlik uzerine sorular icerir."},
    "netflix": {"name": "Netflix", "focus": ["Culture Fit", "Distributed Systems"], "style_hint": "Netflix mulakatlari dagitik sistemler, yuksek erisilebilirlik ve kultur uyumu (ozerklik, sorumluluk) uzerine sorular sorar."},
    "tesla": {"name": "Tesla", "focus": ["Engineering", "Optimizasyon"], "style_hint": "Tesla mulakatlari muhendislik optimizasyonu, performans ve gercek zamanli sistemlere dair pratik problem cozme sorulari icerir."},
    "openai": {"name": "OpenAI", "focus": ["Machine Learning", "LLM", "AI Ethics"], "style_hint": "OpenAI mulakatlari makine ogrenmesi temelleri, buyuk dil modelleri ve AI etigi uzerine derin teknik sorular icerir."},
    "nvidia": {"name": "NVIDIA", "focus": ["CUDA", "Parallel Computing"], "style_hint": "NVIDIA mulakatlari paralel programlama, GPU mimarisi ve performans optimizasyonuna odaklanir."},
    "intel": {"name": "Intel", "focus": ["Computer Architecture", "C/C++"], "style_hint": "Intel mulakatlari bilgisayar mimarisi, dusuk seviyeli C/C++ ve donanim-yazilim etkilesimine odaklanir."},
    "ibm": {"name": "IBM", "focus": ["Enterprise Systems", "Cloud"], "style_hint": "IBM mulakatlari kurumsal sistemler, bulut mimarisi ve entegrasyon uzerine sorular sorar."},
    "oracle": {"name": "Oracle", "focus": ["SQL", "Java", "Database Systems"], "style_hint": "Oracle mulakatlari veritabani sistemleri, SQL optimizasyonu ve Java uzerine derinlemesine sorular icerir."},
    "spotify": {"name": "Spotify", "focus": ["Backend", "Microservices"], "style_hint": "Spotify mulakatlari mikroservis mimarisi, backend olceklenebilirligi ve veri akisi uzerine odaklanir."},
    "airbnb": {"name": "Airbnb", "focus": ["System Design", "Product Sense"], "style_hint": "Airbnb mulakatlari sistem tasarimi ve urun dusuncesini birlestiren senaryo bazli sorular sorar."},
    "uber": {"name": "Uber", "focus": ["System Design", "Scalability"], "style_hint": "Uber mulakatlari gercek zamanli, yuksek olcekli sistem tasarimi senaryolarina odaklanir (orn. konum takibi, eslesme algoritmalari)."},
    "aselsan": {"name": "ASELSAN", "focus": ["Gomulu Sistemler", "C/C++", "RTOS", "Sinyal Isleme"], "style_hint": "ASELSAN mulakatlari gomulu sistemler, C/C++, gercek zamanli isletim sistemleri (RTOS) ve sinyal isleme konularina odaklanan savunma sanayi tarzi teknik sorular icerir."},
    "havelsan": {"name": "HAVELSAN", "focus": ["Java", "Spring Boot", "Microservices"], "style_hint": "HAVELSAN mulakatlari Java/Spring Boot tabanli kurumsal yazilim gelistirme ve mikroservis mimarisine odaklanir."},
    "tusas": {"name": "TUSAS", "focus": ["Havacilik Yazilimi", "Gomulu Sistemler"], "style_hint": "TUSAS mulakatlari havacilik/savunma yazilimlari ve gomulu sistemler uzerine teknik derinlik gerektiren sorular sorar."},
    "roketsan": {"name": "ROKETSAN", "focus": ["Savunma Yazilimi", "C++"], "style_hint": "ROKETSAN mulakatlari savunma sanayi yazilimlari, C++ ve guvenilirlik/gercek zamanlilik gerektiren sistemlere odaklanir."},
    "baykar": {"name": "Baykar", "focus": ["Gomulu Yazilim", "Computer Vision", "Otonom Sistemler"], "style_hint": "Baykar mulakatlari gomulu yazilim, bilgisayarli goru (computer vision) ve otonom sistemler uzerine ileri duzey sorular icerir."},
    "turkcell": {"name": "Turkcell", "focus": ["Java", "Spring Boot", "Kubernetes"], "style_hint": "Turkcell mulakatlari Java/Spring Boot backend gelistirme ve Kubernetes/konteyner tabanli altyapiya odaklanir."},
    "turktelekom": {"name": "Turk Telekom", "focus": ["Cloud", "Network Systems"], "style_hint": "Turk Telekom mulakatlari bulut altyapisi ve network sistemleri uzerine sorular sorar."},
    "garanti": {"name": "Garanti BBVA", "focus": [".NET", "SQL", "Bankacilik Sistemleri", "Guvenlik"], "style_hint": "Garanti BBVA mulakatlari .NET/SQL tabanli bankacilik sistemleri, veri guvenligi ve uyumluluk (compliance) konularina odaklanir."},
    "akbank": {"name": "Akbank", "focus": ["Java", "Bankacilik API'leri"], "style_hint": "Akbank mulakatlari Java tabanli bankacilik API'leri ve islem guvenilirligi uzerine sorular sorar."},
    "yapikredi": {"name": "Yapi Kredi", "focus": ["Backend", "Cloud"], "style_hint": "Yapi Kredi mulakatlari backend gelistirme ve bulut donusumu uzerine sorular sorar."},
    "isbankasi": {"name": "Is Bankasi", "focus": ["Java", "Enterprise Backend"], "style_hint": "Is Bankasi mulakatlari kurumsal Java backend sistemleri uzerine sorular sorar."},
    "vakifbank": {"name": "VakifBank", "focus": [".NET", "SQL Server"], "style_hint": "VakifBank mulakatlari .NET/SQL Server tabanli bankacilik yazilimlarina odaklanir."},
    "ziraat": {"name": "Ziraat Bankasi", "focus": ["Java", "Bankacilik Sistemleri"], "style_hint": "Ziraat Bankasi mulakatlari Java tabanli bankacilik sistemleri uzerine sorular sorar."},
}


def get_company(company_id):
    return COMPANIES.get(company_id)
