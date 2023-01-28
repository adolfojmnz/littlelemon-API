from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView,
)

from .serializers import MenuItemSerializer
from .models import MenuItem


class MenuView(ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer


class MenuItemView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
