from django.db.models import Count
from django.views.generic import TemplateView
from datetime import datetime, date, time, timedelta
import locale
import os
from django.conf import settings
from django.template import Context
from core.erp.models import *


class IndexView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        dataLiderKO = []
        for d4 in Jugadores.objects.all().order_by('-PIT_K')[:1]:
            dataLiderKO.append(d4.toJSON())
        dataLiderGanados = []
        for d8 in Jugadores.objects.all().order_by('-PIT_Ganados')[:1]:
            dataLiderGanados.append(d8.toJSON())
        dataLiderImpulsadas = []
        for d9 in Jugadores.objects.all().order_by('-BAT_CI')[:1]:
            dataLiderImpulsadas.append(d9.toJSON())
        dataLiderHR = []
        for d10 in Jugadores.objects.all().order_by('-BAT_HR')[:1]:
            dataLiderHR.append(d10.toJSON())
        datBateo = []
        for d11 in Jugadores.objects.all():
            item = d11.toJSON()
            datBateo.append(
                {'Jugador': item['Jugador'], 'AVG': item['AVG'], 'Foto': item['Foto'], 'Nombres': d11.Nombres,
                 'ApellidoPaterno': d11.ApellidoPaterno, 'Equipo': d11.Equipo.Nombre})
        data_ordenado = sorted(datBateo, key=lambda x: x["AVG"], reverse=True)
        dataLiderBateo = data_ordenado[:1]
        datEquipos = []
        for d12 in Equipos.objects.all():
            item = d12.toJSON()
            datEquipos.append({
                'Logo': item['Logo'],
                'Nombre': d12.Nombre,
                'Jugados': int(d12.JuegosGanados) + int(d12.JuegosPerdidos) + int(d12.JuegosEmpatados),
                'Ganados': d12.JuegosGanados,
                'Perdidos': d12.JuegosPerdidos,
                'Empatados': d12.JuegosEmpatados,
                'Puntos': item['Puntos'],
                'Favor': d12.CarrerasFavor,
                'Contra': d12.CarrerasContra,
                'AVG': item['AVG'],
            })
        dataTabla = sorted(datEquipos, key=lambda x: (x['Puntos'], x['AVG']), reverse=True)
        dtaGaleria = []
        for lp in Galeria.objects.all().order_by('-date_creation')[:6]:
            dtaGaleria.append(lp.toJSON())
        dtaEntrevistas = []
        for lp in Entrevistas.objects.all().order_by('-date_creation')[:6]:
            dtaEntrevistas.append(lp.toJSON())
        for lp in Calendario.objects.filter(Activo='S'):
            li_idCalendario = lp.id

        ld_Hoy = '2023-06-20'#datetime.now().strftime('%Y-%m-%d')
        dataProximosJuegos = []
        dataJuegosAnteriores = []
        ld_FechaJornadaAnterior = ''
        ld_FechaProximaJornada = ''
        ld_ProximaJornada = ''
        ld_JornadaAnterior = ''
        for pj in DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).filter(Fecha__gte=ld_Hoy).order_by('Fecha')[:1]:
            ld_FechaProximaJornada = pj.Fecha.strftime('%Y-%m-%d')[:10]
            ld_ProximaJornada = pj.Fecha.strftime('%d-%m-%Y')
        for ja in DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).filter(Fecha__lte=ld_Hoy).order_by('-Fecha')[:1]:
            ld_FechaJornadaAnterior = ja.Fecha.strftime('%Y-%m-%d')[:10]
            ld_JornadaAnterior = ja.Fecha.strftime('%d-%m-%Y')

        ln_CantProxJuegos = 0
        ln_CantAntJuegos = 0
        for jpj in DetalleCalendario.objects.filter(Calendario_id=li_idCalendario).order_by('Fecha', 'Horario'):
            ld_Fecha = jpj.Fecha.strftime('%Y-%m-%d')[:10]
            if ld_Fecha == ld_FechaJornadaAnterior:
                dataJuegosAnteriores.append(jpj.toJSON())
                ln_CantAntJuegos = 1
            elif ld_Fecha == ld_FechaProximaJornada:
                dataProximosJuegos.append(jpj.toJSON())
                ln_CantProxJuegos = 1

        context = super().get_context_data(**kwargs)
        context['Tabla'] = dataTabla
        context['dataLiderKO'] = dataLiderKO
        context['dataLiderImpulsadas'] = dataLiderImpulsadas
        context['dataLiderHR'] = dataLiderHR
        context['dataLiderGanados'] = dataLiderGanados
        context['dataLiderBateo'] = dataLiderBateo
        context['DataLiga'] = DataLiga
        context['galeria'] = dtaGaleria
        context['entrevistas'] = dtaEntrevistas
        context['panel'] = 'Panel de administrador'
        context['Fecha'] = datetime.now().strftime('%d-%m-%Y')
        context['ProximosJuegos'] = dataProximosJuegos
        context['JuegosAnteriores'] = dataJuegosAnteriores
        context['FechaProximosJuegos'] = ld_ProximaJornada
        context['FechaJuegosAnteriores'] = ld_JornadaAnterior
        context['CantProximosJuegos'] = ln_CantProxJuegos
        context['CantJuegosAnteriores'] = ln_CantAntJuegos
        return context


