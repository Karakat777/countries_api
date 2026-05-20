/* ═══════════════════════════════════════════════
   ATLAS — main.js
   1) Form validation (login + register)
   2) confirm() before delete
   3) fetch() live search on admin users table
   ═══════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {

  // ── 1. LOGIN FORM VALIDATION ──────────────────────────────────────
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      let valid = true;

      const username = document.getElementById("username");
      const password = document.getElementById("password");
      const uErr     = document.getElementById("username-error");
      const pErr     = document.getElementById("password-error");

      // reset
      [username, password].forEach(el => el.classList.remove("error"));
      uErr.textContent = "";
      pErr.textContent = "";

      if (!username.value.trim() || username.value.trim().length < 3) {
        username.classList.add("error");
        uErr.textContent = "Username must be at least 3 characters";
        valid = false;
      }
      if (!password.value || password.value.length < 6) {
        password.classList.add("error");
        pErr.textContent = "Password must be at least 6 characters";
        valid = false;
      }
      if (!valid) e.preventDefault();
    });
  }

  // ── 2. REGISTER FORM VALIDATION ───────────────────────────────────
  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      let valid = true;

      const username = document.getElementById("username");
      const password = document.getElementById("password");
      const uErr     = document.getElementById("username-error");
      const pErr     = document.getElementById("password-error");

      [username, password].forEach(el => el.classList.remove("error"));
      uErr.textContent = "";
      pErr.textContent = "";

      if (!username.value.trim() || username.value.trim().length < 3) {
        username.classList.add("error");
        uErr.textContent = "Username must be at least 3 characters";
        valid = false;
      }
      if (!password.value || password.value.length < 6) {
        password.classList.add("error");
        pErr.textContent = "Password must be at least 6 characters";
        valid = false;
      }
      if (!valid) e.preventDefault();
    });
  }

  // ── 3. CONFIRM BEFORE DELETE ──────────────────────────────────────
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      const confirmed = confirm("Are you sure you want to delete this user?\nThis will also remove all their records.");
      if (!confirmed) e.preventDefault();
    });
  });

  // ── 4. LIVE SEARCH (fetch) on admin users table ───────────────────
  const searchInput = document.getElementById("user-search");
  const tableBody   = document.getElementById("users-table-body");

  if (searchInput && tableBody) {
    searchInput.addEventListener("input", async function () {
      const query = this.value.trim();

      try {
        const res   = await fetch(`/api/users/search?q=${encodeURIComponent(query)}`);
        const users = await res.json();

        if (users.length === 0) {
          tableBody.innerHTML = `<tr><td colspan="5" class="empty-state">No users found.</td></tr>`;
          return;
        }

        tableBody.innerHTML = users.map(u => `
          <tr class="table-row" data-username="${u.username}">
            <td class="td-id">${u.id}</td>
            <td class="td-name">
              <div class="user-cell">
                <div class="user-avatar">${u.username[0].toUpperCase()}</div>
                ${u.username}
              </div>
            </td>
            <td><span class="role-pill role-pill--${u.role}">${u.role}</span></td>
            <td class="td-meta">${(u.created_at || '').slice(0, 10)}</td>
            <td>
              <form action="/admin/users/delete/${u.id}" method="POST" style="display:inline">
                <button type="submit" class="btn-delete delete-btn" title="Delete user">✕</button>
              </form>
            </td>
          </tr>
        `).join("");

        // переподвязываем confirm на новые кнопки
        tableBody.querySelectorAll(".delete-btn").forEach(btn => {
          btn.addEventListener("click", function (e) {
            if (!confirm("Are you sure you want to delete this user?\nThis will also remove all their records.")) {
              e.preventDefault();
            }
          });
        });

      } catch (err) {
        console.error("Search error:", err);
      }
    });
  }

});