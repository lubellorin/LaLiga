from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import datetime, date, timedelta

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class LigaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Liga
    form_class = LigaForm
    template_name = 'liga/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'change_liga'
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
        DataEstadios = []
        for ie in Estadios.objects.all():
            DataEstadios.append(ie.toJSON())
        DataHorarios = []
        for ih in Horarios.objects.all():
            DataHorarios.append(ih.toJSON())
        DataCalendario = []
        for ic in Calendario.objects.all():
            DataCalendario.append(ic.toJSON())
        context['DataLiga'] = DataLiga
        context['Estadios'] = DataEstadios
        context['Horarios'] = DataHorarios
        context['Calendarios'] = DataCalendario
        context['title'] = 'Editar Liga'
        context['entity'] = 'La Liga'
        context['list_url'] = self.success_url
        context['url_create_estadio'] = reverse_lazy('erp:estadio_create')
        context['url_create_horario'] = reverse_lazy('erp:horario_create')
        context['url_create_calendario'] = reverse_lazy('erp:calendario_create')
        context['action'] = 'edit'
        return context


class EstadioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Estadios
    form_class = EstadioForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'add_estadios'
    url_redirect = success_url

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
        context['title'] = 'Agregar Estadio'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class EstadioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Estadios
    form_class = EstadioForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'change_estadios'
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
        context['title'] = 'Editar Estadio'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class EstadioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Estadios
    template_name = 'liga/delete_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'delete_estadios'
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
        context['title'] = 'Eliminar Estadio'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        return context


class HorariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Horarios
    form_class = HorariosForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'add_horarios'
    url_redirect = success_url

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
        context['title'] = 'Agregar Horarios'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class HorariosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Horarios
    form_class = HorariosForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'change_horarios'
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
        context['title'] = 'Editar Horarios'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class HorariosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Horarios
    template_name = 'liga/delete_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'delete_horarios'
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
        context['title'] = 'Eliminar Horarios'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        return context


class CalendarioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Calendario
    form_class = CalendarioForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'add_calendario'
    url_redirect = success_url

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
        context['title'] = 'Agregar Calendario'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CalendarioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Calendario
    form_class = CalendarioForm
    template_name = 'liga/create_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
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
        context['title'] = 'Editar Calendario'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CalendarioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Calendario
    template_name = 'liga/delete_estadio.html'
    success_url = reverse_lazy('erp:liga_update', kwargs={'pk': 1})
    permission_required = 'delete_calendario'
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
        context['title'] = 'Eliminar Calendario'
        context['entity'] = 'Liga'
        context['list_url'] = self.success_url
        return context

