// Gercek coklu kullanici oturum korumasi.
// Dogrulama sunucu tarafinda httpOnly cerez (ip_session) ile yapilir.
// Bu script her korumali sayfada /api/me'yi kontrol eder; oturum yoksa
// giris sayfasina yonlendirir. Kontrol bitene kadar sayfa gizli kalir.
document.documentElement.style.visibility = "hidden";

window.ipCurrentUser = null;

(async function () {
  try {
    const r = await fetch("/api/me", { credentials: "same-origin" });
    if (!r.ok) throw new Error("unauthorized");
    window.ipCurrentUser = await r.json();
    document.documentElement.style.visibility = "";
    document.dispatchEvent(new CustomEvent("ip-auth-ready", { detail: window.ipCurrentUser }));
  } catch (e) {
    const next = encodeURIComponent(location.pathname.split("/").pop() || "dashboard.html");
    window.location.href = "login.html?next=" + next;
  }
})();

window.ipLogout = async function () {
  try {
    await fetch("/api/logout", { method: "POST", credentials: "same-origin" });
  } catch (e) {
    // yoksay, yine de giris sayfasina don
  }
  window.location.href = "login.html";
};

document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  if (!sidebar || sidebar.querySelector("[data-logout]")) return;
  const link = document.createElement("a");
  link.className = "side-link";
  link.href = "#";
  link.setAttribute("data-logout", "1");
  link.innerHTML = '<span class="icon-box"><i data-lucide="log-out" style="width:17px"></i></span>Cikis Yap';
  link.addEventListener("click", function (e) {
    e.preventDefault();
    window.ipLogout();
  });
  sidebar.appendChild(link);
  if (window.lucide) window.lucide.createIcons();
});
