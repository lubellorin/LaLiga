from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.db import transaction

from core.erp.forms import JugadorAddForm, JugadorMuestraNrosForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *

import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


class JugadorDeleteView(DeleteView):
    model = Jugadores
    template_name = 'jugadores/delete.html'
    success_url = reverse_lazy('erp:equipos_menu')
    permission_required = 'delete_jugadores'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            li_User = self.request.user.id
            Data_User = User.objects.filter(id=li_User)
            for x1 in Data_User:
                userNombre = x1.first_name + ' ' + x1.last_name
            for ii in Jugadores.objects.filter(id=self.get_object().id):
                item = ii.toJSON()
                newGaleria = Galeria()
                newGaleria.Descripcion = userNombre + ' elimino del Roster de ' + ii.Equipo.Nombre + ' al Jugador ' + item['NombreCompleto'] + ' ' + ii.TpIdentificacion.Descripcion + ' ' + ii.NroIdentificacion
                newGaleria.Foto = ii.Foto
                newGaleria.Equipo_id = ii.Equipo.id
                newGaleria.save()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Eliminar Jugador'
        context['entity'] = 'Equipos'
        context['list_url'] = self.success_url
        return context


class MuestraNrosView(UpdateView):
    model = Jugadores
    template_name = 'jugadores/create.html'
    permission_required = 'view_jugadores'
    form_class = JugadorMuestraNrosForm
    success_url = reverse_lazy('erp:equipos_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        try:
            for ii in Jugadores.objects.filter(id=self.get_object().id):
                item = ii.toJSON()
                context['title'] = 'Estadisticas de ' + item['NombreCompleto']
                context['NombreCompleto'] = item['NombreCompleto']
                context['Ficha'] = ii.id
                context['JuegosJugados'] = ii.JuegosJugados
                context['FotoJugador'] = item['Foto']
                context['FotoEquipo'] = item['Equipo']['Logo']
                context['AVG'] = item['AVG']
                context['BAT_VB'] = ii.BAT_VB
                context['BAT_H'] = ii.BAT_H
                context['BAT_2B'] = ii.BAT_2B
                context['BAT_3B'] = ii.BAT_3B
                context['BAT_HR'] = ii.BAT_HR
                context['BAT_BB'] = ii.BAT_BB
                context['BAT_K'] = ii.BAT_K
                context['BAT_SF'] = ii.BAT_SF
                context['BAT_BR'] = ii.BAT_BR
                context['BAT_CI'] = ii.BAT_CI
                context['BAT_CA'] = ii.BAT_CA
                context['BAT_HDEB'] = ii.BAT_HDEB
                context['PIT_IP'] = ii.PIT_IP
                context['PIT_HP'] = ii.PIT_HP
                context['PIT_CP'] = ii.PIT_CP
                context['PIT_CS'] = ii.PIT_CS
                context['PIT_K'] = ii.PIT_K
                context['PIT_BB'] = ii.PIT_BB
                context['PIT_2B'] = ii.PIT_2B
                context['PIT_3B'] = ii.PIT_3B
                context['PIT_HR'] = ii.PIT_HR
                context['Efectividad'] = item['Efectividad']
                context['PIT_Ganados'] = ii.PIT_Ganados
                context['PIT_Perdido'] = item['PIT_Perdido']
                context['Error'] = ii.Error
                context['Asistencia'] = ii.Asistencia
                li_Equipo = ii.Equipo.id
        except Exception as e:
            error = '2: ' + str(e)
            print('Error: ', error)
        context['list_url'] = reverse_lazy('erp:roster_list', kwargs={'pk': li_Equipo})
        context['entity'] = 'Equipos'
        return context


class ActualizaNrosView(UpdateView):
    model = Jugadores
    template_name = 'jugadores/actualiza.html'
    permission_required = 'view_jugadores'
    form_class = JugadorMuestraNrosForm
    success_url = reverse_lazy('erp:equipos_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                li_Id = self.get_object().id
                for xy in Jugadores.objects.filter(id=li_Id):
                    ActJugadores = Jugadores()
                    ActJugadores.id = xy.id
                    ActJugadores.Equipo_id = xy.Equipo.id
                    ActJugadores.TpIdentificacion_id = xy.TpIdentificacion.id
                    ActJugadores.NroIdentificacion = xy.NroIdentificacion
                    ActJugadores.Nombres = xy.Nombres
                    ActJugadores.ApellidoPaterno = xy.ApellidoPaterno
                    ActJugadores.ApellidoMaterno = xy.ApellidoMaterno
                    ActJugadores.Foto = xy.Foto
                    ActJugadores.FechaNacimiento = xy.FechaNacimiento
                    ActJugadores.Telefonos = xy.Telefonos
                    ActJugadores.EsContacto = xy.EsContacto
                    ActJugadores.JuegosJugados = int(xy.JuegosJugados)
                    ActJugadores.BAT_VB = int(xy.BAT_VB) + int(request.POST['BAT_VB'])
                    ActJugadores.BAT_H = int(xy.BAT_H) + int(request.POST['BAT_H'])
                    ActJugadores.BAT_2B = int(xy.BAT_2B) + int(request.POST['BAT_2B'])
                    ActJugadores.BAT_3B = int(xy.BAT_3B) + int(request.POST['BAT_3B'])
                    ActJugadores.BAT_HR = int(xy.BAT_HR) + int(request.POST['BAT_HR'])
                    ActJugadores.BAT_BB = int(xy.BAT_BB) + int(request.POST['BAT_BB'])
                    ActJugadores.BAT_K = int(xy.BAT_K) + int(request.POST['BAT_K'])
                    ActJugadores.BAT_SF = int(xy.BAT_SF) + int(request.POST['BAT_SF'])
                    ActJugadores.BAT_BR = int(xy.BAT_BR) + int(request.POST['BAT_BR'])
                    ActJugadores.BAT_CI = int(xy.BAT_CI) + int(request.POST['BAT_CI'])
                    ActJugadores.BAT_CA = int(xy.BAT_CA) + int(request.POST['BAT_CA'])
                    ActJugadores.BAT_HDEB = int(xy.BAT_HDEB) + int(request.POST['BAT_HDEB'])
                    ActJugadores.Error = int(xy.Error) + int(request.POST['Error'])
                    ActJugadores.Asistencia = int(xy.Asistencia) + int(request.POST['Asistencia'])
                    ActJugadores.PIT_IP = int(xy.PIT_IP) + int(request.POST['PIT_IP'])
                    ActJugadores.PIT_HP = int(xy.PIT_HP) + int(request.POST['PIT_HP'])
                    ActJugadores.PIT_CP = int(xy.PIT_CP) + int(request.POST['PIT_CP'])
                    ActJugadores.PIT_CS = int(xy.PIT_CS) + int(request.POST['PIT_CS'])
                    ActJugadores.PIT_K = int(xy.PIT_K) + int(request.POST['PIT_K'])
                    ActJugadores.PIT_BB = int(xy.PIT_BB) + int(request.POST['PIT_BB'])
                    ActJugadores.PIT_2B = int(xy.PIT_2B) + int(request.POST['PIT_2B'])
                    ActJugadores.PIT_3B = int(xy.PIT_3B) + int(request.POST['PIT_3B'])
                    ActJugadores.PIT_HR = int(xy.PIT_HR) + int(request.POST['PIT_HR'])
                    ActJugadores.PIT_Ganados = int(xy.PIT_Ganados) + int(request.POST['PIT_Ganados'])
                    ActJugadores.PIT_Perdido = int(xy.PIT_Perdido) + int(request.POST['PIT_Perdido'])
                    ActJugadores.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        try:
            for ii in Jugadores.objects.filter(id=self.get_object().id):
                item = ii.toJSON()
                context['title'] = 'Estadisticas de ' + item['NombreCompleto']
                context['NombreCompleto'] = item['NombreCompleto']
                context['Ficha'] = ii.id
                context['JuegosJugados'] = ii.JuegosJugados
                context['FotoJugador'] = item['Foto']
                context['FotoEquipo'] = item['Equipo']['Logo']
                context['AVG'] = item['AVG']
                context['Efectividad'] = item['Efectividad']
                li_Equipo = ii.Equipo.id
        except Exception as e:
            error = '2: ' + str(e)
            print('Error: ', error)
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('erp:roster_list', kwargs={'pk': li_Equipo})
        context['entity'] = 'Equipos'
        return context


class FichaView(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('jugadores/ficha.html')
            Jugador = []
            for i in Jugadores.objects.filter(id=self.kwargs['pk']):
                item = i.toJSON()
                LogoEquipo = item['Equipo']['Logo']
                Jugador.append(item)
            DataLiga = []
            for i in Liga.objects.all():
                DataLiga.append(i.toJSON())
            context = {
                'jugador': Jugador,
                'Liga': DataLiga
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            error = str(e)
        return HttpResponseRedirect(reverse_lazy('erp:equipos_menu'))
