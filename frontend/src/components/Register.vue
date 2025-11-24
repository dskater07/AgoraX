<template>
  <div class="card" style="width: min(520px, 92vw);">
    <h2 style="margin: 0 0 12px 0;">Crear cuenta</h2>

    <div style="margin-bottom: 10px;">
      <label class="label">Nombre completo</label>
      <input class="input" v-model="fullName" placeholder="Jane Doe" />
    </div>

    <div class="row" style="gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
      <div style="flex: 1; min-width: 180px;">
        <label class="label">Correo</label>
        <input class="input" v-model="email" type="email" placeholder="jane@correo.com" />
      </div>
      <div style="flex: 1; min-width: 180px;">
        <label class="label">Contraseña</label>
        <input class="input" v-model="password" type="password" placeholder="********" />
      </div>
    </div>

    <div style="margin-bottom: 14px;">
      <label class="label">Rol</label>
      <select class="select" v-model="role">
        <option value="propietario">Propietario</option>
        <option value="admin">Administrador</option>
      </select>
    </div>

    <div class="row" style="justify-content: space-between; margin-top: 4px;">
      <button class="btn" :disabled="loading" @click="register">
        {{ loading ? "Registrando..." : "Crear cuenta" }}
      </button>
      <button class="link" type="button" @click="$emit('back-login')">
        Ya tengo cuenta
      </button>
    </div>

    <p v-if="error" style="color: var(--danger); margin-top: 8px;">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["registered", "back-login"]);

const fullName = ref("");
const email = ref("");
const password = ref("");
const role = ref("propietario");
const loading = ref(false);
const error = ref("");

async function register() {
  error.value = "";
  if (!fullName.value || !email.value || !password.value) {
    error.value = "Completa todos los campos.";
    return;
  }
  loading.value = true;
  try {
    // aquí iría POST /auth/register
    alert("Cuenta creada (demo). Ahora inicia sesión.");
    emit("registered");
  } catch (e) {
    error.value = "No se pudo registrar.";
  } finally {
    loading.value = false;
  }
}
</script>
