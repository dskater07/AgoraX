<template>
  <div class="card" style="width: min(900px, 96vw);">
    <div class="row" style="justify-content: space-between; margin-bottom: 12px;">
      <div>
        <h2 style="margin: 0;">Resultados de la votación</h2>
        <span class="badge">Asamblea #{{ meetingId }}</span>
      </div>
      <button class="btn ghost" @click="$emit('back-dashboard')">
        Volver al dashboard
      </button>
    </div>

    <div
      style="
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 16px;
      "
    >
      <div class="kpi">
        <h3>SÍ</h3>
        <div class="val">{{ counts.si }}</div>
      </div>
      <div class="kpi">
        <h3>NO</h3>
        <div class="val">{{ counts.no }}</div>
      </div>
      <div class="kpi">
        <h3>ABST.</h3>
        <div class="val">{{ counts.abs }}</div>
      </div>
    </div>

    <div class="card" style="margin-top: 0; padding: 16px;">
      <div class="row" style="justify-content: space-between;">
        <strong>Auditoría (muestra)</strong>
        <button class="btn" @click="signActa">Firmar electrónicamente</button>
      </div>
      <table class="table" style="margin-top: 10px;">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Opción</th>
            <th>IP</th>
            <th>Fecha/Hora</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in audit" :key="idx">
            <td>{{ row.user }}</td>
            <td>{{ row.option }}</td>
            <td style="color: var(--muted);">{{ row.ip }}</td>
            <td style="color: var(--muted);">{{ row.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  meetingId: { type: [String, Number], required: true }
});

const counts = ref({ si: 230, no: 88, abs: 26 });
const audit = ref([]);

onMounted(() => {
  audit.value = [
    {
      user: "prop_102",
      option: "SI",
      ip: "181.55.102.21",
      timestamp: "2025-11-10 14:22"
    },
    {
      user: "prop_077",
      option: "NO",
      ip: "179.23.40.9",
      timestamp: "2025-11-10 14:23"
    }
  ];
});

function signActa() {
  alert("Acta firmada electrónicamente (demo).");
}
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
