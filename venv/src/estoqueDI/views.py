from django.shortcuts import render, redirect
from .models import *
from .forms import StockCreateForm

def home(request):
    title="Home Page"
    text = "Controle de Estoque DI - Suporte e Redes"
    context={
        "title": title,
        "text": text
    }
    return render(request, "home.html", context)

def lista_itens(request):
    title="Relação de Materiais"
    queryset = Stock.objects.all()
    context={
        "title": title,
        "queryset": queryset,
    }
    return render(request, "lista_itens.html", context)

def adicionar_itens(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/lista_itens')
    context = {
        "form": form,
        "title": "Entrada de Materiais",
    }
    return render(request, "adicionar_itens.html", context)

