from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.SumitecLoginView.as_view(), name="login"),
    path("logout/", views.SumitecLogoutView.as_view(), name="logout"),
    path(
        "cambiar-contrasena/",
        views.password_change_required,
        name="password_change_required",
    ),
    path("", views.dashboard, name="dashboard"),
]
