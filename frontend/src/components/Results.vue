<template>
  <div>
    <p v-if="loading">Cargando estado de quórum...</p>

    <div v-else-if="data">
      <p><strong>Presentes:</strong> {{ data.presentes }} / {{ data.total_propietarios }}</p>
      <p><strong>Quórum:</strong> {{ data.porcentaje_quorum }} % (mínimo {{ data.umbral_minimo }} %)</p>
      <p><strong>Estado:</strong> {{ data.estado }}</p>
    </div>

    <p v-else>No se pudo obtener información de quórum.</p>

    <button @click="load" :disabled="loading" class="reload">
      {{ loading ? "Actualizando..." : "Actualizar" }}
    </button>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";

const props = defineProps({
  meetingId: {
    type: Number,
    required: true
  },
  reloadTrigger: {
    type: Number,
    required: false,
    default: 0
  }
});

const data = ref(null);
const loading = ref(false);

const load = async () => {
  loading.value = true;
  try {
    const url = `http://localhost:8000/api/v1/quorum?meeting_id=${props.meetingId}`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error("Error cargando quórum");
    data.value = await resp.json();
  } catch (err) {
    console.error(err);
    data.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(load);

watch(
  () => props.reloadTrigger,
  () => {
    load();
  }
);
</script>

<style scoped>
.reload {
  margin-top: 1rem;
  padding: 0.35rem 0.7rem;
  border-radius: 0.5rem;
  border: 1px solid #334155;
  background: #020617;
  color: #e5e7eb;
  cursor: pointer;
}
</style>
