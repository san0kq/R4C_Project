from django.db import models


class RobotModel(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False, unique=True, verbose_name='model')
