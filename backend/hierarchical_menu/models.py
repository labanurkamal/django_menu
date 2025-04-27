from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

DEFAULT_FALLBACK_URL: str = '#'


class Menu(models.Model):
    """Модель меню, представляющая отдельный набор пунктов меню."""
    name = models.CharField(
        _('Menu Name'),
        max_length=100,
        unique=True,
        help_text=_('Unique identifier for the menu (used for referencing).')
    )

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')

    def __str__(self) -> str:
        return f'{self.name}'


class MenuItem(models.Model):
    """Модель пункта меню с поддержкой вложенности и разрешения URL."""
    name = models.CharField(
        _('Item Name'),
        max_length=100,
        help_text=_('Display name for the menu item.')
    )
    url = models.CharField(
        _('URL or URL Name'),
        max_length=255,
        help_text=_('Direct URL or the name of the URL pattern if "Is Named URL" is checked.')
    )
    named_url = models.BooleanField(
        _('Is Named URL'),
        default=False,
        help_text=_('Check this if "URL or URL Name" is the name of a URL pattern.')
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Menu'),
        help_text=_('The menu this item belongs to.')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent Item'),
        help_text=_('The parent item for nested menus (optional).')
    )

    class Meta:
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')
        ordering = ['id']
        indexes = [
            models.Index(fields=['menu'], name='idx_menu_item_menu'),
            models.Index(fields=['parent'], name='idx_menu_item_parent'),
        ]

    def get_absolute_url(self) -> str:
        """
        Возвращает абсолютный URL для пункта меню.
        Если указан именованный маршрут, пытается его разрешить,
        иначе возвращает прямой URL или fallback URL.
        """
        namespace = getattr(settings, 'MENU_NAMESPACE', 'hierarchical_menu')
        if self.named_url:
            try:
                return reverse(f'{namespace}:{self.url}')
            except NoReverseMatch:
                return DEFAULT_FALLBACK_URL
        return self.url or DEFAULT_FALLBACK_URL

    def clean(self) -> None:
        """
        Проверка целостности данных:
        - Пункт меню не может быть родителем самого себя.
        - Проверка разрешения именованного маршрута, если он указан.
        """
        if self.parent and self.parent == self:
            raise ValidationError({'parent': _('Menu item cannot be parent of itself.')})

        if self.named_url:
            namespace = getattr(settings, 'MENU_NAMESPACE', 'hierarchical_menu')
            try:
                reverse(f'{namespace}:{self.url}')
            except NoReverseMatch:
                raise ValidationError(
                    {'url': _('Cannot resolve named URL: %(url)s') % {'url': self.url}}
                )

    def save(self, *args, **kwargs):
        """Сохраняет объект после полной валидации."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'
