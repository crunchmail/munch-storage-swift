from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StorageSwiftApp(AppConfig):
    name = 'munch_storage_swift'
    verbose_name = _("Storage Swift")

    def ready(self):
        pass
