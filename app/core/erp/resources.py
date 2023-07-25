from import_export import resources
from core.erp.models import ClientesProspectos


class ClientesProspectosResource(resources.ModelResource):

    class meta:
        model = ClientesProspectos
