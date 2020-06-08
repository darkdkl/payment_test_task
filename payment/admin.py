from django.contrib import admin
from .models import User, Payment, Pay
from django.utils import timezone
from django import forms
import requests

admin.site.register(User)
admin.site.register(Payment)


class PayAdminForm(forms.ModelForm):

    def request_for_payment(self):
        invoice = self.data.get("invoice")
        pay = self.data.get('pay')
        url = "https://webhook.site/70093b5d-4aeb-4d20-84f7-a505b71150a9"
        response = requests.post(url, json={"account": invoice, "amount": pay})
        if not response.ok:
            raise forms.ValidationError("Данная выплата не была успешной")

    def clean(self):
        super().clean()
        if self.data.get('_paybutton'):
            if self.instance.user.total_payment < float(self.data.get('pay')):
                raise forms.ValidationError(
                    f'''Сумма выплаты не может превышать 
                баланс пользователя : {self.instance.user.total_payment}''')
            if self.data.get("invoice"):
                self.request_for_payment()
            self.instance.user.total_payment -= float(self.data.get('pay'))
            self.instance.date_processing = timezone.now()
            self.instance.paid_out = True
            self.instance.user.save()
            self.instance.save()


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    form = PayAdminForm
    change_form_template = "payment/change_payment_form.html"

    fields = ["user", "pay", "date_create", "date_processing", "paid_out",
              "invoice"]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.paid_out:
            return ["user", "pay", "date_create", "date_processing", "paid_out",
                    "invoice"]
        else:
            return ["date_create", "date_processing", "paid_out"]
