"""Endpoints JSON versionados para el kárdex ACOM."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from .services import kardex as servicio_kardex


class PuedeConsultarLiberables(BasePermission):
    message = "Se requiere permiso de departamento para consultar liberables."

    def has_permission(self, request, view):
        return request.user.has_perm("acom.can_validate_credits")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def resumen_mis_inscripciones(request):
    datos = servicio_kardex.kardex(request.user)
    return Response({
        "total": datos["total"],
        "faltantes": datos["faltantes"],
        "por_campo": datos["por_campo"],
        "liberado": datos["liberado"],
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated, PuedeConsultarLiberables])
def liberables(request):
    return Response({"estudiantes": servicio_kardex.estudiantes_liberables()})