class EstadisticasView(TemplateView):
    template_name = 'numeros.html'

    def get_context_data(self, **kwargs):
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        dataKORecibidos = []
        for d1 in Jugadores.objects.all().order_by('-BAT_K')[:10]:
            dataKORecibidos.append(d1.toJSON())
        dataBBRecibidos = []
        for d2 in Jugadores.objects.all().order_by('-BAT_BB')[:10]:
            dataBBRecibidos.append(d2.toJSON())
        dataBRRecibidos = []
        for d3 in Jugadores.objects.all().order_by('-BAT_BR')[:10]:
            dataBRRecibidos.append(d3.toJSON())
        dataKOPropinados = []
        dataLiderKO = []
        sw = 1
        for d4 in Jugadores.objects.all().order_by('-PIT_K')[:10]:
            if sw == 1:
                dataLiderKO.append(d4.toJSON())
                sw = 2
            dataKOPropinados.append(d4.toJSON())
        dataAnotadas = []
        for d5 in Jugadores.objects.all().order_by('-BAT_CA')[:10]:
            dataAnotadas.append(d5.toJSON())
        dataTriples = []
        for d6 in Jugadores.objects.all().order_by('-BAT_3B')[:10]:
            dataTriples.append(d6.toJSON())
        dataDobles = []
        for d7 in Jugadores.objects.all().order_by('-BAT_2B')[:10]:
            dataDobles.append(d7.toJSON())
        dataGanados = []
        dataLiderGanados = []
        sw = 1
        for d8 in Jugadores.objects.all().order_by('-PIT_Ganados')[:10]:
            dataGanados.append(d8.toJSON())
            if sw == 1:
                dataLiderGanados.append(d8.toJSON())
                sw = 2
        dataImpulsadas = []
        dataLiderImpulsadas = []
        sw = 1
        for d9 in Jugadores.objects.all().order_by('-BAT_CI')[:10]:
            if sw == 1:
                dataLiderImpulsadas.append(d9.toJSON())
                sw = 2
            dataImpulsadas.append(d9.toJSON())
        dataHR = []
        dataLiderHR = []
        sw = 1
        for d10 in Jugadores.objects.all().order_by('-BAT_HR')[:10]:
            dataHR.append(d10.toJSON())
            if sw == 1:
                dataLiderHR.append(d10.toJSON())
                sw = 2
        datBateo = []
        for d11 in Jugadores.objects.all():
            item = d11.toJSON()
            datBateo.append({'Jugador': item['Jugador'], 'AVG': item['AVG'], 'Foto': item['Foto'], 'Nombres': d11.Nombres, 'ApellidoPaterno': d11.ApellidoPaterno, 'Equipo': d11.Equipo.Nombre})
        data_ordenado = sorted(datBateo, key=lambda x: x["AVG"], reverse=True)
        dataBateo = data_ordenado[:10]
        dataLiderBateo = data_ordenado[:1]

        datEquipos = []
        for d12 in Equipos.objects.all():
            item = d12.toJSON()
            datEquipos.append({
                'Logo': item['Logo'],
                'Nombre': d12.Nombre,
                'Jugados': int(d12.JuegosGanados) + int(d12.JuegosPerdidos) + int(d12.JuegosEmpatados),
                'Ganados': d12.JuegosGanados,
                'Perdidos': d12.JuegosPerdidos,
                'Empatados': d12.JuegosEmpatados,
                'Puntos': item['Puntos'],
                'Favor': d12.CarrerasFavor,
                'Contra': d12.CarrerasContra,
                'AVG': item['AVG'],
            })
        dataTabla = sorted(datEquipos, key=lambda x: (x['Puntos'], x['AVG']), reverse=True)
        context = super().get_context_data(**kwargs)
        context['DataLiga'] = DataLiga
        context['KORecibidos'] = dataKORecibidos
        context['BBRecibidos'] = dataBBRecibidos
        context['BRRecibidos'] = dataBRRecibidos
        context['KOPropinados'] = dataKOPropinados
        context['Anotadas'] = dataAnotadas
        context['Triples'] = dataTriples
        context['Dobles'] = dataDobles
        context['Ganados'] = dataGanados
        context['Impulsadas'] = dataImpulsadas
        context['HR'] = dataHR
        context['Bateo'] = dataBateo
        context['Tabla'] = dataTabla
        context['dataLiderKO'] = dataLiderKO
        context['dataLiderImpulsadas'] = dataLiderImpulsadas
        context['dataLiderHR'] = dataLiderHR
        context['dataLiderGanados'] = dataLiderGanados
        context['dataLiderBateo'] = dataLiderBateo
        context['panel'] = 'Panel de administrador'
        context['Fecha'] = datetime.now().strftime('%d-%m-%Y')
        return context


class ContactosView(TemplateView):
    template_name = 'contactos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        dataContactos = []
        for dC in Jugadores.objects.filter(EsContacto='S'):
            dataContactos.append(dC.toJSON())
        context['DataLiga'] = DataLiga
        context['dataContactos'] = dataContactos
        context['panel'] = 'Panel de administrador'
        context['Fecha'] = datetime.now().strftime('%d-%m-%Y')
        return context

