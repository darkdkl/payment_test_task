from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PayForm


def index(request):
    if request.method == 'POST':
        form = PayForm(request.POST, request=request)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.user = request.user
            pay.save()
            return redirect('payment:index_pay')
    else:
        form = PayForm()

    context = {"user": request.user,
               "form": form}
    return HttpResponse(render(request, 'payment/index.html', context=context))
