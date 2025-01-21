from django.urls import path
from .views import main_views
from .views.shopping_list_views import ShoppingListAllView, ShoppingListCreateView, ShoppingListDetailView, ShoppingListUpdateView, ShoppingListDeleteView
from .swagger import schema_view

urlpatterns = [
    path('', main_views.home, name='home'),  # Home view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    #shopping lists
    path('shopping-lists/', ShoppingListAllView.as_view(), name='shopping_list_all'),
    path('shopping-lists/new/', ShoppingListCreateView.as_view(), name='shopping_list_create'),
    path('shopping-lists/<int:pk>/', ShoppingListDetailView.as_view(), name='shopping_list_detail'),
    path('shopping-lists/<int:pk>/edit/', ShoppingListUpdateView.as_view(), name='shopping_list_update'),
    path('shopping-lists/<int:pk>/delete/', ShoppingListDeleteView.as_view(), name='shopping_list_delete'),
]
