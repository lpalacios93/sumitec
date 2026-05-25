from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CustomerForm
from .models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"
    paginate_by = 15

    def get_queryset(self):
        queryset = Customer.objects.select_related("created_by").order_by("name")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(phone__icontains=query)
                | Q(whatsapp__icontains=query)
                | Q(email__icontains=query)
                | Q(ruc__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class DuplicateWarningMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        duplicate_messages = self.get_duplicate_messages(self.object)
        for warning in duplicate_messages:
            messages.warning(self.request, warning)
        return response

    def get_duplicate_messages(self, customer):
        checks = [
            ("RUC", customer.ruc),
            ("telefono", customer.phone),
            ("WhatsApp", customer.whatsapp),
            ("correo", customer.email),
        ]
        warnings = []
        for label, value in checks:
            if not value:
                continue
            exists = (
                Customer.objects.exclude(pk=customer.pk)
                .filter(**{f"{self.get_lookup_field(label)}__iexact": value})
                .exists()
            )
            if exists:
                warnings.append(
                    f"Advertencia: ya existe otro cliente con el mismo {label}."
                )
        return warnings

    @staticmethod
    def get_lookup_field(label):
        return {
            "RUC": "ruc",
            "telefono": "phone",
            "WhatsApp": "whatsapp",
            "correo": "email",
        }[label]


class CustomerCreateView(LoginRequiredMixin, DuplicateWarningMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Cliente creado correctamente.")
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, DuplicateWarningMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)
