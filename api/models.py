from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.


class Client(models.Model):
    auth_key = models.CharField(max_length=200)
    name = models.CharField(max_length=200, primary_key=True)

class MachineUser(models.Model):
    user = models.ForeignKey(AuthUser, unique=True)
    twitter = models.CharField(max_length=25, blank=True, unique=True)
    student_id = models.CharField(max_length=10, blank=True, unique=True)

class Soda(models.Model):
    short_name = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=200)
    cost = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')

    def __unicode__(self):
        return self.description

class Transaction(models.Model):
    amount = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')
    user = models.ForeignKey(MachineUser)
    date_time = models.DateTimeField(auto_now_add=True)

class SodaTransaction(models.Model):
    transaction = models.ForeignKey(Transaction)
    soda = models.ForeignKey(Soda)

class Inventory(models.Model):
    soda = models.ForeignKey(Soda)
    slot = models.PositiveSmallIntegerField()
    amount = models.PositiveSmallIntegerField()


adminable = (Inventory, MachineUser, Soda, Transaction, SodaTransaction, Client)