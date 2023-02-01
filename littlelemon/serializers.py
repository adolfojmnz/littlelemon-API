from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import MenuItem, Category

from decimal import Decimal
import bleach


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    after_tax = serializers.SerializerMethodField(method_name='price_after_tax')
    category = serializers.HyperlinkedIdentityField(view_name='category-detail', read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'inventory', 'category', 'category_id', 'price', 'after_tax']
        extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(queryset=MenuItem.objects.all()),
                ],
            },
        }
 
    def price_after_tax(self, product:MenuItem):
        return round(product.price * Decimal(1.1), 2)
    
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if attrs['price'] < 2: raise serializers.ValidationError('The price should be greater or equal than 2')
        if attrs['inventory'] < 0: raise serializers.ValidationError('The number of items in inventoy should be greater than 0')
        return super().validate(attrs)
