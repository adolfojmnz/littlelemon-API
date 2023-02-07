from rest_framework import serializers
from django.contrib.auth.models import User, Group

from littlelemon.models import (
    MenuItem, Category, Cart, Order, OrderItem, Purchase,
)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):

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


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['user', 'unit_price', 'price']


class CartSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'orderitems']
    

class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['user', 'orderitems', 'date']
        read_only = ['user', 'date']
        

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'purchase', 'delivery_crew', 'delivered', 'total', 'date']
