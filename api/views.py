from rest_framework.viewsets import ModelViewSet

from littlelemon.models import (
    MenuItem, Category, Cart, Order, OrderItem,
)

from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


class MenuItemListViewSet(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemDetailViewSet(ModelViewSet):
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer


class CategoryListViewSet(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailViewSet(ModelViewSet):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer


class CartListViewSet(ModelViewSet):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class CartDetailViewSet(ModelViewSet):
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer


class OrderListViewSet(ModelViewSet):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer


class OrderDetailViewSet(ModelViewSet):
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer


class OrderItemListViewSet(ModelViewSet):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetailViewSet(ModelViewSet):
    model = OrderItem
    queryset = model.objects.all()
    serializer_class = OrderItemSerializer
