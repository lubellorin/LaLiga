from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.db import transaction

from core.erp.forms import EquiposForm, JugadorAddForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *

import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


class EquiposListView(ListView):
    model = Equipos
    template_name = 'equipos/list.html'
    permission_required = 'view_equipos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Equipos.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Listado de Equipos'
        context['create_url'] = reverse_lazy('erp:equipos_create')
        context['list_url'] = reverse_lazy('erp:equipos_list')
        context['entity'] = 'Equipos'
        return context


class EquiposMenuView(ListView):
    model = Equipos
    template_name = 'equipos/menu.html'
    permission_required = 'view_equipos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        equipos = []
        try:
            for i in Equipos.objects.all():
                item = i.toJSON()
                equipos.append(item)
        except Exception as e:
            error = '1: ' + str(e)
            print('Error: ', error)

        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Roster'
        context['opciones'] = equipos
        context['create_url'] = reverse_lazy('erp:equipos_create')
        context['list_url'] = reverse_lazy('erp:equipos_list')
        context['entity'] = 'Equipos'
        return context


class EquiposCreateView(CreateView):
    model = Equipos
    form_class = EquiposForm
    template_name = 'equipos/create.html'
    success_url = reverse_lazy('erp:equipos_list')
    permission_required = 'add_equipos'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Agregar Equipo'
        context['entity'] = 'Equipos'
        context['list_url'] = reverse_lazy('erp:equipos_list')
        context['action'] = 'add'
        return context


class EquiposUpdateView(UpdateView):
    model = Equipos
    form_class = EquiposForm
    template_name = 'equipos/create.html'
    success_url = reverse_lazy('erp:equipos_list')
    permission_required = 'change_equipos'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Editar Equipo'
        context['entity'] = 'Equipos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class EquiposDeleteView(DeleteView):
    model = Equipos
    template_name = 'equipos/delete.html'
    success_url = reverse_lazy('erp:equipos_list')
    permission_required = 'delete_equipos'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
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
        context['title'] = 'Eliminar Equipo'
        context['entity'] = 'Equipos'
        context['list_url'] = self.success_url
        return context


class RosterView(UpdateView):
    model = Equipos
    template_name = 'equipos/roster.html'
    permission_required = 'view_equipos'
    form_class = EquiposForm
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
            elif action == 'create_jugador':
                print(request.POST)
                NewJugador = Jugadores()
                NewJugador.Equipo_id = request.POST['Equipo_id']
                NewJugador.TpIdentificacion_id = request.POST['TpIdentificacion']
                NewJugador.NroIdentificacion = request.POST['NroIdentificacion']
                NewJugador.FechaNacimiento = request.POST['FechaNacimiento']
                NewJugador.Nombres = request.POST['Nombres']
                NewJugador.ApellidoPaterno = request.POST['ApellidoPaterno']
                NewJugador.ApellidoMaterno = request.POST['ApellidoMaterno']
                NewJugador.Telefonos = request.POST['Telefonos']
                NewJugador.Foto = request.FILES.get('Foto', False)
                NewJugador.save()
                li_idJugador = NewJugador.id
                li_User = self.request.user.id
                Data_User = User.objects.filter(id=li_User)
                for x1 in Data_User:
                    userNombre = x1.first_name + ' ' + x1.last_name
                for ii in Jugadores.objects.filter(id=li_idJugador):
                    item = ii.toJSON()
                    newGaleria = Galeria()
                    newGaleria.Descripcion = userNombre + ' Agrego en el Roster de ' + ii.Equipo.Nombre + ' al Jugador ' + item['NombreCompleto'] + ' ' + ii.TpIdentificacion.Descripcion + ' ' + ii.NroIdentificacion
                    newGaleria.Foto = ii.Foto
                    newGaleria.Equipo_id = ii.Equipo.id
                    newGaleria.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        equipos = []
        jugadores = []
        idEquipoUsuario = 0
        li_User = self.request.user.id
        Data_User = User.objects.filter(id=li_User)
        for x1 in Data_User:
            idEquipoUsuario = x1.Equipo
        try:
            for i in Equipos.objects.filter(id=self.get_object().id):
                item = i.toJSON()
                li_id = i.id
                lv_NombreEquipo = i.Nombre
                equipos.append(item)
        except Exception as e:
            error = '1: ' + str(e)
            print('Error: ', error)
        try:
            for ii in Jugadores.objects.filter(Equipo_id=self.get_object().id):
                item = ii.toJSON()
                jugadores.append(item)
        except Exception as e:
            error = '2: ' + str(e)
            print('Error: ', error)

        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Roster ' + lv_NombreEquipo
        context['equipos'] = equipos
        context['jugadores'] = jugadores
        context['list_url'] = reverse_lazy('erp:equipos_list')
        context['menu_url'] = reverse_lazy('erp:equipos_menu')
        context['roster_url'] = reverse_lazy('erp:roster_list', kwargs={'pk': self.get_object().id})
        context['entity'] = 'Equipos'
        context['idEquipo'] = idEquipoUsuario
        context['EquipoUsuario'] = li_id
        context['frmAddJugador'] = JugadorAddForm()
        return context



