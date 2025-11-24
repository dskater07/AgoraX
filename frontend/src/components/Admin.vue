<template>
  <div class="card" style="max-width: 900px; width: 100%;">
    <div class="row" style="justify-content: space-between; margin-bottom: 12px;">
      <h2 style="margin: 0;">Administración de asamblea</h2>
      <button class="btn ghost" @click="$emit('back-dashboard')">
        Volver al dashboard
      </button>
    </div>

    <div class="row" style="gap: 16px; flex-wrap: wrap; margin-bottom: 12px;">
      <div style="flex: 1; min-width: 260px;">
        <label class="label">Título</label>
        <input
          class="input"
          v-model="form.title"
          placeholder="Asamblea Ordinaria 2026"
        />
      </div>
      <div style="width: 200px;">
        <label class="label">Quorum mínimo (%)</label>
        <input
          class="input"
          type="number"
          min="0"
          max="100"
          v-model.number="form.quorumMin"
        />
      </div>
      <div>
        <button class="btn" @click="createMeeting">Crear asamblea</button>
      </div>
    </div>

    <label class="label">Puntos de agenda</label>
    <div class="row" style="margin-bottom: 8px;">
      <input
        class="input"
        v-model="newItem"
        placeholder="Ej: Aprobación presupuesto"
        style="flex: 1;"
      />
      <button class="btn" @click="addItem">Agregar</button>
    </div>

    <ul style="list-style: none; padding: 0; margin: 0;">
      <li
        v-for="(p, idx) in form.items"
        :key="idx"
        class="row"
        style="justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1f2937;"
      >
        <span>
          {{ p.title }}
          <span
            v-if="p.open"
            class="badge"
            style="margin-left: 8px; border-color: var(--primary);"
          >
            Abierta
          </span>
        </span>
        <span class="row">
          <button class="btn" @click="toggleOpen(idx)">
            {{ p.open ? "Cerrar" : "Abrir" }}
          </button>
        </span>
      </li>
    </ul>

    <div style="text-align: right; margin-top: 12px;">
      <button class="btn" :disabled="!form.items.length" @click="generateActa">
        Generar acta
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";

const form = reactive({
  title: "",
  quorumMin: 51,
  items: []
});
const newItem = ref("");

function addItem() {
  if (!newItem.value.trim()) return;
  form.items.push({
    title: newItem.value.trim(),
    open: false,
    meetingId: Math.floor(Math.random() * 1000)
  });
  newItem.value = "";
}

function toggleOpen(idx) {
  // RB-02: cerrar un punto al abrir otro
  form.items = form.items.map((it, i) => ({
    ...it,
    open: i === idx ? !it.open : false
  }));
}

function createMeeting() {
  if (!form.title.trim()) {
    alert("Ingresa un título para la asamblea.");
    return;
  }
  // POST /meetings
  alert("Asamblea creada (demo).");
}

function generateActa() {
  // POST /reports/acta
  alert("Acta generada (demo).");
}
</script>
