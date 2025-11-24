<template>
  <div>
    <p><strong>Asamblea ID:</strong> {{ meetingId }}</p>

    <div class="buttons">
      <button @click="vote('Sí')" :disabled="loading">Sí</button>
      <button @click="vote('No')" :disabled="loading">No</button>
      <button @click="vote('Abstención')" :disabled="loading">
        Abstención
      </button>
    </div>

    <p v-if="message" :class="{'ok': success, 'error': !success}">
      {{ message }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  meetingId: {
    type: Number,
    required: true
  },
  token: {
    type: String,
    required: true
  }
});

const emit = defineEmits(["voted"]);

const loading = ref(false);
const message = ref("");
const success = ref(false);

const vote = async (option) => {
  loading.value = true;
  message.value = "";
  success.value = false;

  try {
    const resp = await fetch("http://localhost:8000/api/v1/votes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${props.token}`
      },
      body: JSON.stringify({
        meeting_id: props.meetingId,
        vote_option: option
      })
    });

    if (!resp.ok) {
      throw new Error("Error al registrar voto");
    }

    const data = await resp.json();
    message.value = data.message || "Voto registrado correctamente";
    success.value = true;
    emit("voted");
  } catch (err) {
    message.value = err.message || "No se pudo registrar el voto";
    success.value = false;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.buttons {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
}
button {
  flex: 1;
  padding: 0.4rem 0.6rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
button:nth-child(1) {
  background: #22c55e;
  color: #020617;
}
button:nth-child(2) {
  background: #ef4444;
  color: #f9fafb;
}
button:nth-child(3) {
  background: #f59e0b;
  color: #020617;
}
.ok {
  color: #4ade80;
}
.error {
  color: #f97373;
}
</style>
