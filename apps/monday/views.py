from django.shortcuts import render
from .monday import *
from ..neapolitanmods.models import Commessa, Aziende  # Import the Commessa model


def monday_data_view(request):
    """

    """
    # TODO: cancella tabelle prima di iniziare a scrivere

    table_data_commesse = fetch_mdc_commesse()  # Call the function to fetch data
    table_data_aziende = fetch_mdc_aziende()
    table_data_task = fetch_mdc_task()
    table_data_contratti = fetch_mcd_contratti()
    table_data_servizi = fetch_mcd_servizi()
    table_data_contatti = fetch_mcd_contatti()

    write_aziende(table_data_aziende)
    write_commesse(table_data_commesse)
    commesse_aziende_pair()

    write_task(table_data_task)
    task_commesse_pair()

    write_contratti(table_data_contratti)
    contratti_com_att_pass_pair()

    write_servizi(table_data_servizi)

    write_contatti(table_data_contatti)
    contatti_com_az_pair()



    return render(request, 'monday_data.html', {'table_data': table_data_commesse, 'table_data_aziende': table_data_aziende, 'table_data_task': table_data_task, 'table_data_contratti': table_data_contratti, 'table_data_servizi': table_data_servizi, 'table_data_contatti': table_data_contatti})

# def monday_data_aziende(request):
#     table_data_aziende = dump_aziende()
#
#     return render(request, 'monday_aziende.html', {'table_data_aziende': table_data_aziende})

#A
#itero nei dati delle aziende
#se il campo commessa è valorizzato:
# creo commessa con nome e id_monday
# # se no passa
#creo azienda e salvo

#itero nei dati dell commesse
# get or create commessa con id _monday= x

#B
#itero nei dati delle aziende

#creo azienda con colonna "id monday commessa" e salvo

#itero nei dati dell commesse
