from django.db import models


class Robot(models.Model):
    """
    The robots that have already been produced at the factory.
    """

    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.ForeignKey(
        to='RobotModel',
        null=False,
        blank=False,
        related_name='robots',
        related_query_name='robot',
        on_delete=models.CASCADE,
    )
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
