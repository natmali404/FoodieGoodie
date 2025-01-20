from django.urls import path
from . import views
from .swagger import schema_view

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
