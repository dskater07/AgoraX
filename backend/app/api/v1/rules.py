"""
backend/app/api/v1/rules.py

Endpoint para exponer las reglas de negocio (RD, RB, RI) de AgoraX.

Este módulo no persiste reglas en base de datos, pero sirve como
documentación viva de la lógica aplicada en el sistema.

Se alinea con:
- BABOK v3 - Business Rules Analysis (10.9)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])


@router.get("/")
def list_business_rules():
    """
    Devuelve el catálogo de reglas de negocio implementadas en AgoraX.

    Agrupa:
    - Reglas Definicionales (RD)
    - Reglas de Comportamiento (RB)
    - Reglas Implícitas (RI)
    """
    return {
        "definicionales": [
            {
                "id": "RD-01",
                "descripcion": "Un propietario solo puede votar una vez por cada punto.",
                "proposito": "Evitar duplicidad y asegurar integridad.",
            },
            {
                "id": "RD-02",
                "descripcion": "Un apoderado representa máximo a un propietario.",
                "proposito": "Evitar concentración de poder.",
            },
            {
                "id": "RD-03",
                "descripcion": "Solo los usuarios autenticados pueden votar.",
                "proposito": "Validar identidad y legitimidad.",
            },
            {
                "id": "RD-04",
                "descripcion": "El quórum mínimo es del 51% del coeficiente total.",
                "proposito": "Cumplimiento de la Ley 675/2001.",
            },
            {
                "id": "RD-05",
                "descripcion": "Los resultados no pueden modificarse tras el cierre.",
                "proposito": "Garantizar transparencia y trazabilidad.",
            },
            {
                "id": "RD-06",
                "descripcion": "Los votos se almacenan cifrados (AES-256 / Fernet).",
                "proposito": "Proteger confidencialidad.",
            },
            {
                "id": "RD-07",
                "descripcion": "Cada asamblea tiene un identificador único.",
                "proposito": "Facilitar auditoría y trazabilidad.",
            },
            {
                "id": "RD-08",
                "descripcion": "Propietarios con deuda no pueden votar.",
                "proposito": "Cumplimiento normativo interno.",
            },
            {
                "id": "RD-09",
                "descripcion": "El acta debe incluir quórum, votos y firma digital.",
                "proposito": "Evidencia legal de decisiones.",
            },
            {
                "id": "RD-10",
                "descripcion": "Cada conjunto debe registrar su coeficiente total.",
                "proposito": "Calcular quórum ponderado.",
            },
        ],
        "comportamiento": [
            {
                "id": "RB-01",
                "descripcion": "Solo el administrador puede abrir o cerrar votaciones.",
                "proposito": "Control jerárquico del proceso.",
            },
            {
                "id": "RB-02",
                "descripcion": "Debe cerrarse un punto antes de abrir otro.",
                "proposito": "Evitar solapamiento de decisiones.",
            },
            {
                "id": "RB-03",
                "descripcion": "El usuario debe confirmar asistencia antes de votar.",
                "proposito": "Validar participación real en el quórum.",
            },
            {
                "id": "RB-04",
                "descripcion": "El sistema notifica apertura/cierre a todos los usuarios.",
                "proposito": "Transparencia y comunicación.",
            },
            {
                "id": "RB-05",
                "descripcion": "Los votos no pueden modificarse una vez emitidos.",
                "proposito": "Evitar fraude.",
            },
            {
                "id": "RB-06",
                "descripcion": "Registrar IP, fecha y hora de cada voto.",
                "proposito": "Auditoría y trazabilidad.",
            },
            {
                "id": "RB-07",
                "descripcion": "No se puede abrir votación sin quórum mínimo.",
                "proposito": "Cumplimiento legal.",
            },
            {
                "id": "RB-08",
                "descripcion": "Reconexión segura ante fallos, sin duplicar voto.",
                "proposito": "Continuidad operativa.",
            },
            {
                "id": "RB-09",
                "descripcion": "Resultados visibles solo al cierre de todas las votaciones.",
                "proposito": "Evitar sesgo.",
            },
            {
                "id": "RB-10",
                "descripcion": "El administrador debe firmar electrónicamente el acta.",
                "proposito": "Validación final del proceso.",
            },
        ],
        "implicitas": [
            {
                "id": "RI-01",
                "descripcion": "Todas las reglas deben almacenarse en un repositorio central versionado.",
                "tipo": "Definicional",
            },
            {
                "id": "RI-02",
                "descripcion": "Los cambios a reglas requieren aprobación formal.",
                "tipo": "Comportamiento",
            },
            {
                "id": "RI-03",
                "descripcion": "Se debe mantener un glosario de términos del sistema.",
                "tipo": "Definicional",
            },
        ],
    }
