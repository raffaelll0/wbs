"""WB Servizi finanza agevolata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.web.sitemaps import StaticViewSitemap

from neapolitan.views import CRUDView
import apps.neapolitanmods

from apps.monday import views


sitemaps = {
    "static": StaticViewSitemap(),
}

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # redirect Django admin login to main login page
    path("admin/login/", RedirectView.as_view(pattern_name="account_login")),
    path("admin/", admin.site.urls),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("accounts/", include("allauth_2fa.urls")),
    path("accounts/", include("allauth.urls")),
    path("users/", include("apps.users.urls")),
    path("", include("apps.web.urls")),
    path("pegasus/", include("pegasus.apps.examples.urls")),
    path("pegasus/employees/", include("pegasus.apps.employees.urls")),
    path("support/", include("apps.support.urls")),
    path("celery-progress/", include("celery_progress.urls")),
    # API docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI - you may wish to remove one of these depending on your preference
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # hijack urls for impersonation
    path("hijack/", include("hijack.urls", namespace="hijack")),
    path('monday-data/', views.monday_data_view, name='monday_data'),
    #path('monday-aziende/', views.monday_data_aziende, name='monday_aziende')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

class UtenteView(CRUDView):
    model = apps.neapolitanmods.models.Utente
    fields = ["id_monday", "nome", "email", "telefono"]
urlpatterns += UtenteView.get_urls()

class CommessaView(CRUDView):
    model = apps.neapolitanmods.models.Commessa
    fields = ["id_monday", "nome", "tipologia", "ultimo_aggiornamento", "priorità", "cliente_finale"]
urlpatterns += CommessaView.get_urls()

class TaskView(CRUDView):
    model = apps.neapolitanmods.models.Task
    fields = ["id_monday", "nome", "tipo", "data_creazione", "sollecito", "responsabile", "priorità", "commesse"]
urlpatterns += TaskView.get_urls()

class ContrattiView(CRUDView):
    model = apps.neapolitanmods.models.Contratti
    fields = ["id_monday", "nome", "ultimo_aggiornamento", "data_creazione", "commesse", "sog_attivo", "sog_passivo"]
urlpatterns += ContrattiView.get_urls()

class AziendeView(CRUDView):
    model = apps.neapolitanmods.models.Aziende
    fields = ["id_monday", "nome", "responsabile", "commesse", "p_iva", "cod_fis"]
urlpatterns += AziendeView.get_urls()

class FattureView(CRUDView):
    model = apps.neapolitanmods.models.Fatture
    fields = ["id_monday", "nome", "stato", "importo", "contratto", "anno_competenza"]
urlpatterns += FattureView.get_urls()

class ServizioView(CRUDView):
    model = apps.neapolitanmods.models.Servizio
    fields = ["id_monday", "nome", "responsabile", "tipologia", "link_fonte", "documenti"]
urlpatterns += ServizioView.get_urls()

class ContattiView(CRUDView):
    model = apps.neapolitanmods.models.Contatti
    fields = ["id_monday", "nome", "in_qualita_di", "commesse", "azienda_di_appartenenza"]
urlpatterns += ContattiView.get_urls()





#riferimenti_urls
# [<URLPattern 'servizio/' [name='servizio-list']>,
# <URLPattern 'servizio/new/' [name='servizio-create']>,
# <URLPattern 'servizio/<int:pk>/' [name='servizio-detail']>,
# <URLPattern 'servizio/<int:pk>/edit/' [name='servizio-update']>,
# <URLPattern 'servizio/<int:pk>/delete/' [name='servizio-delete']>]

#riferimenti_2
# [<URLPattern 'servizio/' [name='servizio-list']>,
# <URLPattern 'servizio/new/' [name='servizio-create']>,
# <URLPattern 'servizio/<int:pk>/' [name='servizio-detail']>,
# <URLPattern 'servizio/<int:pk>/edit/' [name='servizio-update']>,
# <URLPattern 'servizio/<int:pk>/delete/' [name='servizio-delete']>]