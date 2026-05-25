from django.contrib import admin

from .models import Brand, Category, Product, ProductStock, Supplier, Warehouse


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "description",
        "brand",
        "model",
        "category",
        "sale_price",
        "applies_iva",
        "is_active",
    )
    list_filter = ("category", "brand", "applies_iva", "is_active")
    search_fields = ("code", "barcode", "description", "model")
    inlines = (ProductStockInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "phone", "email")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_active")
    search_fields = ("name", "location")
