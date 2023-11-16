from django.db import models

# Create your models here.
categoria_selecionada = (
    ('NOVO', 'NOVO'),
    ('USADO', 'USADO'),
)


class Categoria(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome


class Stock(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, blank=True)
    nome_item = models.CharField(max_length=50, blank=True, null=True)
    quantidade = models.IntegerField(default='0', blank=True, null=True)
    quantidade_recebida = models.IntegerField(
        default='0', blank=True, null=True)
    recebido_por = models.CharField(max_length=50, blank=True, null=True)
    quantidade_entregue = models.IntegerField(
        default='0', blank=True, null=True)
    entregue_por = models.CharField(max_length=50, blank=True, null=True)
    entregue_para = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    criado_por = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    data_adicionado = models.DateTimeField(auto_now_add=True, auto_now=False)
    data = models.DateTimeField(auto_now_add=True, auto_now=False)

    # exportar_para_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_item

class StockHistory(models.Model):
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
	nome_item = models.CharField(max_length=50, blank=True, null=True)
	quantidade = models.IntegerField(default='0', blank=True, null=True)
	quantidade_recebida = models.IntegerField(default='0', blank=True, null=True)
	recebido_por = models.CharField(max_length=50, blank=True, null=True)
	quantidade_entregue = models.IntegerField(default='0', blank=True, null=True)
	entregue_por = models.CharField(max_length=50, blank=True, null=True)
	entregue_para = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	criado_por = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	data_adicionado = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)