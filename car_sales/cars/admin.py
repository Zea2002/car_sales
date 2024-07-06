from django.contrib import admin
from cars.models import Car,Brand,Comment,Order
# Register your models here.
admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(Comment)
admin.site.register(Order)