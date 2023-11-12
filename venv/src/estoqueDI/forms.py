from django import forms
from .models import Stock


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['categoria', 'nome_item', 'quantidade', 'data']

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError('Campo obrigatório')
        return categoria

    def clean_nome_item(self):
        nome_item = self.cleaned_data.get('nome_item')
        categoria = self.cleaned_data.get('categoria')
        if not nome_item:
            raise forms.ValidationError('Campo obrigatório')
        for instance in Stock.objects.all():
            if instance.nome_item == nome_item and instance.categoria == categoria:
                raise forms.ValidationError(nome_item + ' já existe')
        return nome_item


class stockSearchForm(forms.ModelForm):
    exportar_para_csv = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['categoria', 'nome_item']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['categoria', 'nome_item', 'quantidade']


class SaidaForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantidade_entregue', 'entregue_para']


class EntradaForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantidade_recebida']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
