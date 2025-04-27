from http import HTTPStatus

import pytest
from django.urls import reverse

from .constants import INDEX_PATH, ITEM_PATH


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('path', 'expected_status'),
    (
            (INDEX_PATH, HTTPStatus.OK),
            (ITEM_PATH, HTTPStatus.OK)
    )
)
def test_pages_availability_for_anonymous_user(client, path, expected_status):
    """Тестирует доступность страниц для анонимного пользователя (проверка статуса 200 OK)."""
    url = reverse(path)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('path', 'direct_path'),
    (
            (INDEX_PATH, '/'),
            (ITEM_PATH, '/item/'),
    )
)
def test_index_url_with_namespace(path, direct_path):
    """Тестирует правильность формирования URL с учётом пространств имён (namespace)."""
    assert reverse(path) == direct_path
