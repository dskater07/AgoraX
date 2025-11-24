<template>
  <section class="card">
    <h2>Ingreso a AgoraX</h2>
    <form @submit.prevent="login">
      <label>
        Correo electrónico
        <input v-model="email" type="email" required />
      </label>

      <label>
        Contraseña
        <input v-model="password" type="password" required />
      </label>

      <button type="submit" :disabled="loading">
        {{ loading ? "Ingresando..." : "Ingresar" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["login-success"]);

const email = ref("admin@agorax.com");
const password = ref("admin");
const loading = ref(false);
const error = ref("");

const login = async () => {
  loading.value = true;
  error.value = "";

  try {
    const resp = await fetch("http://localhost:8000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    });

    if (!resp.ok) {
      throw new Error("Credenciales inválidas");
    }

    const data = await resp.json();
    if (!data.access_token) {
      throw new Error("Respuesta inválida del servidor");
    }

    emit("login-success", data.access_token);
  } catch (err) {
    error.value = err.message || "Error de autenticación";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.card {
  max-width: 360px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #020617;
  border-radius: 0.75rem;
  border: 1px solid #1e293b;
}

label {
  display: block;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.4rem 0.5rem;
  margin-top: 0.25rem;
  border-radius: 0.4rem;
  border: 1px solid #334155;
  background: #020617;
  color: #e5e7eb;
}

button {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background: #22c55e;
  color: #020617;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.7;
  cursor: wait;
}

.error {
  margin-top: 0.5rem;
  color: #f97373;
  font-size: 0.85rem;
}
</style>
