from django.db import models



# This model represents donation causes that customer will be donating to.
class Donation(models.Model):

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.amount})"


class Transaction(models.Model):

    invoice = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    paid = models.BooleanField(default=False)

