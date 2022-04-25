from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Pago
from .models import cliente
import decimal
from django.db import transaction

#@transaction.atomic
def procesador_de_pagos(request):
  if request.method == 'POST':

    form = Pago(request.POST)

    if form.is_valid():
        x = form.cleaned_data['envia']
        y = form.cleaned_data['recibe']
        z = decimal.Decimal(form.cleaned_data['monto'])

        with transaction.atomic():
            envia = cliente.objects.get(nombre=x)
            envia.saldo -= z
            envia.save()

            recibe = cliente.objects.get(nombre=y)
            recibe.saldo += z
            recibe.save()

        return HttpResponseRedirect('/')
  else:
    form = Pago()
  return render(request, 'index.html', {'form': form})