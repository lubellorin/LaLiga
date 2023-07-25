from datetime import datetime

from crum import get_current_user
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel
from core.user.models import *
from django.conf import settings


class Liga(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    Logo = models.ImageField(upload_to='teams/Logo', null=True, blank=True, verbose_name='Logo')
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liga_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liga_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Liga, self).save()

    def get_image(self):
        if self.Logo:
            return '{}{}'.format(MEDIA_URL, self.Logo)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Logo'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Liga'
        verbose_name_plural = 'Liga'
        ordering = ['id']


class TiposIdentificacion(BaseModel):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tpidentifica_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tpidentifica_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(TiposIdentificacion, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TiposIdentificacion'
        verbose_name_plural = 'TiposIdentificacion'
        ordering = ['id']


class Equipos(models.Model):
    id = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=40, verbose_name="Nombre del Equipo")
    Logo = models.ImageField(upload_to='teams/Logo', null=True, blank=True, verbose_name='Logo')
    Descripcion = models.TextField(blank=True, verbose_name="Descripcion")
    Manager = models.CharField(max_length=60, null=True, verbose_name="Manager")
    TlfManager = models.CharField(max_length=20, null=True, verbose_name="Celular Manager")
    Delegado = models.CharField(max_length=60, null=True, verbose_name="Delegado")
    TlfDelegado = models.CharField(max_length=20, null=True, verbose_name="Celular Delegado")
    JuegosGanados = models.IntegerField(default=0, verbose_name="Juegos Ganados")
    JuegosPerdidos = models.IntegerField(default=0, verbose_name="Juegos Perdidos")
    JuegosEmpatados = models.IntegerField(default=0, verbose_name="Juegos Empatados")
    CarrerasFavor = models.IntegerField(default=0, verbose_name="Carreras A Favor")
    CarrerasContra = models.IntegerField(default=0, verbose_name="Carreras en Contra")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='equipos_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='equipos_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Nombre

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Equipos, self).save()

    def get_image(self):
        if self.Logo:
            return '{}{}'.format(MEDIA_URL, self.Logo)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Logo'] = self.get_image()
        for i in Jugadores.objects.filter(Equipo_id=item['id']).filter(EsContacto='S'):
            item['NombreContacto'] = i.Nombres + ' ' + i.ApellidoPaterno + ' ' + i.ApellidoMaterno
        item['AVG'] = int(self.CarrerasFavor) - int(self.CarrerasContra)
        item['Puntos'] = (int(self.JuegosGanados) * 3) + int(self.JuegosEmpatados)
        return item

    class Meta:
        verbose_name = 'Equipos'
        verbose_name_plural = 'Equipos'
        ordering = ['id']


class Galeria(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.TextField(blank=True, verbose_name="Descripcion")
    Foto = models.ImageField(upload_to='teams/Galeria', null=True, blank=True, verbose_name='Foto')
    Equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, verbose_name="Equipo")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='galeria_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='galeria_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Galeria, self).save()

    def get_image(self):
        if self.Foto:
            return '{}{}'.format(MEDIA_URL, self.Foto)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Foto'] = self.get_image()
        item['Equipo'] = self.Equipo.toJSON()
        return item

    class Meta:
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galerias'
        ordering = ['id']


