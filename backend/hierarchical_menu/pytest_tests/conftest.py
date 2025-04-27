import pytest

from hierarchical_menu.models import Menu, MenuItem


@pytest.fixture
def menu_db():
    """Создаёт экземпляр модели Menu."""
    return Menu.objects.create(name="menu_name")


@pytest.fixture
def menu_item_is_named_db(menu_db):
    """Создаёт пункт MenuItem с именованной ссылкой (named_url=True)."""
    menu_item = MenuItem.objects.create(
        name="Test MenuItem Item",
        url='item',
        named_url=True,
        menu=menu_db,
        parent=None
    )
    return menu_item


@pytest.fixture
def menu_item_is_direct_db(menu_db):
    """Создаёт пункт MenuItem с прямой ссылкой (named_url=False)."""
    menu_item = MenuItem.objects.create(
        name="Test MenuItem Direct",
        url='/direct/',
        named_url=False,
        menu=menu_db,
        parent=None
    )
    return menu_item
