from django.shortcuts import redirect
from django.urls import reverse


class PasswordChangeRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            allowed_paths = {
                reverse("password_change_required"),
                reverse("logout"),
            }
            path = request.path
            is_allowed = (
                path in allowed_paths
                or path.startswith("/admin/")
                or path.startswith("/static/")
                or path.startswith("/media/")
            )
            must_change = getattr(getattr(user, "profile", None), "must_change_password", False)
            if must_change and not is_allowed:
                return redirect("password_change_required")

        return self.get_response(request)
