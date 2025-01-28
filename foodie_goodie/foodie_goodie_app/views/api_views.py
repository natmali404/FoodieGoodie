from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import ElementListy, Jednostka
from ..serializers import ElementListySerializer
from ..services import add_ingredients_to_shopping_list


@api_view(['POST'])
def add_list_element(request, pk):
    if request.method == "POST":
        nazwa = request.data.get('nazwaElementu')
        ilosc = request.data.get('ilosc')
        jednostka_id = request.data.get('jednostka')

        try:
            jednostka = Jednostka.objects.get(idJednostka=jednostka_id)
        except Jednostka.DoesNotExist:
            return Response({"success": False, "error": "Nieprawidłowa jednostka."}, status=400)

        existing_element = ElementListy.objects.filter(lista_id=pk, nazwaElementu__iexact=nazwa, jednostka=jednostka_id).first()

        if existing_element:
            existing_element.ilosc += float(ilosc)
            existing_element.save()
            serializer = ElementListySerializer(existing_element)
            return Response({"success": True, "list_element": serializer.data})
        else:
            new_element = ElementListy.objects.create(
                lista_id=pk,
                nazwaElementu=nazwa,
                ilosc=ilosc,
                jednostka=jednostka
            )
            serializer = ElementListySerializer(new_element)
            return Response({"success": True, "list_element": serializer.data})



@api_view(['POST'])
def delete_list_element(request, pk):
    id_elementu = request.data.get('idElement')
    try:
        element = ElementListy.objects.get(idElement=id_elementu)
        element.delete()
        return Response({"success": True})
    except ElementListy.DoesNotExist:
        return Response({"success": False, "error": "Element not found"})


@api_view(['POST'])
def update_list_element_status(request, pk):
    id_elementu = request.data.get('idElement')
    zaznaczony = request.data.get('zaznaczony')

    try:
        element = ElementListy.objects.get(idElement=id_elementu)

        element.zaznaczony = zaznaczony
        element.save()

        serializer = ElementListySerializer(element)
        return Response({"success": True, "list_element": serializer.data})

    except ElementListy.DoesNotExist:
        return Response({"success": False, "error": "Element not found"})
