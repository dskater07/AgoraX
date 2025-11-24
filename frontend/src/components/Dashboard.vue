<template>
  <div style="padding: 22px; max-width: 1180px; margin: auto;">
    <div class="row" style="justify-content: space-between; margin-bottom: 16px;">
      <div>
        <h2 style="margin: 0;">Panel principal</h2>
        <p style="color: var(--muted); margin: 4px 0 0 0;">
          Bienvenido, {{ user?.name || "Propietario" }}
        </p>
      </div>
      <div class="row">
        <button class="btn" @click="$emit('go-admin')">Admin asamblea</button>
        <button class="btn ghost" @click="$emit('logout')">Salir</button>
      </div>
    </div>

    <div
      style="
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        margin-bottom: 16px;
      "
    >
      <div class="kpi">
        <h3>Quorum</h3>
        <div class="val">{{ quorum }}%</div>
      </div>
      <div class="kpi">
        <h3>Asistentes</h3>
        <div class="val">{{ attendants }}</div>
      </div>
      <div class="kpi">
        <h3>Votos hoy</h3>
        <div class="val">{{ votesToday }}</div>
      </div>
      <div class="kpi">
        <h3>Votaciones abiertas</h3>
        <div class="val">{{ openPolls }}</div>
      </div>
    </div>

    <div class="card">
      <div class="row" style="justify-content: space-between;">
        <strong>Agenda actual</strong>
        <span class="badge">Asamblea #AGX-2025-11</span>
      </div>
      <table class="table" style="margin-top: 10px;">
        <thead>
          <tr>
            <th>Punto</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in agenda" :key="item.id">
            <td>{{ item.title }}</td>
            <td style="color: var(--muted);">{{ item.desc }}</td>
            <td>
              <span
                class="badge"
                :style="{ borderColor: item.open ? 'var(--primary)' : '#1F2937' }"
              >
                {{ item.open ? "Abierta" : "Cerrada" }}
              </span>
            </td>
            <td class="row">
              <button
                class="btn"
                :disabled="!item.open"
                @click="$emit('go-vote', item)"
              >
                Ir a votar
              </button>
              <button class="btn" @click="$emit('go-results', item)">
                Ver resultados
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  user: { type: Object, default: null }
});

const quorum = ref(58);
const attendants = ref(126);
const votesToday = ref(344);
const openPolls = ref(2);
const agenda = ref([]);

onMounted(() => {
  agenda.value = [
    {
      id: 101,
      title: "Aprobación presupuesto",
      desc: "Presupuesto anual 2026",
      open: true
    },
    {
      id: 102,
      title: "Elección administrador",
      desc: "Periodo 2026-2027",
      open: false
    }
  ];
});
</script>

<style scoped>
.kpi {
  background: #0b1220;
  border: 1px solid #1f2937;
  border-radius: 12px;
  padding: 16px;
}
.kpi h3 {
  margin: 0 0 6px 0;
  color: var(--muted);
  font-weight: 600;
}
.kpi .val {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 0.5px;
}
</style>
