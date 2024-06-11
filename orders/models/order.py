from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        SHIPPED = 'SP', _('Shipped')
        DELIVERED = 'DV', _('Delivered')

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
