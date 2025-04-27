from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HierarchicalMenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hierarchical_menu'
    verbose_name = _('Hierarchical Menu')