class Jugadores(models.Model):
    id = models.AutoField(primary_key=True)
    Equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, verbose_name="Equipo")
    TpIdentificacion = models.ForeignKey(TiposIdentificacion, on_delete=models.CASCADE, verbose_name="Tipo Identificacion")
    NroIdentificacion = models.CharField(max_length=20, verbose_name="Nro. Identificacion")
    Nombres = models.CharField(max_length=30, verbose_name="Nombres")
    ApellidoPaterno = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    ApellidoMaterno = models.CharField(max_length=30, verbose_name="Apellido Materno")
    Foto = models.ImageField(upload_to='teams/Jugadores', null=True, blank=True, verbose_name='Foto')
    FechaNacimiento = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Nacimiento")
    Telefonos = models.CharField(max_length=30, verbose_name="Nro. Celular")
    EsContacto = models.CharField(max_length=1, default="N", verbose_name="Es Contacto")
    JuegosJugados = models.IntegerField(default=0, verbose_name="Juegos Jugados")
    BAT_VB = models.IntegerField(default=0, verbose_name="Veces al Bate")
    BAT_H = models.IntegerField(default=0, verbose_name="Hits")
    BAT_2B = models.IntegerField(default=0, verbose_name="Dobles")
    BAT_3B = models.IntegerField(default=0, verbose_name="Triples")
    BAT_HR = models.IntegerField(default=0, verbose_name="HomeRun")
    BAT_BB = models.IntegerField(default=0, verbose_name="Boletos")
    BAT_K = models.IntegerField(default=0, verbose_name="StrikeOut")
    BAT_SF = models.IntegerField(default=0, verbose_name="Sacrificio")
    BAT_BR = models.IntegerField(default=0, verbose_name="Bases Robadas")
    BAT_CI = models.IntegerField(default=0, verbose_name="Carreras Impulsadas")
    BAT_CA = models.IntegerField(default=0, verbose_name="Carreras Anotadas")
    BAT_HDEB = models.IntegerField(default=0, verbose_name="HDEB")
    Error = models.IntegerField(default=0, verbose_name="Error")
    Asistencia = models.IntegerField(default=0, verbose_name="Asistencia")
    PIT_Ganados = models.IntegerField(default=0, verbose_name="Juegos Ganados")
    PIT_Perdido = models.IntegerField(default=0, verbose_name="Juegos Perdidos")
    PIT_IP = models.IntegerField(default=0, verbose_name="Innings")
    PIT_HP = models.IntegerField(default=0, verbose_name="Hits Permitidos")
    PIT_CP = models.IntegerField(default=0, verbose_name="Carreras Permitidas")
    PIT_CS = models.IntegerField(default=0, verbose_name="Carreras Sucias")
    PIT_K = models.IntegerField(default=0, verbose_name="K Propinados")
    PIT_BB = models.IntegerField(default=0, verbose_name="BB Propinados")
    PIT_2B = models.IntegerField(default=0, verbose_name="2B Permitidos")
    PIT_3B = models.IntegerField(default=0, verbose_name="3B Permitidos")
    PIT_HR = models.IntegerField(default=0, verbose_name="HR Permitidos")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jugadores_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jugadores_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Nombres + ' ' + self.ApellidoPaterno + ' ' + self.ApellidoMaterno

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Jugadores, self).save()

    def get_image(self):
        if self.Foto:
            return '{}{}'.format(MEDIA_URL, self.Foto)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Equipo'] = self.Equipo.toJSON()
        item['TpIdentificacion'] = self.TpIdentificacion.toJSON()
        item['FechaNacimiento'] = self.FechaNacimiento.strftime('%d-%m-%Y')
        item['Foto'] = self.get_image()
        item['NombreCompleto'] = self.Nombres + ' ' + self.ApellidoPaterno + ' ' + self.ApellidoMaterno
        item['Jugador'] = self.Nombres + ' ' + self.ApellidoPaterno + ' - ' + self.Equipo.Nombre
        try:
            item['AVG'] = int(((int(self.BAT_H) + int(self.BAT_2B) + int(self.BAT_3B) + int(self.BAT_HR))/int(self.BAT_VB))*1000)
        except Exception as e:
            item['AVG'] = 0
        try:
            item['Efectividad'] = (int(self.PIT_CP) * 9)/int(self.PIT_IP)
        except Exception as e:
            item['Efectividad'] = 20
        return item

    class Meta:
        verbose_name = 'Jugadores'
        verbose_name_plural = 'Jugadores'
        ordering = ['id']


class EstadoCivil(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=100, verbose_name="Descripcion")

    def __str__(self):
        return self.Descripcion

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'EstadoCivil'
        verbose_name_plural = 'EstadoCivil'
        ordering = ['id']


class Estados(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=30, verbose_name="Descripcion")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estados_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estados_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Estados, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Estados'
        verbose_name_plural = 'Estados'
        ordering = ['id']


class Entrevistas(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.TextField(blank=True, verbose_name="Descripcion")
    Video = models.FileField(upload_to='entrevistas', null=True, blank=True, verbose_name='Video')
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entrevista_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entrevista_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Entrevistas, self).save()

    def get_video(self):
        if self.Video:
            return '{}{}'.format(MEDIA_URL, self.Video)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Video'] = self.get_video()
        return item

    class Meta:
        verbose_name = 'Entrevistas'
        verbose_name_plural = 'Entrevistas'
        ordering = ['id']


