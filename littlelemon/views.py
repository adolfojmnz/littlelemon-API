from rest_framework.viewsets import ModelViewSet

from .serializers import MenuItemSerializer, CategorySerializer
from .models import MenuItem, Category


class MenuItemsViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'inventory']
    search_fields = ['title', 'category__title']


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryItemsViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title']
    search_fields = ['title']


class CategoryItemViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer