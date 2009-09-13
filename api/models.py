from django.db import models
from django.contrib.auth.models import User as AuthUser

class Client(models.Model):
    auth_key = models.CharField(max_length=200)
    name = models.CharField(max_length=200, primary_key=True)

class MachineUser(AuthUser):
    twitter = models.CharField(max_length=25, blank=True, unique=True)
    student_id = models.CharField(max_length=10, blank=True, unique=True)
    balance = models.IntegerField(help_text='measured in pennies', default=0)

class Soda(models.Model):
    short_name = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=200)
    cost = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class Transaction(models.Model):
    amount = models.IntegerField(help_text='measured in pennies (ie, 500 = $5)')
    user = models.ForeignKey(MachineUser)
    date_time = models.DateTimeField(auto_now_add=True)

class SodaTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, primary_key=True)
    soda = models.ForeignKey(Soda)

class Inventory(models.Model):
    soda = models.ForeignKey(Soda, primary_key=True)
    slot = models.PositiveSmallIntegerField()
    amount = models.PositiveSmallIntegerField()

    @staticmethod
    def returnQs(qs):
        output = []
        for i in qs:
            output.append(
            {
                'soda': {
                    'short_name': i.soda.short_name,
                    'description': i.soda.description,
                    'cost': i.soda.cost
                },
                'quantity': i.amount
            })
        return output

    @staticmethod
    def getEntireInventory():
        return Inventory.returnQs(Inventory.objects.select_related(depth=1).all())

    @staticmethod
    def getInventoryForSoda(soda):
        return Inventory.returnQs(Inventory.objects.select_related(depth=1).filter(pk=soda).all())


adminable = (Inventory, MachineUser, Soda, Transaction, SodaTransaction, Client)
