from django.urls import path
from .views import main_views
from .swagger import schema_view

urlpatterns = [
    path('', main_views.home, name='home'),  # Home view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('przepis/<int:id>/', main_views.przepis_detail, name='recipe_detail'),
]
