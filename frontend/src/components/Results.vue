<script setup>
/**
 * Results.vue
 *
 * Muestra resultados básicos para el punto de agenda seleccionado:
 * - Lista de votos (solo metadatos, NO el valor real, por confidencialidad).
 * - Conteo total de votos.
 *
 * Nota:
 * El backend actual devuelve VoteResponse sin el contenido del voto
 * (value_encrypted). Por eso aquí nos centramos en:
 *  - cuántos votos hay
 *  - quién votó (owner_id) y cuándo
 */

import { ref, watch } from "vue";
import axios from "axios";

const props = defineProps({
  apiBaseUrl: {
    type: String,
    required: true
  },
  token: {
    type: String,
    required: true
  },
  meetingId: {
    type: Number,
    default: null
  },
  agendaItemId: {
    type: Number,
    default: null
  }
});

const votes = ref([]);
const loading = ref(false);
const errorMsg = ref("");

const authHeaders = () => ({
  Authorization: `Bearer ${props.token}`
});

/**
 * Carga los votos para el punto de agenda seleccionado.
 */
async function fetchVotes() {
  votes.value = [];
  errorMsg.value = "";

  if (!props.meetingId || !props.agendaItemId) {
    return;
  }

  loading.value = true;
  try {
    const url = `${props.apiBaseUrl}/api/v1/votes/${props.meetingId}/agenda/${props.agendaItemId}`;
    const { data } = await axios.get(url, { headers: authHeaders() });
    votes.value = data;
  } catch (err) {
    errorMsg.value =
      err?.response?.data?.detail ||
      "No fue posible obtener los votos para este punto.";
  } finally {
    loading.value = false;
  }
}

/**
 * Se dispara cuando cambian meetingId o agendaItemId.
 */
watch(
  () => [props.meetingId, props.agendaItemId],
  () => {
    fetchVotes();
  }
);
</script>

<template>
  <div>
    <div v-if="!meetingId || !agendaItemId" class="msg">
      Selecciona una asamblea y un punto de agenda para ver los resultados.
    </div>

    <div v-else>
      <div class="tag" style="margin-bottom: 10px;">
        <span class="tag-dot" />
        Punto seleccionado · Meeting ID: {{ meetingId }} · Agenda ID:
        {{ agendaItemId }}
      </div>

      <div v-if="loading" class="msg">Cargando votos...</div>

      <div v-if="errorMsg" class="msg msg-error">
        {{ errorMsg }}
      </div>

      <div v-if="!loading && !errorMsg">
        <p class="msg">
          <strong>Total de votos registrados:</strong> {{ votes.length }}
        </p>

        <ul v-if="votes.length" class="list">
          <li
            v-for="v in votes"
            :key="v.id"
            class="list-item"
          >
            <span>
              <span class="chip-small">Voto #{{ v.id }}</span>
              &nbsp; owner_id={{ v.owner_id }}
            </span>
            <span class="chip-small">
              {{ new Date(v.created_at).toLocaleString() }}
            </span>
          </li>
        </ul>

        <p v-else class="msg">
          Aún no hay votos registrados para este punto de agenda.
        </p>
      </div>
    </div>
  </div>
</template>
