
from django.db import models
from django.contrib.auth.models import AbstractUser


# Django has built-in User model
# Will need to redo the whole database if we switch to custom:
#   https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
#   https://docs.djangoproject.com/en/6.0/ref/settings/#auth-user-model
#   https://docs.djangoproject.com/en/6.0/ref/contrib/auth/
class User(AbstractUser):
    # username from `AbstractUser`
    # password from `AbstractUser`
    # email from `AbstractUser`
    balance = models.IntegerField(default=0) # balance in cents


class Stock(models.Model):
    shares = models.IntegerField()
    ticker = models.CharField(max_length=5)
    value = models.IntegerField() # value in cents


class Transaction(models.Model):
    date = models.DateTimeField()
    amount = models.IntegerField() # percent of product purchased
    ticker = models.CharField(max_length=5)


# must this be separate from `Transaction`?
class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


# Maps users to stocks they own.
class Owns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    creation_date = models.DateField()
    balance_per_capita = models.IntegerField()


# History of a stock.
# This is used to cach information from other APIs to avoid spamming them.
class StockHistory(models.Model):
    day = models.IntegerField()
    date = models.DateField()
    predicted_price = models.IntegerField() # value in cents
    ticker = models.CharField(max_length=5)
