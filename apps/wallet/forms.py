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
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        label='Счет',
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=Category.objects.first(),
        label='Категория',
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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=user)

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
            raise ValidationError('transaction')

        return form_data

    @transaction_atomic.atomic
    def save(self, commit=True):
        transaction = super().save(commit=False)
        from_account = transaction.account

        if transaction.category.type == TRANSACTION_CHOICES.TRANSFER:
            to_account = transaction.to_account

            from_account.balance -= transaction.amount
            to_account.balance += transaction.amount

            from_account.save()
            to_account.save()

        elif transaction.category.type == TRANSACTION_CHOICES.EXPENSE:
            from_account.balance -= transaction.amount
            from_account.save()

        elif transaction.category.type == TRANSACTION_CHOICES.INCOME:
            from_account.balance += transaction.amount
            from_account.save()

        transaction.save()
        return transaction
