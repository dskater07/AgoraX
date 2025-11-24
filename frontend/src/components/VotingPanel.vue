<script setup>
/**
 * VotingPanel.vue
 *
 * Panel principal de votación:
 * - Lista asambleas.
 * - Muestra puntos de agenda de la asamblea seleccionada.
 * - Permite registrar presencia (RB-03).
 * - Permite emitir voto sobre un punto (RD-01, RD-03, RD-08, etc.).
 */

import { ref, onMounted, watch } from "vue";
import axios from "axios";

const props = defineProps({
  apiBaseUrl: {
    type: String,
    required: true
  },
  token: {
    type: String,
    required: true
  }
});

const emit = defineEmits(["selection-changed"]);

const meetings = ref([]);
const selectedMeetingId = ref(null);
const meetingDetail = ref(null);

const selectedAgendaItemId = ref(null);
const voteOption = ref("");

const ownerId = ref("");
const coeficiente = ref("");

const loadingMeetings = ref(false);
const loadingDetail = ref(false);
const voting = ref(false);
const presenceRegistering = ref(false);

const msgSuccess = ref("");
const msgError = ref("");

const authHeaders = () => ({
  Authorization: `Bearer ${props.token}`
});

/**
 * Carga las asambleas disponibles.
 */
async function fetchMeetings() {
  loadingMeetings.value = true;
  msgError.value = "";
  try {
    const { data } = await axios.get(
      `${props.apiBaseUrl}/api/v1/meetings`,
      { headers: authHeaders() }
    );
    meetings.value = data;
  } catch (err) {
    msgError.value =
      err?.response?.data?.detail ||
      "No fue posible cargar las asambleas disponibles.";
  } finally {
    loadingMeetings.value = false;
  }
}

/**
 * Cuando el usuario elige una asamblea, cargamos su detalle (agenda).
 */
async function fetchMeetingDetail() {
  if (!selectedMeetingId.value) {
    meetingDetail.value = null;
    selectedAgendaItemId.value = null;
    emitSelectionChanged();
    return;
  }

  loadingDetail.value = true;
  msgError.value = "";
  try {
    const { data } = await axios.get(
      `${props.apiBaseUrl}/api/v1/meetings/${selectedMeetingId.value}`,
      { headers: authHeaders() }
    );
    meetingDetail.value = data;

    // Reset de selección de punto al cambiar de asamblea
    selectedAgendaItemId.value = null;
    emitSelectionChanged();
  } catch (err) {
    msgError.value =
      err?.response?.data?.detail ||
      "No fue posible cargar el detalle de la asamblea.";
  } finally {
    loadingDetail.value = false;
  }
}

/**
 * Emite hacia App la selección actual para que Results pueda usarla.
 */
function emitSelectionChanged() {
  emit("selection-changed", {
    meetingId: selectedMeetingId.value,
    agendaItemId: selectedAgendaItemId.value
  });
}

/**
 * Registra asistencia de un propietario a la asamblea actual.
 * Aquí, por simplicidad, el usuario ingresa manualmente:
 *  - ownerId
 *  - coeficiente
 */
async function registerPresence() {
  msgSuccess.value = "";
  msgError.value = "";
  presenceRegistering.value = true;

  try {
    if (!selectedMeetingId.value) {
      throw new Error("Debes seleccionar una asamblea primero.");
    }

    if (!ownerId.value || !coeficiente.value) {
      throw new Error("Completa ownerId y coeficiente para registrar presencia.");
    }

    const payload = {
      owner_id: Number(ownerId.value),
      meeting_id: Number(selectedMeetingId.value),
      coeficiente: Number(coeficiente.value)
    };

    await axios.post(
      `${props.apiBaseUrl}/api/v1/meetings/${selectedMeetingId.value}/presence`,
      payload,
      { headers: authHeaders() }
    );

    msgSuccess.value = "Presencia registrada correctamente.";
  } catch (err) {
    msgError.value =
      err?.response?.data?.detail || err.message || "Error al registrar presencia.";
  } finally {
    presenceRegistering.value = false;
  }
}

/**
 * Emite un voto sobre un punto de la agenda.
 */
