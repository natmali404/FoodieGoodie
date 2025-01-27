from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import ListaZakupow, Uzytkownik, ElementListy, Przepis, Skladnik, Jednostka, Jadlospis, JadlospisPrzepis
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from ..forms.shopping_list_form import ShoppingListForm
from ..services import add_ingredients_to_shopping_list

from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.templatetags.static import static


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.get_object()
        print(ElementListy.objects.all())
        context['elements'] = ElementListy.objects.filter(lista=shopping_list)
        context['jednostki'] = Jednostka.objects.all()
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

        ##################
        # WAZNE JAK NIE MA ZAZNACZONYCH RECIPOW TO ODSWIEZ PO PROSTU ALBO COFNIJ DO WIDOKU DETAIL!!!!
        
        pk = self.kwargs.get('pk')
        return redirect('confirm_ingredients', pk=pk)
    
    
#view #2 - select ingredients and confirm/refuse
class ConfirmIngredientsView(TemplateView):
    template_name = 'shopping_list/confirm_ingredients.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("getting context data!")
        
        selected_recipe_ids = self.request.session.get('selected_recipes', [])
       
        selected_recipes = Przepis.objects.filter(idPrzepis__in=selected_recipe_ids)
        
        print("ConfirmIngredientsView - selected recipes:", selected_recipes)
        
        context['selected_recipes'] = selected_recipes
        
        return context
    
    def post(self, request, *args, **kwargs):
        
        #route from add_from_recipe
        if 'selected_recipes' in request.POST:
            selected_recipes = request.POST.getlist('selected_recipes')
            request.session['selected_recipes'] = selected_recipes
            return redirect('confirm_ingredients', pk=self.kwargs['pk'])

        #route from confirm_ingredients
        elif 'selected_ingredients' in request.POST:
            pk = self.kwargs['pk']
            selected_ingredients = request.POST.getlist('selected_ingredients')
            add_ingredients_to_shopping_list(pk, selected_ingredients)
            return redirect('shopping_list_detail', pk=pk)

        return redirect('confirm_ingredients', pk=self.kwargs['pk'])
    
    
#add from diet
class AddFromDietView(ListView):
    model = Jadlospis
    template_name = 'shopping_list/add_from_diet.html'
    
    def get_queryset(self):
        return Jadlospis.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs.get('pk')
        context['pk'] = pk
        
        print("AddFromDietView - pk:", context['pk'])
        return context
       
    def post(self, request, *args, **kwargs):
        selected_diets = request.POST.getlist('selected_diets')
        request.session['selected_diets' ] = selected_diets
        print("AddFromDietView - selected diets:", selected_diets)
        
        #get all recipes ids from selected diets
        recipes = JadlospisPrzepis.objects.filter(jadlospis__in=selected_diets)
        selected_recipes = [str(recipe.przepis.idPrzepis) for recipe in recipes]
        request.session['selected_recipes' ] = selected_recipes
        print("AddFromDietView - selected recipes:", selected_recipes)

        ##################
        # WAZNE JAK NIE MA ZAZNACZONYCH RECIPOW TO ODSWIEZ PO PROSTU ALBO COFNIJ DO WIDOKU DETAIL!!!!
        
        pk = self.kwargs.get('pk')
        return redirect('confirm_ingredients', pk=pk)
    
    
    
#pdf export

def lista_zakupow_pdf(request):
    elements = ElementListy.objects.all()

    html_string = render(request, 'shopping_list_pdf.html', {'elements': elements}).content.decode('utf-8')

    css_url = static('css/shopping_list_styles.css')
    css = CSS(css_url)

    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[css])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="lista_zakupow.pdf"'
    return response
