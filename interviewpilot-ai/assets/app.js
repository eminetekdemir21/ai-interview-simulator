/* ==========================================================================
   InterviewPilot AI — shared app logic (theme, mock data, small helpers)
   This is a design/UX prototype: data below is sample data for demonstration.
   ========================================================================== */

// ---------- Theme ----------
(function initTheme() {
  const saved = localStorage.getItem("ip_theme") || "light";
  document.documentElement.setAttribute("data-theme", saved);
})();

function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("ip_theme", next);
  document.querySelectorAll(".theme-switch").forEach(el => el.classList.toggle("on", next === "dark"));
}

document.addEventListener("DOMContentLoaded", () => {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  document.querySelectorAll(".theme-switch").forEach(el => el.classList.toggle("on", isDark));
});

// ---------- Company data (Company Interview Mode — flagship feature) ----------
const COMPANIES = [
  { id: "google", name: "Google", initials: "G", focus: ["Algoritmalar", "Veri Yapilari", "System Design"], difficulty: "Zor", color: "#4285F4", category: "tech" },
  { id: "microsoft", name: "Microsoft", initials: "MS", focus: ["C#", ".NET", "Azure", "OOP"], difficulty: "Orta-Zor", color: "#00A4EF", category: "tech" },
  { id: "amazon", name: "Amazon", initials: "A", focus: ["Leadership Principles", "Ownership", "Scalability"], difficulty: "Zor", color: "#FF9900", category: "tech" },
  { id: "meta", name: "Meta", initials: "M", focus: ["Coding", "Product Thinking", "System Design"], difficulty: "Zor", color: "#0668E1", category: "tech" },
  { id: "apple", name: "Apple", initials: "A", focus: ["Swift", "System Design", "Detay Odagi"], difficulty: "Zor", color: "#555555", category: "tech" },
  { id: "netflix", name: "Netflix", initials: "N", focus: ["Culture Fit", "Distributed Systems"], difficulty: "Zor", color: "#E50914", category: "tech" },
  { id: "tesla", name: "Tesla", initials: "T", focus: ["Engineering", "Optimizasyon"], difficulty: "Zor", color: "#CC0000", category: "tech" },
  { id: "openai", name: "OpenAI", initials: "AI", focus: ["Machine Learning", "LLM", "AI Ethics"], difficulty: "Cok Zor", color: "#10A37F", category: "tech" },
  { id: "nvidia", name: "NVIDIA", initials: "NV", focus: ["CUDA", "Parallel Computing"], difficulty: "Zor", color: "#76B900", category: "tech" },
  { id: "intel", name: "Intel", initials: "IN", focus: ["Computer Architecture", "C/C++"], difficulty: "Orta-Zor", color: "#0071C5", category: "tech" },
  { id: "ibm", name: "IBM", initials: "IB", focus: ["Enterprise Systems", "Cloud"], difficulty: "Orta", color: "#054ADA", category: "tech" },
  { id: "oracle", name: "Oracle", initials: "OR", focus: ["SQL", "Java", "Database Systems"], difficulty: "Orta", color: "#F80000", category: "tech" },
  { id: "spotify", name: "Spotify", initials: "SP", focus: ["Backend", "Microservices"], difficulty: "Orta-Zor", color: "#1DB954", category: "tech" },
  { id: "airbnb", name: "Airbnb", initials: "AB", focus: ["System Design", "Product Sense"], difficulty: "Zor", color: "#FF5A5F", category: "tech" },
  { id: "uber", name: "Uber", initials: "U", focus: ["System Design", "Scalability"], difficulty: "Zor", color: "#000000", category: "tech" },
  { id: "aselsan", name: "ASELSAN", initials: "AS", focus: ["Gomulu Sistemler", "C/C++", "RTOS", "Sinyal Isleme"], difficulty: "Zor", color: "#1F3B57", category: "defense" },
  { id: "havelsan", name: "HAVELSAN", initials: "HV", focus: ["Java", "Spring Boot", "Microservices"], difficulty: "Orta-Zor", color: "#0B4C8C", category: "defense" },
  { id: "tusas", name: "TUSAS", initials: "TA", focus: ["Havacilik Yazilimi", "Gomulu Sistemler"], difficulty: "Zor", color: "#12355B", category: "defense" },
  { id: "roketsan", name: "ROKETSAN", initials: "RK", focus: ["Savunma Yazilimi", "C++"], difficulty: "Zor", color: "#7A1F2B", category: "defense" },
  { id: "baykar", name: "Baykar", initials: "BK", focus: ["Gomulu Yazilim", "Computer Vision", "Otonom Sistemler"], difficulty: "Cok Zor", color: "#C8102E", category: "defense" },
  { id: "turkcell", name: "Turkcell", initials: "TC", focus: ["Java", "Spring Boot", "Kubernetes"], difficulty: "Orta", color: "#FFC72C", category: "telco" },
  { id: "turktelekom", name: "Turk Telekom", initials: "TT", focus: ["Cloud", "Network Systems"], difficulty: "Orta", color: "#6633CC", category: "telco" },
  { id: "garanti", name: "Garanti BBVA", initials: "GB", focus: [".NET", "SQL", "Bankacilik Sistemleri", "Guvenlik"], difficulty: "Orta-Zor", color: "#00A99D", category: "finance" },
  { id: "akbank", name: "Akbank", initials: "AK", focus: ["Java", "Bankacilik API'leri"], difficulty: "Orta", color: "#E4032E", category: "finance" },
  { id: "yapikredi", name: "Yapi Kredi", initials: "YK", focus: ["Backend", "Cloud"], difficulty: "Orta", color: "#003DA5", category: "finance" },
  { id: "isbankasi", name: "Is Bankasi", initials: "IB", focus: ["Java", "Enterprise Backend"], difficulty: "Orta", color: "#0033A0", category: "finance" },
  { id: "vakifbank", name: "VakifBank", initials: "VB", focus: [".NET", "SQL Server"], difficulty: "Orta", color: "#FFCB05", category: "finance" },
  { id: "ziraat", name: "Ziraat Bankasi", initials: "ZB", focus: ["Java", "Bankacilik Sistemleri"], difficulty: "Orta", color: "#00913A", category: "finance" },
];

