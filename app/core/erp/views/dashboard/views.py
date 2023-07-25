from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import *


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # if action == 'get_graph_sales_year_month':
            #     data = {
            #         'name': 'Ventas',
            #         'showInLegend': False,
            #         'colorByPoint': True,
            #         'data': self.get_graph_sales_year_month()
            #     }
            # elif action == 'get_graph_sales_products_year_month':
            #     data = {
            #         'name': 'Ventas',
            #         'colorByPoint': True,
            #         'data': self.get_graph_sales_products_year_month(),
            #     }
            # else:
            #     data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # @staticmethod
    # def get_graph_sales_year_month():
    #     data = []
    #     try:
    #         ln_trx = Transacciones.objects.filter(Descripcion__icontains="Ventas").values_list("id", flat=True)
    #         for xxx in ln_trx:
    #             trx = xxx
    #         year = datetime.now().year
    #         for m in range(1, 13):
    #             total_ventas = MaestroMovimientos.objects.filter(Transaccion_id=trx).filter(Fecha__year=year, Fecha__month=m).aggregate(Sum('Total', default=0))
    #             data.append(float(total_ventas['Total__sum']))
    #     except:
    #         pass
    #     return data
    #
    # @staticmethod
    # def get_graph_sales_products_year_month():
    #     data = []
    #     year = datetime.now().year
    #     month = datetime.now().month
    #     try:
    #         ln_trx = Transacciones.objects.filter(Descripcion__icontains="Ventas").values_list("id", flat=True)
    #         for xxx in ln_trx:
    #             trx = xxx
    #         for p in Catalogo.objects.all():
    #             t_ventas = MaestroMovimientos.objects.filter(Transaccion_id=trx).filter(Fecha__year=year, Fecha__month=month)
    #             print(t_ventas)
    #             ln_Total = 0.00
    #             for h in t_ventas:
    #                 print('1')
    #                 ttt = DetalleMovimientos.objects.filter(Movimiento=h.id, Articulo_id=p.id)
    #                 for hx in ttt:
    #                     ln_Total = ln_Total + float(hx.Total)
    #             if ln_Total > 0:
    #                 data.append({
    #                 'name': p.Descripcion,
    #                 'y': float(ln_Total)
    #                 })
    #         print(data)
    #     except:
    #         pass
    #     return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['panel'] = 'Panel de administrador'
        context['Fecha'] = datetime.now().strftime('%d-%m-%Y')
        return context

