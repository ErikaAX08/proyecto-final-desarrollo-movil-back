from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None
    )
    clave_admin = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin " + self.user.first_name + " " + self.user.last_name


class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None
    )
    matricula = models.CharField(max_length=255, null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno " + self.user.first_name + " " + self.user.last_name


class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None
    )
    id_trabajador = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    cubiculo = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    area_investigacion = models.CharField(max_length=255, null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del maestro " + self.user.first_name + " " + self.user.last_name


class EventoAcademico(models.Model):
    """
    Modelo para almacenar eventos académicos de la Facultad.
    """

    # Choices para tipo de evento
    TIPO_EVENTO_CHOICES = [
        ("Conferencia", "Conferencia"),
        ("Taller", "Taller"),
        ("Seminario", "Seminario"),
        ("Concurso", "Concurso"),
    ]

    # Choices para programa educativo
    PROGRAMA_EDUCATIVO_CHOICES = [
        (
            "Licenciatura en Ciencias de la Computación",
            "Licenciatura en Ciencias de la Computación",
        ),
        (
            "Licenciatura en Ingeniería en Tecnologías de la Información",
            "Licenciatura en Ingeniería en Tecnologías de la Información",
        ),
        (
            "Licenciatura en Ingeniería de Software",
            "Licenciatura en Ingeniería de Software",
        ),
    ]

    id = models.BigAutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=200, null=False, blank=False)
    tipo_evento = models.CharField(
        max_length=50, choices=TIPO_EVENTO_CHOICES, null=False, blank=False
    )
    fecha_realizacion = models.DateField(null=False, blank=False)
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_fin = models.TimeField(null=False, blank=False)
    lugar = models.CharField(max_length=200, null=False, blank=False)

    # Público objetivo: guardado como JSONField (lista de strings)
    publico_objetivo = models.JSONField(null=False, blank=False)

    # Programa educativo: solo requerido si público objetivo incluye "Estudiantes"
    programa_educativo = models.CharField(
        max_length=200, choices=PROGRAMA_EDUCATIVO_CHOICES, null=True, blank=True
    )

    # Responsable del evento: ForeignKey a User (maestro o administrador)
    responsable_evento = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="eventos"
    )

    descripcion_breve = models.TextField(max_length=300, null=False, blank=False)

    # Cupo máximo: entre 1 y 999
    cupo_maximo = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=False,
        blank=False,
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "eventos_academicos"
        ordering = ["-fecha_realizacion", "-hora_inicio"]
        indexes = [
            models.Index(fields=["fecha_realizacion"]),
            models.Index(fields=["tipo_evento"]),
            models.Index(fields=["responsable_evento"]),
        ]

    def __str__(self):
        return f"{self.nombre_evento} - {self.fecha_realizacion}"

    def clean(self):
        """
        Validaciones personalizadas del modelo
        """
        from django.core.exceptions import ValidationError

        # Validar que la fecha no sea anterior al día actual
        if self.fecha_realizacion and self.fecha_realizacion < date.today():
            raise ValidationError(
                {"fecha_realizacion": "No se pueden seleccionar fechas pasadas"}
            )

        # Validar que hora_inicio < hora_fin
        if self.hora_inicio and self.hora_fin:
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError(
                    {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio"}
                )

        # Validar programa_educativo si público objetivo incluye "Estudiantes"
        if self.publico_objetivo and isinstance(self.publico_objetivo, list):
            if "Estudiantes" in self.publico_objetivo:
                if not self.programa_educativo:
                    raise ValidationError(
                        {
                            "programa_educativo": "Debe seleccionar un programa educativo cuando el público objetivo incluye Estudiantes"
                        }
                    )

    @property
    def duracion_horas(self):
        """
        Calcula la duración del evento en horas
        """
        from datetime import datetime, timedelta

        inicio = datetime.combine(date.today(), self.hora_inicio)
        fin = datetime.combine(date.today(), self.hora_fin)
        duracion = fin - inicio
        return duracion.total_seconds() / 3600

    @property
    def esta_activo(self):
        """
        Verifica si el evento está activo (fecha >= hoy)
        """
        return self.fecha_realizacion >= date.today()
