from django.db import models
from django.utils.text import slugify
import unidecode
import os


class Product(models.Model):
    name = models.CharField(max_length=191)
    price = models.IntegerField()
    slug = models.SlugField(default='',blank=True,null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='products_images/', blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.slug=='':
            self.slug=slugify(unidecode.unidecode(self.name))
        super().save( *args, **kwargs)


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price


class Order(models.Model):
    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def cost(self):
        return self.price * self.quantity