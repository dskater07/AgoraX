<script setup>
/**
 * Componente raíz de AgoraX.
 *
 * Responsabilidades:
 * - Gestionar el estado global de autenticación (token + usuario).
 * - Controlar qué se ve: Login vs Panel de Votación + Resultados.
 * - Compartir selección de reunión/punto entre VotingPanel y Results.
 */

import { ref } from "vue";
import Login from "./components/Login.vue";
import VotingPanel from "./components/VotingPanel.vue";
import Results from "./components/Results.vue";

// Base del backend: se puede sobreescribir con VITE_API_BASE_URL
const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const token = ref(localStorage.getItem("agx_token") || "");
const currentUserEmail = ref(localStorage.getItem("agx_user_email") || "");

// Selección actual de asamblea/punto para compartir con Results
const selectedMeetingId = ref(null);
const selectedAgendaItemId = ref(null);

/**
 * Maneja login exitoso, guarda token en memoria y localStorage.
 */
function handleLoginSuccess(payload) {
  token.value = payload.token;
  currentUserEmail.value = payload.email;
  localStorage.setItem("agx_token", payload.token);
  localStorage.setItem("agx_user_email", payload.email);
}

/**
 * Permite que VotingPanel notifique qué punto está seleccionado.
 */
function handleSelectionChanged(selection) {
  selectedMeetingId.value = selection.meetingId;
  selectedAgendaItemId.value = selection.agendaItemId;
}

/**
 * Limpia sesión local.
 */
function handleLogout() {
  token.value = "";
  currentUserEmail.value = "";
  selectedMeetingId.value = null;
  selectedAgendaItemId.value = null;
  localStorage.removeItem("agx_token");
  localStorage.removeItem("agx_user_email");
}
</script>

<template>
  <div class="app-shell">
    <!-- HEADER -->
    <header class="app-header">
      <div class="app-header-left">
        <div class="app-title">AgoraX</div>
        <div class="app-subtitle">
          Sistema de votación electrónica para Asambleas de Conjuntos
          Residenciales
        </div>
      </div>

      <div class="app-header-right">
        <span class="chip">Proyecto ITM · Calidad del Software</span>
        <template v-if="token">
          <span class="tag">
            <span class="tag-dot" /> {{ currentUserEmail }}
          </span>
          <button class="btn btn-ghost" @click="handleLogout">
            Cerrar sesión
          </button>
        </template>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="app-main">
      <!-- Si NO hay token, mostramos solo Login -->
      <div v-if="!token" class="layout-grid">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Ingreso a AgoraX</div>
              <div class="card-subtitle">
                Autentícate para participar en la asamblea.
              </div>
            </div>
          </div>
          <Login :api-base-url="apiBaseUrl" @login-success="handleLoginSuccess" />
        </div>
      </div>

      <!-- Si hay token, mostramos Panel + Resultados -->
      <div v-else class="layout-grid">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Panel de Votación</div>
              <div class="card-subtitle">
                Selecciona la asamblea, registra asistencia y emite tu voto.
              </div>
            </div>
            <span class="badge">Votación activa</span>
          </div>
          <VotingPanel
            :api-base-url="apiBaseUrl"
            :token="token"
            @selection-changed="handleSelectionChanged"
          />
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Resultados y Actividad</div>
              <div class="card-subtitle">
                Resumen de votos registrados por punto de agenda.
              </div>
            </div>
          </div>
          <Results
            :api-base-url="apiBaseUrl"
            :token="token"
            :meeting-id="selectedMeetingId"
            :agenda-item-id="selectedAgendaItemId"
          />
        </div>
      </div>
    </main>
  </div>
</template>
