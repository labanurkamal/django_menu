from typing import Any
from urllib.parse import urlparse

from django import template

from hierarchical_menu.models import MenuItem

register = template.Library()


def is_active(url: str, current_path: str) -> bool:
    """Проверяет, активен ли пункт меню на основе текущего URL."""
    current_path = urlparse(current_path).path.rstrip('/')
    url = url.rstrip('/')

    return current_path == url or current_path.startswith(url + '/')


def get_nodes_to_extend(nodes: dict) -> set[int]:
    """
    Определяет, какие узлы дерева меню необходимо раскрыть,
    чтобы показать путь до активного элемента.
    """
    nodes_to_extend = set()
    active_node_id = next((node_id for node_id, node in nodes.items() if node['is_active']), None)
    if active_node_id:
        nodes_to_extend.add(active_node_id)
        parent_node_id = nodes[active_node_id]['parent_id']
        while parent_node_id:
            nodes_to_extend.add(parent_node_id)
            parent_node_id = nodes[parent_node_id]['parent_id']
    return nodes_to_extend


def get_nested_nodes(nodes: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Формирует вложенную структуру узлов меню на основе их родительских связей.
    """
    nested_nodes = []
    for node_id, node in nodes.items():
        parent_id = node['parent_id']
        if parent_id and parent_id in nodes:
            nodes[parent_id]['children'].append(node)
        else:
            nested_nodes.append(node)
    return nested_nodes


@register.inclusion_tag('hierarchical_menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name: str) -> dict[str, Any]:
    """Отображает меню, основываясь на текущем URL из контекста запроса."""
    current_path = context['request'].path
    items = MenuItem.objects.filter(menu__name=menu_name).select_related('menu').order_by('id')

    nodes = {}
    for item in items:
        url = item.get_absolute_url()
        nodes[item.id] = {
            'item': item,
            'parent_id': item.parent_id,
            'url': url,
            'children': [],
            'is_active': is_active(url, current_path),
        }

    return {
        'nodes': get_nested_nodes(nodes),
        'nodes_to_extend': get_nodes_to_extend(nodes)
    }
