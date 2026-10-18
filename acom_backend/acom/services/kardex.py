"""Casos de uso de consulta para el kárdex y liberación ACOM."""

from decimal import Decimal

from .. import selectors
from ..domain import reglas
from ..models import CategoriaActividad


def kardex(estudiante):
    total = selectors.total_validado(estudiante)
    por_campo = selectors.avance_por_campo(estudiante)
    return {
        "total": total,
        "faltantes": reglas.faltantes(total),
        "por_campo": por_campo,
        "campos": [
            {"codigo": codigo, "nombre": nombre, "creditos": por_campo[codigo]}
            for codigo, nombre in CategoriaActividad.choices
        ],
        "liberado": reglas.puede_liberar(total, por_campo),
    }


def estudiantes_liberables():
    liberables = []
    campos = tuple(codigo for codigo, _ in CategoriaActividad.choices)
    for estudiante in selectors.estudiantes_liberables():
        por_campo = {
            campo: Decimal(getattr(estudiante, f"creditos_{campo}") or 0).quantize(Decimal("0.01"))
            for campo in campos
        }
        total = Decimal(estudiante.total_validado).quantize(Decimal("0.01"))
        if reglas.puede_liberar(total, por_campo):
            liberables.append({
                "id": estudiante.pk,
                "username": estudiante.get_username(),
                "nombre": estudiante.get_full_name() or estudiante.get_username(),
                "total": total,
                "por_campo": por_campo,
            })
    return liberables
