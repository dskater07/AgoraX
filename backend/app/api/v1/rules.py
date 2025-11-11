from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Reglas de negocio centralizadas (BABOK 10.9)
RULES = {
    "definicionales": [
        {"id": "RD-01", "desc": "Un propietario solo puede votar una vez por cada punto.", "proposito": "Evitar duplicidad y asegurar integridad."},
        {"id": "RD-02", "desc": "Un apoderado representa máximo a un propietario.", "proposito": "Evitar concentración de poder."},
        {"id": "RD-03", "desc": "Solo los usuarios autenticados pueden votar.", "proposito": "Validar identidad y legitimidad."},
        {"id": "RD-04", "desc": "Quorum mínimo del 51% del coeficiente total.", "proposito": "Cumplimiento de la Ley 675/2001."},
        {"id": "RD-05", "desc": "Resultados inmodificables tras el cierre.", "proposito": "Garantizar transparencia y trazabilidad."},
        {"id": "RD-06", "desc": "Los votos deben almacenarse cifrados (AES-256).", "proposito": "Proteger confidencialidad."},
        {"id": "RD-07", "desc": "Cada asamblea tiene un identificador único.", "proposito": "Facilitar auditoría y trazabilidad."},
        {"id": "RD-08", "desc": "Propietarios con deuda no pueden votar.", "proposito": "Cumplimiento del reglamento interno."},
        {"id": "RD-09", "desc": "El acta debe incluir quorum, votos y firma digital.", "proposito": "Soporte legal de decisiones."},
        {"id": "RD-10", "desc": "Debe registrarse el coeficiente total del conjunto.", "proposito": "Calcular quorum y ponderación."},
    ],
    "comportamiento": [
        {"id": "RB-01", "desc": "Solo el administrador abre o cierra votaciones.", "proposito": "Control jerárquico del proceso."},
        {"id": "RB-02", "desc": "Debe cerrarse un punto antes de abrir otro.", "proposito": "Evitar solapamiento y desorden."},
        {"id": "RB-03", "desc": "Confirmar asistencia antes de votar.", "proposito": "Validar quorum y participación."},
        {"id": "RB-04", "desc": "Notificar apertura/cierre a todos los usuarios.", "proposito": "Transparencia y comunicación."},
        {"id": "RB-05", "desc": "Votos no editables tras emisión.", "proposito": "Evitar fraude y manipulación."},
        {"id": "RB-06", "desc": "Registrar IP, fecha y hora de cada voto.", "proposito": "Auditoría y trazabilidad."},
        {"id": "RB-07", "desc": "Bloquear apertura si no hay quorum mínimo.", "proposito": "Cumplimiento legal (RD-04)."},
        {"id": "RB-08", "desc": "Permitir reconexión segura sin duplicar voto.", "proposito": "Continuidad operativa."},
        {"id": "RB-09", "desc": "Resultados visibles solo al cierre total.", "proposito": "Evitar sesgos durante la votación."},
        {"id": "RB-10", "desc": "El administrador firma electrónicamente el acta.", "proposito": "Validación final y custodia."},
    ],
    "implicitas": [
        {"id": "RI-01", "desc": "Reglas centralizadas y versionadas.", "proposito": "Gobierno del conocimiento del negocio."},
        {"id": "RI-02", "desc": "Cambios a reglas requieren aprobación formal.", "proposito": "Control de cambios y auditoría."},
        {"id": "RI-03", "desc": "Glosario oficial del sistema mantenido al día.", "proposito": "Evitar ambigüedades."},
    ],
}

@router.get("/", summary="Listar reglas de negocio (todas)")
def list_rules():
    """Devuelve todas las reglas RD, RB y RI."""
    return {"rules": RULES, "count": sum(len(v) for v in RULES.values()), "timestamp": datetime.utcnow()}

@router.get("/{rule_id}", summary="Obtener detalle de una regla por ID")
def get_rule(rule_id: str):
    """
    Busca una regla por su identificador (ej: RD-04, RB-01, RI-02).
    """
    rule_id = rule_id.upper()
    for group, items in RULES.items():
        for r in items:
            if r["id"] == rule_id:
                return {"group": group, "rule": r, "timestamp": datetime.utcnow()}
    return {"detail": "Regla no encontrada", "rule_id": rule_id, "timestamp": datetime.utcnow()}
