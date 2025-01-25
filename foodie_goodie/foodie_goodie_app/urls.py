from django.urls import path
from .views import main_views,recipe_views
from .swagger import schema_view

urlpatterns = [
    path('', main_views.home, name='home'),  # Home view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('przepis/<int:id>/', recipe_views.przepis_detail, name='recipe_detail'),
    path('przepis/<int:id>/stars', recipe_views.przepis_detail_stars, name='recipe_detail_stars'),
    path('przepis/<int:id>/addcomment', recipe_views.add_komentarz, name='addcomment'),
    path('przepis/<int:id>/obserw', recipe_views.obserwuj_przepis, name='obserw'),
]
