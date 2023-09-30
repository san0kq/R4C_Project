from django.db import models


class Customer(models.Model):
    """
    Customer/Client Model. Email must be unique.
    """

    email = models.CharField(max_length=255, blank=False, null=False, unique=True)
