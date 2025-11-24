<template>
  <div class="card" style="width: min(640px, 95vw);">
    <h2 style="margin-top: 0;">Votación: {{ meetingTitle }}</h2>
    <p style="color: var(--muted); margin-top: 4px;">
      Se vota el presupuesto anual del conjunto residencial.
    </p>

    <div style="margin: 16px 0;">
      <label class="row" style="justify-content: flex-start; gap: 10px;">
        <input type="radio" value="SI" v-model="choice" />
        Sí
      </label>
      <label class="row" style="justify-content: flex-start; gap: 10px;">
        <input type="radio" value="NO" v-model="choice" />
        No
      </label>
      <label class="row" style="justify-content: flex-start; gap: 10px;">
        <input type="radio" value="ABSTENCION" v-model="choice" />
        Abstención
      </label>
    </div>

    <div class="row" style="justify-content: space-between; margin-top: 8px;">
      <span class="badge">Quorum actual: {{ quorum }}%</span>
      <span class="badge">Tiempo restante: {{ timeLeft }}</span>
    </div>

    <div class="row" style="margin-top: 16px; justify-content: flex-end; gap: 8px;">
      <button class="btn ghost" @click="$emit('back-dashboard')">
        Volver al dashboard
      </button>
      <button
        class="btn"
        :disabled="sending || !choice || voted"
        @click="sendVote"
      >
        {{ voted ? "Voto registrado" : sending ? "Enviando..." : "Enviar voto" }}
      </button>
      <button class="btn ghost" @click="$emit('show-results')">
        Ver resultados
      </button>
    </div>

    <p v-if="error" style="color: var(--danger); margin-top: 10px;">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  meetingId: { type: [Number, String], required: true },
  meetingTitle: { type: String, default: "Aprobación presupuesto 2026" }
});

const quorum = ref(58);
const timeLeft = ref("03:12");
const choice = ref("");
const sending = ref(false);
const voted = ref(false);
const error = ref("");

async function sendVote() {
  error.value = "";
  if (!choice.value) return;
  sending.value = true;
  try {
    // POST /votes/{meetingId}
    // await api.post(`/votes/${props.meetingId}`, { option: choice.value });
    voted.value = true;
  } catch (e) {
    error.value = "No se pudo registrar tu voto.";
  } finally {
    sending.value = false;
  }
}
</script>
