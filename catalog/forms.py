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
    new_category_name = forms.CharField(
        label="Nueva categoria",
        required=False,
        help_text="Usar solo si la categoria no existe.",
    )
    new_brand_name = forms.CharField(
        label="Nueva marca",
        required=False,
        help_text="Usar solo si la marca no existe.",
    )
    new_supplier_name = forms.CharField(
        label="Nuevo proveedor",
        required=False,
        help_text="Usar solo si el proveedor no existe.",
    )
    new_warehouse_name = forms.CharField(
        label="Nueva bodega",
        required=False,
        help_text="Usar solo si la bodega no existe.",
    )
    new_warehouse_location = forms.CharField(
        label="Ubicacion de nueva bodega",
        required=False,
    )

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
        self.fields["category"].required = False
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

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        new_category_name = cleaned_data.get("new_category_name", "").strip()
        new_warehouse_location = cleaned_data.get("new_warehouse_location", "").strip()

        if not category and not new_category_name:
            self.add_error(
                "category",
                "Selecciona una categoria existente o escribe una nueva categoria.",
            )

        if new_warehouse_location and not cleaned_data.get("new_warehouse_name", "").strip():
            self.add_error(
                "new_warehouse_name",
                "Escribe el nombre de la nueva bodega.",
            )

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        new_category_name = self.cleaned_data.get("new_category_name", "").strip()
        new_brand_name = self.cleaned_data.get("new_brand_name", "").strip()
        new_supplier_name = self.cleaned_data.get("new_supplier_name", "").strip()
        new_warehouse_name = self.cleaned_data.get("new_warehouse_name", "").strip()
        new_warehouse_location = self.cleaned_data.get("new_warehouse_location", "").strip()

        if new_category_name:
            product.category = self.get_or_create_named(Category, new_category_name)
        if new_brand_name:
            product.brand = self.get_or_create_named(Brand, new_brand_name)
        if new_supplier_name:
            product.supplier = self.get_or_create_named(Supplier, new_supplier_name)
        if new_warehouse_name:
            Warehouse.objects.get_or_create(
                name=new_warehouse_name,
                defaults={"location": new_warehouse_location, "is_active": True},
            )

        if commit:
            product.save()
            self.save_m2m()
        return product

    @staticmethod
    def get_or_create_named(model, name):
        existing = model.objects.filter(name__iexact=name).first()
        if existing:
            return existing
        return model.objects.create(name=name)


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
