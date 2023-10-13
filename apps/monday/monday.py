import requests
import json
import pandas as pd
import numpy as np
from tabulate import tabulate
from django.db import models
from django.db.models import Q
from ..neapolitanmods.models import *  # Import all models
from django.core.exceptions import ObjectDoesNotExist


def fetch_mdc_commesse():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data = [['NAME', 'ID', 'TIPO', 'PRIOR', 'DATA', "CLIENTE FINALE", "ID AZIENDA", "MISURA FINANZIARIA"]]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_commessa = '786045221'

    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query= ' { boards (ids: '+id_board_commessa+' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "stato_1", "dup__of_priorit_", "ultimo_aggiornamento", "cliente_1", "collega_schede9" ]) { id type value text } }  } }'
    data = {'query' : query}

    #FACCIAMO UNA RICHIESTA JSON
    r = requests.post(url=apiUrl, json=data, headers=headers)

    #DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data = r.json()
    #ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards = response_data['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board in boards:
        items = board['items']

        #PRENDIAMO I VALORI DI OGNI ITEM
        for item in items:
            #item_id = item['id']
            item_name = item['name']
            column = item['column_values']
            #print(f"Name: {item_name}")
            #print(f"ID: {item_id}, Name: {item_name}")

            #ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row = [item_name]

            #PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values in column:
                value_text = values['text']
                value_id = values['id']
                value = values['value']
                #print(f"TEXT: {value_text}")

                #SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id in ["id_elemento", "stato_1", "dup__of_priorit_", "ultimo_aggiornamento", "cliente_1", "collega_schede9"]:
                    row.append(value_text)

                    #print(f"Processing value_id: {value_id}, value: {value}")

                    if value_id == "cliente_1" and value is not None:
                        try:
                            # Parse the JSON string in 'value_text'
                            data = json.loads(value)
                            #print("Parsed JSON data:", data)

                            if "linkedPulseIds" in data:
                                linked_pulse_ids = data["linkedPulseIds"]

                                if linked_pulse_ids:
                                    linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")
                                    #print("Linked Pulse ID: ", linked_pulse_id)
                                    row.append(linked_pulse_id)

                        except json.JSONDecodeError:
                            pass
                    else:
                        pass

            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data.append(row)
    return table_data
    #FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA
    #print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

def fetch_mdc_aziende():
    # AZIENDE
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_aziende = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_aziende = "https://api.monday.com/v2"
    headers_aziende = {"Authorization": apiKey_aziende}

    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_aziende = [['NAME', 'RESPONSABILE', 'ID RESPONSABILE', "COMMESSE", "ID COMMESSA", "PARTITA IVA", "CODICE FISCALE",  "ID"]]

    # CODICE DELLA BOARD DI NOME LISTA CLIENTI
    id_board_aziende = '813707989'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_aziende = ' { boards (ids: ' + id_board_aziende + ' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "persone", "link_to_attivit_", "p_iva1", "testo9", "collega_schede0"]) { id type value text } }  } }'
    data_aziende = {'query': query_aziende}

    # FACCIAMO UNA RICHIESTA JSON
    r_aziende = requests.post(url=apiUrl_aziende, json=data_aziende, headers=headers_aziende)

    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_aziende = r_aziende.json()
    # ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_aziende = response_data_aziende['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_aziende in boards_aziende:
        items_aziende = board_aziende['items']

        # PRENDIAMO I VALORI DI OGNI ITEM
        for item_aziende in items_aziende:
            item_name_aziende = item_aziende['name']
            column_aziende = item_aziende['column_values']

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_aziende = [item_name_aziende]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_aziende in column_aziende:
                value_text_aziende = values_aziende['text']
                value_id_aziende = values_aziende['id']
                value_aziende = values_aziende['value']


                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_aziende in ["id_elemento", "persone", "link_to_attivit_", "p_iva1", "testo9", "collega_schede0"]:
                    row_aziende.append(value_text_aziende)

                    linked_pulse_ids = []

                    # Process linked pulse IDs
                    if value_id_aziende == "link_to_attivit_":
                        linked_pulse_id = None
                        if value_aziende is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_aziende = json.loads(value_aziende)

                                if "linkedPulseIds" in data_aziende:
                                    linked_pulse_ids = [linked_pulse.get("linkedPulseId") for linked_pulse in data_aziende["linkedPulseIds"]]
                                    id_list_str = ', '.join(map(str, linked_pulse_ids))
                                    row_aziende.append(id_list_str)

                                else:
                                    row_aziende.append(None)

                            except json.JSONDecodeError:

                                pass
                        else:
                            row_aziende.append(None)


                    if value_id_aziende == "persone":
                        if value_aziende is not None:
                            persone_data = json.loads(value_aziende)
                            if "personsAndTeams" in persone_data:
                                id_list = [person_info.get("id") for person_info in persone_data["personsAndTeams"]]
                                # Convert the list of IDs to a comma-separated string
                                id_list_str = ', '.join(map(str, id_list))
                                row_aziende.append(id_list_str)
                            else:
                                row_aziende.append(None)
                        else:
                            row_aziende.append(None)


            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_aziende.append(row_aziende)
    return table_data_aziende

def fetch_mdc_task():
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_task = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_task = "https://api.monday.com/v2"
    headers_task = {"Authorization": apiKey_task}

    # TASK
    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_task = [['NAME', 'TIPO', "PRIORITA'", 'DATA CREAZIONE', "DATA SOLLECITO", "RESPONSABILE", "ID RESPONSABILE", "COMMESSA", 'ID COMMESSA', 'ID']]

    # CODICE DELLA BOARD DI NOME SPORTELLO STUDIO
    id_board_task = '985523481'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_task = ' { boards (ids: ' + id_board_task + ' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "stato_19", "registro_di_creazione8", "data", "persone", "priorit_", "collega_schede", "collega_schede" ]) { id type value text } }  } }'
    data_task = {'query': query_task}

    # FACCIAMO UNA RICHIESTA JSON
    r_task = requests.post(url=apiUrl_task, json=data_task, headers=headers_task)

    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_task = r_task.json()
    #print(r_task.json())

    # ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_task = response_data_task['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_task in boards_task:
        items_task = board_task['items']

        # PRENDIAMO I VALORI DI OGNI ITEM
        for item_task in items_task:
            # item_id_task = item_task['id']
            item_name_task = item_task['name']
            column_task = item_task['column_values']


            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_task = [item_name_task]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_task in column_task:
                value_text_task = values_task['text']
                value_id_task = values_task['id']
                value_task = values_task['value']

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if values_task['id'] in ["id_elemento", "stato_19", "registro_di_creazione8", "data", "persone", "priorit_", "collega_schede"]:
                    row_task.append(values_task['text'])

                    if value_id_task == "collega_schede":
                        linked_pulse_ids = []  # Initialize an empty list to store pulseIds

                        if value_task is not None:
                            try:
                                data_task = json.loads(value_task)

                                if "linkedPulseIds" in data_task:
                                    linked_pulse_ids = data_task["linkedPulseIds"]

                            except json.JSONDecodeError:
                                pass

                        # Concatenate the pulseIds into a comma-separated string
                        pulse_id_str = ",".join(
                            str(linked_pulse.get("linkedPulseId")) for linked_pulse in linked_pulse_ids)
                        row_task.append(pulse_id_str)
                    else:
                        pass


                    if value_id_task == "persone" and value_task is not None:
                        persone_data = json.loads(value_task)
                        if "personsAndTeams" in persone_data:
                            id_list = [person_info.get("id") for person_info in persone_data["personsAndTeams"]]
                            row_task.extend(id_list)
                    elif value_id_task == "persone" and value_task is None:
                        # Handle the case when 'value_task' is None, you can append a default value or handle it as needed
                        row_task.append(None)


            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_task.append(row_task)

    return table_data_task

def fetch_mcd_contratti():
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_contratti = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_contratti = "https://api.monday.com/v2"
    headers_contratti = {"Authorization": apiKey_contratti}


    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_contratti = [['NAME', 'ULTIMO AGGIORNAMENTO', 'DATA CREAZIONE', "COMMESSA", "ID COMMESSA", "SOGGETTO ATTIVO", "ID ATTIVO ", "SOGGETTO PASSIVO", "ID PASSIVO", "ID MONDAY"]]

    # CODICE DELLA BOARD DI NOME SPORTELLO STUDIO
    id_board_contratti = '1641120827'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_contratti = ' { boards (ids: ' + id_board_contratti + ') { items (limit:10) { id  name column_values (ids: ["id_elemento0", "ultimo_aggiornamento", "registro_di_creazione_1", "collega_schede7", "collega_schede", "collega_schede0"]) { id type value text } }  } }'
    data_contratti = {'query': query_contratti}

    # FACCIAMO UNA RICHIESTA JSON
    r_contratti = requests.post(url=apiUrl_contratti, json=data_contratti, headers=headers_contratti)

    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_contratti = r_contratti.json()

    # ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_contratti = response_data_contratti['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_contratti in boards_contratti:
        items_contratti = board_contratti['items']

        # PRENDIAMO I VALORI DI OGNI ITEM
        for item_contratti in items_contratti:
            item_id_contratti = item_contratti['id']
            item_name_contratti = item_contratti['name']
            column_contratti = item_contratti['column_values']

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_contratti = [item_name_contratti]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_contratti in column_contratti:
                value_text_contratti = values_contratti['text']
                value_id_contratti = values_contratti['id']
                value_contratti = values_contratti['value']


                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_contratti in ["id_elemento0", "ultimo_aggiornamento", "registro_di_creazione_1", "collega_schede7", "collega_schede", "collega_schede0"]:
                    row_contratti.append(values_contratti['text'])

                    #ID COMMESSA
                    # Process linked pulse IDs
                    if value_id_contratti == "collega_schede7":
                        linked_pulse_id = None
                        if value_contratti is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_contratti= json.loads(value_contratti)

                                if "linkedPulseIds" in data_contratti:
                                    linked_pulse_ids = [linked_pulse.get("linkedPulseId") for linked_pulse in data_contratti["linkedPulseIds"]]
                                    id_list_str = ', '.join(map(str, linked_pulse_ids))
                                    row_contratti.append(id_list_str)

                                else:
                                    row_contratti.append(None)

                            except json.JSONDecodeError:

                                pass
                        else:
                            row_contratti.append(None)

                    #ID PARTE ATTIVA
                    if value_id_contratti == "collega_schede":
                        linked_pulse_id = None
                        if value_contratti is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_contratti = json.loads(value_contratti)

                                if "linkedPulseIds" in data_contratti:
                                    linked_pulse_ids = data_contratti["linkedPulseIds"]

                                    if linked_pulse_ids:
                                        linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")

                            except json.JSONDecodeError:
                                pass
                        row_contratti.append(linked_pulse_id)
                    else:
                        pass

                    #ID PARTE PASSIVA
                    if value_id_contratti == "collega_schede0":
                        linked_pulse_id = None
                        if value_contratti is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_contratti = json.loads(value_contratti)

                                if "linkedPulseIds" in data_contratti:
                                    linked_pulse_ids = data_contratti["linkedPulseIds"]

                                    if linked_pulse_ids:
                                        linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")

                            except json.JSONDecodeError:
                                pass
                        row_contratti.append(linked_pulse_id)
                    else:
                        pass


            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_contratti.append(row_contratti)

    return table_data_contratti

def fetch_mcd_servizi():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_servizi = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_servizi = "https://api.monday.com/v2"
    headers_servizi = {"Authorization": apiKey_servizi}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_servizi = [['NAME', 'UTENTE', 'ID UTENTE', 'TIPOLOGIA', 'LINK FONTE', 'DOCUMENTI', 'ID']]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_servizi= '937015673'



    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_servizi= ' { boards (ids: '+id_board_servizi+' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "persone", "stato_1", "link", "file"]) { id type value text } }  } }'
    data_servizi = {'query' : query_servizi}

    #FACCIAMO UNA RICHIESTA JSON
    r_servizi = requests.post(url=apiUrl_servizi, json=data_servizi, headers=headers_servizi)

    #DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_servizi = r_servizi.json()
    #ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_servizi = response_data_servizi['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_servizi in boards_servizi:
        items_servizi = board_servizi['items']

        #PRENDIAMO I VALORI DI OGNI ITEM
        for item_servizi in items_servizi:
            item_name_servizi = item_servizi['name']
            column_servizi = item_servizi['column_values']


            #ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_servizi = [item_name_servizi]

            #PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_servizi in column_servizi:
                value_text_servizi = values_servizi['text']
                value_id_servizi = values_servizi['id']
                value_servizi = values_servizi['value']


                #SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_servizi in ["id_elemento", "persone", "stato_1", "link", "file"]:
                    row_servizi.append(value_text_servizi)

                    if value_id_servizi == "persone":
                        if value_servizi is not None:
                            persone_data = json.loads(value_servizi)
                            if "personsAndTeams" in persone_data:
                                id_list = [person_info.get("id") for person_info in persone_data["personsAndTeams"]]
                                # Convert the list of IDs to a comma-separated string
                                id_list_str = ', '.join(map(str, id_list))
                                row_servizi.append(id_list_str)
                            else:
                                row_servizi.append(None)
                        else:
                            row_servizi.append(None)

            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_servizi.append(row_servizi)
    return table_data_servizi

def fetch_mcd_contatti():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_contatti = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_contatti = "https://api.monday.com/v2"
    headers_contatti = {"Authorization": apiKey_contatti}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_contatti = [['NAME', 'IN QUALITA DI', 'AZIENDE', 'ID AZIENDE', 'COMMESSE', 'ID COMMESSE', 'ID MONDAY']]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_contatti= '1986160544'



    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_contatti= ' { boards (ids: '+id_board_contatti+' ) { items (limit:10) { id  name column_values (ids: ["text0", "collega_schede3", "collega_schede4", "id_elemento"]) { id type value text } }  } }'
    data_contatti = {'query' : query_contatti}

    #FACCIAMO UNA RICHIESTA JSON
    r_contatti = requests.post(url=apiUrl_contatti, json=data_contatti, headers=headers_contatti)
    #DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_contatti = r_contatti.json()
    #ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_contatti = response_data_contatti['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_contatti in boards_contatti:
        items_contatti = board_contatti['items']

        #PRENDIAMO I VALORI DI OGNI ITEM
        for item_contatti in items_contatti:
            item_name_contatti = item_contatti['name']
            column_contatti = item_contatti['column_values']


            #ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_contatti = [item_name_contatti]

            #PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_contatti in column_contatti:
                value_text_contatti = values_contatti['text']
                value_id_contatti = values_contatti['id']
                value_contatti = values_contatti['value']


                #SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_contatti in ["text0", "collega_schede3", "collega_schede4", "id_elemento"]:
                    row_contatti.append(value_text_contatti)

                    if value_id_contatti == "collega_schede3":
                        linked_pulse_ids = []
                        if value_contatti is not None:
                            try:
                                data_contatti = json.loads(value_contatti)

                                if "linkedPulseIds" in data_contatti:
                                    linked_pulse_ids = [linked_pulse.get("linkedPulseId") for linked_pulse in
                                                        data_contatti["linkedPulseIds"]]

                            except json.JSONDecodeError:
                                pass

                        id_list_str = ', '.join(map(str, linked_pulse_ids))
                        row_contatti.append(id_list_str)
                    else:
                        pass


                    if value_id_contatti == "collega_schede4":
                        linked_pulse_ids = []
                        if value_contatti is not None:
                            try:
                                data_contatti = json.loads(value_contatti)

                                if "linkedPulseIds" in data_contatti:
                                    linked_pulse_ids = [linked_pulse.get("linkedPulseId") for linked_pulse in
                                                        data_contatti["linkedPulseIds"]]

                            except json.JSONDecodeError:
                                pass

                        id_list_str = ', '.join(map(str, linked_pulse_ids))
                        row_contatti.append(id_list_str)
                    else:
                        pass


            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_contatti.append(row_contatti)
    return table_data_contatti

def fetch_mdc_fatture():
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_fatture = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_fatture = "https://api.monday.com/v2"
    headers_fatture = {"Authorization": apiKey_fatture}

    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_fatture = [['NAME', 'IMPORTO', 'STATO PAGAMENTO', 'CONTRATTO', 'ID CONTRATTO', 'ANNO COMPETENZA', 'ID MONDAY']]

    # CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_fatture = '952669855'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_fatture = ' { boards (ids: ' + id_board_fatture + ' ) { items (limit:10) { id  name column_values (ids: ["name", "id_elemento", "collega_schede", "stato_1", "cliente_1", "collega_schede9", "sotto_elementi_importo0", "sotto_elementi_stato_pagamento_incasso" ]) { id type value text } }  } }'
    data_fatture = {'query': query_fatture}

    # FACCIAMO UNA RICHIESTA JSON
    r_fatture = requests.post(url=apiUrl_fatture, json=data_fatture, headers=headers_fatture)
    # print(r_fatture.json())
    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_fatture = r_fatture.json()
    # ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_fatture = response_data_fatture['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_fatture in boards_fatture:
        items_fatture = board_fatture['items']

        # PRENDIAMO I VALORI DI OGNI ITEM
        for item_fatture in items_fatture:
            item_name_fatture = item_fatture['name']
            column_fatture = item_fatture['column_values']

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_fatture = [item_name_fatture]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_fatture in column_fatture:
                value_text_fatture = values_fatture['text']
                value_id_fatture = values_fatture['id']
                value_fatture = values_fatture['value']

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_fatture in ["name", "id_elemento", "collega_schede", "stato_1", "cliente_1", "collega_schede9", "sotto_elementi_importo0", "sotto_elementi_stato_pagamento_incasso"]:
                    row_fatture.append(value_text_fatture)

                    if value_id_fatture == "collega_schede":
                        linked_pulse_id = None
                        if value_fatture is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_fatture = json.loads(value_fatture)

                                if "linkedPulseIds" in data_fatture:
                                    linked_pulse_ids = data_fatture["linkedPulseIds"]

                                    if linked_pulse_ids:
                                        linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")

                            except json.JSONDecodeError:
                                pass
                        row_fatture.append(linked_pulse_id)
                    else:
                        pass

            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_fatture.append(row_fatture)
    return table_data_fatture

def fetch_mdc_utenti():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_utenti = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_utenti = "https://api.monday.com/v2"
    headers_utenti = {"Authorization": apiKey_utenti}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_utenti = [['NAME', 'EMAIL','ID']]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_utenti = '952669855'



    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_utenti= ' {users(limit: 10) {    name email  id   }  }'
    data_utenti = {'query' : query_utenti}


    #FACCIAMO UNA RICHIESTA JSON
    r_utenti = requests.post(url=apiUrl_utenti, json=data_utenti, headers=headers_utenti)
    #DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_utenti = r_utenti.json()
    #print(response_data_utenti)

    #ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO USERS
    users = response_data_utenti['data']['users']

    for user in users:
        name_utenti = user['name']
        email_utenti = user['email']
        id_utenti = user['id']

        # Create a row and append the values
        row_utenti = [name_utenti, email_utenti, id_utenti]

        # Append the row to the table data
        table_data_utenti.append(row_utenti)

    return table_data_utenti




def write_utenti(table_data_utenti):

    #CLASSIFICAZIONE DEI SINGOLI DATI PER ROW
    for row_utenti in table_data_utenti[1:]:  # Start from index 1 to skip headers
        nome_utenti = row_utenti[0]
        email_utenti = row_utenti[1]
        id_utenti = row_utenti[2]

    #ASSEGNAZIONE DATI NELL'ISTANZA
        utenti_instance, created = Utente.objects.get_or_create(nome=nome_utenti,
                                                               email=email_utenti,
                                                               id_monday=id_utenti)

        utenti_instance.save()



def write_aziende(table_data_aziende):
    """
    Function which gets table_data of aziende, iterate through them and saves them in django db

    Args:
        -table_data_aziende: table data of aziende fetche from monday.com

    """

    #CLASSIFICAZIONE DEI SINGOLI DATI PER ROW
    for row_az in table_data_aziende[1:]:  # Start from index 1 to skip headers
        #mappo variabili
        nome_az = row_az[0]
        id_responsabile = row_az[2]
        id_commessa_az = row_az[4]
        p_iva_az = row_az[5]
        cod_fis_az = row_az[6]
        id_monday_az = row_az[7]

        #CONTROLLO DATI VUOTI
        if p_iva_az != '':
            try:
                #PROVA A CONVERTIRE p_iva_az IN FORMATO NUMERICO (e.g., int or float)
                p_iva_az = int(p_iva_az)  # PUOI USARE int() or float() DIPENDE DAL TIPO DI DATI
            except ValueError:
                #GESTISCI IL CASO IN CUI p_iva_az NON E' UN NUMERO VALIDO
                p_iva_az = None
        else:
            p_iva_az = None

        if id_monday_az:
            try:
                id_monday_az = int(id_monday_az)
            except ValueError:
                continue

        #CONTROLLA SE id_responsabile NON E' None PRIMA DEL SPLIT
        if id_responsabile is not None:
            #CONVERTI p_iva_az IN FORMATO NUMERICO (e.g., int or float)
            id_responsabile_list = [int(id) for id in id_responsabile.split(",")]

        else:
            id_responsabile_list = []  #O QUALUNQUE VALORE DI DEFAULT


        # CONTROLLA SE id_commessa_az  NON E' None PRIMA DEL SPLIT
        if id_commessa_az is not None:
            #CONVERTI p_iva_az IN FORMATO NUMERICO (e.g., int or float)
            id_commessa_az_list = [int(id) for id in id_commessa_az.split(",")]

        else:

            id_commessa_az_list = []  #O QUALUNQUE VALORE DI DEFAULT


        #ASSEGNAZIONE DATI NELL'ISTANZA
        a, created = Aziende.objects.get_or_create(nome=nome_az,
                                                   id_monday=id_monday_az,
                                                   cod_fis=cod_fis_az,
                                                   p_iva=p_iva_az
                                                   #id_utente=id_responsabile
                                                   )

        #AGGIUNGI UTENTE FILTRANDO GLI ID  (ManyToMany-field)
        for utente_id in id_responsabile_list:
            try:
                responsabile = Utente.objects.get(id_monday=utente_id)
                a.responsabile.add(responsabile)
            except ObjectDoesNotExist:
                # Handle the case where the Utente doesn't exist
                # You can log an error, skip, or take other appropriate actions
                pass


        #AGGIUNGI COMMESSA FILTRANDO GLI ID  (ManyToMany-field)
        for com_id in id_commessa_az_list:
            try:
                com = Commessa.objects.get(id_monday=com_id)
                a.commesse.add(com)
            except ObjectDoesNotExist:
                 # Handle the case where the Utente doesn't exist
                # You can log an error, skip, or take other appropriate actions
                pass

        #SALVA L'ISTANZA
        a.save()



def write_commesse(table_data_commesse):
    """
    Function which gets table_data of commesse, iterate through them and saves them in django db

    Args:
        -table_data_commesse: table data of commesse fetched from monday.com

    """
    #CLASSIFICAZIONE DEI SINGOLI DATI PER ROW
    for row in table_data_commesse[1:]:  # Start from index 1 to skip headers
        nome = row[0]
        id_monday = row[1]
        tipo = row[2]
        priority = row[3]
        date = row[4][0:10]
        aziende_name = row[5]
        aziende_value = row[6]

        #CONTROLLO DATI VUOTI
        if aziende_value != '':
            try:
                #CONVERTI IN INT
                aziende_value = int(aziende_value)
            except ValueError:
                #GESTISCI QUANDO NON E' UN NUMERO VALIDO
                continue
        else:
            continue

        # CONTROLLO ESISTENZA VALORE
        if id_monday:
            try:
                # CONVERTI IN INT
                id_monday = int(id_monday)
            except ValueError:
                # GESTISCI QUANDO NON E' UN NUMERO VALIDO
                continue

##########################################################################################

        # ASSEGNAZIONE DATI NELL'ISTANZA
        c, created = Commessa.objects.get_or_create(nome=nome,
                                                     id_monday=id_monday,
                                                     tipologia=tipo,
                                                     ultimo_aggiornamento=date,
                                                     priorità=priority,
                                                     id_azienda=aziende_value)
        c.save()



def commesse_aziende_pair():

    #ITERIAMO TUTTE LE ISTANZE IN AZIENDA
    for aziende_instance in Aziende.objects.all():

        id_commessa_az = aziende_instance.id_commessa

        #CONTROLLA SE id_commessa_az NON E' None
        if id_commessa_az is not None:
            # TROVA LA Commessa  TRAMITE FILTRAGGIO DI ID
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_az).first()

            # SE L'ISTANZA Commessa E' TROVATA , ASSEGNA AL CAMPO commesse DI Aziende
            if matching_commessa is not None:
                aziende_instance.commesse.add(matching_commessa)
                aziende_instance.save()

###########################################################################################################

    #ASSEGNAZIONE DI UNA VARIABILE DI TUTTE LE ISTANZE IN COMMESSA
    commesse = Commessa.objects.all()

    #ITERIAMO LE COMMESSE
    for commessa in commesse:
        id_azienda = commessa.id_azienda

    #CONTROLLO L'ESISTENZA DI id_azienda
        if id_azienda:
            #CERCHIAMO AZIENDE CON ID UGUALE
            matching_aziende = Aziende.objects.filter(id_monday=id_azienda).first()

            if matching_aziende:
                #ASSEGNAZIONE DELL'AZIENDA TROVATA AL CAMPO cliente_finale DI Commessa
                commessa.cliente_finale = matching_aziende
                commessa.save()



def aziende_utenti_pair():

    #ASSEGNAZIONE DI UNA VARIABILE DI TUTTE LE ISTANZE IN AZIENDA
    aziende = Aziende.objects.all()

    # ITERIAMO LE AZIENDE
    for azienda in aziende:
        id_responsabile = azienda.id_utente

        #VERIFICHIAMO L'ESISTENZA DI id_responsabile
        if id_responsabile:
            #CERCHIAMO UTENTI CHE HANNO ID UGUALI
            matching_utente = Utente.objects.filter(id_monday=id_responsabile).first()

            if matching_utente:
                # ASSEGNIAMO GLI UTENTI CHE COMBACIANO AL CAMPO RESPONSABILE DI AZIENDE
                azienda.responsabile = matching_utente
                azienda.save()



def write_task(table_data_task):

    """
        Function which gets table_data of task, iterate through them and saves them in django db

        Args:
            -table_data_task: table data of task fetched from monday.com

        """
    #CLASSIFICAZIONE DEI SINGOLI DATI PER ROW
    for row_task in table_data_task[1:]:  # Start from index 1 to skip headers
        nome_task = row_task[0]
        tipo_task = row_task[1]
        priorita_task = row_task[2]
        data_creazione_task = row_task[3][0:10]
        data_sollecito_task = row_task[4][0:10]
        responsabile_task = row_task[5]
        id_responsabile = row_task[6]
        id_commessa_task = row_task[8]
        id_task = row_task[9]


    #FILTRIAMO LE COMBINAZIONI DI VALORI ES: [1234, 4321]
        if id_commessa_task is not None and id_commessa_task.strip():  # CONTROLLA SE ESISTE E SE NON E' VUOTO
            #CONVERTI id_commessa_task IN LISTA INT
            id_commessa_task_list = [int(id) for id in id_commessa_task.split(",")]

    #ALTRIMENTI LA LISTA SARA' VUOTA
        else:
            id_commessa_task_list = []  #O VALORE DEFAULT


    #CREAZIONE DELL'ISTANZA E ASSEGNAZIONE VALORI
        t, created = Task.objects.get_or_create(nome=nome_task,
                                                id_monday=id_task,
                                                tipo=tipo_task,
                                                data_creazione=data_creazione_task,
                                                sollecito=data_sollecito_task,
                                                priorità=priorita_task,
                                                id_utente=id_responsabile
                                                )


        #ITERIAMO GLI ID DELLA LISTA E PROVIAMO AD AGGIUNGERLI
        for com_id in id_commessa_task_list:
            try:
                com = Commessa.objects.get(id_monday=com_id)
                t.commesse.add(com)
            except ObjectDoesNotExist:
                pass

        #SALVIAMO L'ISTANZA
        t.save()



def task_commesse_pair():

    #ITERIAMO LE ISTANZE
    for task_instance in Task.objects.all():

        id_commessa_task = task_instance.id_commessa

        #CONTROLLA SE id_commessa_az NON E' None
        if id_commessa_task is not None:
            #CERCHIAMO LA Commessa CON ID UGUALE
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_task).first()

            #SE L'ISTANZA Commessa E' TROVATA, AGGIUNGI AL CAMPO commesse DI Aziende
            if matching_commessa is not None:
                task_instance.commesse.add(matching_commessa)
                task_instance.save()



def task_utenti_pair():

    #ASSEGNAZIONE DI TUTTE LE ISTANZE TRAMITE VARIABILE
    tasks = Task.objects.all()

    #ITERO ISTANZE CONTROLLO GLI ID E AGGIUNGO
    for task in tasks:
        id_responsabile = task.id_utente

        if id_responsabile:
            # Find the matching Aziende instance by id_monday
            matching_utente = Utente.objects.filter(id_monday=id_responsabile).first()

            if matching_utente:
                # Assign the matching Aziende instance to the cliente_finale field of the Commessa instance
                task.responsabile = matching_utente
                task.save()



def write_contratti(table_data_contratti):

    #ASSEGNAZIONE VALORI A ROW
    for row_contratti in table_data_contratti[1:]:  # Start from index 1 to skip headers
        nome_contratti = row_contratti[0]
        ultimo_aggiornamento_contratti = row_contratti[1][0:10]
        data_creazione_contratti = row_contratti[2][0:10]
        id_commessa_contratti = row_contratti[4]
        id_attivo_contratti = row_contratti[6]
        id_passivo_contratti = row_contratti[8]
        id_contratti = row_contratti[9]

        # CONTROLLA SE id_commessa_az  NON E' None PRIMA DEL SPLIT
        if id_commessa_contratti is not None:
            # CONVERTI p_iva_az IN FORMATO NUMERICO (e.g., int or float)
            id_commessa_contratti_list = [int(id) for id in id_commessa_contratti.split(",")]

        else:

            id_commessa_contratti_list = []  # O QUALUNQUE VALORE DI DEFAULT

    #CREAZIONE DELL'ISTANZA E ASSEGNAZIONE VALORI
        contratti_instance, created = Contratti.objects.get_or_create(nome=nome_contratti,
                                                                      id_monday=id_contratti,
                                                                      ultimo_aggiornamento=ultimo_aggiornamento_contratti,
                                                                      data_creazione=data_creazione_contratti,
                                                                      #id_commessa=id_commessa_contratti,
                                                                      id_attivo=id_attivo_contratti,
                                                                      id_passivo=id_passivo_contratti)

        # AGGIUNGI COMMESSA FILTRANDO GLI ID  (ManyToMany-field)
        for com_id in id_commessa_contratti_list:
            try:
                com = Commessa.objects.get(id_monday=com_id)
                contratti_instance.commesse.add(com)
            except ObjectDoesNotExist:
                pass

    #SALVATAGGIO ISTANZA
        contratti_instance.save()



def contratti_com_att_pass_pair():

    #ITERAZIONE ISTANZE FILTRAGGIO ID UGUALI ED ASSEGNAZIONE
    for contratti_instance in Contratti.objects.all():

        id_commessa_contratti = contratti_instance.id_commessa

        # Check if id_commessa_az is not None
        if id_commessa_contratti is not None:
            # Find the matching Commessa instance based on id_monday
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_contratti).first()

            # If a matching Commessa instance is found, assign it to commesse field of Aziende
            if matching_commessa is not None:
                contratti_instance.commesse.add(matching_commessa)
                contratti_instance.save()


    #CREAZIONE DI UNA VARIABILE CON TUTTE LE ISTANZE
    contratti = Contratti.objects.all()

    #ITERAZIONE DELLE ISTANZE CONTROLLO ID E ASSEGNAZIONE AZIENDA ATTIVA
    for contratto in contratti:
        id_attivo = contratto.id_attivo

        if id_attivo:
            # Find the matching Aziende instance by id_monday
            matching_attivo = Aziende.objects.filter(id_monday=id_attivo).first()

            if matching_attivo:
                # Assign the matching Aziende instance to the cliente_finale field of the Commessa instance
                contratto.sog_attivo = matching_attivo
                contratto.save()

    # ITERAZIONE DELLE ISTANZE CONTROLLO ID E ASSEGNAZIONE AZIENDA PASSIVA
    for contratto in contratti:
        id_passivo = contratto.id_passivo

        if id_passivo:
            # Find the matching Aziende instance by id_monday
            matching_passivo = Aziende.objects.filter(id_monday=id_passivo).first()

            if matching_passivo:
                # Assign the matching Aziende instance to the cliente_finale field of the Commessa instance
                contratto.sog_passivo = matching_passivo
                contratto.save()



def write_servizi(table_data_servizi):

    #ASSEGNAZIONE VALORI A ROW
    for row_servizi in table_data_servizi[1:]:  # Start from index 1 to skip headers
        nome_servizi = row_servizi[0]
        tipo_servizi = row_servizi[3]
        link_servizi = row_servizi[4]
        documenti_servizi = row_servizi[5]
        id_servizi = row_servizi[6]
        id_responsabile = row_servizi[2]

        #CONTROLLO VALORI VUOTI PRIMA DI SPLIT
        if id_responsabile is not None:
            #CONVERTO IN INT
            id_responsabile_list = [int(id) for id in id_responsabile.split(",")]
        else:
            id_responsabile_list = []  #O VALORE DEFAULT


        #CREAZIONE ISTANZA CON ASSEGNAZIONE VALORI
        servizi_instance, created = Servizio.objects.get_or_create(nome=nome_servizi,
                                                              tipologia=tipo_servizi,
                                                              link_fonte=link_servizi,
                                                              documenti=documenti_servizi,
                                                              id_monday=id_servizi
                                                              )

        #ITERO VALORI MULTIPLI DALLA LISTA E AGGIUNGO
        for utente_id in id_responsabile_list:
            try:
                responsabile = Utente.objects.get(id_monday=utente_id)
                servizi_instance.responsabile.add(responsabile)
            except ObjectDoesNotExist:
                pass

        #SALVO ISTANZA
        servizi_instance.save()



def write_contatti(table_data_contatti):

    #ASSEGNAZIONE VALORI A ROW
    for row_contatti in table_data_contatti[1:]:  # Start from index 1 to skip headers
        nome_contatti = row_contatti[0]
        qualita_contatti = row_contatti[1]
        id_aziende_contatti = row_contatti[3]
        id_commesse_contatti = row_contatti[5]
        id_contatti = row_contatti[6]

    #CONTROLLO VALORI SE ESISTONO E SE NON VUOTI PRIMA DI SPLIT
        if id_commesse_contatti is not None and id_commesse_contatti.strip():
            #CONVERTI IN INT
            id_commesse_contatti_list = [int(id) for id in id_commesse_contatti.split(",")]
        else:
            id_commesse_contatti_list = []  #O VALORE DEFAULT



        if id_aziende_contatti is not None and id_aziende_contatti.strip():
            #CONVERTI IN INT
            id_aziende_contatti_list = [int(id) for id in id_aziende_contatti.split(",")]
        else:
            id_aziende_contatti_list = []  #O VALORE DEFAULT



    #CREAZIONE ISTANZA E ASSEGNAZIONE VALORI
        contatti_instance, created = Contatti.objects.get_or_create(nome=nome_contatti,
                                                                    in_qualita_di=qualita_contatti,
                                                                    #id_azienda=id_aziende_contatti,
                                                                    #id_commessa=id_commesse_contatti,
                                                                    id_monday=id_contatti
                                                                    )

        #ITERO DATI LISTA UTENTI E PROVO AD ASSEGNARE
        for com_id in id_commesse_contatti_list:
            try:
                com = Commessa.objects.get(id_monday=com_id)
                contatti_instance.commesse.add(com)

            except ObjectDoesNotExist:
                pass


        #ITERO DATI LISTA AZIENDE E PROVO AD ASSEGNARE
        for az_id in id_aziende_contatti_list:
            try:
                az = Aziende.objects.get(id_monday=az_id)
                contatti_instance.azienda_di_appartenenza.add(az)

            except ObjectDoesNotExist:
                pass

        #SALVO ISTANZA
        contatti_instance.save()



def contatti_com_az_pair():

    #ITERO ISTANZE CONTROLLO ID UGUALE E ASSEGNO COMMESSA
    for contatti_instance in Contatti.objects.all():

        id_commessa_contatti = contatti_instance.id_commessa

        #CONTROLLO SE id_commessa_az NON E' None
        if id_commessa_contatti is not None:
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_contatti).first()

            #SE L'ISTANZA Commessa E' TROVATA,ASSEGNA AL CAMPO commesse DI Aziende
            if matching_commessa is not None:
                contatti_instance.commesse.add(matching_commessa)
                contatti_instance.save()

        contatti = Contatti.objects.all()

        #ITERO ISTANZE CONTROLLO ID UGUALE E ASSEGNO COMMESSA
        for contatto in contatti:
            id_azienda = contatto.id_azienda

            if id_azienda:
                matching_azienda = Aziende.objects.filter(id_monday=id_azienda).first()

                if matching_azienda:
                    contatto.azienda_di_appartenenza = matching_azienda
                    contatto.save()



def write_fatture(table_data_fatture):

    #ASSEGNO VALORI A ROW
    for row_fatture in table_data_fatture[1:]:  # Start from index 1 to skip headers
        nome_fatture = row_fatture[0]
        importo_fatture = row_fatture[1]
        stato_fatture = row_fatture[2]
        id_commmessa_fatture = row_fatture[3]
        id_contratto_fatture = row_fatture[4]
        anno_fatture = row_fatture[5]
        id_fatture = row_fatture[6]

        #LA VARIABILE ESISTE SE E' DIVERSA DA 0
        importo_fatture = importo_fatture if importo_fatture else 0

        #CONTROLLA SE LA DATA E' UN NUMERO
        if anno_fatture.isdigit():
            anno_fatture = anno_fatture
        else:
            anno_fatture = None

        #CREAZIONE ISTANZA ED ASSEGNAZIONE VALORI
        fatture_instance, created = Fatture.objects.get_or_create(nome=nome_fatture,
                                                                  id_monday=id_fatture,
                                                                  stato=stato_fatture,
                                                                  importo=importo_fatture,
                                                                  id_contratti=id_contratto_fatture,
                                                                  anno_competenza=anno_fatture,
                                                                  )
        #SALVA ISTANZA
        fatture_instance.save()



def fatt_contr_pair():

    #CREAZIONE VARIABILE CONTENENTE TUTTE LE ISTANZE
    fatture = Fatture.objects.all()

    #ITERIAMO LE ISTANZE FILTRIAMO E ASSEGNAMO
    for fattura in fatture:
        id_contratti = fattura.id_contratti

        if id_contratti:
            matching_contratto= Contratti.objects.filter(id_monday=id_contratti).first()

            if matching_contratto:
                fattura.contratto = matching_contratto
                fattura.save()












