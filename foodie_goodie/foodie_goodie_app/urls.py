from django.urls import path
from .views import main_views
from .swagger import schema_view
from foodie_goodie_app.views.main_views import wpis_list, wpis_detail, wpis_create, wpis_update, wpis_delete, add_przepis_to_jadlospis,remove_przepis,  JadlospisListView, JadlospisDetailView, JadlospisCreateView, JadlospisUpdateView,JadlospisDeleteView, JadlospisPrzepisDeleteView, pokaz_jadlospis, dodaj_przepis_do_jadlospisu, wybierz_przepis, usun_przepis_z_jadlospisu, szczegoly_jadlospisu



urlpatterns = [
    path('', main_views.home, name='home'),  # Home view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('wpisy/', wpis_list, name='wpis-list'),
    path('wpisy/<int:pk>/', wpis_detail, name='wpis-detail'),
    path('wpisy/create/', wpis_create, name='wpis-create'),
    path('wpisy/<int:pk>/update/', wpis_update, name='wpis-update'),
    path('wpisy/<int:pk>/delete/', wpis_delete, name='wpis-delete'),
    path('jadlospisy/', JadlospisListView.as_view(), name="jadlospis-list"),
    path("jadlospisy/create/", JadlospisCreateView.as_view(), name="jadlospis-create"),
    path("jadlospisy/<int:pk>/update/", JadlospisUpdateView.as_view(), name="jadlospis-update"),
    path("jadlospisy/<int:pk>/delete/", JadlospisDeleteView.as_view(), name="jadlospis-delete"),
    
    path('jadlospisy/remove/<int:jadlospis_przepis_id>/', remove_przepis, name='remove_przepis'),
    path('jadlospis/<int:jadlospis_id>/', pokaz_jadlospis, name='pokaz_jadlospis'),
    path('jadlospis/<int:jadlospis_id>/wybierz/', wybierz_przepis, name='wybierz_przepis'),
    path('jadlospis/<int:jadlospis_id>/wybierz_przepis/<int:dzienTygodnia>/<int:godzina>/', wybierz_przepis, name='wybierz_przepis_dzien_godzina'),
    path('jadlospis/<int:jadlospis_id>/dodaj_przepis/', dodaj_przepis_do_jadlospisu, name='dodaj_przepis_do_jadlospisu'),
    path('jadlospis/<int:jadlospis_id>/usun_przepis/', usun_przepis_z_jadlospisu, name='usun_przepis_z_jadlospisu'),
    path('jadlospisy/<int:jadlospis_id>/', szczegoly_jadlospisu, name='szczegoly_jadlospisu'),


]
