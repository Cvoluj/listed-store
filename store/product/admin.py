from django.contrib import admin

from store.product.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'user', 'public_id', 'hidden')
    search_fields = ('name', 'description')
