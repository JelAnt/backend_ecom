from django.contrib import admin
from .models import Computer, Category

class ComputerAdmin(admin.ModelAdmin):
    list_display = ('model', 'category', 'cpu', 'price')
    search_fields = ('model', 'category__name', 'cpu')
    list_filter = ('category', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Computer, ComputerAdmin)
admin.site.register(Category, CategoryAdmin)