from django.db import models
from django.contrib.auth.models import User


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField()
    category = models.ForeignKey('littlelemon.Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ['user', 'menuitem']

    def __str__(self):
        return f'{self.user.username} ordered items'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f'{self.user.username} cart'

class PurchaseItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} purchase items'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)
    purchaseitems = models.ManyToManyField(PurchaseItem, default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} purchase on {str(self.date).split(" ")[0]}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase = models.OneToOneField(Purchase, on_delete=models.PROTECT, default=0)
    delivery_crew = models.ForeignKey(
        User,
        on_delete = models.CASCADE, 
        related_name = 'delivery_crew',
        null = True, blank = True,
    )
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.user} order'
