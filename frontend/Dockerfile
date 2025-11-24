# ============================================================
# Frontend AgoraX - Vue 3 + Vite
# Se ejecuta SOLO dentro de Docker, sin npm local
# ============================================================

FROM node:20-alpine

WORKDIR /app

# Copiamos definiciones de dependencias
COPY package.json ./

# Instalamos dependencias dentro del contenedor
RUN npm install

# Copiamos el resto del frontend
COPY . .

# Vite dev server
EXPOSE 5173

# Ejecutamos Vite en modo dev, accesible desde el host
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
