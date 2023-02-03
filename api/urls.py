from django.urls import path

from .views import (
    MenuItemListViewSet, MenuItemDetailViewSet,
    CategoryListViewSet, CategoryDetailViewSet,
    CartListViewSet, CartDetailViewSet,
    OrderListViewSet, OrderDetailViewSet,
    OrderItemListViewSet, OrderItemDetailViewSet,
)

LIST = {'get': 'list', 'post': 'create'}
DETAIL = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}


urlpatterns = [
    path('menu-items', MenuItemListViewSet.as_view(LIST)),
    path('menu-items/<int:pk>', MenuItemDetailViewSet.as_view(DETAIL)),

    path('categories', CategoryListViewSet.as_view(LIST)),
    path('categories/<int:pk>', CategoryDetailViewSet.as_view(DETAIL), name='category-detail'),

    path('carts', CartListViewSet.as_view(LIST)),
    path('carts/<int:pk>', CartDetailViewSet.as_view(DETAIL)),

    path('orders', OrderListViewSet.as_view(LIST)),
    path('orders/<int:pk>', CartDetailViewSet.as_view(DETAIL)),

    path('order-items', OrderItemListViewSet.as_view(LIST)),
    path('order-items/<int:pk>', OrderItemDetailViewSet.as_view(DETAIL)),
]