from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from datetime import date
import json


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administradores
        fields = "__all__"


class AlumnoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Alumnos
        fields = "__all__"


class MaestroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Maestros
        fields = "__all__"


class ResponsableSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información básica del responsable
    """

    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "nombre_completo"]

    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EventoAcademicoSerializer(serializers.ModelSerializer):
    """
    Serializer para eventos académicos
    """

    responsable_evento = ResponsableSerializer(read_only=True)
    responsable_evento_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="responsable_evento", write_only=True
    )

    class Meta:
        model = EventoAcademico
        fields = [
            "id",
            "nombre_evento",
            "tipo_evento",
            "fecha_realizacion",
            "hora_inicio",
            "hora_fin",
            "lugar",
            "publico_objetivo",
            "programa_educativo",
            "responsable_evento",
            "responsable_evento_id",
            "descripcion_breve",
            "cupo_maximo",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_nombre_evento(self, value):
        """
        Validar que el nombre del evento solo contenga letras, números y espacios
        """
        import re

        if not re.match(r"^[a-zA-Z0-9\s]+$", value):
            raise serializers.ValidationError(
                "Solo se permiten letras, números y espacios"
            )
        return value

    def validate_lugar(self, value):
        """
        Validar que el lugar solo contenga caracteres alfanuméricos y espacios
        """
        import re

        if not re.match(r"^[a-zA-Z0-9\s]+$", value):
            raise serializers.ValidationError(
                "Solo se permiten caracteres alfanuméricos y espacios"
            )
        return value

    def validate_fecha_realizacion(self, value):
        """
        Validar que la fecha no sea anterior al día actual
        """
        if value < date.today():
            raise serializers.ValidationError(
                "No se pueden seleccionar fechas anteriores al día actual"
            )
        return value

    def validate_descripcion_breve(self, value):
        """
        Validar que la descripción tenga máximo 300 caracteres y solo contenga
        letras, números y signos de puntuación básicos
        """
        import re

        if len(value) > 300:
            raise serializers.ValidationError(
                "La descripción debe tener máximo 300 caracteres"
            )

        if not re.match(r"^[a-zA-Z0-9\s.,;:()!?¿¡\-]+$", value):
            raise serializers.ValidationError(
                "Solo se permiten letras, números y signos de puntuación básicos"
            )

        return value

    def validate_cupo_maximo(self, value):
        """
        Validar que el cupo esté entre 1 y 999
        """
        if value < 1 or value > 999:
            raise serializers.ValidationError(
                "El cupo debe ser un número entre 1 y 999"
            )
        return value

    def validate_publico_objetivo(self, value):
        """
        Validar que publico_objetivo sea una lista válida
        """
        opciones_validas = ["Estudiantes", "Profesores", "Público general"]

        # Si viene como string JSON, parsearlo
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    "El público objetivo debe ser un JSON válido"
                )

        # Validar que sea una lista
        if not isinstance(value, list):
            raise serializers.ValidationError("El público objetivo debe ser una lista")

        # Validar que tenga al menos un elemento
        if len(value) == 0:
            raise serializers.ValidationError(
                "Debe seleccionar al menos un público objetivo"
            )

        # Validar que todos los elementos sean válidos
        for publico in value:
            if publico not in opciones_validas:
                raise serializers.ValidationError(
                    f"'{publico}' no es un público objetivo válido. Opciones: {', '.join(opciones_validas)}"
                )

        return value

    def validate(self, data):
        """
        Validaciones que requieren múltiples campos
        """
        # Validar que hora_inicio < hora_fin
        if "hora_inicio" in data and "hora_fin" in data:
            if data["hora_inicio"] >= data["hora_fin"]:
                raise serializers.ValidationError(
                    {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
                )

        # Validar programa_educativo si público objetivo incluye "Estudiantes"
        publico_objetivo = data.get("publico_objetivo", [])

        # Si viene como string, parsearlo
        if isinstance(publico_objetivo, str):
            try:
                publico_objetivo = json.loads(publico_objetivo)
            except json.JSONDecodeError:
                pass

        if "Estudiantes" in publico_objetivo:
            if not data.get("programa_educativo"):
                raise serializers.ValidationError(
                    {
                        "programa_educativo": "Debe seleccionar un programa educativo cuando el público objetivo incluye Estudiantes"
                    }
                )

        return data

    def to_representation(self, instance):
        """
        Personalizar la representación del objeto
        """
        representation = super().to_representation(instance)

        # Asegurar que publico_objetivo sea una lista (no string JSON)
        if isinstance(representation["publico_objetivo"], str):
            try:
                representation["publico_objetivo"] = json.loads(
                    representation["publico_objetivo"]
                )
            except json.JSONDecodeError:
                representation["publico_objetivo"] = []

        # Formatear la fecha en formato DD/MM/YYYY
        if representation["fecha_realizacion"]:
            fecha_obj = (
                instance.fecha_realizacion
                if hasattr(instance, "fecha_realizacion")
                else None
            )
            if fecha_obj:
                representation["fecha_realizacion"] = fecha_obj.strftime("%d/%m/%Y")

        return representation
