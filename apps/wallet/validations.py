from django.core.exceptions import ValidationError

from apps.wallet.constants import TRANSACTION_CHOICES


def transaction_validation(object):
    if object.category.type != TRANSACTION_CHOICES.TRANSFER:
        return

    if not object.to_account:
        raise ValidationError("Укажите счет для перевода")

    if object.account == object.to_account:
        raise ValidationError("Счета должны отличаться")

    if object.account.balance < object.amount:
        raise ValidationError("Недостаточно средств")
