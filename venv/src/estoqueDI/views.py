from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .models import *
from .forms import StockCreateForm, stockSearchForm, StockUpdateForm, SaidaForm, EntradaForm
from django.contrib import messages


def home(request):
    title = "Home Page"
    text = "Controle de Estoque DI - Suporte e Redes"
    context = {
        "title": title,
        "text": text
    }
    return render(request, "home.html", context)


def lista_itens(request):
    title = "Relação de Materiais"
    form = stockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(categoria__id__icontains=form['categoria'].value(),
                                        nome_item__icontains=form['nome_item'].value())
        if form['exportar_para_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Lista do Estoque.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORIA', 'NOME ITEM', 'QUANTIDADE'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.categoria, stock.nome_item, stock.quantidade])
            return response

        context = {
            "form": form,
            "title": title,
            "queryset": queryset
        }
    return render(request, "lista_itens.html", context)


def adicionar_itens(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Adicionado com sucesso')
        return redirect('/lista_itens')
    context = {
        "form": form,
        "title": "Entrada de Materiais",
    }
    return render(request, "adicionar_itens.html", context)


def atualizar_itens(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atualizado com sucesso')
            return redirect('/lista_itens')
    context = {
        'form': form
    }
    return render(request, 'adicionar_itens.html', context)


def delete_itens(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deletado com sucesso')
        return redirect('/lista_itens')
    return render(request, 'delete_itens.html')


def detalhe_estoque(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {

        "queryset": queryset
    }
    return render(request, "detalhe_estoque.html", context)


def saida_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = SaidaForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantidade -= instance.quantidade_entregue
        messages.success(request, "Baixa com SUCESSO. " + str(instance.quantidade) +
                         " " + str(instance.nome_item) + "s restantes no estoque")
        instance.save()

        return redirect('/detalhe_estoque/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Saida ' + str(queryset.nome_item),
        "queryset": queryset,
        "form": form,
    }
    return render(request, "adicionar_itens.html", context)


def entrada_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = EntradaForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantidade += instance.quantidade_recebida
        instance.save()
        messages.success(request, "Recebido com SUCESSO. " + str(
            instance.quantidade) + " " + str(instance.nome_item)+"s agora no estoque")

        return redirect('/detalhe_estoque/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Receber o item: ' + str(queryset.nome_item),
        "instance": queryset,
        "form": form,
    }
    return render(request, "adicionar_itens.html", context)
