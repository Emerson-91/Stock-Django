from django.contrib import admin
from .forms import StockCreateForm

from .models import Stock, Categoria

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'nome_item', 'quantidade']
    form = StockCreateForm
    list_filter = ['categoria']
    search_fields = ['categoria', 'nome_item']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Categoria)