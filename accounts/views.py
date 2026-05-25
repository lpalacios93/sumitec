from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import StyledAuthenticationForm, StyledPasswordChangeForm


class SumitecLoginView(LoginView):
    authentication_form = StyledAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        profile = getattr(self.request.user, "profile", None)
        if profile and profile.must_change_password:
            return reverse_lazy("password_change_required")
        return reverse_lazy("dashboard")


class SumitecLogoutView(LogoutView):
    next_page = reverse_lazy("login")


@login_required
def dashboard(request):
    profile = getattr(request.user, "profile", None)
    role = profile.role if profile else "seller"
    return render(
        request,
        "accounts/dashboard.html",
        {
            "role": role,
            "is_admin": role == "admin",
        },
    )


@login_required
def password_change_required(request):
    if request.method == "POST":
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            profile = getattr(user, "profile", None)
            if profile:
                profile.must_change_password = False
                profile.save(update_fields=["must_change_password", "updated_at"])
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect("dashboard")
    else:
        form = StyledPasswordChangeForm(request.user)

    return render(request, "accounts/password_change_required.html", {"form": form})
