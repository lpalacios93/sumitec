from decimal import Decimal

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("nombre", max_length=120, unique=True)
    description = models.TextField("descripcion", blank=True)
    is_active = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField("nombre", max_length=120, unique=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "marca"
        verbose_name_plural = "marcas"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField("nombre", max_length=160, unique=True)
    phone = models.CharField("telefono", max_length=30, blank=True)
    email = models.EmailField("correo", blank=True)
    address = models.TextField("direccion", blank=True)
    notes = models.TextField("observaciones", blank=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField("nombre", max_length=120, unique=True)
    location = models.CharField("ubicacion", max_length=180, blank=True)
    is_active = models.BooleanField("activo", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "bodega"
        verbose_name_plural = "bodegas"

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField("codigo interno", max_length=60, unique=True)
    barcode = models.CharField("codigo de barras", max_length=80, blank=True)
    description = models.CharField("descripcion", max_length=255)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="marca",
    )
    model = models.CharField("modelo", max_length=120, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="categoria",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="proveedor",
    )
    cost_price = models.DecimalField("costo sin IVA", max_digits=12, decimal_places=2)
    sale_price = models.DecimalField("precio venta sin IVA", max_digits=12, decimal_places=2)
    applies_iva = models.BooleanField("aplica IVA", default=True)
    warranty = models.CharField("garantia", max_length=160, blank=True)
    image = models.ImageField("imagen", upload_to="products/", blank=True)
    notes = models.TextField("observaciones", blank=True)
    is_active = models.BooleanField("activo", default=True)
    last_price_update = models.DateTimeField("ultima actualizacion de precio", auto_now=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["description"]),
            models.Index(fields=["model"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.description}"

    def get_absolute_url(self):
        return reverse("catalog:products")

    @property
    def stock_total(self):
        total = self.stock_entries.aggregate(total=models.Sum("quantity"))["total"]
        return total or Decimal("0")


class ProductStock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_entries",
        verbose_name="producto",
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stock_entries",
        verbose_name="bodega",
    )
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        unique_together = ("product", "warehouse")
        ordering = ["warehouse__name"]
        verbose_name = "stock de producto"
        verbose_name_plural = "stock de productos"

    def __str__(self):
        return f"{self.product.code} - {self.warehouse.name}: {self.quantity}"
