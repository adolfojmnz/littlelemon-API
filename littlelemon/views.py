from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.response import Response

from .throttle import TenCallPerHour, TenCallPerMinute

from .serializers import MenuItemSerializer, CategorySerializer
from .models import MenuItem, Category


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallPerMinute])
def secret(request):
    return Response({'secrete': 'super secret message'})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallPerHour])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'secrete': 'super secret message for the manager'})
    return Response({'message': 'Unauthorized to access the resource'}, status=403)


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