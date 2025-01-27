from django.urls import path
from .views import main_views
from .views.shopping_list_views import ShoppingListAllView, ShoppingListCreateView, ShoppingListDetailView, ShoppingListUpdateView, ShoppingListDeleteView, AddFromRecipeView, AddFromDietView, ConfirmIngredientsView, export_shopping_list
from .views.api_views import add_list_element, delete_list_element, update_list_element_status
from .views.forum_views import ForumAllView
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
    
    #api
    path('shopping_list/<int:pk>/add_list_element/', add_list_element, name='add_list_element'),
    path('shopping_list/<int:pk>/delete_list_element/', delete_list_element, name='delete_list_element'),
    path('shopping_list/<int:pk>/update_list_element_status/', update_list_element_status, name='update_list_element_status'),
    
    #add from recipe and add from diet
    path('shopping-lists/<int:pk>/add-from-recipe/', AddFromRecipeView.as_view(), name='add_from_recipe'),
    path('shopping-lists/<int:pk>/confirm-ingredients/', ConfirmIngredientsView.as_view(), name='confirm_ingredients'),
    
    path('shopping-lists/<int:pk>/add-from-diet/', AddFromDietView.as_view(), name='add_from_diet'),

    #export
    path('shopping-list/export/', export_shopping_list, name='export-shopping-list'),

    #forum
    path('forums/', ForumAllView.as_view(), name='forum_all'),
    ]