from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "customer_type", "phone", "whatsapp", "email", "ruc")
    list_filter = ("customer_type",)
    search_fields = ("name", "phone", "whatsapp", "email", "ruc")
    readonly_fields = ("created_at", "updated_at")
