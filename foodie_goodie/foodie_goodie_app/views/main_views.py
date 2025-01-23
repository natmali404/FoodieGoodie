from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from foodie_goodie_app.models import Wpis, Uzytkownik,  Jadlospis, JadlospisPrzepis, Przepis
from foodie_goodie_app.forms import WpisForm, JadlospisForm, JadlospisPrzepisForm
from django.shortcuts import get_object_or_404

from django.utils.timezone import now  # Import dla aktualnej daty

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# def home(request):
#     return HttpResponse("<h1>Witaj w aplikacji FoodieGoodie!</h1><p>To jest strona powitalna.</p>")

def home(request):
    return render(request, "home.html")

from django.shortcuts import render

def wpis_list(request):
    wpisy = Wpis.objects.all().order_by('-dataDodania') 
    return render(request, 'wpis_list.html', {'wpisy': wpisy})

def wpis_detail(request, pk):
    wpis = get_object_or_404(Wpis, pk=pk)
    return render(request, 'wpis_detail.html', {'wpis': wpis})

from django.shortcuts import render, redirect

def wpis_create(request):
    if request.method == 'POST':
        form = WpisForm(request.POST, request.FILES)  # Obsługa plików
        if form.is_valid():
            wpis = form.save(commit=False)
            wpis.autor = Uzytkownik.objects.get(nazwaUzytkownika='Natalia')  # Domyślny autor
            wpis.save()
            return redirect('wpis-list')
    else:
        form = WpisForm()
    return render(request, 'wpis_form.html', {'form': form})

def wpis_update(request, pk):
    wpis = get_object_or_404(Wpis, pk=pk)
    
    if request.method == 'POST':
        form = WpisForm(request.POST, request.FILES, instance=wpis)  # Include request.FILES here
        if form.is_valid():
            form.save()  # Save the updated entry (including the image)
            return redirect('wpis-list')  # Redirect to the list of posts after saving
    else:
        form = WpisForm(instance=wpis)  # Pre-fill the form with the existing data for editing
    
    return render(request, 'wpis_form.html', {'form': form})

def wpis_delete(request, pk):
    wpis = get_object_or_404(Wpis, pk=pk)
    if request.method == 'POST':
        wpis.delete()
        return redirect('wpis-list')
    return render(request, 'wpis_confirm_delete.html', {'wpis': wpis})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render

from django.shortcuts import render

def pokaz_jadlospis(request, jadlospis_id):
    jadlospis = Jadlospis.objects.get(pk=jadlospis_id)
    przepisy_jadlospisu = JadlospisPrzepis.objects.filter(jadlospis=jadlospis)
    przepisy = Przepis.objects.all()
    context = {
        'jadlospis': jadlospis,
        'przepisy_jadlospisu': przepisy_jadlospisu,
        'dni_tygodnia': JadlospisPrzepis.DZIEŃ_TYGODNIA_CHOICES,
        'pory_dnia': JadlospisPrzepis.PORA_DNIA_CHOICES,
        'przepisy' : przepisy,
    }
    return render(request, 'jadlospis.html', context)


def add_przepis_to_jadlospis(request, jadlospis_id, dzien, pora):
    jadlospis = get_object_or_404(Jadlospis, pk=jadlospis_id)
    wszystkie_przepisy = Przepis.objects.all()

    if request.method == "POST":
        przepis_id = request.POST.get("przepis_id")
        przepis = get_object_or_404(Przepis, pk=przepis_id)
        JadlospisPrzepis.objects.create(
            jadlospis=jadlospis,
            przepis=przepis,
            dzienTygodnia=dzien,
            godzina=pora
        )
        return redirect("jadlospis-detail", pk=jadlospis_id)

    return render(request, "add_przepis_form.html", {
        "jadlospis": jadlospis,
        "dzien": dzien,
        "pora": pora,
        "wszystkie_przepisy": wszystkie_przepisy
    })



def remove_przepis(request, jadlospis_przepis_id):
    jadlospis_przepis = get_object_or_404(JadlospisPrzepis, pk=jadlospis_przepis_id)
    jadlospis_id = jadlospis_przepis.jadlospis.pk
    jadlospis_przepis.delete()
    return redirect('jadlospis-detail', pk=jadlospis_id)

