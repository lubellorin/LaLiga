from datetime import datetime

from django.db.models.functions import Upper, Substr
from django.forms import *
from django import forms

from core.erp.models import *


class LigaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Liga
        fields = '__all__'
        widgets = {'Descripcion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese una Descripción'})}
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TipoIdentificacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = TiposIdentificacion
        fields = '__all__'
        widgets = {'Descripcion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese una Descripción',}),}
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EquiposForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Equipos
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'JuegosGanados', 'JuegosPerdidos', 'JuegosEmpatados', 'CarrerasFavor', 'CarrerasContra']
        widgets = {'Nombre': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'}),
                   'Descripcion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese una Reseña'}),
                   'Manager': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'}),
                   'TlfManager': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nro. Celular'}),
                   'Delegado': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'}),
                   'TlfDelegado': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nro. Celular'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GaleriaForm(ModelForm):
    Equipo = forms.ModelChoiceField(queryset=Equipos.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Galeria
        fields = '__all__'
        widgets = {'Descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una Descripción', 'style': 'width: 100%', 'rows': 5, 'cols': 125})}
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EntrevistasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Entrevistas
        fields = '__all__'
        widgets = {'Descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una Descripción', 'style': 'width: 100%', 'rows': 5, 'cols': 125})}
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class JugadorAddForm(ModelForm):
    TpIdentificacion = ModelChoiceField(queryset=TiposIdentificacion.objects.all(), widget=Select(attrs={
        'class': 'form-control select2', 'style': 'width: 100%'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TpIdentificacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Jugadores
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'Equipo', 'EsContacto', 'JuegosJugados', 'BAT_VB', 'BAT_H', 'BAT_2B', 'BAT_3B', 'BAT_HR',
                   'BAT_BB', 'BAT_K', 'BAT_SF', 'BAT_BR', 'BAT_CI', 'BAT_CA', 'BAT_HDEB', 'Error', 'Asistencia', 'PIT_IP', 'PIT_HP', 'PIT_CP',
                   'PIT_CS', 'PIT_K', 'PIT_BB', 'PIT_2B', 'PIT_3B', 'PIT_HR']
        widgets = {'TpIdentificacion': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
                   'NroIdentificacion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Nro. Identificación', 'style': 'width: 100%'}),
                   'Nombres': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%'}),
                   'ApellidoPaterno': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido Paterno', 'style': 'width: 100%'}),
                   'ApellidoMaterno': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido Materno', 'style': 'width: 100%'}),
                   'FechaNacimiento': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'),
                                                                          'style': 'width: 100%',
                                                                          'autocomplete': 'off',
                                                                          'class': 'form-control datetimepicker-input',
                                                                          'id': 'Fecha', 'data-target': '#Fecha',
                                                                          'data-toggle': 'datetimepicker'}),
                   'Telefonos': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nro. Telefono', 'style': 'width: 100%'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class JugadorMuestraNrosForm(ModelForm):
    TpIdentificacion = ModelChoiceField(queryset=TiposIdentificacion.objects.all(), widget=Select(attrs={
        'class': 'form-control select2', 'style': 'width: 100%'}))
    Equipo = ModelChoiceField(queryset=Equipos.objects.all(), widget=Select(attrs={
        'class': 'form-control select2', 'style': 'width: 100%'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TpIdentificacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Jugadores
        fields = '__all__'
        exclude = ['user_updated', 'user_creation']
        widgets = {'TpIdentificacion': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
                   'NroIdentificacion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Nro. Identificación', 'style': 'width: 100%'}),
                   'Nombres': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres', 'style': 'width: 100%'}),
                   'ApellidoPaterno': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido Paterno', 'style': 'width: 100%'}),
                   'ApellidoMaterno': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido Materno', 'style': 'width: 100%'}),
                   'FechaNacimiento': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'),
                                                                          'style': 'width: 100%',
                                                                          'autocomplete': 'off',
                                                                          'class': 'form-control datetimepicker-input',
                                                                          'id': 'Fecha', 'data-target': '#Fecha',
                                                                          'data-toggle': 'datetimepicker'}),
                   'Telefonos': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nro. Telefono', 'style': 'width: 100%'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EstadioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Estadios
        fields = '__all__'
        widgets = {
                    'Nombre': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'}),
                    'Direccion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese una Direccion'})
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class HorariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Horarios
        fields = '__all__'
        widgets = {'Descripcion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'})}
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CalendarioForm(ModelForm):
    Activo = forms.ChoiceField(choices=[('S', 'SI'), ('N', 'NO')], widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Descripcion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Calendario
        fields = '__all__'
        widgets = {
            'Descripcion': TextInput(attrs={'class': 'form-control', 'style': 'width: 100%', 'autocomplete': 'off', 'placeholder': 'Ingrese un Nombre'}),
            'Activo': TextInput(attrs={'class': 'form-control select2', 'style': 'width: 100%'})
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class JornadaAddForm(ModelForm):
    Estadio = ModelChoiceField(queryset=Estadios.objects.all(), widget=Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}))
    Horario = ModelChoiceField(queryset=Horarios.objects.all(), widget=Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}))
    Visitante = forms.ModelChoiceField(queryset=Equipos.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    HomeClub = forms.ModelChoiceField(queryset=Equipos.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Estadio'].widget.attrs['autofocus'] = True

    class Meta:
        model = DetalleCalendario
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'Calendario', 'LogoVisitante', 'LogoHomeClub', 'CarrerasVisitante', 'CarrerasHomeClub',
                   'PitcherGanador', 'PitcherPerdedor', 'MVP', 'Pizarra']
        widgets = {'Estadio': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
                   'Horario': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Horario', 'style': 'width: 100%'}),
                   'Visitante': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese El Equipo Visitante', 'style': 'width: 100%'}),
                   'HomeClub': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese El Equipo HomeClub', 'style': 'width: 100%'}),
                   'Fecha': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'),
                                                                          'style': 'width: 100%',
                                                                          'autocomplete': 'off',
                                                                          'class': 'form-control datetimepicker-input',
                                                                          'id': 'Fecha', 'data-target': '#Fecha',
                                                                          'data-toggle': 'datetimepicker'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class JornadaActForm(ModelForm):
    Estadio = ModelChoiceField(queryset=Estadios.objects.all(), widget=Select(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'readonly': True, 'disabled': 'disabled', }))
    Horario = ModelChoiceField(queryset=Horarios.objects.all(), widget=Select(attrs={'class': 'form-control select2', 'style': 'width: 100%', 'readonly': True, 'disabled': 'disabled', }))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Estadio'].widget.attrs['autofocus'] = True

    class Meta:
        model = DetalleCalendario
        fields = '__all__'
        exclude = ['user_updated', 'user_creation', 'Calendario', 'LogoVisitante', 'LogoHomeClub', 'Estadio', 'Horario', 'Visitante', 'HomeClub', 'Fecha', 'PitcherGanador', 'PitcherPerdedor', 'MVP']
        widgets = {'CarrerasVisitante': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Carreras del Visitante', 'style': 'width: 100%'}),
                   'CarrerasHomeClub': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Carreras del HomeClub', 'style': 'width: 100%'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
