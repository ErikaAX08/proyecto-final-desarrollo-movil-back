from django.db.models import Q
from django.db import transaction
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import json

from ..models import EventoAcademico
from ..serializers import EventoAcademicoSerializer
from django.contrib.auth.models import User


class EventoAcademicoView(generics.CreateAPIView):
    """
    Vista para CRUD de eventos académicos
    - GET: Obtener evento por ID (requiere autenticación)
    - POST: Registrar nuevo evento (requiere autenticación, solo admin)
    - PUT: Actualizar evento (requiere autenticación, solo admin)
    - DELETE: Eliminar evento (requiere autenticación, solo admin)
    """

    permission_classes = (permissions.IsAuthenticated,)

    def is_admin(self, user):
        """
        Verifica si el usuario es administrador
        """
        try:
            user_group = user.groups.first()
            if user_group:
                return user_group.name.lower() == "administrador"
            return False
        except Exception as e:
            print(f"Error al verificar permisos: {e}")
            return False

    # Obtener evento por ID
    def get(self, request, *args, **kwargs):
        try:
            evento_id = request.GET.get("id")
            if not evento_id:
                return Response(
                    {"message": "Se requiere el parámetro 'id'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            evento = get_object_or_404(EventoAcademico, id=evento_id)
            evento_data = EventoAcademicoSerializer(evento, many=False).data

            return Response(evento_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error al obtener el evento", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Registrar nuevo evento (solo administradores)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Verificar que el usuario sea administrador
            if not self.is_admin(request.user):
                return Response(
                    {"message": "Solo los administradores pueden registrar eventos"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Validar campos requeridos
            required_fields = [
                "nombre_evento",
                "tipo_evento",
                "fecha_realizacion",
                "hora_inicio",
                "hora_fin",
                "lugar",
                "publico_objetivo",
                "responsable_evento_id",
                "descripcion_breve",
                "cupo_maximo",
            ]

            for field in required_fields:
                if field not in request.data or not request.data[field]:
                    return Response(
                        {"message": f"El campo '{field}' es requerido"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Parsear publico_objetivo si viene como string JSON
            data = request.data.copy()
            if isinstance(data.get("publico_objetivo"), str):
                try:
                    data["publico_objetivo"] = json.loads(data["publico_objetivo"])
                except json.JSONDecodeError:
                    return Response(
                        {
                            "message": "El campo 'publico_objetivo' debe ser un JSON válido"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Crear el evento usando el serializer
            serializer = EventoAcademicoSerializer(data=data)

            if serializer.is_valid():
                evento = serializer.save()

                return Response(
                    {
                        "message": "Evento académico creado exitosamente",
                        "evento_id": evento.id,
                        "evento": EventoAcademicoSerializer(evento).data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": "Error de validación", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"message": "Error al crear el evento", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Actualizar evento (solo administradores)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        try:
            # Verificar que el usuario sea administrador
            if not self.is_admin(request.user):
                return Response(
                    {"message": "Solo los administradores pueden actualizar eventos"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Validar que venga el ID
            evento_id = request.data.get("id")
            if not evento_id:
                return Response(
                    {"message": "Se requiere el campo 'id' del evento a actualizar"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Obtener el evento
            evento = get_object_or_404(EventoAcademico, id=evento_id)

            # Parsear publico_objetivo si viene como string JSON
            data = request.data.copy()
            if isinstance(data.get("publico_objetivo"), str):
                try:
                    data["publico_objetivo"] = json.loads(data["publico_objetivo"])
                except json.JSONDecodeError:
                    pass  # Si falla, dejar como está y que el serializer lo maneje

            # Actualizar usando el serializer (partial=True para actualización parcial)
            serializer = EventoAcademicoSerializer(evento, data=data, partial=True)

            if serializer.is_valid():
                evento_actualizado = serializer.save()

                return Response(
                    {
                        "message": "Evento actualizado correctamente",
                        "evento": EventoAcademicoSerializer(evento_actualizado).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Error de validación", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"message": "Error al actualizar el evento", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Eliminar evento (solo administradores)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            # Verificar que el usuario sea administrador
            if not self.is_admin(request.user):
                return Response(
                    {"message": "Solo los administradores pueden eliminar eventos"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Obtener el ID del evento
            evento_id = request.GET.get("id")
            if not evento_id:
                return Response(
                    {"message": "Se requiere el parámetro 'id'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Obtener y eliminar el evento
            evento = get_object_or_404(EventoAcademico, id=evento_id)
            nombre_evento = evento.nombre_evento

            evento.delete()

            return Response(
                {"message": f"Evento '{nombre_evento}' eliminado correctamente"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error al eliminar el evento", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListaEventosView(generics.CreateAPIView):
    """
    Vista para obtener la lista de todos los eventos académicos
    GET: Obtener todos los eventos (requiere autenticación)
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los eventos ordenados por fecha
            eventos = EventoAcademico.objects.all().order_by(
                "-fecha_realizacion", "-hora_inicio"
            )

            # Serializar los eventos
            eventos_data = EventoAcademicoSerializer(eventos, many=True).data

            return Response(eventos_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error al obtener la lista de eventos", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EventosPorRolView(generics.CreateAPIView):
    """
    Vista para filtrar eventos según el rol del usuario
    - Administrador: Ve todos los eventos
    - Maestro: Ve eventos para "Profesores" y "Público general"
    - Alumno: Ve eventos para "Estudiantes" y "Público general"
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_user_role(self, user):
        """
        Obtiene el rol del usuario
        """
        try:
            user_group = user.groups.first()
            if user_group:
                return user_group.name.lower()
            return None
        except Exception:
            return None

    def get(self, request, *args, **kwargs):
        try:
            # Obtener el rol del usuario
            rol = self.get_user_role(request.user)

            if not rol:
                return Response(
                    {"message": "No se pudo determinar el rol del usuario"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filtrar eventos según el rol
            if rol == "administrador":
                # El admin ve todos los eventos
                eventos = EventoAcademico.objects.all()
            elif rol == "maestro" or rol == "teacher":
                # El maestro ve eventos para profesores y público general
                eventos = EventoAcademico.objects.filter(
                    Q(publico_objetivo__contains="Profesores")
                    | Q(publico_objetivo__contains="Público general")
                )
            elif rol == "alumno" or rol == "student":
                # El alumno ve eventos para estudiantes y público general
                eventos = EventoAcademico.objects.filter(
                    Q(publico_objetivo__contains="Estudiantes")
                    | Q(publico_objetivo__contains="Público general")
                )
            else:
                # Rol no reconocido
                return Response(
                    {"message": f"Rol '{rol}' no reconocido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Ordenar por fecha y hora
            eventos = eventos.order_by("-fecha_realizacion", "-hora_inicio")

            # Serializar
            eventos_data = EventoAcademicoSerializer(eventos, many=True).data

            return Response(eventos_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error al obtener eventos por rol", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
