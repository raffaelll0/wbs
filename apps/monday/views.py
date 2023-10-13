from django.shortcuts import render
from .monday import *
from ..neapolitanmods.models import Commessa, Aziende
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def monday_data_view(request):

    # INIZIALLIZZIAMO LE TABELLE CON DEI VALORI DI DEFAULT
    table_data_commesse = []
    table_data_aziende = []
    table_data_task = []
    table_data_contratti = []
    table_data_servizi = []
    table_data_contatti = []
    table_data_fatture = []
    table_data_utenti = []

    #VENGONO CARICATI I DATI SOLO SE SI SPINGE IL BOTTONE
    if 'load_data' in request.GET:

        # DUMP DI TUTTE LE TABELLE
        table_data_commesse = fetch_mdc_commesse()
        table_data_aziende = fetch_mdc_aziende()
        table_data_task = fetch_mdc_task()
        table_data_contratti = fetch_mcd_contratti()
        table_data_servizi = fetch_mcd_servizi()
        table_data_contatti = fetch_mcd_contatti()
        table_data_fatture = fetch_mdc_fatture()
        table_data_utenti = fetch_mdc_utenti()


        # SCRITTURA
        write_utenti(table_data_utenti)

        #SCRITTURA DATI DEI MODELLI
        write_commesse(table_data_commesse)
        write_aziende(table_data_aziende)
        write_commesse(table_data_commesse)
        write_task(table_data_task)
        write_contratti(table_data_contratti)
        write_servizi(table_data_servizi)
        write_contatti(table_data_contatti)
        write_fatture(table_data_fatture)

        #COLLEGAMENTO DELLE ISTANZE TRA DUE MODELLI
        commesse_aziende_pair()
        aziende_utenti_pair()
        task_commesse_pair()
        task_utenti_pair()
        contratti_com_att_pass_pair()
        contatti_com_az_pair()
        fatt_contr_pair()



    return render(request, 'monday_data.html', {'table_data': table_data_commesse, 'table_data_aziende': table_data_aziende, 'table_data_task': table_data_task, 'table_data_contratti': table_data_contratti, 'table_data_servizi': table_data_servizi, 'table_data_contatti': table_data_contatti, 'table_data_fatture': table_data_fatture, 'table_data_utenti': table_data_utenti})

