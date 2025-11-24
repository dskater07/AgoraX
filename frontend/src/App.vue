<template>
  <div class="app">
    <header class="app-header">
      <h1>AgoraX – Sistema de Votación Electrónica</h1>
    </header>

    <main class="app-main">
      <Login
        v-if="!isAuthenticated"
        @login-success="handleLoginSuccess"
      />

      <section v-else class="layout">
        <div class="column">
          <h2>Votación</h2>
          <VotingPanel
            :meeting-id="meetingId"
            :token="token"
            @voted="handleVoted"
          />
        </div>

        <div class="column">
          <h2>Estado de quórum</h2>
          <Results
            :meeting-id="meetingId"
            :reload-trigger="reloadResults"
          />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Login from "./components/Login.vue";
import VotingPanel from "./components/VotingPanel.vue";
import Results from "./components/Results.vue";

const token = ref(localStorage.getItem("agorax_token") || "");
const isAuthenticated = ref(!!token.value);

// Por simplicidad, trabajamos con la asamblea #1
const meetingId = ref(1);

// Trigger para recargar resultados después de votar
const reloadResults = ref(0);

const handleLoginSuccess = (newToken) => {
  token.value = newToken;
  isAuthenticated.value = true;
  localStorage.setItem("agorax_token", newToken);
};

const handleVoted = () => {
  // Cada vez que se vote, incrementamos el trigger
  reloadResults.value++;
};
</script>

<style>
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
  background: #0f172a;
  color: #e5e7eb;
}

.app-header {
  background: #020617;
  padding: 1rem 2rem;
  border-bottom: 1px solid #1f2933;
}

.app-main {
  padding: 1.5rem 2rem;
}

.layout {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.column {
  flex: 1;
  min-width: 280px;
  background: #020617;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #1e293b;
}
</style>
