from django import forms
from django.db import transaction as transaction_atomic
from django.core.exceptions import ValidationError

from apps.wallet.constants import TRANSACTION_CHOICES
from apps.wallet.models import Category, Account, Transaction, Tag, Image


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'balance',)


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True
    )

    class Meta:
        model = Transaction
        fields = (
            'account',
            'to_account',
            'category',
            'tags',
            'description',
            'amount',
        )

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get('amount')
        account = form_data.get('account')
        category = form_data.get('category')

        if category.type != TRANSACTION_CHOICES.TRANSFER:
            return form_data

        to_account = form_data.get('to_account')

        if not to_account:
            raise ValidationError('Укажите счет для перевода')

        if account == to_account:
            raise ValidationError('Счета должны отличаться')

        if account.balance < int(amount):
            return ValidationError('transaction')

        return form_data

    @transaction_atomic.atomic
    def save(self, commit=True):
        transaction = super().save(commit=False)

        if transaction.to_account:
            from_account = transaction.account
            to_account = transaction.to_account

            from_account.balance -= transaction.amount
            to_account.balance += transaction.amount

            from_account.save()
            to_account.save()

        return transaction
