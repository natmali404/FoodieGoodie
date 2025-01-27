from django.contrib import admin

from foodie_goodie_app.models import *

# Register your models here.
admin.site.register(Przepis)
admin.site.register(Skladnik)
admin.site.register(SkladnikPrzepisu)
admin.site.register(Jednostka)
admin.site.register(OcenyPrzepisu)
admin.site.register(KomentarzePrzepisu)
admin.site.register(Uzytkownik)



