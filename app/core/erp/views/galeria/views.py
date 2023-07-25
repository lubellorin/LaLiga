from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import *


class GaleriaListView(ListView):
    model = Galeria
    template_name = 'galeria/list.html'
    permission_required = 'view_galeria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                datosGaleria = []
                liEquipo = int(request.POST['idEquipo'])
                if liEquipo == 0:
                    datosGaleria = Galeria.objects.all()
                else:
                    datosGaleria = Galeria.objects.filter(Equipo_id=liEquipo)
                for i in datosGaleria:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dtaGaleria = []
        for lp in Galeria.objects.all():
            dtaGaleria.append(lp.toJSON())
        dtaEquipos = []
        for lep in Equipos.objects.all():
            dtaEquipos.append({'id': lep.id, 'Descripcion': lep.Nombre, })
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Galeria de Noticias'
        context['create_url'] = reverse_lazy('erp:galeria_create')
        context['list_url'] = reverse_lazy('erp:galeria_list')
        context['entity'] = 'Galeria'
        context['action'] = 'searchdata'
        context['idEquipo'] = 0
        context['galeria'] = dtaGaleria
        context['ListadoEquipos'] = dtaEquipos
        return context


class GaleriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Galeria
    form_class = GaleriaForm
    template_name = 'galeria/create.html'
    success_url = reverse_lazy('erp:galeria_list')
    permission_required = 'add_galeria'
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
        context['title'] = 'Agregar Noticia'
        context['entity'] = 'Galeria'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context