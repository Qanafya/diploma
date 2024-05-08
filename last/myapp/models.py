from django.db import models

# Create your models here.
class Chef(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Customer(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class CustomerInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()

class Jur(models.Model):
    role_choices = (
        ('chef', 'Chef'),
        ('customer', 'Customer'),
    )
    user_id = models.IntegerField()
    role = models.CharField(max_length=255, choices=role_choices)

class ChefDetail(models.Model):
    chef_id = models.IntegerField()
    about = models.CharField(max_length=255, default="")
    short = models.CharField(max_length=255, default="")
    speciality = models.CharField(max_length=255, default="")
    service = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default=False)

class Meal(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    desc = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    photo_link = models.CharField(max_length=255)
    ingredient = models.CharField(max_length=255)
    chef_id = models.IntegerField()

class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('ready', 'Ready'),
    )

    meal_id = models.IntegerField()
    customer_id = models.IntegerField()
    chef_id = models.IntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)








