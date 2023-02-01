from rest_framework.viewsets import ModelViewSet

from .serializers import MenuItemSerializer, CategorySerializer
from .throttle import UserThrottleMixin, AnonThrottleMixin
from .models import MenuItem, Category


class MenuItemsViewSet(UserThrottleMixin, AnonThrottleMixin, ModelViewSet):
    throttle_classes = []
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_throttles(self):
        return super().get_throttles()


class MenuItemViewSet(UserThrottleMixin, AnonThrottleMixin, ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryItemsViewSet(UserThrottleMixin, AnonThrottleMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title']
    search_fields = ['title']


class CategoryItemViewSet(UserThrottleMixin, AnonThrottleMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer