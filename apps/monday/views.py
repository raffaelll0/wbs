from django.shortcuts import render
from .monday import dump_mdc_to_django, dump_aziende  # Import your module with dump_mdc_to_django function
from apps.neapolitanmods.models import Commessa, Aziende  # Import the Commessa model


def monday_data_view(request):
    table_data = dump_mdc_to_django() # Call the function to fetch data
    table_data_aziende = dump_aziende()
    
    for row_az in table_data_aziende[1:]:  # Start from index 1 to skip headers
        nome_az = row_az[0]
        id_monday_az = row_az[5]

        aziende, created = Aziende.objects.get_or_create(nome=nome_az)
        aziende.id_monday = id_monday_az

        aziende.save()
    # Iterate through the data and update the Commessa model
    for row in table_data[1:]:  # Start from index 1 to skip headers
        nome = row[0]  # Assuming the name is in the first column
        id_monday = row[1]  # Assuming the id_monday is in the second column
        tipo = row[2]
        priority = row[3]
        date = row[4][0:10]
        aziende_value = row[5]

        commessa, created = Commessa.objects.get_or_create(nome=nome)
        commessa.id_monday = id_monday
        commessa.tipologia = tipo
        commessa.ultimo_aggiornamento = date

        selected_choice = None
        for choice_value, choice_label in Commessa.STATUS_PRIORITA:
            if priority == choice_label:
                selected_choice = choice_value
                break

        # Set the selected choice to the 'priorità' field
        if selected_choice is not None:
            commessa.priorità = selected_choice
        else:
            # Handle the case when the value doesn't match any choices
            pass

        try:
            aziende_instance = Aziende.objects.get(nome=aziende_value)
        except Aziende.DoesNotExist:
            aziende_instance = None

        # Create a new Commessa instance and associate it with the Aziende instance (if found)
        if aziende_instance:
            commessa.id_aziende = aziende_instance

        else:
            # Handle the case when the value doesn't match any existing Aziende instance
            pass


        commessa.save()





    return render(request, 'monday_data.html', {'table_data': table_data, 'table_data_aziende': table_data_aziende})

# def monday_data_aziende(request):
#     table_data_aziende = dump_aziende()
#
#     return render(request, 'monday_aziende.html', {'table_data_aziende': table_data_aziende})