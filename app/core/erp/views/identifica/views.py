from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class TiposIdentificacionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TiposIdentificacion
    template_name = 'identifica/list.html'
    permission_required = 'view_tiposidentificacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TiposIdentificacion.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        li_User = self.request.user.id
        cantMsg = Comentarios.objects.filter(Estado='Pendiente').filter(Usuario=li_User).count()
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['cantMsg'] = cantMsg
        context['title'] = 'Listado de Tipos de Identificación'
        context['create_url'] = reverse_lazy('erp:identifica_create')
        context['list_url'] = reverse_lazy('erp:identifica_list')
        context['entity'] = 'TiposIdentificacion'
        return context


class TiposIdentificacionCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TiposIdentificacion
    form_class = TipoIdentificacionForm
    template_name = 'identifica/create.html'
    success_url = reverse_lazy('erp:identifica_list')
    permission_required = 'add_tiposidentificacion'
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
        li_User = self.request.user.id
        cantMsg = Comentarios.objects.filter(Estado='Pendiente').filter(Usuario=li_User).count()
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['cantMsg'] = cantMsg
        context['title'] = 'Agregar Tipo de Identificación'
        context['entity'] = 'TiposIdentificacion'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TiposIdentificacionUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TiposIdentificacion
    form_class = TipoIdentificacionForm
    template_name = 'identifica/create.html'
    success_url = reverse_lazy('erp:identifica_list')
    permission_required = 'change_tiposidentificacion'
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
        li_User = self.request.user.id
        cantMsg = Comentarios.objects.filter(Estado='Pendiente').filter(Usuario=li_User).count()
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['cantMsg'] = cantMsg
        context['title'] = 'Editar Tipo de Identificación'
        context['entity'] = 'TiposIdentificacion'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TiposIdentificacionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TiposIdentificacion
    template_name = 'identifica/delete.html'
    success_url = reverse_lazy('erp:identifica_list')
    permission_required = 'delete_tiposidentificacion'
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
        li_User = self.request.user.id
        cantMsg = Comentarios.objects.filter(Estado='Pendiente').filter(Usuario=li_User).count()
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['cantMsg'] = cantMsg
        context['title'] = 'Eliminar Tipo de Identificación'
        context['entity'] = 'TiposIdentificacion'
        context['list_url'] = self.success_url
        return context