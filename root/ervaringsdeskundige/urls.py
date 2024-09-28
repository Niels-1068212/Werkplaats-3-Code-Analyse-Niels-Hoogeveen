from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path(
        "dashboard",
        views.dashboard_ervaringsdeskundige,
        name="ervaringsdeskundige_login",
    ),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("logout", views.logout_ervaringsdeskundige, name="logout"),
    path("onderzoeken", views.onderzoeken, name="onderzoeken"),
    path(
        "investigation/<int:investigation_id>",
        views.register_investigation,
        name="register_investigation",
    ),
    path(
        "registered_investigations",
        views.registered_investigations,
        name="registered_investigations",
    ),
    path(
        "register_investigation_succes",
        views.register_investigation_succes,
        name="register_investigation_succes",
    ),
    path(
        "unsubscribe_investigation/<int:investigation_id>",
        views.unsubscribe_investigation,
        name="unsubscribe_investigation",
    ),
    path("delete_account", views.delete_account, name="delete_account"),
    path("live_dashboard_data", views.live_dashboard_data, name="live_dashboard_data"),
    path(
        "75584bb7-2266-4c41-87f1-97cd5d53b5c4/notification.mp3",
        views.notification,
        name="notification",
    ),
    path(
        "inspect_investigation/<int:investigation_id>",
        views.inspect_investigation,
        name="inspect_investigation",
    ),
    path(
        "completed_investigations",
        views.completed_investigations,
        name="completed_investigations",
    ),
]
