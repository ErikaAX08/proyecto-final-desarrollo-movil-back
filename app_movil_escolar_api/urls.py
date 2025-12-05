from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from app_movil_escolar_api.views import bootstrap
from app_movil_escolar_api.views import users
from app_movil_escolar_api.views import alumnos
from app_movil_escolar_api.views import maestros
from app_movil_escolar_api.views import auth
from app_movil_escolar_api.views import eventos
from django.core.management import call_command
from django.http import HttpResponse

# from sistema_escolar_api.views import alumnos
# from sistema_escolar_api.views import maestros


def run_migrations(request):
    try:
        call_command("migrate")
        return HttpResponse("Migraciones ejecutadas correctamente.")
    except Exception as e:
        return HttpResponse(f"Error ejecutando migraciones: {e}")


urlpatterns = [
    # Create Admin
    path("admin/", users.AdminView.as_view()),
    path("run-migrations/", run_migrations),
    # Admin Data
    path("lista-admins/", users.AdminAll.as_view()),
    # Edit Admin
    # path('admins-edit/', users.AdminsViewEdit.as_view())
    # Create Alumno
    path("alumnos/", alumnos.AlumnosView.as_view()),
    # Alumnos Data
    path("lista-alumnos/", alumnos.AlumnosAll.as_view()),
    # Create Maestro
    path("maestros/", maestros.MaestrosView.as_view()),
    # Maestro Data
    path("lista-maestros/", maestros.MaestrosAll.as_view()),
    # Total Users
    path("total-usuarios/", users.TotalUsers.as_view()),
    # Login
    path("login/", auth.CustomAuthToken.as_view()),
    # Logout
    path("logout/", auth.Logout.as_view()),
    # CRUD de eventos académicos
    # POST: Registrar evento (solo admin)
    # GET: Obtener evento por ID (?id=X)
    # PUT: Actualizar evento (solo admin)
    # DELETE: Eliminar evento (?id=X) (solo admin)
    path(
        "eventos-academicos/",
        eventos.EventoAcademicoView.as_view(),
        name="eventos_academicos",
    ),
    # GET: Listar todos los eventos
    path("lista-eventos/", eventos.ListaEventosView.as_view(), name="lista_eventos"),
    # GET: Listar eventos filtrados por rol del usuario
    path(
        "eventos-por-rol/", eventos.EventosPorRolView.as_view(), name="eventos_por_rol"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
