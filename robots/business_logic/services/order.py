from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot

if TYPE_CHECKING:
    from django.db.models.base import ModelBase


logger = getLogger(__name__)


@receiver(post_save, sender=Robot)
def email_to_customer(sender: ModelBase, instance: Robot, **kwargs: dict[Any, Any]) -> None:
    """
    Listener for the post-save signal from the Robot model.
    When a new record is saved in Robot, the function checks if there are active orders
    for this model and version.
    If there are, an email is sent to the first one in the list.
    """

    order = Order.objects.select_related('customer').filter(robot_serial=instance.serial)
    if order:
        email = order[0].customer.email

        model = instance.serial.split('-')[0]
        serial = instance.serial.split('-')[1]

        send_mail(
            subject='Ваш робот в наличии!',
            message=(
                f'Добрый день! Недавно вы интересовались нашим роботом модели {model}, версии {serial}.\n'
                f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
            ),
            from_email=settings.EMAIL_FROM,
            recipient_list=[email],
        )
        logger.info('Email successfully sent', extra={'email': email, 'robot_serial': instance.serial})
