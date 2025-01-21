from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import ListaZakupow, Uzytkownik, ElementListy, Przepis
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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

class RecipeToListView():
    def get_queryset(self):
        return Przepis.objects.all()