class FichaRosterView(View):
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
            template = get_template('equipos/ficha.html')
            data1 = []
            data2 = []
            data3 = []
            data4 = []
            data5 = []
            sw = 1
            for i in Jugadores.objects.filter(Equipo_id=self.kwargs['pk']):
                item = i.toJSON()
                if sw == 1:
                    sw = 2
                    data1.append(
                        {
                            'Foto': item['Foto'],
                            'NombreCompleto': item['NombreCompleto'],
                            'Id': i.id,
                            'Identificacion': i.TpIdentificacion.Descripcion + ' ' + i.NroIdentificacion,
                        }
                    )
                elif sw == 2:
                    sw = 3
                    data2.append(
                        {
                            'Foto': item['Foto'],
                            'NombreCompleto': item['NombreCompleto'],
                            'Id': i.id,
                            'Identificacion': i.TpIdentificacion.Descripcion + ' ' + i.NroIdentificacion,
                        }
                    )
                elif sw == 3:
                    sw = 4
                    data3.append(
                        {
                            'Foto': item['Foto'],
                            'NombreCompleto': item['NombreCompleto'],
                            'Id': i.id,
                            'Identificacion': i.TpIdentificacion.Descripcion + ' ' + i.NroIdentificacion,
                        }
                    )
                elif sw == 4:
                    sw = 5
                    data4.append(
                        {
                            'Foto': item['Foto'],
                            'NombreCompleto': item['NombreCompleto'],
                            'Id': i.id,
                            'Identificacion': i.TpIdentificacion.Descripcion + ' ' + i.NroIdentificacion,
                        }
                    )
                elif sw == 5:
                    sw = 1
                    data5.append(
                        {
                            'Foto': item['Foto'],
                            'NombreCompleto': item['NombreCompleto'],
                            'Id': i.id,
                            'Identificacion': i.TpIdentificacion.Descripcion + ' ' + i.NroIdentificacion,
                        }
                    )
            Equipo = []
            for i in Equipos.objects.filter(id=self.kwargs['pk']):
                item = i.toJSON()
                Equipo.append(item)
            DataLiga = []
            for i in Liga.objects.all():
                DataLiga.append(i.toJSON())
            context = {
                'equipo': Equipo,
                'LogoLiga': '{}{}'.format(settings.STATIC_URL, 'dist/img/LigaSoftballArequipa.jpg'),
                'data1': data1,
                'data2': data2,
                'data3': data3,
                'data4': data4,
                'data5': data5,
                'Liga': DataLiga
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            error = str(e)
            print(error)
        return HttpResponseRedirect(reverse_lazy('erp:equipos_menu'))