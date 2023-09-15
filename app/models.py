from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Products(models.Model):
    product_name=models.CharField(max_length=100, null=True)
    product_details=models.TextField(max_length=150, null=True)
    product_price = models.DecimalField(max_digits=10,null=True, decimal_places=2, default=1) 
    product_image=models.ImageField(upload_to= 'product-images', null=True) 
    create_date=models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.product_name
    
class Profile(models.Model):
    user_address_1=models.CharField(max_length=150, null=True)  
    user_address_2=models.CharField(max_length=150, null=True)
    user_pincode=models.CharField(max_length=6,null=True)
    user_email=models.CharField(max_length=100, null=True)
    user_phone=models.CharField(max_length=10, null=True) 
    var=models.ForeignKey(User, default=0,null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_phone
 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Products)
    order_date = models.DateTimeField(auto_now_add=True)   
    total_amount = models.DecimalField(max_digits=10, default=1, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='carts')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity = models.DecimalField(max_digits=10,null=True, decimal_places=0,default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    var = models.ForeignKey(User, default=1, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cart)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.product_price * self.quantity
        super(CartItem, self).save(*args, **kwargs)


class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    total_amount = models.DecimalField(max_digits=10,  decimal_places=2)
    bill_date = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f'Bill for Order {self.order.id}'


   


    
      