from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.


class Client(models.Model):
    authKey = models.CharField(max_length=200)
    name = models.CharField(max_length=200, primary_key=True)

class MachineUser(models.Model):
    user = models.ForeignKey(AuthUser, unique=True)
    twitter = models.CharField(max_length=25, blank=True, unique=True)
    studentId = models.CharField(max_length=10, blank=True, unique=True)

class Soda(models.Model):
    shortName = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=200)

class Transaction(models.Model):
    amount = models.IntegerField() #number of pennies
    user = models.ForeignKey(MachineUser)
    dateTime = models.DateTimeField(auto_now_add=True)

class SodaTransaction(models.Model):
    transaction = models.ForeignKey(Transaction)
    soda = models.ForeignKey(Soda)

class Inventory(models.Model):
    soda = models.ForeignKey(Soda)
    slot = models.PositiveSmallIntegerField()
    amount = models.PositiveSmallIntegerField()


adminable = (Inventory, MachineUser, Soda, Transaction, SodaTransaction, Client)