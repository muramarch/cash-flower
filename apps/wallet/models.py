from django.db import models
from django.contrib.auth.models import User

from apps.wallet.constants import TRANSACTION_CHOICES
from apps.wallet.validations import transaction_validation


class Account(models.Model):
    """ Моделька счета """
    name = models.CharField(
        'Название счета',
        max_length=50,
        default="Счет",
        db_index=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Владелец'
    )
    balance = models.BigIntegerField(
        "Баланс",
        default=0
    )

    def __str__(self):
        return f"{self.name} - {self.balance}"

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'


class Tag(models.Model):
    """ Теги """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=20,
        choices=TRANSACTION_CHOICES.choices,
        default=TRANSACTION_CHOICES.INCOME
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="Счет",
        related_name="from_account"
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Счет для перевода",
        related_name="to_account",
        null=True, blank=True
    )
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.account} - {self.category} - {self.amount}"

    def clean(self):
        transaction_validation(self)
        super().clean()

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class TransactionImage(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='media/images/')

    def __str__(self):
        return str(self.transaction)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
