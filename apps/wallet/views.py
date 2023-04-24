from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.decorators import login_required

from apps.wallet.forms import AccountForm, TransactionForm
from apps.wallet.models import Account


class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        return context


class AccountView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class AccountListView(AccountView, ListView):
    template_name = 'wallet/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountCreateView(AccountView, CreateView):
    model = Account
    fields = ('name', 'balance')
    template_name = 'wallet/form.html'
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def account_update(request, pk):
    user = request.user
    account = get_object_or_404(Account, pk=pk, owner=user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)

        if form.is_valid():
            form.save()

        return redirect('account')

    form = AccountForm(instance=account)

    context = {
        'form': form,
        'title': 'Редактировать счет',
    }

    return render(request, 'wallet/form.html', context)


def account_delete(request, pk):
    user = request.user
    account = get_object_or_404(Account, pk=pk, owner=user)
    account.delete()
    return redirect('account')


class TransactionView(View):
    def get(self, request):
        form = TransactionForm()
        return render(request, 'wallet/transaction.html', {'form': form, 'title': 'Создать транзакцию'})

    def post(self, request):
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Транзакция успешно создана')
            return redirect('transaction')

        messages.success(request, f"{form.errors}")
        return redirect('transaction')
