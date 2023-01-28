from django.urls import path

from .views import (
    MenuListView, MenuItemView, CategoryListView, CategoryItemView,
)


urlpatterns = [
    path('menu', MenuListView.as_view()),
    path('menu/<int:pk>/', MenuItemView.as_view()),

    path('categories', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryItemView.as_view(), name='category-detail'),
]