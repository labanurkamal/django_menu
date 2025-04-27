from django.contrib import admin

from hierarchical_menu.models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """Вложенная форма для пунктов меню внутри меню."""
    model = MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Админка для модели Menu."""
    inlines = [MenuItemInline]
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Админка для модели MenuItem."""
    list_display = ('id', 'name', 'menu', 'parent', 'named_url', 'url')
    list_filter = ('menu', 'named_url')
    search_fields = ('name', 'url')
    ordering = ('menu', 'parent', 'id')

    raw_id_fields = ('parent',)
    autocomplete_fields = ('menu',)
