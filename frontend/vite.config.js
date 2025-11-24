// frontend/vite.config.js
//
// Configuración de Vite para Vue 3.
// Expone el servidor en 0.0.0.0:5173 para que Docker lo pueda mapear.

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5173
  },
  // Podemos usar VITE_API_BASE_URL para apuntar al backend
  // Ejemplo: VITE_API_BASE_URL=http://localhost:8000
});
