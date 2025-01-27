from .models import Skladnik, ElementListy, ListaZakupow

#used in adding ingredients from a recipe or from a diet. accounts for ingredients with the same name.
def add_ingredients_to_shopping_list(shopping_list_id, ingredient_ids):
    shopping_list = ListaZakupow.objects.get(idLista=shopping_list_id)
    list_elements = ElementListy.objects.filter(lista=shopping_list)

    for ingredient_id in ingredient_ids:
        element_found = False
        print("ingredient_id:", ingredient_id)
        ingredient = Skladnik.objects.get(idSkladnik=ingredient_id)

        #check if the ingredient is already in the shopping list
        #if it is, increase the amount
        #if not, add the ingredient to the shopping list
        
        for element in list_elements:
            if element.nazwaElementu.lower() == ingredient.nazwaSkladnika.lower(): #can be more optimal with iexact
                print("element already on the list")
                element.ilosc += ingredient.ilosc
                element.save()
                element_found = True
                break
        
        if not element_found:
            print("element not on the list, creating a new one")
            new_element = ElementListy(lista=shopping_list, nazwaElementu=ingredient.nazwaSkladnika, ilosc=ingredient.ilosc, jednostka=ingredient.jednostka)
            new_element.save()