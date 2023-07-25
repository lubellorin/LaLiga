from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class EntrevistasListView(ListView):
    model = Entrevistas
    template_name = 'entrevistas/list.html'
    permission_required = 'view_entrevistas'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Entrevistas.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dtaEntrevistas = []
        for lp in Entrevistas.objects.all():
            dtaEntrevistas.append(lp.toJSON())
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Galeria de Entrevistas'
        context['create_url'] = reverse_lazy('erp:entrevistas_create')
        context['list_url'] = reverse_lazy('erp:entrevistas_list')
        context['entity'] = 'Entrevistas'
        context['action'] = 'searchdata'
        context['entrevistas'] = dtaEntrevistas
        return context


class EntrevistasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Entrevistas
    form_class = EntrevistasForm
    template_name = 'entrevistas/create.html'
    success_url = reverse_lazy('erp:entrevistas_list')
    permission_required = 'add_entrevistas'
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
        context['title'] = 'Agregar Entrevista'
        context['entity'] = 'Entrevistas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
