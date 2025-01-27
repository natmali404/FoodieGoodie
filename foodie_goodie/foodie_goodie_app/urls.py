from django.urls import path
from .views import main_views
from .views.shopping_list_views import ShoppingListAllView, ShoppingListCreateView, ShoppingListDetailView, ShoppingListUpdateView, ShoppingListDeleteView, AddFromRecipeView, ConfirmIngredientsView
from .views.forum_views import ForumAllView, ForumDetailView, VotePostView, CreateThreadView
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
    
    #add from recipe and add from diet
    path('shopping-lists/<int:pk>/add-from-recipe/', AddFromRecipeView.as_view(), name='add_from_recipe'),
    path('shopping-lists/<int:pk>/confirm-ingredients/', ConfirmIngredientsView.as_view(), name='confirm_ingredients'),


    #forum
    path('forums/', ForumAllView.as_view(), name='forum_all'),
    path('forums/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('vote-post/', VotePostView.as_view(), name='vote_post'),
    path('new-forum/', CreateThreadView.as_view(), name='new_forum'),
]
