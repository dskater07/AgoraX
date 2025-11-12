"""
Módulo de Reglas de Negocio (API v1)
------------------------------------

Centraliza y expone las reglas de negocio del sistema AgoraX, clasificadas en:
    - Definicionales (RD-xx): Condiciones estáticas del dominio.
    - De comportamiento (RB-xx): Políticas que regulan procesos y acciones.
    - Implícitas (RI-xx): Suposiciones operativas y de gobierno del conocimiento.

Referencias:
    - BABOK v3, sección 10.9 (Business Rules).
    - Ley 675 de 2001 (Colombia) — marco general de propiedad horizontal.

Uso:
    - Los clientes pueden consumir `/rules` para obtener el catálogo completo,
      o `/rules/{rule_id}` para recuperar una regla específica.

Trazabilidad:
    - Cada regla cuenta con `id`, `desc` (descripción) y `proposito` (rationale).
"""

from datetime import datetime
from fastapi import APIRouter

router = APIRouter()

# -------------------------------------------------------------------
# Catálogo de reglas de negocio (puede migrar a BD o motor BRMS)
# -------------------------------------------------------------------
RULES = {
    "definicionales": [
        {
            "id": "RD-01",
            "desc": "Un propietario solo puede votar una vez por cada punto.",
            "proposito": "Evitar duplicidad y preservar integridad del resultado.",
        },
        {
            "id": "RD-02",
            "desc": "Un apoderado representa máximo a un propietario.",
            "proposito": "Prevenir concentración de poder de voto.",
        },
        {
            "id": "RD-03",
            "desc": "Solo usuarios autenticados pueden votar.",
            "proposito": "Garantizar identidad y legitimidad del sufragio.",
        },
        {
            "id": "RD-04",
            "desc": "Quórum mínimo del 51% del coeficiente/propietarios.",
            "proposito": "Cumplir con el estándar legal y reglamentario.",
        },
        {
            "id": "RD-05",
            "desc": "Los resultados no pueden modificarse tras el cierre.",
            "proposito": "Asegurar inmutabilidad, auditoría y confianza.",
        },
        {
            "id": "RD-06",
            "desc": "Los votos se almacenan cifrados en repositorio seguro.",
            "proposito": "Proteger confidencialidad y mitigar filtraciones.",
        },
        {
            "id": "RD-07",
            "desc": "Cada asamblea tiene un identificador único.",
            "proposito": "Trazabilidad y correlación de evidencias.",
        },
        {
            "id": "RD-08",
            "desc": "Propietarios con deuda vencida no pueden votar.",
            "proposito": "Observar reglamentos internos del CR.",
        },
        {
            "id": "RD-09",
            "desc": "El acta debe incluir quórum, resultados y firma digital.",
            "proposito": "Soporte legal y verificación posterior.",
        },
        {
            "id": "RD-10",
            "desc": "El sistema mantiene el coeficiente total del conjunto.",
            "proposito": "Base para cálculo de quórum y ponderación.",
        },
    ],
    "comportamiento": [
        {
            "id": "RB-01",
            "desc": "Solo el administrador puede abrir o cerrar votaciones.",
            "proposito": "Control jerárquico del proceso.",
        },
        {
            "id": "RB-02",
            "desc": "Debe cerrarse un punto/asamblea antes de abrir otro.",
            "proposito": "Evitar solapamiento y ambigüedad de estado.",
        },
        {
            "id": "RB-03",
            "desc": "El usuario debe confirmar asistencia antes de votar.",
            "proposito": "Vincular participación efectiva con quórum.",
        },
        {
            "id": "RB-04",
            "desc": "Notificar apertura y cierre a todos los usuarios.",
            "proposito": "Transparencia y comunicación oportuna.",
        },
        {
            "id": "RB-05",
            "desc": "Los votos no pueden editarse tras su emisión.",
            "proposito": "Evitar fraude y manipulación de resultados.",
        },
        {
            "id": "RB-06",
            "desc": "Registrar IP, fecha y hora de cada voto.",
            "proposito": "Auditoría forense y trazabilidad técnica.",
        },
        {
            "id": "RB-07",
            "desc": "Bloquear apertura si no hay quórum mínimo (RD-04).",
            "proposito": "Cumplimiento legal y consistencia operativa.",
        },
        {
            "id": "RB-08",
            "desc": "Permitir reconexión segura sin duplicar voto.",
            "proposito": "Resiliencia frente a fallos de red.",
        },
        {
            "id": "RB-09",
            "desc": "Ocultar resultados parciales hasta cierre total.",
            "proposito": "Mitigar sesgos durante la votación.",
        },
        {
            "id": "RB-10",
            "desc": "El administrador firma electrónicamente el acta.",
            "proposito": "Cierre formal y custodia de evidencias.",
        },
    ],
    "implicitas": [
        {
            "id": "RI-01",
            "desc": "Las reglas se gestionan en un repositorio versionado.",
            "proposito": "Gobernanza del conocimiento del negocio.",
        },
        {
            "id": "RI-02",
            "desc": "Cambios de reglas requieren aprobación formal.",
            "proposito": "Control de cambios y auditoría.",
        },
        {
            "id": "RI-03",
            "desc": "El sistema mantiene glosario oficial y definiciones.",
            "proposito": "Eliminar ambigüedades terminológicas.",
        },
    ],
}


@router.get("/", summary="Listar reglas de negocio (catálogo completo)")
def list_rules():
    """Devuelve el catálogo completo de reglas de negocio.

    Returns:
        dict: Estructura con reglas por categoría, conteo y timestamp.
    """
    return {
        "rules": RULES,
        "count": sum(len(group) for group in RULES.values()),
        "timestamp": datetime.utcnow(),
    }


@router.get("/{rule_id}", summary="Consultar una regla específica por ID")
def get_rule(rule_id: str):
    """Busca y devuelve una regla de negocio por su identificador.

    Args:
        rule_id: Identificador de la regla (p. ej., 'RD-04', 'RB-01', 'RI-02').

    Returns:
        dict: Grupo, detalle de la regla y timestamp, o mensaje si no existe.
    """
    rid = rule_id.strip().upper()
    for group_name, items in RULES.items():
        for rule in items:
            if rule["id"] == rid:
                return {"group": group_name, "rule": rule, "timestamp": datetime.utcnow()}
    return {"detail": "Regla no encontrada", "rule_id": rid, "timestamp": datetime.utcnow()}
