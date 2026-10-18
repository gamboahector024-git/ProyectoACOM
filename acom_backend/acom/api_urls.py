from django.urls import path

from . import api

urlpatterns = [
    path("mis-inscripciones/resumen/", api.resumen_mis_inscripciones, name="api_resumen_mis_inscripciones"),
    path("departamento/liberables/", api.liberables, name="api_liberables"),
]
