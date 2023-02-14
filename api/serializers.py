from rest_framework import serializers
from django.contrib.auth.models import User, Group

from littlelemon.models import (
    MenuItem, Category, Cart, Order, OrderItem, Purchase, PurchaseItem,
)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        read_only_fields = ['category']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['user', 'unit_price', 'price']


class CartSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user', 'orderitems']
        read_only = ['user']


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Purchase
        fields = ['user', 'purchaseitems', 'date']
        read_only = ['user', 'date']


class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PurchaseItem
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'purchase', 'delivery_crew', 'status', 'total', 'date']
        read_only = ['id', 'user', 'purchase', 'delivery_crew', 'total', 'date']
        extra_kwargs = {
            'delivery_crew_id': {'write_only': True},
        }
