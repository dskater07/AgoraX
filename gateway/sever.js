import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: '*' },
});

io.on('connection', (socket) => {
  console.log(`🔌 Cliente conectado: ${socket.id}`);
  socket.on('vote', (data) => io.emit('vote_update', data));
  socket.on('disconnect', () => console.log(`❌ Cliente desconectado: ${socket.id}`));
});

httpServer.listen(7000, () => console.log('🚀 Gateway activo en puerto 7000'));
