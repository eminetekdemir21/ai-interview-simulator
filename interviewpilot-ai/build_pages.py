#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates secondary InterviewPilot AI pages from a shared sidebar/topbar shell."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def sidebar(active):
    links = [
        ("dashboard.html", "layout-dashboard", "Dashboard", "main"),
        ("interview-setup.html", "play-circle", "Yeni Mulakat", "main"),
        ("history.html", "history", "Gecmis", "main"),
        ("analytics.html", "bar-chart-3", "Analitik", "main"),
        ("roadmap.html", "map", "Yol Haritasi", "main"),
        ("resume-analysis.html", "file-search", "CV Analizi", "career"),
        ("job-match.html", "target", "Is Uyumu", "career"),
        ("career-coach.html", "compass", "AI Kariyer Kocu", "career"),
        ("portfolio.html", "github", "Portfolyo", "career"),
        ("leaderboard.html", "trophy", "Liderlik Tablosu", "community"),
        ("challenges.html", "swords", "Gunluk Meydan Okuma", "community"),
        ("profile.html", "user", "Profil", "account"),
        ("admin.html", "shield", "Admin Panel", "account"),
    ]
    out = ['<aside class="sidebar">',
           '  <div class="brand" style="padding:10px 10px 18px;"><div class="brand-mark">IP</div>InterviewPilot</div>']
    last_group = "main"
    labels = {"career": "Kariyer", "community": "Topluluk", "account": "Hesap"}
    for href, icon, label, group in links:
        if group != last_group and group in labels:
            out.append(f'  <div class="sidebar-section-label">{labels[group]}</div>')
        cls = "side-link active" if href == active else "side-link"
        out.append(f'  <a class="{cls}" href="{href}"><span class="icon-box"><i data-lucide="{icon}" style="width:17px"></i></span>{label}</a>')
        last_group = group
    out.append('</aside>')
    return "\n".join(out)

def topbar(title, subtitle, cta_href=None, cta_label=None):
    cta = f'<a href="{cta_href}" class="btn btn-primary btn-sm">{cta_label}</a>' if cta_href else ''
    return f'''    <div class="topbar">
      <div><div class="h4">{title}</div><div class="faint" style="font-size:13px;">{subtitle}</div></div>
      <div class="flex items-center gap-12">
        <div class="switch theme-switch" onclick="toggleTheme()"></div>
        {cta}
      </div>
    </div>'''

def page(filename, title, active, top_title, top_sub, extra_style, body, extra_script="", cta_href=None, cta_label=None, extra_head=""):
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — InterviewPilot AI</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800&display=swap" rel="stylesheet">
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
{extra_head}
<link rel="stylesheet" href="assets/style.css">
<style>
{extra_style}
</style>
</head>
<body>
<div class="app-shell">
{sidebar(active)}
  <div class="main-content">
{topbar(top_title, top_sub, cta_href, cta_label)}
    <div class="page-body">
{body}
    </div>
  </div>
