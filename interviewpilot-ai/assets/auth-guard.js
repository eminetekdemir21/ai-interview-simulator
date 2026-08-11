// Basit tek-kullanicili giris korumasi.
// Gercek dogrulama /api/login uzerinden sifre ile yapilir; burada sadece
// basarili girisin izini (localStorage) kontrol edip korumali sayfalara
// girisi engelliyoruz.
(function () {
  if (!localStorage.getItem("ip_authed")) {
    const next = encodeURIComponent(location.pathname.split("/").pop() || "dashboard.html");
    window.location.href = "login.html?next=" + next;
  }
})();

window.ipLogout = function () {
  localStorage.removeItem("ip_authed");
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
