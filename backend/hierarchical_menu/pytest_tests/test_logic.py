from http import HTTPStatus

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from pytest_django.asserts import assertNumQueries

from hierarchical_menu.models import MenuItem
from .constants import ITEM_PATH


@pytest.mark.django_db
def test_menu_item_creation(menu_item_is_named_db, menu_db):
    """Тестирует создание пункта меню и его привязку к меню."""
    assert MenuItem.objects.count() == 1
    assert menu_item_is_named_db.menu == menu_db


@pytest.mark.django_db
def test_self_parent_validation(menu_item_is_named_db):
    """Тестирует запрет установки элемента меню в качестве собственного родителя."""
    menu_item_is_named_db.parent = menu_item_is_named_db

    with pytest.raises(ValidationError):
        menu_item_is_named_db.save()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('menu_item_name', 'expected_path'),
    (
            ('menu_item_is_named_db', reverse(ITEM_PATH)),
            ('menu_item_is_direct_db', '/direct/'),
    )
)
def test_get_absolute_url_with_named_url(menu_item_name, expected_path, request):
    """Тестирует корректность формирования абсолютного URL для пунктов меню."""
    menu_item_fixtures = request.getfixturevalue(menu_item_name)
    assert menu_item_fixtures.get_absolute_url() == expected_path


@pytest.mark.django_db
def test_draw_menu_query_count(client, menu_item_is_named_db, menu_db):
    """Тестирует количество SQL-запросов при отрисовке меню (ожидается 1 запрос)."""
    MenuItem.objects.create(menu=menu_db, name='Test About', url='/about/', parent=menu_item_is_named_db)
    with assertNumQueries(1):
        response = client.get(reverse(ITEM_PATH))
        assert response.status_code == HTTPStatus.OK
