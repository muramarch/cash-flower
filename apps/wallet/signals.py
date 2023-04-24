from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import TransactionImage


@receiver(pre_save, sender=TransactionImage)
def limit_transaction_images(sender, instance, **kwargs):
    if instance.pk:
        return

    if instance.transaction.images.count() >= 2:
        raise ValidationError("Transaction can only have 2 images.")
