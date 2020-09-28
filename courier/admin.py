from django.contrib import admin
from .models import Product,Order,OrderUpdate,Contact,Profile,Pending_order

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Pending_order)







