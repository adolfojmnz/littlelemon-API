from django.urls import path

from .views import (
    MenuItemsViewSet, MenuItemViewSet, CategoryItemsViewSet, CategoryItemViewSet,
)


urlpatterns = [
    path('menu/', MenuItemsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('menu/<int:pk>/', MenuItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='menuitem-detail'),

    path('categories', CategoryItemsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>', CategoryItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
]