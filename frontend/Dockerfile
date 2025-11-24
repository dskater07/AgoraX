# ============================================================
# Frontend AgoraX - Vue 3 + Vite en Docker
# ============================================================
FROM node:20-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar manifests primero para aprovechar cache
COPY package.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código (src, index.html, vite.config.js, etc.)
COPY . .

EXPOSE 5173

# Servidor de desarrollo Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
