from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView
from django.db.models import F
from django.db.models import Count, Q

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class CalendarioListView(ListView):
    model = DetalleCalendario
    template_name = 'calendario/list.html'
    permission_required = 'view_calendario'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                li_Equipo = int(request.POST['idEquipo'])
                li_temporada = int(request.POST['Temporada'])
                lFecha = request.POST['Fecha']

                datosCalendario = DetalleCalendario.objects.filter(Calendario_id=li_temporada)
                if li_Equipo > 0:
                    for ixa in Equipos.objects.filter(id=li_Equipo):
                        lv_Equipo = ixa.Nombre
                    condicion_visitante = Q(Visitante=lv_Equipo)
                    condicion_homeclub = Q(HomeClub=lv_Equipo)
                    datosCalendario = datosCalendario.filter(condicion_visitante | condicion_homeclub)
                if lFecha != '0':
                    ld_Fecha = datetime.strptime(request.POST['Fecha'], "%d-%m-%Y")
                    year = ld_Fecha.year
                    month = ld_Fecha.month
                    day = ld_Fecha.day
                    datosCalendario = datosCalendario.filter(Fecha__year=year, Fecha__month=month, Fecha__day=day)
                fechas_conteo = datosCalendario.values('Fecha').annotate(cantidad=Count('Fecha'))
                Fechas = []
                for fecha_info in fechas_conteo:
                    fecha = fecha_info['Fecha'].strftime('%d-%m-%Y')
                    Fechas.append({'Fecha': fecha})
                    cantidad = int(fecha_info['cantidad'])
                    dtaFechasCalendario = []
                    if cantidad > 0:
                        dataJuegos = datosCalendario.order_by('Fecha', 'Horario')
                        print(datosCalendario.order_by('Fecha', 'Horario').query)
                        for lpdx in dataJuegos:
                            FechaC = lpdx.Fecha.strftime('%d-%m-%Y')
                            if fecha == FechaC:
                                dtaFechasCalendario.append(lpdx.toJSON())
                    data.append({'Fecha': fecha, 'Juegos': dtaFechasCalendario})

            elif action == 'search_homeclub':
                li_id = request.POST['id']
                data = []
                for i in Equipos.objects.exclude(id=li_id):
                    data.append({'id': i.id, 'text': i.Nombre})
            elif action == 'search_fechas':
                data = [{'id': '', 'text': '------------'}]
                li_idCalendario = request.POST['id']
                for i in DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).values('Fecha').annotate(cantidad=Count('Fecha')):
                    fecha = i['Fecha'].strftime('%d-%m-%Y')
                    data.append({'id': fecha, 'text': fecha})
            elif action == 'create_jornada':
                for i in Equipos.objects.all():
                    if i.id == int(request.POST['Visitante']):
                        lv_Visitante = i.Nombre
                        lv_LogoVisitante = i.Logo
                    elif i.id == int(request.POST['HomeClub']):
                        lv_HomeClub = i.Nombre
                        lv_LogoHomeClub = i.Logo
                newJornada = DetalleCalendario()
                newJornada.Calendario_id = request.POST['Calendario']
                newJornada.Estadio_id = request.POST['Estadio']
                newJornada.Fecha = datetime.strptime(request.POST['Fecha'], "%Y-%m-%d")
                newJornada.Horario_id = request.POST['Horario']
                newJornada.Visitante = lv_Visitante
                newJornada.LogoVisitante = lv_LogoVisitante
                newJornada.HomeClub = lv_HomeClub
                newJornada.LogoHomeClub = lv_LogoHomeClub
                newJornada.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dtaCalendario = []
        dtaTemporadas = []
        for lp in Calendario.objects.all():
            dtaTemporadas.append(lp.toJSON())
            if lp.Activo == 'S':
                li_idCalendario = lp.id
        for lpd in DetalleCalendario.objects.filter(Calendario_id=li_idCalendario):
            dtaCalendario.append(lpd.toJSON())
        dtaEquipos = []
        for lep in Equipos.objects.all():
            dtaEquipos.append({'id': lep.id, 'Descripcion': lep.Nombre, })
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        fechas_conteo = DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).values('Fecha').annotate(cantidad=Count('Fecha'))
        FechasCalendario = []
        Fechas = []
        for fecha_info in fechas_conteo:
            fecha = fecha_info['Fecha'].strftime('%d-%m-%Y')
            Fechas.append({'Fecha': fecha})
            cantidad = int(fecha_info['cantidad'])
            dtaFechasCalendario = []
            if cantidad > 0:
                dataJuegos = DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).order_by('Fecha', 'Horario')
                for lpdx in dataJuegos:
                    FechaC = lpdx.Fecha.strftime('%d-%m-%Y')
                    if fecha == FechaC:
                        dtaFechasCalendario.append(lpdx.toJSON())
            FechasCalendario.append({'Fecha': fecha, 'Juegos': dtaFechasCalendario})
        context['DataLiga'] = DataLiga
        context['title'] = 'Calendario'
        context['create_url'] = reverse_lazy('erp:galeria_create')
        context['list_url'] = reverse_lazy('erp:galeria_list')
        context['entity'] = 'Calendario'
        context['action'] = 'searchdata'
        context['idEquipo'] = 0
        context['FechasCalendario'] = FechasCalendario
        context['ListadoEquipos'] = dtaEquipos
        context['Fechas'] = Fechas
        context['Temporadas'] = dtaTemporadas
        context['frmAddJornada'] = JornadaAddForm()
        return context


class JornadaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = DetalleCalendario
    form_class = JornadaActForm
    template_name = 'calendario/create.html'
    success_url = reverse_lazy('erp:calendario_list')
    permission_required = 'change_calendario'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                for h in DetalleCalendario.objects.filter(id=self.get_object().id):
                    actJornada = DetalleCalendario()
                    actJornada.id = h.id
                    actJornada.Calendario_id = h.Calendario.id
                    actJornada.Estadio_id = h.Estadio.id
                    actJornada.Fecha = h.Fecha
                    actJornada.Horario_id = h.Horario.id
                    actJornada.Visitante = h.Visitante
                    actJornada.LogoVisitante = h.LogoVisitante
                    actJornada.HomeClub = h.HomeClub
                    actJornada.LogoHomeClub = h.LogoHomeClub
                    actJornada.CarrerasVisitante = request.POST['CarrerasVisitante']
                    actJornada.CarrerasHomeClub = request.POST['CarrerasHomeClub']
                    actJornada.PitcherGanador = request.POST['textoPG']
                    actJornada.PitcherPerdedor = request.POST['textoPP']
                    actJornada.MVP = request.POST['textoMVP']
                    actJornada.Pizarra = request.FILES.get('Pizarra', False)
                    actJornada.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        jugadoresVisitante = []
        jugadoresHomeClub = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())

        for h in DetalleCalendario.objects.filter(id=self.get_object().id):
            itemH = h.toJSON()
            lv_Visitante = h.Visitante
            lv_HomeClub = h.HomeClub
            LogoVisitante = itemH['LogoVisitante']
            LogoHomeClub = itemH['LogoHomeClub']
            Estadio = h.Estadio.Nombre
            Horario = h.Horario.Descripcion
            Fecha = itemH['Fecha']

        for lep in Equipos.objects.all():
            if lep.Nombre == lv_Visitante:
                li_IdVisitante = lep.id
            if lep.Nombre == lv_HomeClub:
                li_IdHomeClub = lep.id

        for ii in Jugadores.objects.filter(Equipo_id=li_IdVisitante):
            item = ii.toJSON()
            jugadoresVisitante.append({'id': ii.id, 'text': item['NombreCompleto']})

        for iii in Jugadores.objects.filter(Equipo_id=li_IdHomeClub):
            item = iii.toJSON()
            jugadoresHomeClub.append({'id': iii.id, 'text': item['NombreCompleto']})

        context['DataLiga'] = DataLiga
        context['title'] = 'Actualizar Jornada'
        context['entity'] = 'Calendario'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['LogoVisitante'] = LogoVisitante
        context['Visitante'] = lv_Visitante
        context['jugadoresVisitante'] = jugadoresVisitante
        context['LogoHomeClub'] = LogoHomeClub
        context['HomeClub'] = lv_HomeClub
        context['jugadoresHomeClub'] = jugadoresHomeClub
        context['Estadio'] = Estadio
        context['Horario'] = Horario
        context['Fecha'] = Fecha
        return context
