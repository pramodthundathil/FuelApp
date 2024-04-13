from django.db import models
from django.contrib.auth.models import User

class StaffProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    address  = models.TextField(max_length=255)


class FuelStocks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    fuel_category = models.CharField(max_length=255, choices=(("Petrol","Petrol"),("Diesel","Diesel"),("LPG","LPG")))
    stock = models.FloatField()
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)


class FuelRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name="customer")
    staff = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name="staff")
    fuel = models.CharField(max_length=255)
    qunty = models.FloatField()
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.IntegerField()
    latitude = models.FloatField()
    logitude = models.FloatField()
    status = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=25)
    completion_status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)


class FuelPrice(models.Model):
    Petrol = models.FloatField()
    Diesel = models.FloatField()
    LPG = models.FloatField()