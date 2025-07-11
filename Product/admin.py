from django.contrib import admin
from .models import (
    Catagory,
    Product,
    Slider,
)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('tittle',)}  # Fix: correct tuple syntax

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('tittle',)} # Fix: correct tuple syntax

admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Slider)
