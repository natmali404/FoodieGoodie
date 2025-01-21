from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import ListaZakupow, Uzytkownik, ElementListy, Przepis, Skladnik
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from ..forms.shopping_list_form import ShoppingListForm


# def shopping_list_all(request):
#     #FOR TESTING PURPOSES
#     user = Uzytkownik.objects.get(id=1)
#     lists = ListaZakupow.objects.filter(autor=user)
#     return render(request, 'shopping_list/shopping_list_all.html', {'lists': lists})

TEST_USER_ID = 1

class ShoppingListAllView(ListView):
    model = ListaZakupow
    template_name = 'shopping_list/shopping_list_all.html'
    context_object_name = 'lists'

    def get_queryset(self):
        return ListaZakupow.objects.filter(autor_id=TEST_USER_ID)
    

class ShoppingListDetailView(DetailView):
    model = ListaZakupow
    template_name = 'shopping_list/shopping_list_detail.html'
    context_object_name = 'shopping_list'

    # def get_queryset(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     self.object = self.get_object()
    #     context['elements'] = ElementListy.objects.filter(lista=self.object)
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.get_object()
        print(ElementListy.objects.all())
        context['elements'] = ElementListy.objects.filter(lista=shopping_list)
        print(context['elements'])
        return context

class ShoppingListCreateView(CreateView):
    model = ListaZakupow
    form_class = ShoppingListForm
    template_name = 'shopping_list/shopping_list_form.html'
    success_url = reverse_lazy('shopping_list_all')

    def form_valid(self, form):
        form.instance.autor = Uzytkownik.objects.get(idUzytkownik=TEST_USER_ID)
        return super().form_valid(form)
    

class ShoppingListUpdateView(UpdateView):
    model = ListaZakupow
    form_class = ShoppingListForm
    template_name = 'shopping_list/shopping_list_form.html'
    success_url = reverse_lazy('shopping_list_all')


class ShoppingListDeleteView(DeleteView):
    model = ListaZakupow
    template_name = 'shopping_list/shopping_list_confirm_delete.html'
    success_url = reverse_lazy('shopping_list_all')


#view #1 - select recipes
class AddFromRecipeView(ListView):
    model = Przepis
    template_name = 'shopping_list/add_from_recipe.html'
    
    def get_queryset(self):
        return Przepis.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        
        print("AddFromRecipeView - pk:", context['pk'])
        return context
       
    
    def post(self, request, *args, **kwargs):
        
        selected_recipes = request.POST.getlist('selected_recipes')
        request.session['selected_recipes'] = selected_recipes
        print("AddFromRecipeView - selected recipes:", selected_recipes)
        
        pk = self.kwargs.get('pk')
        return redirect('confirm_ingredients', pk=pk)
    
    
#view #2 - select ingredients and confirm/refuse
class ConfirmIngredientsView(TemplateView):
    template_name = 'shopping_list/confirm_ingredients.html'
    
    # def get_context_data(self, **kwargs):
    #     print("ok")
    #     context = super().get_context_data(**kwargs)
    #     selected_recipes = self.request.session.get('selected_recipes', [])
        
    #     print("ConfirmIngredientsView - selected recipes:", selected_recipes)
        
    #     # context['ingredients'] = Skladnik.objects.filter(przepis__id__in=selected_recipes)
        
    #     pk = self.kwargs.get('pk')
    #     context['pk'] = pk
        
    #     print("ConfirmIngredientsView - pk:", context['pk'])

    #     return context
    
    
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Pobieranie listy wybranych przepisów z sesji
    #     selected_recipes_ids = self.request.session.get('selected_recipes', [])
        
    #     # Filtrujesz składniki dla wybranych przepisów
    #     selected_recipes = Przepis.objects.filter(id__in=selected_recipes_ids)
        
    #     skladniki_przepisu = SkladnikPrzepisu.objects.filter(przepis_id=przepis_id)
        
    #     context['selected_recipes'] = selected_recipes
        
    #     pk = self.kwargs.get('pk')
    #     context['pk'] = pk
        
    #     return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("getting context data!")
        
        selected_recipe_ids = self.request.session.get('selected_recipes', [])
       
        selected_recipes = Przepis.objects.filter(idPrzepis__in=selected_recipe_ids)
        
        print("ConfirmIngredientsView - selected recipes:", selected_recipes)
        
        context['selected_recipes'] = selected_recipes
        
        return context
    
    
    # def get(self, request, *args, **kwargs):
    #     print("ConfirmIngredientsView - get")
    #     selected_recipes = self.request.session.get('selected_recipes', [])
    #     print("ConfirmIngredientsView - selected recipes:", selected_recipes)
        
    #     pk = kwargs.get('pk')
    #     return render(request, 'shopping_list/confirm_ingredients.html', {'pk': pk})
    
    
    
    def post(self, request, *args, **kwargs):
        selected_recipes = request.POST.getlist('selected_recipes')
        
        # Możesz teraz przetworzyć te dane, np. dodać składniki do listy zakupów, zapisać je itp.
        print("Selected recipes:", selected_recipes)
        
        # Przykładowe przekierowanie po przetworzeniu danych:
        return redirect('confirm_ingredients', pk=self.kwargs['pk'])