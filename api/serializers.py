from rest_framework import serializers

from littlelemon.models import MenuItem, Category, Cart, Order, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedIdentityField(view_name='category-detail', read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category', 'category_id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'slug']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
    

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['user', 'delivery_crew', 'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']