async function castVote() {
  msgSuccess.value = "";
  msgError.value = "";
  voting.value = true;

  try {
    if (!selectedMeetingId.value || !selectedAgendaItemId.value) {
      throw new Error("Selecciona asamblea y punto de agenda antes de votar.");
    }
    if (!voteOption.value) {
      throw new Error("Escribe la opción de voto (ejemplo: 'Sí', 'No').");
    }

    const payload = {
      agenda_item_id: selectedAgendaItemId.value,
      value: voteOption.value,
      ip_address: null
    };

    const url = `${props.apiBaseUrl}/api/v1/votes/${selectedMeetingId.value}/agenda/${selectedAgendaItemId.value}`;

    await axios.post(url, payload, { headers: authHeaders() });

    msgSuccess.value = "Voto registrado correctamente.";
    voteOption.value = "";

    // Notificamos al componente padre para que Results se actualice
    emitSelectionChanged();
  } catch (err) {
    msgError.value =
      err?.response?.data?.detail || err.message || "No fue posible registrar el voto.";
  } finally {
    voting.value = false;
  }
}

onMounted(() => {
  fetchMeetings();
});

// Emitir siempre que cambie agenda seleccionada
watch(selectedAgendaItemId, () => emitSelectionChanged());
</script>

<template>
  <div>
    <!-- Selección de Asamblea -->
    <div class="form-field">
      <label class="form-label">Asamblea</label>
      <select
        v-model="selectedMeetingId"
        class="form-select"
        @change="fetchMeetingDetail"
      >
        <option value="">Selecciona una asamblea</option>
        <option
          v-for="m in meetings"
          :key="m.id"
          :value="m.id"
        >
          {{ m.title }} · {{ new Date(m.date).toLocaleString() }} · {{ m.status }}
        </option>
      </select>
      <div v-if="loadingMeetings" class="msg">Cargando asambleas...</div>
    </div>

    <!-- Campos para registrar presencia -->
    <div
      v-if="selectedMeetingId"
      style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 6px;"
    >
      <div class="form-field">
        <label class="form-label">ID Propietario (owner_id)</label>
        <input
          v-model="ownerId"
          type="number"
          class="form-input"
          placeholder="Ej: 1"
        />
      </div>
      <div class="form-field">
        <label class="form-label">Coeficiente</label>
        <input
          v-model="coeficiente"
          type="number"
          step="0.01"
          class="form-input"
          placeholder="Ej: 10.5"
        />
      </div>
    </div>

    <button
      v-if="selectedMeetingId"
      class="btn btn-ghost"
      style="margin-top: 4px;"
      :disabled="presenceRegistering"
      @click="registerPresence"
    >
      {{ presenceRegistering ? "Registrando..." : "Registrar asistencia" }}
    </button>

    <!-- Detalle de agenda -->
    <div v-if="loadingDetail" class="msg" style="margin-top: 10px;">
      Cargando detalle de la asamblea...
    </div>

    <div v-if="meetingDetail" style="margin-top: 10px;">
      <div class="tag" style="margin-bottom: 10px;">
        <span class="tag-dot" />
        {{ meetingDetail.title }} · Estado: {{ meetingDetail.status }}
      </div>

      <div class="form-field">
        <label class="form-label">Punto de agenda</label>
        <select
          v-model="selectedAgendaItemId"
          class="form-select"
        >
          <option value="">Selecciona un punto</option>
          <option
            v-for="item in meetingDetail.agenda_items"
            :key="item.id"
            :value="item.id"
          >
            {{ item.title }} · {{ item.status }}
          </option>
        </select>
      </div>
    </div>

    <!-- Emisión de voto -->
    <div v-if="selectedAgendaItemId" style="margin-top: 10px;">
      <div class="form-field">
        <label class="form-label">Opción de voto</label>
        <input
          v-model="voteOption"
          type="text"
          class="form-input"
          placeholder="Ejemplo: 'Sí', 'No', 'En blanco'"
        />
      </div>

      <button
        class="btn btn-primary"
        :disabled="voting"
        @click="castVote"
      >
        {{ voting ? "Enviando voto..." : "Emitir voto" }}
      </button>
    </div>

    <!-- Mensajes -->
    <div v-if="msgSuccess" class="msg msg-success">
      {{ msgSuccess }}
    </div>
    <div v-if="msgError" class="msg msg-error">
      {{ msgError }}
    </div>
  </div>
</template>
