"""Infraestructura: todas las lecturas. Las vistas y servicios no arman consultas."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Q, Sum

from .models import (
    ActividadComplementaria,
    CategoriaActividad,
    Inscripcion,
    RegistroCreditos,
)


def actividades_activas():
    return ActividadComplementaria.objects.filter(activa=True)


def inscripciones_de(estudiante):
    return Inscripcion.objects.filter(estudiante=estudiante).select_related("actividad")


def inscripcion_de_responsable(inscripcion_id, responsable):
    """None si la inscripción no existe o la actividad no es de este responsable."""
    return (
        Inscripcion.objects.select_related("estudiante", "actividad")
        .filter(pk=inscripcion_id, actividad__responsable=responsable)
        .first()
    )


def inscripcion_por_id(inscripcion_id):
    return (
        Inscripcion.objects.select_related("estudiante", "actividad")
        .filter(pk=inscripcion_id)
        .first()
    )


def total_validado(estudiante) -> Decimal:
    total = RegistroCreditos.objects.filter(inscripcion__estudiante=estudiante).aggregate(
        total=Sum("creditos_otorgados")
    )["total"]
    return Decimal(total or 0).quantize(Decimal("0.01"))


def avance_por_campo(estudiante) -> dict[str, Decimal]:
    """Créditos validados por categoría, incluyendo categorías sin registros."""
    avance = {valor: Decimal("0.00") for valor, _ in CategoriaActividad.choices}
    totales = (
        RegistroCreditos.objects.filter(inscripcion__estudiante=estudiante)
        .values("inscripcion__actividad__categoria")
        .annotate(total=Sum("creditos_otorgados"))
    )

    for fila in totales:
        campo = fila["inscripcion__actividad__categoria"]
        if campo in avance:
            avance[campo] = Decimal(fila["total"] or 0).quantize(Decimal("0.01"))

    return avance


def estudiantes_liberables():
    """Devuelve candidatos con totales agregados para que aplicación aplique la regla pura."""
    por_campo = {
        f"creditos_{campo}": Sum(
            "inscripciones_acom__registro_creditos__creditos_otorgados",
            filter=Q(inscripciones_acom__actividad__categoria=campo),
            default=Decimal("0.00"),
        )
        for campo, _ in CategoriaActividad.choices
    }
    total = Sum("inscripciones_acom__registro_creditos__creditos_otorgados")

    return (
        get_user_model()
        .objects.annotate(total_validado=total, **por_campo)
        .filter(total_validado__isnull=False)
        .order_by("username", "pk")
    )
