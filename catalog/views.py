from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
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