# Lista jadłospisów
class JadlospisListView(ListView):
    model = Jadlospis
    template_name = "jadlospis_list.html"
    context_object_name = "jadlospisy"


# Szczegóły jadłospisu
class JadlospisDetailView(DetailView):
    model = Jadlospis
    template_name = "jadlospis_detail.html"
    context_object_name = "jadlospis"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Wszystkie przepisy w bazie
        context["wszystkie_przepisy"] = Przepis.objects.all()

        # Przepisy przypisane do jadłospisu
        jadlospis = self.get_object()
        context["przepisy_jadlospisu"] = JadlospisPrzepis.objects.filter(jadlospis=jadlospis)

        # Choices dla dni tygodnia i pór dnia
        context["dzien_tygodnia_choices"] = JadlospisPrzepis.DZIEŃ_TYGODNIA_CHOICES
        context["pora_dnia_choices"] = JadlospisPrzepis.PORA_DNIA_CHOICES

        return context

    def post(self, request, *args, **kwargs):
        """Obsługa dodawania przepisu do jadłospisu"""
        jadlospis = self.get_object()
        form = self.get_form()

        if form.is_valid():
            przepis = form.cleaned_data["przepis"]
            dzien_tygodnia = form.cleaned_data["dzienTygodnia"]
            pora_dnia = form.cleaned_data["godzina"]

            JadlospisPrzepis.objects.create(
                jadlospis=jadlospis,
                przepis=przepis,
                dzienTygodnia=dzien_tygodnia,
                godzina=pora_dnia,
            )
            return redirect("jadlospis-detail", pk=jadlospis.pk)

        return self.form_invalid(form)



# Tworzenie jadłospisu

class JadlospisCreateView(CreateView):
    model = Jadlospis
    template_name = "jadlospis_form.html"
    form_class = JadlospisForm

    def form_valid(self, form):
        # Automatycznie przypisz autora (np. użytkownik Natalia)
        form.instance.autor = Uzytkownik.objects.get(nazwaUzytkownika="Natalia")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("jadlospis-list")
    
# Edycja jadłospisu
class JadlospisUpdateView(UpdateView):
    model = Jadlospis
    template_name = "jadlospis_form.html"
    form_class = JadlospisForm
    success_url = reverse_lazy("jadlospis-list")


# Usuwanie jadłospisu
class JadlospisDeleteView(DeleteView):
    model = Jadlospis
    template_name = "jadlospis_confirm_delete.html"
    success_url = reverse_lazy("jadlospis-list")


class JadlospisPrzepisDeleteView(DeleteView):
    def post(self, request, jadlospis_pk, przepis_pk):
        jadlospis_przepis = get_object_or_404(
            JadlospisPrzepis, jadlospis_id=jadlospis_pk, przepis_id=przepis_pk
        )
        jadlospis_przepis.delete()
        return redirect("jadlospis-detail", pk=jadlospis_pk)
    
from django.http import JsonResponse
from django.http import JsonResponse

