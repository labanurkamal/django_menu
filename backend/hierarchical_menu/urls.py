from django.conf import settings
from django.urls import path
from django.views.generic.base import TemplateView

app_name = getattr(settings, 'MENU_NAMESPACE', 'hierarchical_menu')

urlpatterns = [
    path('', TemplateView.as_view(template_name='hierarchical_menu/index.html'), name='index'),
    path('item/', TemplateView.as_view(template_name='hierarchical_menu/item.html'), name='item')
]
