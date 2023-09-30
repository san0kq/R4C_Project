from django.db import models


class RobotModel(models.Model):
    """
    Models of robots manufactured at the factory.
    Model names are unique.
    """

    name = models.CharField(max_length=2, blank=False, null=False, unique=True, verbose_name='model')
