from django.urls import path

from core.erp.views.dashboard.views import *
from core.erp.views.identifica.views import *
from core.erp.views.equipos.views import *
from core.erp.views.galeria.views import *
from core.erp.views.entrevistas.views import *
from core.erp.views.jugadores.views import *
from core.erp.views.liga.views import *
from core.erp.views.calendario.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Liga
    path('liga/update/<int:pk>/', LigaUpdateView.as_view(), name='liga_update'),
    path('liga/estadio/add/', EstadioCreateView.as_view(), name='estadio_create'),
    path('liga/estadio/update/<int:pk>/', EstadioUpdateView.as_view(), name='estadio_update'),
    path('liga/estadio/delete/<int:pk>/', EstadioDeleteView.as_view(), name='estadio_delete'),
    path('liga/horario/add/', HorariosCreateView.as_view(), name='horario_create'),
    path('liga/horario/update/<int:pk>/', HorariosUpdateView.as_view(), name='horario_update'),
    path('liga/horario/delete/<int:pk>/', HorariosDeleteView.as_view(), name='horario_delete'),
    path('liga/calendario/add/', CalendarioCreateView.as_view(), name='calendario_create'),
    path('liga/calendario/update/<int:pk>/', CalendarioUpdateView.as_view(), name='calendario_update'),
    path('liga/calendario/delete/<int:pk>/', CalendarioDeleteView.as_view(), name='calendario_delete'),
    # Tipos Identificacion
    path('identifica/list/', TiposIdentificacionListView.as_view(), name='identifica_list'),
    path('identifica/add/', TiposIdentificacionCreateView.as_view(), name='identifica_create'),
    path('identifica/update/<int:pk>/', TiposIdentificacionUpdateView.as_view(), name='identifica_update'),
    path('identifica/delete/<int:pk>/', TiposIdentificacionDeleteView.as_view(), name='identifica_delete'),
    # Equipos
    path('equipos/list/', EquiposListView.as_view(), name='equipos_list'),
    path('equipos/add/', EquiposCreateView.as_view(), name='equipos_create'),
    path('equipos/update/<int:pk>/', EquiposUpdateView.as_view(), name='equipos_update'),
    path('equipos/delete/<int:pk>/', EquiposDeleteView.as_view(), name='equipos_delete'),
    path('equipos/menu/', EquiposMenuView.as_view(), name='equipos_menu'),
    path('equipos/roster/<int:pk>/', RosterView.as_view(), name='roster_list'),
    path('equipos/ficha/<int:pk>/', FichaRosterView.as_view(), name='equipos_ficha'),
    # Galeria
    path('galeria/list/', GaleriaListView.as_view(), name='galeria_list'),
    path('galeria/add/', GaleriaCreateView.as_view(), name='galeria_create'),
    # Noticias
    path('entrevistas/list/', EntrevistasListView.as_view(), name='entrevistas_list'),
    path('entrevistas/add/', EntrevistasCreateView.as_view(), name='entrevistas_create'),
    # Jugadores
    path('jugadores/delete/<int:pk>/', JugadorDeleteView.as_view(), name='jugador_delete'),
    path('jugadores/muestranros/<int:pk>/', MuestraNrosView.as_view(), name='jugador_nros'),
    path('jugadores/actualizanros/<int:pk>/', ActualizaNrosView.as_view(), name='jugador_actualiza'),
    path('jugadores/ficha/<int:pk>/', FichaView.as_view(), name='jugador_ficha'),
    # Calendario
    path('calendario/list/', CalendarioListView.as_view(), name='calendario_list'),
    path('calendario/update/<int:pk>/', JornadaUpdateView.as_view(), name='jornada_update'),
]