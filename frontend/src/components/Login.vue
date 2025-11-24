<template>
  <div class="card" style="width: min(420px, 92vw);">
    <div style="text-align: center; margin-bottom: 18px;">
      <strong style="font-size: 24px; letter-spacing: 0.6px;">Iniciar sesión</strong>
      <div style="color: var(--muted); margin-top: 4px;">
        Accede a la asamblea electrónica
      </div>
    </div>

    <div style="margin-bottom: 10px;">
      <label class="label">Correo</label>
      <input
        class="input"
        v-model="email"
        type="email"
        placeholder="tu@correo.com"
      />
    </div>

    <div style="margin-bottom: 10px;">
      <label class="label">Contraseña</label>
      <input
        class="input"
        v-model="password"
        type="password"
        placeholder="********"
        @keyup.enter="submit"
      />
    </div>

    <div class="row" style="justify-content: space-between; margin-bottom: 12px;">
      <label style="color: var(--muted); font-size: 13px;">
        <input type="checkbox" v-model="remember" />
        Recordarme
      </label>
      <button class="link" type="button" @click="$emit('go-register')">
        Crear cuenta
      </button>
    </div>

    <button class="btn" style="width: 100%;" :disabled="loading" @click="submit">
      {{ loading ? "Ingresando..." : "Iniciar sesión" }}
    </button>

    <p v-if="error" style="color: var(--danger); margin-top: 8px;">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["login-success", "go-register"]);

const email = ref("");
const password = ref("");
const remember = ref(true);
const loading = ref(false);
const error = ref("");

async function submit() {
  error.value = "";
  if (!email.value || !password.value) {
    error.value = "Completa correo y contraseña.";
    return;
  }
  loading.value = true;
  try {
    // aquí conectarías con FastAPI /auth/login
    const mockUser = {
      name: "Propietario 101",
      role: "propietario",
      email: email.value
    };
    if (remember.value) {
      localStorage.setItem("agx_user", JSON.stringify(mockUser));
    }
    emit("login-success", mockUser);
  } catch (e) {
    error.value = "No se pudo iniciar sesión.";
  } finally {
    loading.value = false;
  }
}
</script>