class Horarios(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='horario_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='horario_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Horarios, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Horarios'
        verbose_name_plural = 'Horarios'
        ordering = ['id']


class Estadios(models.Model):
    id = models.AutoField(primary_key=True)
    Nombre = models.TextField(blank=True, verbose_name="Nombre")
    Direccion = models.TextField(blank=True, verbose_name="Dirección")
    Foto = models.ImageField(upload_to='estadios', null=True, blank=True, verbose_name='Foto')
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estadio_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estadio_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Nombre

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Estadios, self).save()

    def get_image(self):
        if self.Foto:
            return '{}{}'.format(MEDIA_URL, self.Foto)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Foto'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Estadios'
        verbose_name_plural = 'Estadios'
        ordering = ['id']


class Calendario(models.Model):
    id = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    Activo = models.CharField(max_length=1, default='N', verbose_name="Activo")
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendario_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendario_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Descripcion

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Calendario, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        if self.Activo == 'S':
            item['CalendarioActivo'] = 'SI'
        else:
            item['CalendarioActivo'] = 'NO'
        return item

    class Meta:
        verbose_name = 'Calendario'
        verbose_name_plural = 'Calendario'
        ordering = ['id']


class DetalleCalendario(models.Model):
    id = models.AutoField(primary_key=True)
    Calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE, verbose_name="Calendario")
    Estadio = models.ForeignKey(Estadios, on_delete=models.CASCADE, verbose_name="Estadio")
    Fecha = models.DateTimeField(null=True, blank=True, verbose_name="Fecha")
    Horario = models.ForeignKey(Horarios, on_delete=models.CASCADE, verbose_name="Hora")
    Visitante = models.CharField(max_length=30, default=0, verbose_name="Equipo Visitante")
    LogoVisitante = models.ImageField(upload_to='pizarras/teams', null=True, blank=True, verbose_name='Logo Equipo Visitante')
    HomeClub = models.CharField(max_length=30, default=0, verbose_name="Equipo HomeClub")
    LogoHomeClub = models.ImageField(upload_to='pizarras/teams', null=True, blank=True, verbose_name='Logo Equipo HomeClub')
    CarrerasVisitante = models.IntegerField(default=0, verbose_name="Carreras Visitante")
    CarrerasHomeClub = models.IntegerField(default=0, verbose_name="Carreras HomeClub")
    PitcherGanador = models.CharField(max_length=30, default=0, verbose_name="Pitcher Ganador")
    PitcherPerdedor = models.CharField(max_length=30, default=0, verbose_name="Pitcher Perdedor")
    MVP = models.CharField(max_length=30, default=0, verbose_name="MVP")
    Pizarra = models.ImageField(upload_to='pizarras', null=True, blank=True, verbose_name='Pizarra')
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detcalendario_user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detcalendario_user_updated', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.Fecha.strftime('%d-%m-%Y') + ' - ' + self.Horario.Descripcion + ': ' + self.Visitante + ' vs ' + self.HomeClub

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(DetalleCalendario, self).save()

    def get_pizarra(self):
        if self.Pizarra:
            return '{}{}'.format(MEDIA_URL, self.Pizarra)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def get_visitante(self):
        if self.LogoVisitante:
            return '{}{}'.format(MEDIA_URL, self.LogoVisitante)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def get_homeclub(self):
        if self.LogoHomeClub:
            return '{}{}'.format(MEDIA_URL, self.LogoHomeClub)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['Fecha'] = self.Fecha.strftime('%d-%m-%Y')
        item['Calendario'] = self.Calendario.toJSON()
        item['Horario'] = self.Horario.toJSON()
        item['Estadio'] = self.Estadio.toJSON()
        item['Pizarra'] = self.get_pizarra()
        item['LogoVisitante'] = self.get_visitante()
        item['LogoHomeClub'] = self.get_homeclub()
        return item

    class Meta:
        verbose_name = 'DetalleCalendario'
        verbose_name_plural = 'DetalleCalendario'
        ordering = ['id']
