from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView,
)

from .serializers import MenuItemSerializer, CategorySerializer
from .models import MenuItem, Category


class MenuListView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryItemView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer