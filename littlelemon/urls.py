from django.urls import path

from .views import (
    menuitem_list,
    MenuListView, MenuItemView, CategoryListView, CategoryItemView,
)


urlpatterns = [
    path('menu/', menuitem_list),
    path('menu/', MenuListView.as_view()), # unreachable 
    path('menu/<int:pk>/', MenuItemView.as_view()),

    path('categories', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryItemView.as_view(), name='category-detail'),
]