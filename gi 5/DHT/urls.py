from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view),
    path('register/', views.register_view),

    # Sensor
    path('post_data/', views.DhtCreateView),
    path('list/', views.Dlist),

    # Alerts & tickets
    path('alerts/', views.alerts_list),
    path('tickets/', views.ticket_list),
    path('tickets/create/', views.ticket_create),
    path('tickets/update/<int:pk>/', views.ticket_update),

    # Audit
    path('audit/', views.audit_list),
]