</div>
<script src="assets/app.js"></script>
<script>
  lucide.createIcons();
{extra_script}
</script>
</body>
</html>
'''
    with open(os.path.join(BASE, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)

# ---------------------------------------------------------------- history.html
page(
  "history.html", "Gecmis", "history.html", "Mulakat Gecmisi", "Tum gecmis mulakatlarin ve raporlarin",
  extra_style='''
  .filter-bar { display:flex; gap:10px; margin-bottom:18px; flex-wrap:wrap; }
  .hist-row { display:grid; grid-template-columns: 44px 1.6fr 1fr 1fr 90px 90px; align-items:center; gap:14px; padding:14px 6px; border-bottom:1px solid var(--border); }
  .hist-row:last-child { border-bottom:none; }
  ''',
  body='''      <div class="filter-bar">
        <select class="input" style="width:180px;"><option>Tum Sirketler</option><option>Google</option><option>Amazon</option><option>ASELSAN</option></select>
        <select class="input" style="width:180px;"><option>Tum Turler</option><option>Teknik</option><option>Davranissal</option><option>System Design</option></select>
        <select class="input" style="width:180px;"><option>Son 30 gun</option><option>Son 7 gun</option><option>Tum zamanlar</option></select>
      </div>
      <div class="card fade-up">
        <div class="hist-row" style="font-size:12px; font-weight:700; color:var(--text-faint); text-transform:uppercase;">
          <span></span><span>Sirket / Rol</span><span>Tur</span><span>Tarih</span><span>Sure</span><span>Skor</span>
        </div>
        <div id="histRows"></div>
      </div>''',
  extra_script='''
  const rows = document.getElementById("histRows");
  const items = [
    {c:"google", role:"Backend Developer", type:"Teknik", date:"2 gun once", dur:"22 dk", score:82},
    {c:"amazon", role:"Backend Developer", type:"Davranissal", date:"4 gun once", dur:"18 dk", score:74},
    {c:"aselsan", role:"Gomulu Yazilim", type:"Teknik", date:"6 gun once", dur:"26 dk", score:69},
    {c:"microsoft", role:"Full Stack", type:"Karisik", date:"1 hafta once", dur:"24 dk", score:88},
    {c:"meta", role:"Frontend Developer", type:"Teknik", date:"1 hafta once", dur:"20 dk", score:71},
    {c:"turkcell", role:"Backend Developer", type:"Teknik", date:"2 hafta once", dur:"19 dk", score:65},
    {c:"netflix", role:"System Design", type:"System Design", date:"2 hafta once", dur:"30 dk", score:58},
  ];
  items.forEach(it => {
    const co = COMPANIES.find(x => x.id === it.c) || {name: it.c, initials:"?", color:"#888"};
    const badgeClass = it.score >= 80 ? "badge-success" : it.score >= 65 ? "badge-warning" : "badge-danger";
    const div = document.createElement("div");
    div.className = "hist-row";
    div.innerHTML = `<div class="co-logo" style="width:36px;height:36px;font-size:12px;background:${co.color}">${co.initials}</div>
      <div><div style="font-weight:700; font-size:13.5px;">${co.name}</div><div class="faint" style="font-size:12px;">${it.role}</div></div>
      <span class="tag">${it.type}</span><span class="faint" style="font-size:13px;">${it.date}</span><span class="faint" style="font-size:13px;">${it.dur}</span>
      <span class="badge ${badgeClass}">${it.score}</span>`;
    rows.appendChild(div);
  });
  '''
)

# --------------------------------------------------------------- analytics.html
page(
  "analytics.html", "Analitik", "analytics.html", "Performans Analitigi", "Zaman icinde ilerlemeni detayli incele",
  extra_style='''
  .an-grid { grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px; }
  @media (max-width:1100px) { .an-grid { grid-template-columns:1fr; } }
  ''',
  extra_head='<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>',
  body='''      <div class="grid kpi-grid" style="grid-template-columns:repeat(4,1fr);">
        <div class="card kpi-card"><div class="kpi-label">Toplam Mulakat</div><div class="kpi-value">34</div></div>
        <div class="card kpi-card"><div class="kpi-label">Ortalama Skor</div><div class="kpi-value">78</div></div>
        <div class="card kpi-card"><div class="kpi-label">En Iyi Skor</div><div class="kpi-value">94</div></div>
        <div class="card kpi-card"><div class="kpi-label">Toplam Sure</div><div class="kpi-value">11.4 sa</div></div>
      </div>
      <div class="grid an-grid">
        <div class="card fade-up"><div class="h4" style="margin-bottom:14px;">Skor Trendi (Son 8 Hafta)</div><canvas id="trendChart" height="110"></canvas></div>
        <div class="card fade-up delay-1"><div class="h4" style="margin-bottom:14px;">Konu Bazli Ortalama</div><canvas id="topicChart" height="110"></canvas></div>
        <div class="card fade-up delay-2"><div class="h4" style="margin-bottom:14px;">Mulakat Turu Dagilimi</div><canvas id="typeChart" height="180"></canvas></div>
        <div class="card fade-up delay-3">
          <div class="h4" style="margin-bottom:10px;">Sirket Bazli Ortalama Skor</div>
          <div id="coScoreList"></div>
        </div>
      </div>''',
  extra_script='''
  new Chart(document.getElementById("trendChart"), { type:"line", data:{ labels:["1","2","3","4","5","6","7","8"], datasets:[{data:[58,61,65,63,70,74,76,78], borderColor:"#6366f1", backgroundColor:"rgba(99,102,241,.12)", fill:true, tension:.4}] }, options:{ plugins:{legend:{display:false}}, scales:{y:{min:0,max:100}} } });
  new Chart(document.getElementById("topicChart"), { type:"bar", data:{ labels:["Algoritma","API","DB","System Design","OOP"], datasets:[{data:[80,85,72,58,76], backgroundColor:"#8b5cf6", borderRadius:6}] }, options:{ plugins:{legend:{display:false}}, scales:{y:{min:0,max:100}} } });
  new Chart(document.getElementById("typeChart"), { type:"doughnut", data:{ labels:["Teknik","Davranissal","System Design","Karisik"], datasets:[{data:[18,7,5,4], backgroundColor:["#6366f1","#8b5cf6","#3b82f6","#22c55e"]}] } });
  const list = document.getElementById("coScoreList");
  [["google",82],["microsoft",88],["amazon",74],["aselsan",69],["meta",71]].forEach(([id,score]) => {
    const co = COMPANIES.find(c=>c.id===id);
    const div = document.createElement("div");
    div.style.cssText = "display:flex; align-items:center; gap:10px; padding:8px 0;";
    div.innerHTML = `<div class="co-logo" style="width:30px;height:30px;font-size:11px;background:${co.color}">${co.initials}</div><span style="flex:1; font-size:13.5px; font-weight:600;">${co.name}</span><span class="badge badge-primary">${score}</span>`;
    list.appendChild(div);
  });
  '''
)

# --------------------------------------------------------------- roadmap.html
page(
  "roadmap.html", "Yol Haritasi", "roadmap.html", "Ogrenme Yol Haritasi", "Zayif konularina gore AI tarafindan olusturuldu",
  extra_style='''
  .rm-week { display:flex; gap:18px; margin-bottom:24px; }
  .rm-dot-col { display:flex; flex-direction:column; align-items:center; }
  .rm-dot { width:34px; height:34px; border-radius:50%; background:var(--grad-brand); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:13px; flex-shrink:0; }
  .rm-line { width:2px; flex:1; background:var(--border); margin-top:6px; }
  .rm-content { flex:1; padding-bottom:8px; }
  .rm-task { display:flex; align-items:center; gap:10px; padding:8px 0; font-size:13.5px; }
  ''',
  body='''      <div class="card fade-up" style="margin-bottom:20px; background:var(--grad-brand-soft);">
        <div class="flex items-center gap-16">
          <div class="feature-icon" style="margin:0;"><i data-lucide="sparkles"></i></div>
          <div><div class="h4">Odak Alanin: System Design</div><p class="faint" style="font-size:13px; margin-top:2px;">Son mulakatlara gore olusturulan 3 haftalik kisisellestirilmis plan</p></div>
        </div>
      </div>
      <div class="card fade-up">
        <div class="rm-week">
          <div class="rm-dot-col"><div class="rm-dot">1</div><div class="rm-line"></div></div>
          <div class="rm-content">
            <div class="h4" style="margin-bottom:6px;">Hafta 1 — Temeller</div>
            <div class="rm-task"><input type="checkbox" checked> <span style="text-decoration:line-through; color:var(--text-faint);">Load Balancing kavramlarini ogren</span></div>
            <div class="rm-task"><input type="checkbox" checked> <span style="text-decoration:line-through; color:var(--text-faint);">CAP Teoremi uzerine makale oku</span></div>
            <div class="rm-task"><input type="checkbox"> <span>Caching stratejileri (Redis) pratik yap</span></div>
          </div>
        </div>
        <div class="rm-week">
          <div class="rm-dot-col"><div class="rm-dot" style="background:var(--surface-2); color:var(--text-faint); border:2px solid var(--border);">2</div><div class="rm-line"></div></div>
          <div class="rm-content">
            <div class="h4" style="margin-bottom:6px;">Hafta 2 — Uygulama</div>
            <div class="rm-task"><input type="checkbox"> <span>Database sharding & replication</span></div>
            <div class="rm-task"><input type="checkbox"> <span>Bir URL kisaltici sistemi tasarla (pratik)</span></div>
            <div class="rm-task"><input type="checkbox"> <span>Rate limiting algoritmalari (token bucket vb.)</span></div>
          </div>
        </div>
        <div class="rm-week">
          <div class="rm-dot-col"><div class="rm-dot" style="background:var(--surface-2); color:var(--text-faint); border:2px solid var(--border);">3</div></div>
          <div class="rm-content">
            <div class="h4" style="margin-bottom:6px;">Hafta 3 — Mock Mulakat</div>
            <div class="rm-task"><input type="checkbox"> <span>Google System Design mulakat modunda 2 pratik yap</span></div>
            <div class="rm-task"><input type="checkbox"> <span>Zayif konulari tekrar degerlendir</span></div>
          </div>
        </div>
      </div>''',
)

# --------------------------------------------------------------- resume-analysis.html
page(
  "resume-analysis.html", "CV Analizi", "resume-analysis.html", "CV Analizi", "CV'ni yukle, AI aninda analiz etsin",
  extra_style='''
  .upload-zone { border:2px dashed var(--border); border-radius:16px; padding:44px; text-align:center; cursor:pointer; transition:.15s; }
  .upload-zone:hover { border-color:var(--indigo); background:var(--grad-brand-soft); }
  .score-badge-lg { width:64px; height:64px; border-radius:50%; background:var(--grad-brand); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:20px; }
  ''',
  body='''      <div class="grid" style="grid-template-columns:1fr 1.3fr; gap:20px;">
        <div class="card fade-up">
          <div class="upload-zone">
            <i data-lucide="upload-cloud" style="width:36px; color:var(--indigo);"></i>
            <p style="font-weight:700; margin-top:12px;">CV'ni surukle birak</p>
            <p class="faint" style="font-size:12.5px; margin-top:4px;">PDF, DOCX — 10MB'a kadar</p>
            <button class="btn btn-primary" style="margin-top:16px;">Dosya Sec</button>
          </div>
          <div class="flex items-center gap-12" style="margin-top:16px; padding:12px; background:var(--surface-2); border-radius:10px;">
            <i data-lucide="file-text" style="width:20px; color:var(--indigo);"></i>
            <div style="flex:1; font-size:13px; font-weight:600;">emine_tekdemir_cv.pdf</div>
            <span class="badge badge-success">Analiz Edildi</span>
          </div>
        </div>
        <div class="card fade-up delay-1">
          <div class="flex items-center gap-16" style="margin-bottom:20px;">
            <div class="score-badge-lg">84</div>
            <div><div class="h4">CV Skoru: Iyi</div><p class="faint" style="font-size:13px;">ATS uyumlulugu ve icerik kalitesine gore</p></div>
          </div>
          <div style="font-size:13px; font-weight:700; color:var(--success); margin-bottom:8px;">Guclu Yonler</div>
          <div class="checklist-item" style="display:flex; gap:8px; font-size:13.5px; padding:5px 0;"><i data-lucide="check-circle-2" style="width:16px; color:var(--success);"></i>Olculebilir basarilar var (%20 performans artisi vb.)</div>
          <div class="checklist-item" style="display:flex; gap:8px; font-size:13.5px; padding:5px 0;"><i data-lucide="check-circle-2" style="width:16px; color:var(--success);"></i>Anahtar kelimeler is ilanlariyla uyumlu</div>
          <div style="font-size:13px; font-weight:700; color:var(--warning); margin:14px 0 8px;">Iyilestirme Onerileri</div>
          <div class="checklist-item" style="display:flex; gap:8px; font-size:13.5px; padding:5px 0;"><i data-lucide="alert-circle" style="width:16px; color:var(--warning);"></i>Ozet (summary) bolumu eksik</div>
          <div class="checklist-item" style="display:flex; gap:8px; font-size:13.5px; padding:5px 0;"><i data-lucide="alert-circle" style="width:16px; color:var(--warning);"></i>Proje linklerini (GitHub) ekle</div>
          <div class="checklist-item" style="display:flex; gap:8px; font-size:13.5px; padding:5px 0;"><i data-lucide="alert-circle" style="width:16px; color:var(--warning);"></i>Bazi bolumler cok uzun, 1 sayfaya sigdir</div>
        </div>
      </div>''',
)

# --------------------------------------------------------------- job-match.html
page(
  "job-match.html", "Is Uyumu", "job-match.html", "CV — Is Ilani Uyumu", "Is ilanini yapistir, CV'nle karsilastir",
  extra_style='''
  .match-ring { width:120px; height:120px; margin:0 auto; }
  .kw-chip { display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border-radius:999px; font-size:12.5px; font-weight:600; margin:3px; }
  .kw-match { background:var(--success-soft); color:var(--success); }
  .kw-missing { background:var(--danger-soft); color:var(--danger); }
  ''',
  extra_head='<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>',
  body='''      <div class="grid" style="grid-template-columns:1fr 1fr; gap:20px;">
        <div class="card fade-up">
          <div class="h4" style="margin-bottom:10px;">Is Ilani</div>
          <textarea class="input" style="min-height:220px; resize:vertical;" placeholder="Is ilani metnini buraya yapistir...">Google - Backend Developer
