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


# function-based views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def menuitem_list(request):
    if request.method == 'GET':
        queryset = MenuItem.objects.select_related('category').all()
        serialized_data = MenuItemSerializer(queryset, many=True, context={'request': request})
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serialized_data = MenuItemSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)