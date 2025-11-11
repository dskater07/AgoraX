
🧱 Todo el sistema se ejecuta en **contenedores Docker** orquestados con `docker-compose`.

---

## 🔐 Tecnologías Principales

| Componente | Tecnología | Descripción |
|-------------|-------------|-------------|
| Backend | **FastAPI (Python)** | Lógica de negocio, autenticación JWT, reglas RD/RB |
| Frontend | **Vue.js 3 (Vite)** | Interfaz interactiva, gestión de asambleas y votos |
| Gateway | **Node.js + Socket.io** | Comunicación en tiempo real y quorum activo |
| Base de datos | **PostgreSQL 17** | Datos de usuarios, votos, auditoría |
| Cache | **Redis** | Sesiones y validación rápida de quorum |
| Contenedores | **Docker + Compose** | Despliegue modular y replicable |
| Monitoreo | **Prometheus + Grafana** | Métricas de rendimiento y calidad |

---

## ⚖️ Reglas de Negocio (BABOK v3 – Cap. 10.9)

### 🔷 Reglas Definicionales (RD)
| ID | Descripción | Propósito |
|----|--------------|------------|
| **RD-01** | Un propietario solo puede votar una vez por cada punto. | Evitar duplicidad y asegurar integridad. |
| **RD-02** | Un apoderado representa máximo a un propietario. | Evitar concentración de poder. |
| **RD-03** | Solo los usuarios autenticados pueden votar. | Validar identidad y legitimidad. |
| **RD-04** | El quorum mínimo es del 51% del coeficiente total. | Cumplimiento de la Ley 675/2001. |
| **RD-05** | Los resultados no pueden modificarse tras el cierre. | Garantizar transparencia y trazabilidad. |
| **RD-06** | Los votos se almacenan cifrados (AES-256). | Proteger confidencialidad. |
| **RD-07** | Cada asamblea tiene un identificador único. | Facilitar auditoría. |
| **RD-08** | Propietarios con deuda no pueden votar. | Cumplimiento normativo interno. |
| **RD-09** | El acta debe incluir quorum, votos y firma digital. | Evidencia legal de decisiones. |
| **RD-10** | Cada conjunto debe registrar su coeficiente total. | Calcular quorum ponderado. |

---

### 🔶 Reglas de Comportamiento (RB)
| ID | Descripción | Propósito |
|----|--------------|------------|
| **RB-01** | Solo el administrador puede abrir o cerrar votaciones. | Control jerárquico del proceso. |
| **RB-02** | Debe cerrarse un punto antes de abrir otro. | Evitar solapamiento. |
| **RB-03** | El usuario debe confirmar asistencia antes de votar. | Validar quorum y participación. |
| **RB-04** | El sistema notifica apertura/cierre a todos los usuarios. | Transparencia y comunicación. |
| **RB-05** | Los votos no pueden modificarse una vez emitidos. | Evitar fraude. |
| **RB-06** | Registrar IP, fecha y hora de cada voto. | Auditoría y trazabilidad. |
| **RB-07** | No se puede abrir votación sin quorum mínimo. | Cumplimiento legal. |
| **RB-08** | Reconexion segura ante fallos, sin duplicar voto. | Continuidad operativa. |
| **RB-09** | Resultados visibles solo al cierre de todas las votaciones. | Evitar sesgo. |
| **RB-10** | El administrador debe firmar electrónicamente el acta. | Validación final del proceso. |

---

### 🧠 Reglas Implícitas (RI)
| ID | Descripción | Tipo |
|----|--------------|------|
| **RI-01** | Todas las reglas deben almacenarse en un repositorio central versionado. | Definicional |
| **RI-02** | Los cambios a reglas requieren aprobación formal. | Comportamiento |
| **RI-03** | Se debe mantener un glosario de términos del sistema. | Definicional |

---

## 🧩 Cumplimiento de Calidad (ISO/IEC 25010)

| Característica | Descripción |
|----------------|-------------|
| **Funcionalidad** | Cumple requerimientos de votación, quorum y auditoría. |
| **Fiabilidad** | Soporte de reintentos y registro de eventos. |
| **Usabilidad** | Interfaz clara, accesible desde PC o móvil. |
| **Eficiencia** | Respuesta en tiempo real mediante WebSockets y Redis. |
| **Mantenibilidad** | Código modular, documentación y tests. |
| **Seguridad** | Autenticación JWT, cifrado AES-256 y HTTPS. |
| **Compatibilidad** | Contenedores Docker portables. |
| **Portabilidad** | Deploy multiplataforma (local o nube). |

---

## 🧠 Metodología
El proyecto sigue los lineamientos del **BABOK v3**:
- *Manage Stakeholder Collaboration* (4.5)
- *Requirements Life Cycle Management* (5.x)
- *Business Rules Analysis* (10.9)

Y aplica control de calidad en:
- Pruebas unitarias y de integración.
- Verificación de reglas y validación de requerimientos.
- Documentación técnica (README + diagramas).
- Medición de desempeño y disponibilidad.

---

## 👥 Autores
**Proyecto académico desarrollado por:**  
- GAVIRIA OCAMPO JOHAN ESTEBAN
- PATIÑO MONTOYA DAMIAN
- VELILLA FLOREZ LUISA FERNANDA
> Estudiantes de Ingeniería de Sistemas – Instituto Tecnológico Metropolitano (ITM)  
> Asignatura: *Calidad del Software (2025-2)*  

**Director académico:**  
> [Nombre del docente a cargo]  
> ITM – Facultad de Ingenierías  

---

## 🪪 Licencia
Proyecto distribuido bajo licencia **MIT**, de uso académico y educativo.  
Se permite su reutilización y adaptación citando la fuente original.