Aradigimiz: 2+ yil Python/Java deneyimi, REST API tasarimi, SQL/NoSQL, dagitik sistemler bilgisi, CS temelleri (algoritma, veri yapilari)...</textarea>
          <button class="btn btn-primary" style="width:100%; margin-top:14px;">Uyumu Analiz Et</button>
        </div>
        <div class="card fade-up delay-1 text-center">
          <div class="match-ring"><canvas id="matchRing"></canvas></div>
          <div class="h3" style="margin-top:-70px;">%82</div>
          <p class="faint" style="font-size:13px; margin-top:52px;">Genel Uyum Skoru</p>
          <hr style="border:none; border-top:1px solid var(--border); margin:16px 0;">
          <div style="text-align:left;">
            <div style="font-size:13px; font-weight:700; margin-bottom:6px;">Eslesen Anahtar Kelimeler</div>
            <div><span class="kw-chip kw-match"><i data-lucide="check" style="width:12px"></i>Python</span><span class="kw-chip kw-match"><i data-lucide="check" style="width:12px"></i>REST API</span><span class="kw-chip kw-match"><i data-lucide="check" style="width:12px"></i>SQL</span></div>
            <div style="font-size:13px; font-weight:700; margin:14px 0 6px;">Eksik Anahtar Kelimeler</div>
            <div><span class="kw-chip kw-missing"><i data-lucide="x" style="width:12px"></i>Dagitik Sistemler</span><span class="kw-chip kw-missing"><i data-lucide="x" style="width:12px"></i>Kubernetes</span></div>
          </div>
        </div>
      </div>''',
  extra_script='''
  new Chart(document.getElementById("matchRing"), { type:"doughnut", data:{ datasets:[{data:[82,18], backgroundColor:["#6366f1","rgba(150,150,180,.12)"], borderWidth:0}] }, options:{ cutout:"78%", plugins:{legend:{display:false}} } });
  '''
)

# --------------------------------------------------------------- career-coach.html
page(
  "career-coach.html", "AI Kariyer Kocu", "career-coach.html", "AI Kariyer Kocu", "Kariyer sorularini sor, kisisel rehberlik al",
  extra_style='''
  .chat-wrap { display:flex; flex-direction:column; height:calc(100vh - 160px); }
  .chat-msgs { flex:1; overflow-y:auto; padding:8px; }
  .cbubble { max-width:70%; padding:12px 16px; border-radius:16px; margin-bottom:14px; font-size:14px; line-height:1.6; }
  .cbubble.ai { background:var(--surface-2); border-bottom-left-radius:4px; }
  .cbubble.user { background:var(--grad-brand); color:#fff; margin-left:auto; border-bottom-right-radius:4px; }
  .suggest-chip { display:inline-block; padding:8px 14px; border:1px solid var(--border); border-radius:999px; font-size:13px; font-weight:600; cursor:pointer; margin:4px; background:var(--surface); }
  .suggest-chip:hover { border-color:var(--indigo); color:var(--indigo-600); }
  ''',
  body='''      <div class="card fade-up chat-wrap">
        <div class="chat-msgs">
          <div class="cbubble ai">Merhaba Emine! Ben senin AI kariyer kocunum 👋 Son mulakat sonuclarina baktim — System Design konusunda gelisim firsati var. Sana nasil yardimci olabilirim?</div>
          <div class="cbubble user">Google'a basvurmadan once ne kadar hazir olmam lazim?</div>
          <div class="cbubble ai">Su anki 78/100 ortalama skorunla orta seviye hazirsin. Google icin genelde 85+ ve System Design'da en az 75 oneriyoruz. Onerilen yol haritani takip edersen 2-3 haftada bu seviyeye ulasabilirsin. Ister misin sana haftalik bir plan cikarayim?</div>
        </div>
        <div>
          <div style="margin-bottom:10px;">
            <span class="suggest-chip">Maas pazarligi icin ipucu ver</span>
            <span class="suggest-chip">CV'mde neyi degistirmeliyim?</span>
            <span class="suggest-chip">Hangi sirkete once basvurmaliyim?</span>
          </div>
          <div class="flex gap-12">
            <input class="input" placeholder="Bir soru yaz...">
            <button class="btn btn-primary btn-icon"><i data-lucide="send" style="width:16px"></i></button>
          </div>
        </div>
      </div>''',
)

# --------------------------------------------------------------- portfolio.html
page(
  "portfolio.html", "Portfolyo", "portfolio.html", "Portfolyo Modu", "GitHub ve LinkedIn'ini baglayarak profilini guclendir",
  extra_style='''
  .connect-card { display:flex; align-items:center; gap:14px; padding:16px; border:1px solid var(--border); border-radius:14px; margin-bottom:12px; }
  .repo-card { padding:14px; border:1px solid var(--border); border-radius:12px; margin-bottom:10px; }
  ''',
  body='''      <div class="grid" style="grid-template-columns:1fr 1.4fr; gap:20px;">
        <div>
          <div class="connect-card fade-up">
            <i data-lucide="github" style="width:28px;"></i>
            <div style="flex:1;"><div style="font-weight:700; font-size:14px;">GitHub</div><div class="faint" style="font-size:12.5px;">eminetekdemir21 baglandi</div></div>
            <span class="badge badge-success">Bagli</span>
          </div>
          <div class="connect-card fade-up delay-1">
            <i data-lucide="linkedin" style="width:28px;"></i>
            <div style="flex:1;"><div style="font-weight:700; font-size:14px;">LinkedIn</div><div class="faint" style="font-size:12.5px;">Profil analiz icin baglan</div></div>
            <button class="btn btn-secondary btn-sm">Bagla</button>
          </div>
          <div class="card fade-up delay-2" style="margin-top:8px;">
            <div class="h4" style="margin-bottom:8px;">Kod Kalitesi Skoru</div>
            <div style="font-size:32px; font-weight:800;">76<span style="font-size:15px; color:var(--text-faint);">/100</span></div>
            <p class="faint" style="font-size:12.5px; margin-top:4px;">Commit sikligi, README kalitesi ve test kapsamina gore (orunek analiz)</p>
          </div>
        </div>
        <div class="card fade-up">
          <div class="h4" style="margin-bottom:14px;">Repolar</div>
          <div class="repo-card"><div class="flex justify-between items-center"><span style="font-weight:700; font-size:13.5px;">ai-interview-simulator</span><span class="tag">Python</span></div><p class="faint" style="font-size:12.5px; margin-top:4px;">FastAPI + Gemini AI ile mulakat simulasyonu</p></div>
          <div class="repo-card"><div class="flex justify-between items-center"><span style="font-weight:700; font-size:13.5px;">finans-takip-app</span><span class="tag">JavaScript</span></div><p class="faint" style="font-size:12.5px; margin-top:4px;">Kisisel butce ve harcama takip uygulamasi</p></div>
          <div class="repo-card"><div class="flex justify-between items-center"><span style="font-weight:700; font-size:13.5px;">e-ticaret-api</span><span class="tag">Node.js</span></div><p class="faint" style="font-size:12.5px; margin-top:4px;">PostgreSQL destekli REST API</p></div>
        </div>
      </div>''',
)

# --------------------------------------------------------------- leaderboard.html
page(
  "leaderboard.html", "Liderlik Tablosu", "leaderboard.html", "Liderlik Tablosu", "Topluluktaki diger adaylarla karsilastir",
  extra_style='''
  .lb-row { display:grid; grid-template-columns:40px 1fr 100px 100px; align-items:center; gap:14px; padding:12px 6px; border-bottom:1px solid var(--border); }
  .lb-row.me { background:var(--grad-brand-soft); border-radius:10px; }
  .lb-rank { font-weight:800; font-size:14px; text-align:center; }
  ''',
  body='''      <div class="card fade-up">
        <div class="lb-row" style="font-size:12px; font-weight:700; color:var(--text-faint); text-transform:uppercase;">
          <span>#</span><span>Kullanici</span><span>Mulakat</span><span>Ort. Skor</span>
        </div>
        <div class="lb-row"><span class="lb-rank">🥇</span><div class="flex items-center gap-12"><div class="avatar" style="width:32px;height:32px;font-size:12px;">CK</div>Can K.</div><span>52</span><span class="badge badge-success">94</span></div>
        <div class="lb-row"><span class="lb-rank">🥈</span><div class="flex items-center gap-12"><div class="avatar" style="width:32px;height:32px;font-size:12px;">SD</div>Selin D.</div><span>41</span><span class="badge badge-success">91</span></div>
        <div class="lb-row"><span class="lb-rank">🥉</span><div class="flex items-center gap-12"><div class="avatar" style="width:32px;height:32px;font-size:12px;">MY</div>Mert Y.</div><span>38</span><span class="badge badge-success">89</span></div>
        <div class="lb-row"><span class="lb-rank">4</span><div class="flex items-center gap-12"><div class="avatar" style="width:32px;height:32px;font-size:12px;">AB</div>Aylin B.</div><span>29</span><span class="badge badge-warning">85</span></div>
        <div class="lb-row me"><span class="lb-rank">12</span><div class="flex items-center gap-12"><div class="avatar" style="width:32px;height:32px;font-size:12px;">ET</div>Emine T. (Sen)</div><span>34</span><span class="badge badge-warning">78</span></div>
      </div>''',
)

# --------------------------------------------------------------- challenges.html
page(
  "challenges.html", "Meydan Okumalar", "challenges.html", "Gunluk Meydan Okuma", "Her gun yeni bir mini teknik soru, seriyi bozma",
  extra_style='''
  .chall-card { padding:20px; text-align:center; }
  ''',
  body='''      <div class="grid" style="grid-template-columns:1fr 1fr 1fr; gap:16px;">
        <div class="card chall-card fade-up card-glow">
          <i data-lucide="flame" style="width:28px; color:#f59e0b;"></i>
          <div class="h4" style="margin-top:10px;">Bugunku Soru</div>
          <p class="faint" style="font-size:13px; margin-top:6px;">"Bir array icinde tekrarlanmayan tek elemani bul"</p>
          <button class="btn btn-primary" style="width:100%; margin-top:14px;">Cozmeye Basla</button>
        </div>
        <div class="card chall-card fade-up delay-1">
          <i data-lucide="calendar-check" style="width:28px; color:var(--indigo);"></i>
          <div class="h4" style="margin-top:10px;">Bu Hafta</div>
          <p class="faint" style="font-size:13px; margin-top:6px;">5/7 gun tamamlandi</p>
          <div class="progress-track" style="margin-top:12px;"><div class="progress-fill" style="width:71%;"></div></div>
        </div>
        <div class="card chall-card fade-up delay-2">
          <i data-lucide="medal" style="width:28px; color:#8b5cf6;"></i>
          <div class="h4" style="margin-top:10px;">Rozet Ilerlemesi</div>
          <p class="faint" style="font-size:13px; margin-top:6px;">"30 Gun Serisi" rozetine 24 gun kaldi</p>
        </div>
      </div>''',
)

# --------------------------------------------------------------- profile.html
page(
  "profile.html", "Profil", "profile.html", "Profil & Ayarlar", "Hesap bilgilerini ve tercihlerini yonet",
  extra_style='''
  .settings-row { display:flex; justify-content:space-between; align-items:center; padding:14px 0; border-bottom:1px solid var(--border); }
  .settings-row:last-child { border-bottom:none; }
  ''',
  body='''      <div class="grid" style="grid-template-columns:1fr 1.6fr; gap:20px;">
        <div class="card fade-up text-center">
          <div class="avatar" style="width:84px; height:84px; font-size:28px; margin:0 auto 14px;">ET</div>
          <div class="h4">Emine Tekdemir</div>
          <p class="faint" style="font-size:13px;">eminetekdemir8821@gmail.com</p>
          <span class="badge badge-primary" style="margin-top:10px;">Level 7 · Pro Uye</span>
          <button class="btn btn-secondary" style="width:100%; margin-top:18px;">Fotografi Degistir</button>
        </div>
        <div>
          <div class="card fade-up delay-1" style="margin-bottom:16px;">
            <div class="h4" style="margin-bottom:6px;">Kisisel Bilgiler</div>
            <div class="settings-row"><span class="muted">Ad Soyad</span><span style="font-weight:600;">Emine Tekdemir</span></div>
            <div class="settings-row"><span class="muted">E-posta</span><span style="font-weight:600;">eminetekdemir8821@gmail.com</span></div>
            <div class="settings-row"><span class="muted">Hedef Rol</span><span style="font-weight:600;">Backend Developer</span></div>
          </div>
          <div class="card fade-up delay-2">
            <div class="h4" style="margin-bottom:6px;">Tercihler</div>
            <div class="settings-row"><span>E-posta bildirimleri</span><div class="switch active"></div></div>
            <div class="settings-row"><span>Gunluk hatirlatma</span><div class="switch active"></div></div>
            <div class="settings-row"><span>Karanlik mod</span><div class="switch theme-switch" onclick="toggleTheme()"></div></div>
            <div class="settings-row"><span>Sesli mulakat modu (varsayilan)</span><div class="switch"></div></div>
          </div>
        </div>
      </div>''',
)

# --------------------------------------------------------------- admin.html
page(
  "admin.html", "Admin Panel", "admin.html", "Admin Panel", "Platform yonetimi (demo — sadece goruntuleme)",
  extra_style='''
  .admin-row { display:grid; grid-template-columns:1fr 1fr 1fr 100px; align-items:center; gap:14px; padding:12px 6px; border-bottom:1px solid var(--border); font-size:13.5px; }
  ''',
  body='''      <div class="grid kpi-grid" style="grid-template-columns:repeat(4,1fr);">
        <div class="card kpi-card"><div class="kpi-label">Toplam Kullanici</div><div class="kpi-value">12.480</div></div>
        <div class="card kpi-card"><div class="kpi-label">Aktif Bugun</div><div class="kpi-value">1.920</div></div>
        <div class="card kpi-card"><div class="kpi-label">Toplam Mulakat</div><div class="kpi-value">88.300</div></div>
        <div class="card kpi-card"><div class="kpi-label">AI Maliyeti (Ay)</div><div class="kpi-value">$1.240</div></div>
      </div>
      <div class="card fade-up" style="margin-top:20px;">
        <div class="h4" style="margin-bottom:8px;">AI Model Konfigurasyonu</div>
        <div class="settings-row" style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border);"><span class="muted">Aktif Model</span><span class="tag">gemini-2.0-flash</span></div>
        <div class="settings-row" style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border);"><span class="muted">Gunluk Istek Limiti</span><span style="font-weight:600;">20.000</span></div>
        <div class="settings-row" style="display:flex; justify-content:space-between; padding:10px 0;"><span class="muted">Bugun Kullanilan</span><span style="font-weight:600;">14.220 (%71)</span></div>
      </div>
      <div class="card fade-up" style="margin-top:20px;">
        <div class="h4" style="margin-bottom:8px;">Son Kayitlar</div>
        <div class="admin-row" style="font-weight:700; color:var(--text-faint); font-size:12px; text-transform:uppercase;"><span>Kullanici</span><span>E-posta</span><span>Kayit Tarihi</span><span>Durum</span></div>
        <div class="admin-row"><span>Can K.</span><span class="faint">can@ornek.com</span><span class="faint">2 saat once</span><span class="badge badge-success">Aktif</span></div>
        <div class="admin-row"><span>Selin D.</span><span class="faint">selin@ornek.com</span><span class="faint">5 saat once</span><span class="badge badge-success">Aktif</span></div>
        <div class="admin-row"><span>Emine T.</span><span class="faint">eminetekdemir8821@gmail.com</span><span class="faint">1 gun once</span><span class="badge badge-success">Aktif</span></div>
      </div>''',
)

print("All pages generated.")
