from django.db import models


class TRANSACTION_CHOICES(models.TextChoices):
    TRANSFER = 'Переводы'
    EXPENSE = 'Расходы'
    INCOME = 'Доходы'
