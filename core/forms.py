from django.forms import ModelForm
from core.models import Transaction

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('currency','comment',)