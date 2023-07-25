from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from core.erp.models import *

from config.settings import MEDIA_URL, STATIC_URL



class User(AbstractUser):
    Equipo = models.IntegerField(default=0, verbose_name="Equipo")
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name="Foto")
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%d-%m-%Y')
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass