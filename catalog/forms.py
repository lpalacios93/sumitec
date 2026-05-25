from decimal import Decimal

from django import forms

from .models import Brand, Category, Product, ProductStock, Supplier, Warehouse


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "phone", "email", "address", "notes"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location", "is_active"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "code",
            "barcode",
            "description",
            "brand",
            "model",
            "category",
            "supplier",
            "cost_price",
            "sale_price",
            "applies_iva",
            "warranty",
            "image",
            "notes",
            "is_active",
        ]
        widgets = {
            "description": forms.TextInput(attrs={"autofocus": True}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True).order_by("name")
        self.fields["brand"].queryset = Brand.objects.order_by("name")
        self.fields["supplier"].queryset = Supplier.objects.order_by("name")

    def clean_cost_price(self):
        return self.clean_non_negative_decimal("cost_price")

    def clean_sale_price(self):
        return self.clean_non_negative_decimal("sale_price")

    def clean_non_negative_decimal(self, field_name):
        value = self.cleaned_data[field_name]
        if value < Decimal("0"):
            raise forms.ValidationError("El valor no puede ser negativo.")
        return value


class ProductStockForm(forms.Form):
    def __init__(self, *args, product, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        warehouses = Warehouse.objects.filter(is_active=True).order_by("name")
        existing = {
            item.warehouse_id: item.quantity
            for item in product.stock_entries.select_related("warehouse")
        }
        for warehouse in warehouses:
            self.fields[f"warehouse_{warehouse.pk}"] = forms.DecimalField(
                label=warehouse.name,
                min_value=Decimal("0"),
                max_digits=12,
                decimal_places=2,
                initial=existing.get(warehouse.pk, Decimal("0")),
                required=False,
            )

    def save(self):
        for name, quantity in self.cleaned_data.items():
            warehouse_id = int(name.replace("warehouse_", ""))
            ProductStock.objects.update_or_create(
                product=self.product,
                warehouse_id=warehouse_id,
                defaults={"quantity": quantity or Decimal("0")},
            )
