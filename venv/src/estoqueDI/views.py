from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
#from weasyprint import HTML
from django.utils import timezone
import csv
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    title = "Home Page"
    text = "Controle de Estoque DI - Suporte e Redes"
    context = {
        "title": title,
        "text": text
    }
    return render(request, "home.html", context)

def login(request):
    title = "Login"
    context = {
        "title": title,
    }
    return render(request, "login.html", context)

@login_required
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

@login_required
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

@login_required
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

@login_required
def delete_itens(request, pk):
    instance = Stock.objects.get(id=pk)

    if request.method == 'POST':
        valor_digitado = request.POST.get('valor', '')

        if valor_digitado == instance.nome_item:
            instance.delete()
            messages.success(request, 'Deletado com sucesso')
            return redirect('/lista_itens')
        else:
            messages.error(request, 'Nome do item incorreto. Tente novamente.')

    return redirect('/lista_itens')

@login_required
def detalhe_estoque(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {

        "queryset": queryset
    }
    return render(request, "detalhe_estoque.html", context)

@login_required
def saida_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = SaidaForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantidade_recebida=0
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

@login_required
def entrada_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = EntradaForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantidade_entregue = 0
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

@login_required
def reorderlevel(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Nivel de reabastecimento de " + str(
            instance.nome_item) + "é atualizado para " + str(instance.reorder_level))
        return redirect('/lista_itens')
    context={
        "instance":queryset,
        "form": form
    }
    return render(request, "adicionar_itens.html", context)

@login_required
def historico_geral(request):
    title = 'HISTORICO DOS ITENS'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()

    if request.method == 'POST':
        form = StockHistorySearchForm(request.POST)
        if form.is_valid():
            nome_item = form.cleaned_data.get('nome_item')
            categoria = form.cleaned_data.get('categoria')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            
            if nome_item:
                queryset = queryset.filter(nome_item__icontains=nome_item)
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            if data_inicio:
                queryset = queryset.filter(last_updated__gte=data_inicio)
            if data_fim:
                data_fim = timezone.datetime.combine(data_fim, timezone.datetime.max.time())
                queryset = queryset.filter(last_updated__lte=data_fim)
            
            if form['exportar_para_csv'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Lista do Estoque.csv"'
                writer = csv.writer(response)
                writer.writerow(['CATEGORIA', 'NOME ITEM', 'QUANTIDADE'])
                instance = queryset
                for stockHistory in instance:
                    writer.writerow(
                        [stockHistory.categoria, stockHistory.nome_item, stockHistory.quantidade])
                return response
        
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    return render(request, "historico_geral.html", context)

@login_required
def historico_entrada(request):
    title = 'HISTORICO DE MATERIAIS RECEBIDOS'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()

    if request.method == 'POST':
        form = StockHistorySearchForm(request.POST)
        if form.is_valid():
            nome_item = form.cleaned_data.get('nome_item')
            categoria = form.cleaned_data.get('categoria')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            
            if nome_item:
                queryset = queryset.filter(nome_item__icontains=nome_item)
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            if data_inicio:
                queryset = queryset.filter(last_updated__gte=data_inicio)
            if data_fim:
                data_fim = timezone.datetime.combine(data_fim, timezone.datetime.max.time())
                queryset = queryset.filter(last_updated__lte=data_fim)
                
            if form['exportar_para_csv'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Lista do materiais recebidos.csv"'
                writer = csv.writer(response)
                writer.writerow(['CATEGORIA', 'NOME ITEM', 'QUANTIDADE RECEBIDA'])
                instance = queryset
                for stockHistory in instance:
                    if stockHistory.quantidade_recebida != 0:
                        writer.writerow(
                            [stockHistory.categoria, stockHistory.nome_item, stockHistory.quantidade_recebida])
                return response
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    return render(request, "historico_entrada.html", context)

@login_required
def historico_saida(request):
    title = 'HISTORICO DE SAIDA DOS MATERIAIS'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()

    if request.method == 'POST':
        form = StockHistorySearchForm(request.POST)
        if form.is_valid():
            nome_item = form.cleaned_data.get('nome_item')
            categoria = form.cleaned_data.get('categoria')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            
            if nome_item:
                queryset = queryset.filter(nome_item__icontains=nome_item)
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            if data_inicio:
                queryset = queryset.filter(last_updated__gte=data_inicio)
            if data_fim:
                data_fim = timezone.datetime.combine(data_fim, timezone.datetime.max.time())
                queryset = queryset.filter(last_updated__lte=data_fim)
            
            if form['exportar_para_csv'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Lista de Saida de Estoque.csv"'
                writer = csv.writer(response)
                writer.writerow(['CATEGORIA', 'NOME ITEM', 'QUANTIDADE Entregue', 'Setor Entregue', 'Data de Entrega' ])
                instance = queryset
                for stockHistory in instance:
                    if stockHistory.quantidade_entregue != 0:
                        writer.writerow(
                            [stockHistory.categoria, stockHistory.nome_item, stockHistory.quantidade_entregue, stockHistory.entregue_para, stockHistory.last_updated ])
                return response

    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    return render(request, "historico_saida.html", context)