// ---------- Mock analytics/dashboard data ----------
const MOCK = {
  user: { name: "Emine Tekdemir", role: "Backend Developer Adayi", level: "Level 7", xp: 3240, xpNext: 4000 },
  kpis: {
    todayGoal: { done: 1, target: 2 },
    streak: 6,
    avgScore: 78,
    totalInterviews: 34,
    weakestTopic: "System Design",
    strongestTopic: "REST API",
    jobMatchAvg: 82,
    level: 7,
  },
  weeklyScores: [62, 68, 71, 75, 70, 79, 78],
  weekLabels: ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"],
  radar: {
    labels: ["Teknik", "Iletisim", "Guven", "Problem Cozme", "Kodlama", "Sistem Tasarimi"],
    values: [78, 82, 70, 74, 80, 60],
  },
  recentInterviews: [
    { company: "Google", role: "Backend Developer", score: 82, date: "2 gun once", type: "Technical" },
    { company: "Amazon", role: "Backend Developer", score: 74, date: "4 gun once", type: "Behavioral" },
    { company: "ASELSAN", role: "Gomulu Yazilim", score: 69, date: "6 gun once", type: "Technical" },
    { company: "Microsoft", role: "Full Stack", score: 88, date: "1 hafta once", type: "Mixed" },
  ],
  achievements: [
    { icon: "🔥", name: "6 Gunluk Seri", desc: "Ust uste 6 gun pratik yaptin" },
    { icon: "🎯", name: "Keskin Nisanci", desc: "Bir mulakatta %90 uzeri skor" },
    { icon: "🚀", name: "Ilk Roket", desc: "Ilk mulakatini tamamladin" },
  ],
};
