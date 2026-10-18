"""Reglas de negocio puras: reciben valores y devuelven valores, sin ORM."""

from decimal import Decimal

META_CREDITOS = Decimal("5.00")
MAX_CREDITOS_POR_CAMPO = Decimal("1.00")


def excede_limite(creditos_actuales: Decimal) -> bool:
    return creditos_actuales >= META_CREDITOS


def faltantes(creditos_actuales: Decimal) -> Decimal:
    return max(Decimal(0), META_CREDITOS - creditos_actuales)


def puede_liberar(total: Decimal, por_campo: dict[str, Decimal]) -> bool:
    return total >= META_CREDITOS and all(
        creditos <= MAX_CREDITOS_POR_CAMPO for creditos in por_campo.values()
    )


def es_responsable(responsable_id: int, usuario_id: int) -> bool:
    return responsable_id == usuario_id


def generar_folio(inscripcion_id: int) -> str:
    return f"ACOM-{inscripcion_id:06d}"
