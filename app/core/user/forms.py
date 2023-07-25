from datetime import datetime

from django.forms import *
from django import forms

from core.user.models import *
from core.erp.models import *


class UserForm(ModelForm):
    Equipo = forms.ModelChoiceField(queryset=Equipos.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image', 'groups'
        widgets = {'first_name': TextInput(attrs={'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'last_name': TextInput(attrs={'placeholder': 'Ingrese sus Apellidos', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'username': TextInput(attrs={'placeholder': 'Ingrese su Usuario', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'password': PasswordInput(render_value=True, attrs={'placeholder': 'Ingrese su Password', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'email': TextInput(attrs={'placeholder': 'Ingrese Email', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'groups': SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'multiple': 'multiple', 'autocomplete': 'off'})}
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserProfileForm(ModelForm):
    Equipo = forms.ModelChoiceField(queryset=Equipos.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'image', 'Equipo'
        widgets = {'first_name': TextInput(attrs={'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'last_name': TextInput(attrs={'placeholder': 'Ingrese sus Apellidos', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'username': TextInput(attrs={'placeholder': 'Ingrese su Usuario', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'Equipo': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
                   'email': TextInput(attrs={'placeholder': 'Ingrese Email', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'})}
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = 'Error en Forms: ' + str(form.errors)
        except Exception as e:
            data['error'] = str(e)
        return data


class UserGroupsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'groups'
        widgets = {'first_name': TextInput(attrs={'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control', 'readonly': True}),
                   'last_name': TextInput(attrs={'placeholder': 'Ingrese sus Apellidos', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control', 'readonly': True}),
                   'username': TextInput(attrs={'placeholder': 'Ingrese su Usuario', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control', 'readonly': True}),
                   'groups': SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'multiple': 'multiple'})}
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password', 'image', 'email']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                # if u.pk is None:
                #     u.set_password(pwd)
                # else:
                #     user = User.objects.get(pk=u.pk)
                #     if user.password != pwd:
                #         u.set_password(pwd)
                u.save()
                u.groups.clear()
                print(self.cleaned_data['groups'])
                for g in self.cleaned_data['groups']:
                    print(g.name)
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserUpdateProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'image'
        widgets = {'first_name': TextInput(attrs={'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'last_name': TextInput(attrs={'placeholder': 'Ingrese sus Apellidos', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'}),
                   'email': TextInput(attrs={'placeholder': 'Ingrese Email', 'style': 'width: 100%', 'autocomplete': 'off', 'class': 'form-control'})}
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password', 'groups', 'Equipo', 'username']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                u.save()
            else:
                data['error'] = 'Error en Forms: ' + str(form.errors)
        except Exception as e:
            data['error'] = str(e)
        return data