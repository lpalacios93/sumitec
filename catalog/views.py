from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q, Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from accounts.mixins import AdminRequiredMixin

from .forms import (
    BrandForm,
    CategoryForm,
    ProductForm,
    ProductStockForm,
    SupplierForm,
    WarehouseForm,
)
from .models import Brand, Category, Product, Supplier, Warehouse


PICKER_CONFIG = {
    "categorias": {
        "model": Category,
        "form": CategoryForm,
        "title": "Categorias",
        "field_id": "id_category",
    },
    "marcas": {
        "model": Brand,
        "form": BrandForm,
        "title": "Marcas",
        "field_id": "id_brand",
    },
    "proveedores": {
        "model": Supplier,
        "form": SupplierForm,
        "title": "Proveedores",
        "field_id": "id_supplier",
    },
    "bodegas": {
        "model": Warehouse,
        "form": WarehouseForm,
        "title": "Bodegas",
        "field_id": "",
    },
}


def user_is_admin(user):
    profile = getattr(user, "profile", None)
    return user.is_superuser or bool(profile and profile.is_admin)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("brand", "category", "supplier")
            .annotate(stock_total_value=Sum("stock_entries__quantity"))
            .order_by("code")
        )
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(code__icontains=query)
                | Q(barcode__icontains=query)
                | Q(description__icontains=query)
                | Q(model__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(category__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["is_admin"] = user_is_admin(self.request.user)
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products")

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductStockUpdateView(AdminRequiredMixin, View):
    template_name = "catalog/product_stock_form.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductStockForm(product=product)
        return render(request, self.template_name, {"product": product, "form": form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductStockForm(request.POST, product=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock actualizado correctamente.")
            return redirect("catalog:products")
        return render(request, self.template_name, {"product": product, "form": form})


class CatalogPickerView(AdminRequiredMixin, View):
    template_name = "catalog/picker.html"

    def dispatch(self, request, kind, *args, **kwargs):
        self.config = PICKER_CONFIG[kind]
        self.kind = kind
        return super().dispatch(request, kind, *args, **kwargs)

    def get(self, request, kind):
        return self.render_picker()

    def post(self, request, kind):
        action = request.POST.get("action")
        model = self.config["model"]
        form_class = self.config["form"]

        if action == "delete":
            item = get_object_or_404(model, pk=request.POST.get("item_id"))
            try:
                item.delete()
                messages.success(request, "Registro eliminado correctamente.")
            except (ProtectedError, IntegrityError):
                messages.error(
                    request,
                    "No se puede eliminar porque ya esta siendo usado.",
                )
            return redirect(request.path)

        instance = None
        if action == "update":
            instance = get_object_or_404(model, pk=request.POST.get("item_id"))

        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect(request.path)

        return self.render_picker(form=form)

    def render_picker(self, form=None):
        model = self.config["model"]
        form_class = self.config["form"]
        query = self.request.GET.get("q", "").strip()
        edit_id = self.request.GET.get("edit")
        edit_object = None
        if edit_id:
            edit_object = get_object_or_404(model, pk=edit_id)

        queryset = model.objects.order_by("name")
        if query:
            queryset = queryset.filter(name__icontains=query)

        if form is None:
            form = form_class(instance=edit_object)

        return render(
            self.request,
            self.template_name,
            {
                "kind": self.kind,
                "title": self.config["title"],
                "field_id": self.request.GET.get("field_id") or self.config["field_id"],
                "items": queryset,
                "query": query,
                "form": form,
                "edit_object": edit_object,
            },
        )

class SimpleAdminListView(AdminRequiredMixin, ListView):
    template_name = "catalog/simple_list.html"
    paginate_by = 20
    create_url_name = ""
    update_url_name = ""
    title = ""
    eyebrow = "Catalogo"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "query": self.request.GET.get("q", "").strip(),
                "title": self.title,
                "eyebrow": self.eyebrow,
                "create_url_name": self.create_url_name,
                "update_url_name": self.update_url_name,
            }
        )
        return context


class SimpleAdminFormMixin(AdminRequiredMixin):
    template_name = "catalog/simple_form.html"
    success_message = "Registro guardado correctamente."
    title = ""
    list_url_name = ""

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title, "list_url_name": self.list_url_name})
        return context


class CategoryListView(SimpleAdminListView):
    model = Category
    title = "Categorias"
    create_url_name = "catalog:category_create"
    update_url_name = "catalog:category_update"


class CategoryCreateView(SimpleAdminFormMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:categories")
    title = "Crear categoria"
    list_url_name = "catalog:categories"


class CategoryUpdateView(SimpleAdminFormMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:categories")
    title = "Editar categoria"
    list_url_name = "catalog:categories"


class BrandListView(SimpleAdminListView):
    model = Brand
    title = "Marcas"
    create_url_name = "catalog:brand_create"
    update_url_name = "catalog:brand_update"


class BrandCreateView(SimpleAdminFormMixin, CreateView):
    model = Brand
    form_class = BrandForm
    success_url = reverse_lazy("catalog:brands")
    title = "Crear marca"
    list_url_name = "catalog:brands"


class BrandUpdateView(SimpleAdminFormMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    success_url = reverse_lazy("catalog:brands")
    title = "Editar marca"
    list_url_name = "catalog:brands"


class SupplierListView(SimpleAdminListView):
    model = Supplier
    title = "Proveedores"
    create_url_name = "catalog:supplier_create"
    update_url_name = "catalog:supplier_update"


class SupplierCreateView(SimpleAdminFormMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("catalog:suppliers")
    title = "Crear proveedor"
    list_url_name = "catalog:suppliers"


class SupplierUpdateView(SimpleAdminFormMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("catalog:suppliers")
    title = "Editar proveedor"
    list_url_name = "catalog:suppliers"


class WarehouseListView(SimpleAdminListView):
    model = Warehouse
    title = "Bodegas"
    create_url_name = "catalog:warehouse_create"
    update_url_name = "catalog:warehouse_update"


class WarehouseCreateView(SimpleAdminFormMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    success_url = reverse_lazy("catalog:warehouses")
    title = "Crear bodega"
    list_url_name = "catalog:warehouses"


class WarehouseUpdateView(SimpleAdminFormMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    success_url = reverse_lazy("catalog:warehouses")
    title = "Editar bodega"
    list_url_name = "catalog:warehouses"
