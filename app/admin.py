from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Bill)
