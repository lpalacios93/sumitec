from django.urls import path

from . import views


app_name = "catalog"

urlpatterns = [
    path("productos/", views.ProductListView.as_view(), name="products"),
    path("productos/nuevo/", views.ProductCreateView.as_view(), name="product_create"),
    path("productos/<int:pk>/editar/", views.ProductUpdateView.as_view(), name="product_update"),
    path("productos/<int:pk>/stock/", views.ProductStockUpdateView.as_view(), name="product_stock"),
    path("categorias/", views.CategoryListView.as_view(), name="categories"),
    path("categorias/nueva/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categorias/<int:pk>/editar/", views.CategoryUpdateView.as_view(), name="category_update"),
    path("marcas/", views.BrandListView.as_view(), name="brands"),
    path("marcas/nueva/", views.BrandCreateView.as_view(), name="brand_create"),
    path("marcas/<int:pk>/editar/", views.BrandUpdateView.as_view(), name="brand_update"),
    path("proveedores/", views.SupplierListView.as_view(), name="suppliers"),
    path("proveedores/nuevo/", views.SupplierCreateView.as_view(), name="supplier_create"),
    path("proveedores/<int:pk>/editar/", views.SupplierUpdateView.as_view(), name="supplier_update"),
    path("bodegas/", views.WarehouseListView.as_view(), name="warehouses"),
    path("bodegas/nueva/", views.WarehouseCreateView.as_view(), name="warehouse_create"),
    path("bodegas/<int:pk>/editar/", views.WarehouseUpdateView.as_view(), name="warehouse_update"),
]
