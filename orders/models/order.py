from django.db import models


class Order(models.Model):
    """
    The model responsible for storing customer orders.
    One record corresponds to one customer and one order.
    """

    customer = models.ForeignKey(
        to='customers.Customer',
        blank=False,
        null=False,
        related_name='orders',
        related_query_name='order',
        on_delete=models.CASCADE,
    )
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
