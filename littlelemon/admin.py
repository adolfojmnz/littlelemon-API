from django.contrib import admin


from .models import (
    MenuItem, Category, Cart, Order, OrderItem, Purchase,
)

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Purchase)