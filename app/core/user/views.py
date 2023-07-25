from datetime import datetime, date, time, timedelta
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.db import transaction

from core.user.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.user.models import User
from core.erp.models import *

from core.erp.forms import EquiposForm


class UserListView(ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    item = i.toJSON()
                    DataEquipo = Equipos.objects.filter(id=i.Equipo).values_list("Nombre", flat=True)
                    for xxx in DataEquipo:
                        lv_NombreEquipo = xxx
                    item['NombreEquipo'] = lv_NombreEquipo
                    data.append(item)
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
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                data = {}
                form = self.get_form()
                data = form.save()
                lnn = request.POST['username']
                li_Equipo = request.POST['Equipo']
                DataUser = User.objects.filter(username=lnn)
                for c in DataUser:
                    cta = User()
                    cta.id = c.id
                    cta.password = c.password
                    cta.last_login = c.last_login
                    cta.is_superuser = 1
                    cta.username = c.username
                    cta.first_name = c.first_name
                    cta.last_name = c.last_name
                    cta.email = c.email
                    cta.is_staff = 1
                    cta.is_active = 1
                    cta.date_joined = c.date_joined
                    cta.image = c.image
                    cta.Equipo = li_Equipo
                    cta.save()
            elif action == 'create_equipo':
                data = {}
                print(action)
                with transaction.atomic():
                    frmCaja = EquiposForm(request.POST)
                    data = frmCaja.save()
                    for i in Equipos.objects.filter(Nombre=request.POST['Nombre']):
                        data['id'] = i.id
                        data['Nombre'] = i.Nombre
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
        context['title'] = 'Agregar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['frmCaja'] = EquiposForm()
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                li_id = self.get_object().id
                DataUser = User.objects.filter(id=li_id)
                li_Equipo = int(request.POST['Equipo'])
                for c in DataUser:
                    cta = User()
                    cta.id = c.id
                    cta.password = c.password
                    cta.last_login = c.last_login
                    cta.is_superuser = c.is_superuser
                    cta.username = request.POST['username']
                    cta.first_name = request.POST['first_name']
                    cta.last_name = request.POST['last_name']
                    cta.email = request.POST['email']
                    cta.is_staff = c.is_staff
                    cta.is_active = c.is_active
                    cta.date_joined = c.date_joined
                    cta.image = request.FILES.get("image")
                    cta.Equipo = li_Equipo
                    cta.save()
                # form = self.get_form()
                # data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print('Error General: ' + str(e))
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DataLiga = []
        for i in Liga.objects.all():
            DataLiga.append(i.toJSON())
        context['DataLiga'] = DataLiga
        context['title'] = 'Editar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'delete_user'
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
        context['title'] = 'Eliminar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('erp:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                li_id = self.get_object().id
                DataUser = User.objects.filter(id=li_id)
                li_Equipo = int(request.POST['Equipo'])
                for c in DataUser:
                    cta = User()
                    cta.id = c.id
                    cta.password = c.password
                    cta.last_login = c.last_login
                    cta.is_superuser = c.is_superuser
                    cta.username = request.POST['username']
                    cta.first_name = request.POST['first_name']
                    cta.last_name = request.POST['last_name']
                    cta.email = request.POST['email']
                    cta.is_staff = c.is_staff
                    cta.is_active = c.is_active
                    cta.date_joined = c.date_joined
                    cta.image = request.FILES.get("image")
                    cta.Equipo = li_Equipo
                    cta.save()
                # form = self.get_form()
                # data = form.save()
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
        context['title'] = 'Editar Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserChangePasswordView(FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña Actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su Nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su Nueva contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
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
        context['title'] = 'Editar Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserUpdateGroupsView(UpdateView):
    model = User
    form_class = UserGroupsForm
    template_name = 'user/groups.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'groups':
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
        context['title'] = 'Editar Grupos de Usuarios'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'groups'
        return context


class UserChangeGroup(View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy('erp:dashboard'))