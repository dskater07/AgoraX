<template>
  <div class="app-root">
    <header class="app-header">
      <div class="header-left">
        <div class="logo-dot"></div>
        <strong>AgoraX</strong>
        <span class="badge">Sistema de votación electrónica</span>
      </div>

      <div class="header-right" v-if="currentView !== 'login' && currentView !== 'register'">
        <span class="user-label">
          Sesión: {{ user?.name || "Invitado" }}
        </span>
        <button class="btn ghost" @click="goDashboard" v-if="currentView !== 'dashboard'">
          Ir al dashboard
        </button>
        <button class="btn ghost" @click="logout">Salir</button>
      </div>
    </header>

    <main class="app-main">
      <!-- LOGIN -->
      <Login
        v-if="currentView === 'login'"
        @login-success="onLoginSuccess"
        @go-register="goRegister"
      />

      <!-- REGISTRO -->
      <Register
        v-else-if="currentView === 'register'"
        @registered="goLogin"
        @back-login="goLogin"
      />

      <!-- DASHBOARD -->
      <Dashboard
        v-else-if="currentView === 'dashboard'"
        :user="user"
        @go-vote="openVote"
        @go-results="openResults"
        @go-admin="goAdmin"
        @logout="logout"
      />

      <!-- VOTAR -->
      <VotingPanel
        v-else-if="currentView === 'voting'"
        :meeting-id="meetingId"
        :meeting-title="meetingTitle"
        @back-dashboard="goDashboard"
        @show-results="openResultsFromVote"
      />

      <!-- ADMIN -->
      <Admin
        v-else-if="currentView === 'admin'"
        @back-dashboard="goDashboard"
      />

      <!-- RESULTADOS -->
      <Results
        v-else-if="currentView === 'results'"
        :meeting-id="meetingId"
        @back-dashboard="goDashboard"
      />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import Dashboard from "./components/Dashboard.vue";
import VotingPanel from "./components/VotingPanel.vue";
import Admin from "./components/Admin.vue";
import Results from "./components/Results.vue";

const currentView = ref("login"); // login | register | dashboard | voting | admin | results
const user = ref(null);
const meetingId = ref(101);
const meetingTitle = ref("Aprobación presupuesto 2026");

function onLoginSuccess(u) {
  user.value = u;
  currentView.value = "dashboard";
}

function goRegister() {
  currentView.value = "register";
}
function goLogin() {
  currentView.value = "login";
}

function goDashboard() {
  currentView.value = "dashboard";
}

function openVote(meeting) {
  meetingId.value = meeting.id;
  meetingTitle.value = meeting.title;
  currentView.value = "voting";
}

function openResults(meeting) {
  meetingId.value = meeting.id;
  meetingTitle.value = meeting.title;
  currentView.value = "results";
}

function openResultsFromVote() {
  currentView.value = "results";
}

function goAdmin() {
  currentView.value = "admin";
}

function logout() {
  user.value = null;
  localStorage.removeItem("agx_user");
  currentView.value = "login";
}
</script>

<style>
:root {
  --bg: #0d1117;
  --surface: #111827;
  --text: #e6e6e6;
  --muted: #9ca3af;
  --primary: #00cfff;
  --danger: #ef4444;
  --success: #10b981;
  --border: rgba(0, 207, 255, 0.22);
  --glow: 0 0 18px rgba(0, 207, 255, 0.25);
}

html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  background: radial-gradient(
      1200px 800px at 85% -10%,
      rgba(0, 207, 255, 0.1),
      transparent 40%
    ),
    var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Ubuntu, Arial;
}

.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 10px 20px;
  background: #0b1220;
  border-bottom: 1px solid #1f2937;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--primary);
  box-shadow: var(--glow);
}

.badge {
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid #1f2937;
  background: #0b1220;
  color: var(--muted);
  font-size: 12px;
}

.user-label {
  font-size: 13px;
  color: var(--muted);
}

.app-main {
  flex: 1;
  display: grid;
  place-items: center;
  padding: 24px 12px;
}

/* utilidades compartidas */

.card {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.03),
    rgba(255, 255, 255, 0.01)
  );
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: var(--glow);
  padding: 20px;
}

.input,
.select {
  width: 100%;
  padding: 12px 14px;
  background: #0b1220;
  color: var(--text);
  border: 1px solid #1f2937;
  border-radius: 10px;
  outline: none;
}
.input:focus,
.select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(0, 207, 255, 0.08);
}

.label {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 6px;
  display: block;
}

.btn {
  background: linear-gradient(
    180deg,
    rgba(0, 207, 255, 0.25),
    rgba(0, 207, 255, 0.12)
  );
  border: 1px solid var(--primary);
  color: var(--text);
  padding: 10px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.2s ease;
  font-size: 14px;
}
.btn:hover {
  box-shadow: var(--glow);
  transform: translateY(-1px);
}
.btn.ghost {
  background: transparent;
  border-color: #1f2937;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.link {
  color: var(--primary);
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}

.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  padding: 10px 12px;
  border-bottom: 1px solid #1f2937;
  text-align: left;
}
</style>
