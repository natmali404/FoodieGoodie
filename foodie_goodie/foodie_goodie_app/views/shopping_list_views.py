from django.shortcuts import redirect
from django.urls import reverse_lazy
from ..models import ListaZakupow, Uzytkownik, ElementListy, Przepis, Jednostka, Jadlospis, JadlospisPrzepis
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from ..forms.shopping_list_form import ShoppingListForm
from ..services import add_ingredients_to_shopping_list

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import pdfbase
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
import os


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
        context['shopping_list_name'] = shopping_list.nazwaListy
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
        form.instance.autor = Uzytkownik.objects.get(idUzytkownik=1)
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
        
        if not selected_recipes:
            return redirect('shopping_list_detail', pk=self.kwargs['pk'])

        
        pk = self.kwargs.get('pk')
        return redirect('confirm_ingredients', pk=pk)
    
    
#view #2 - select ingredients and confirm/refuse
class ConfirmIngredientsView(TemplateView):
    template_name = 'shopping_list/confirm_ingredients.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_recipe_ids = self.request.session.get('selected_recipes', [])
        selected_recipes = Przepis.objects.filter(idPrzepis__in=selected_recipe_ids)
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
        
        #get all recipes ids from selected diets
        recipes = JadlospisPrzepis.objects.filter(jadlospis__in=selected_diets)
        selected_recipes = [str(recipe.przepis.idPrzepis) for recipe in recipes]
        request.session['selected_recipes' ] = selected_recipes

        if not selected_recipes:
            return redirect('shopping_list_detail', pk=self.kwargs['pk'])
        
        pk = self.kwargs.get('pk')
        return redirect('confirm_ingredients', pk=pk)
    
    
    
#pdf export

def export_shopping_list(request, pk):
    shopping_list = ListaZakupow.objects.get(pk=pk)
    elements = ElementListy.objects.filter(lista=shopping_list)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    font_path = os.path.join(settings.BASE_DIR, 'foodie_goodie_app', 'static', 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    p.setFont("DejaVuSans", 12)


    p.drawString(100, height - 100, f"Lista Zakupów - {shopping_list.nazwaListy}")

    y_position = height - 150

    for element in elements:
        checkbox_x = 100
        checkbox_y = y_position - 2

        p.rect(checkbox_x, checkbox_y, 12, 12)

        if element.zaznaczony:
            p.rect(checkbox_x + 1, checkbox_y + 1, 11, 11, fill=1)


        item_text = f"{element.nazwaElementu} {element.ilosc} {element.jednostka.nazwaJednostki}"
        
        p.drawString(checkbox_x + 20, y_position, item_text)

        y_position -= 20

    p.showPage()
    p.save()
    
    return response
