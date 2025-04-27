from django.conf import settings

MENU_NAMESPACE = getattr(settings, 'MENU_NAMESPACE', 'hierarchical_menu')

INDEX_PATH = f'{MENU_NAMESPACE}:index'
ITEM_PATH = f'{MENU_NAMESPACE}:item'
