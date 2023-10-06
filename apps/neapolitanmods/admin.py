from django.contrib import admin

from .models import *


admin.site.register(Utente)
admin.site.register(Commessa)
admin.site.register(Task)
admin.site.register(Contratti)
admin.site.register(Aziende)
admin.site.register(Fatture)
#admin.site.register(Incassi)
admin.site.register(Servizio)
admin.site.register(Contatti)

