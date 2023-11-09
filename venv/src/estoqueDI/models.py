from django.db import models

# Create your models here.

class Stock(models.Model):
	categoria = models.CharField(max_length=50, blank=False, null=True)
	nome_item = models.CharField(max_length=50, blank=False, null=True)
	quantidade = models.IntegerField(default='0', blank=True, null=True)
	quantidade_recebida = models.IntegerField(default='0', blank=True, null=True)
	recebido_por = models.CharField(max_length=50, blank=True, null=True)
	quantidade_entregue = models.IntegerField(default='0', blank=True, null=True)
	entregue_por = models.CharField(max_length=50, blank=True, null=True)
	entregue_para = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	criado_por = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	exportar_para_CSV = models.BooleanField(default=False)

	def __str__(self):
		return self.nome_item