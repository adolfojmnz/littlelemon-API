from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.SmallIntegerField()
    category = models.ForeignKey('littlelemon.Category', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
