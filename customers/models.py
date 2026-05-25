from django.conf import settings
from django.db import models


class Customer(models.Model):
    class CustomerType(models.TextChoices):
        NATURAL = "natural", "Persona natural"
        COMPANY = "company", "Empresa"
        GOVERNMENT = "government", "Institucion"
        OTHER = "other", "Otro"

    customer_type = models.CharField(
        "tipo de cliente",
        max_length=20,
        choices=CustomerType.choices,
        default=CustomerType.NATURAL,
    )
    name = models.CharField("nombre", max_length=180)
    phone = models.CharField("telefono", max_length=30, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=30, blank=True)
    email = models.EmailField("correo", blank=True)
    address = models.TextField("direccion", blank=True)
    ruc = models.CharField("RUC", max_length=30, blank=True)
    notes = models.TextField("observaciones", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers_created",
        verbose_name="creado por",
    )
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["whatsapp"]),
            models.Index(fields=["email"]),
            models.Index(fields=["ruc"]),
        ]

    def __str__(self):
        return self.name
