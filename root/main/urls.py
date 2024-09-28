from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("API", views.API, name="api_list_test"),
    path("api/organisatie/<int:pk>", views.organisatie_details, name="organisatie_details"),
    path(
        "api/organisatie/onderzoeken/<int:onderzoeks_id>",
        views.update_onderzoek,
        name="update_onderzoek",
    ),
    path(
        "api/organisatie/onderzoeken", views.lijst_onderzoeken, name="lijst_onderzoeken"
    ),
    path("login", views.custom_login, name="customlogin"),
]
