from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json
from django.shortcuts import get_object_or_404


class AdminAll(generics.CreateAPIView):
    # Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)

    # Invocamos la petición GET para obtener todos los administradores
    def get(self, request, *args, **kwargs):
        admin = Administradores.objects.filter(user__is_active=1).order_by("id")
        lista = AdminSerializer(admin, many=True).data
        return Response(lista, 200)


class AdminView(generics.CreateAPIView):
    """
    Vista para CRUD de administradores
    - POST: No requiere autenticación (registro público)
    - GET, PUT, DELETE: Requieren autenticación
    """

    # Permisos por método (sobrescribe el comportamiento default)
    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    # Obtener usuario por ID
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id=request.GET.get("id"))
        admin = AdminSerializer(admin, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(admin, 200)

    # Registrar nuevo administrador
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Validar que vengan todos los campos requeridos
            required_fields = [
                "rol",
                "first_name",
                "last_name",
                "email",
                "password",
                "clave_admin",
                "telefono",
                "rfc",
                "edad",
                "ocupacion",
            ]

            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {"message": f"El campo '{field}' es requerido"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Obtener datos del request
            role = request.data["rol"]
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            email = request.data["email"]
            password = request.data["password"]

            # Validar si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response(
                    {"message": f"El email {email} ya está registrado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Crear el usuario en la tabla auth_user
            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=1,
            )

            # Cifrar la contraseña
            user.set_password(password)
            user.save()

            # Asignar el grupo/rol al usuario
            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # Almacenar los datos adicionales del administrador
            admin = Administradores.objects.create(
                user=user,
                clave_admin=request.data["clave_admin"],
                telefono=request.data["telefono"],
                rfc=request.data["rfc"].upper(),
                edad=request.data["edad"],
                ocupacion=request.data["ocupacion"],
            )
            admin.save()

            return Response(
                {
                    "message": "Administrador creado exitosamente",
                    "admin_created_id": admin.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Si algo sale mal, revertir la transacción
            return Response(
                {"message": "Error al crear el administrador", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Actualizar datos del administrador
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        try:
            # Primero obtenemos el administrador a actualizar
            admin = get_object_or_404(Administradores, id=request.data["id"])

            # Actualizamos los datos del administrador
            admin.clave_admin = request.data.get("clave_admin", admin.clave_admin)
            admin.telefono = request.data.get("telefono", admin.telefono)
            admin.rfc = request.data.get("rfc", admin.rfc).upper()
            admin.edad = request.data.get("edad", admin.edad)
            admin.ocupacion = request.data.get("ocupacion", admin.ocupacion)
            admin.save()

            # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
            user = admin.user
            user.first_name = request.data.get("first_name", user.first_name)
            user.last_name = request.data.get("last_name", user.last_name)
            user.save()

            return Response(
                {
                    "message": "Administrador actualizado correctamente",
                    "admin": AdminSerializer(admin).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error al actualizar el administrador", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Eliminar administrador (Borrado real de la base de datos)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            admin = get_object_or_404(Administradores, id=request.GET.get("id"))

            # Guardamos el email para el mensaje de respuesta
            email = admin.user.email

            # Eliminamos el usuario asociado (esto también eliminará el admin por CASCADE)
            admin.user.delete()

            return Response(
                {"message": f"Administrador {email} eliminado correctamente"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error al eliminar el administrador", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TotalUsers(generics.CreateAPIView):
    """
    Vista para contar el total de cada tipo de usuarios (Administradores, Maestros, Alumnos).
    Se simplifica para solo obtener los conteos sin serializar.
    """

    # Sólo usuarios autenticados pueden acceder a las estadísticas
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            # TOTAL ADMINISTRADORES (Usuarios activos)
            total_admins = Administradores.objects.filter(user__is_active=True).count()

            # TOTAL MAESTROS (Usuarios activos)
            total_maestros = Maestros.objects.filter(user__is_active=True).count()

            # TOTAL ALUMNOS (Usuarios activos)
            total_alumnos = Alumnos.objects.filter(user__is_active=True).count()

            # Respuesta final con los conteos
            return Response(
                {
                    "admins": total_admins,
                    "maestros": total_maestros,
                    "alumnos": total_alumnos,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Manejo de error genérico en el servidor
            return Response(
                {"message": "Error al obtener el conteo de usuarios", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
