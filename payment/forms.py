from django import forms
from .models import User,Pay

class PayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args,**kwargs)

    class Meta:
        model =Pay
        fields=("pay","invoice")

    def clean_pay(self):
        if self.cleaned_data['pay'] > self.request.user.total_payment:
            raise forms.ValidationError('Сумма выплаты не может превышать '
                                        'баланс пользователя')
        return self.cleaned_data['pay']