def dodaj_przepis_do_jadlospisu(request, jadlospis_id):
    if request.method == 'POST':
        # Pobierz wartości z formularza
        przepis_id = request.POST.get('przepis')
        dzien_tygodnia = request.POST.get('dzienTygodnia')
        godzina = request.POST.get('godzina')

        # Sprawdź, czy wszystkie wymagane dane są obecne
        if not przepis_id or dzien_tygodnia is None or godzina is None:
            return JsonResponse({'error': 'Wszystkie pola są wymagane (przepis, dzień tygodnia, godzina)'}, status=400)

        try:
            dzien_tygodnia = int(dzien_tygodnia)
            godzina = int(godzina)

            # Sprawdź, czy wartości są poprawne
            if dzien_tygodnia not in dict(JadlospisPrzepis.DZIEŃ_TYGODNIA_CHOICES):
                return JsonResponse({'error': 'Nieprawidłowy dzień tygodnia'}, status=400)

            if godzina not in dict(JadlospisPrzepis.PORA_DNIA_CHOICES):
                return JsonResponse({'error': 'Nieprawidłowa pora dnia'}, status=400)

            # Pobierz jadłospis i przepis
            jadlospis = Jadlospis.objects.get(pk=jadlospis_id)
            przepis = Przepis.objects.get(pk=przepis_id)

            # Spróbuj utworzyć nowy obiekt
            obj, created = JadlospisPrzepis.objects.get_or_create(
                jadlospis=jadlospis,
                przepis=przepis,
                dzienTygodnia=dzien_tygodnia,
                godzina=godzina
            )

            if created:
                return JsonResponse({'przepis_nazwa': przepis.nazwaPrzepisu},  status=200)
            else:
                return JsonResponse({'error': 'Przepis dla tego dnia i pory już istnieje'}, status=400)

        except ValueError:
            return JsonResponse({'error': 'Nieprawidłowe dane (dzień tygodnia i godzina muszą być liczbami)'}, status=400)
        except Jadlospis.DoesNotExist:
            return JsonResponse({'error': 'Jadłospis nie znaleziony'}, status=404)
        except Przepis.DoesNotExist:
            return JsonResponse({'error': 'Przepis nie znaleziony'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def wybierz_przepis(request, jadlospis_id, dzienTygodnia, godzina):
    jadlospis = get_object_or_404(Jadlospis, pk=jadlospis_id)
    przepisy = Przepis.objects.all()
    print(przepisy)  
    context = {
        'jadlospis': jadlospis,
        'przepisy': przepisy,
        'dzienTygodnia': dzienTygodnia,
        'godzina': godzina,
    }
    return render(request, 'wybierz_przepis.html', context)


def usun_przepis_z_jadlospisu(request, jadlospis_id):
    if request.method == 'POST':
        # Pobierz dane z formularza
        przepis_id = request.POST.get('przepis_id')
        dzien_tygodnia = request.POST.get('dzienTygodnia')
        godzina = request.POST.get('godzina')

        # Sprawdź, czy wszystkie dane są obecne
        if not przepis_id or dzien_tygodnia is None or godzina is None:
            return JsonResponse({'error': 'Brak wymaganych danych (przepis, dzień tygodnia, godzina)'}, status=400)

        try:
            dzien_tygodnia = int(dzien_tygodnia)
            godzina = int(godzina)

            # Pobierz jadłospis i przepis
            jadlospis = Jadlospis.objects.get(pk=jadlospis_id)
            przepis = Przepis.objects.get(pk=przepis_id)

            # Spróbuj usunąć przepis z jadłospisu
            jadlospis_przepis = JadlospisPrzepis.objects.get(
                jadlospis=jadlospis,
                przepis=przepis,
                dzienTygodnia=dzien_tygodnia,
                godzina=godzina
            )
            jadlospis_przepis.delete()

            return JsonResponse({'success': 'Przepis usunięty', 'przepis_nazwa': przepis.nazwaPrzepisu}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Nieprawidłowe dane (dzień tygodnia i godzina muszą być liczbami)'}, status=400)
        except Jadlospis.DoesNotExist:
            return JsonResponse({'error': 'Jadłospis nie znaleziony'}, status=404)
        except Przepis.DoesNotExist:
            return JsonResponse({'error': 'Przepis nie znaleziony'}, status=404)
        except JadlospisPrzepis.DoesNotExist:
            return JsonResponse({'error': 'Nie znaleziono przepisu w tym jadłospisie dla wybranego dnia i godziny'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def szczegoly_jadlospisu(request, jadlospis_id):
    jadlospis = Jadlospis.objects.get(pk=jadlospis_id)
    przepisy_jadlospisu = JadlospisPrzepis.objects.filter(jadlospis=jadlospis)
    przepisy = Przepis.objects.all()
    context = {
        'jadlospis': jadlospis,
        'przepisy_jadlospisu': przepisy_jadlospisu,
        'dni_tygodnia': JadlospisPrzepis.DZIEŃ_TYGODNIA_CHOICES,
        'pory_dnia': JadlospisPrzepis.PORA_DNIA_CHOICES,
        'przepisy' : przepisy,
    }
    return render(request, 'jadlospisprzepis_detail.html', context)
        
