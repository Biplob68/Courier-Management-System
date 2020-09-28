from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from enum import Enum
from django.utils.translation import gettext_lazy as _


class UserType(Enum):
    Employee = 'Employee',
    Permitted_Employee = 'Permitted_Employee',
    Customer = 'Customer',
    Admin = 'Admin'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20,  choices=[('Employee', _('Employee')),('Permitted_Employee', _('Permitted_Employee')),
                                                          ('Customer', _('Customer')),('Admin', _('Admin'))],)
    address = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_Description = models.CharField(max_length=300)
    product_type = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='courier/images', default="")
    product_weight = models.FloatField()
    product_price = models.FloatField()

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    email = models.EmailField(max_length=111, default="")
    phone = models.CharField(max_length=12, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    sender_name = models.CharField(max_length=90)
    sender_email = models.EmailField(max_length=111, default="")
    sender_address = models.CharField(max_length=111)
    sender_phone = models.CharField(max_length=111, default="")
    receiver_name = models.CharField(max_length=90)
    receiver_email = models.EmailField(max_length=111, default="")
    receiver_address = models.CharField(max_length=111)
    receiver_phone = models.CharField(max_length=111, default="")
    product_name = models.CharField(max_length=111)
    weight = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    quantity = models.FloatField(default=1.0)
    description = models.CharField(max_length=300, default="")
    dateTime = models.DateTimeField(default=datetime.now, blank=True)
    expectedDate = models.DateTimeField(default=datetime.now, blank=True)


class Pending_order(models.Model):
    pending_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    time = models.DateTimeField(auto_now_add=True)


class OrderStatus(Enum):
    placed = 'Placed Order',
    confirmed = 'Confirmed Order',
    picked_up = 'Picked-up',
    dispatched = 'Dispatched Product',
    reached = 'Reached Product',
    delivered = 'Delivered Product'


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=150)
    status = models.CharField(max_length=50,
                              choices=[('Placed Order', _('Placed Order')), ('Confirmed Order', _('Confirmed Order')),
                                       ('Picked-up', _('Picked-up')), ('Dispatched Product', _('Dispatched Product')),
                                       ('Reached Product', _('Reached Product')),
                                       ('Delivered Product', _('Delivered Product')),
                                       ], default='Placed Order')

    def __str__(self):
        return str(self.update_id) + " Order Id(" + str(self.order_id) + ")"
