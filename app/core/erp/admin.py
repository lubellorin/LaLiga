from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from core.erp.models import *

@admin.register(Estados)
class EstadosAdmin(ImportExportModelAdmin):
	pass


@admin.register(EstadoCivil)
class EstadoCivilAdmin(ImportExportModelAdmin):
	pass