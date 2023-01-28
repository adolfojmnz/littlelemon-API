from django.urls import path

from .views import MenuView, MenuItemView


urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('menu/<int:pk>/', MenuItemView.as_view(), name='menu-item'),
]