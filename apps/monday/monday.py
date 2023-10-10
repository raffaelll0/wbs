import requests
import json
import pandas as pd
import numpy as np
from tabulate import tabulate
from django.db import models
from django.db.models import Q
from ..neapolitanmods.models import *  # Import all models


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






                        #print("\n")
            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data.append(row)
    return table_data
    #for row in table_data:
        #print("\t".join(str(cell) for cell in row))

    #FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA
    #print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
    #print(table_data[1])
    #print(row[4][0:10])

def fetch_mdc_aziende():
    # AZIENDE
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_aziende = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_aziende = "https://api.monday.com/v2"
    headers_aziende = {"Authorization": apiKey_aziende}

    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_aziende = [['NAME', 'RESPONSABILE', "COMMESSE", "ID COMMESSA", "PARTITA IVA", "CODICE FISCALE",  "ID"]]

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
            # item_id = item['id']
            item_name_aziende = item_aziende['name']
            column_aziende = item_aziende['column_values']
            # print(f"Name: {item_name}")
            # print(f"ID: {item_id}, Name: {item_name}")

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_aziende = [item_name_aziende]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_aziende in column_aziende:
                value_text_aziende = values_aziende['text']
                value_id_aziende = values_aziende['id']
                value_aziende = values_aziende['value']
                # print(f"TEXT: {value_text}")

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if value_id_aziende in ["id_elemento", "persone", "link_to_attivit_", "p_iva1", "testo9", "collega_schede0"]:
                    row_aziende.append(value_text_aziende)

                    # print(f"Processing value_id: {value_id}, value: {value}")
                    if value_id_aziende == "link_to_attivit_":
                        linked_pulse_id = None
                        if value_aziende is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_aziende = json.loads(value_aziende)
                                # print("Parsed JSON data:", data)

                                if "linkedPulseIds" in data_aziende:
                                    linked_pulse_ids = data_aziende["linkedPulseIds"]

                                    if linked_pulse_ids:
                                        linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")
                                        #print("Linked Pulse ID: ", linked_pulse_id)

                            except json.JSONDecodeError:
                                pass
                        row_aziende.append(linked_pulse_id)
                    else:
                        pass
                        # APPEND None TO row IF linked_pulse_id IS None
                         #row.append(None)





                        # print("\n")
            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_aziende.append(row_aziende)
    return table_data_aziende
    # for row in table_data:
    # print("\t".join(str(cell) for cell in row))

    # FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA
    #print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
    # print(table_data[1])
    # print(row[4][0:10])

def fetch_mdc_task():
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_task = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_task = "https://api.monday.com/v2"
    headers_task = {"Authorization": apiKey_task}

    # TASK
    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_task = [
        ['NAME', 'TIPO', "PRIORITA'", 'DATA CREAZIONE', "DATA SOLLECITO", "RESPONSABILE", "COMMESSA", 'ID COMMESSA',
         'ID']]

    # CODICE DELLA BOARD DI NOME SPORTELLO STUDIO
    id_board_task = '985523481'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_task = ' { boards (ids: ' + id_board_task + ' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "stato_19", "registro_di_creazione8", "data", "persone", "priorit_", "collega_schede", "collega_schede" ]) { id type value text } }  } }'
    data_task = {'query': query_task}

    # FACCIAMO UNA RICHIESTA JSON
    r_task = requests.post(url=apiUrl_task, json=data_task, headers=headers_task)

    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_task = r_task.json()
    # print(r_task.json())

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
            # print(f"Name: {item_name}")
            # print(f"ID: {item_id}, Name: {item_name}")

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_task = [item_name_task]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_task in column_task:
                value_text_task = values_task['text']
                value_id_task = values_task['id']
                value_task = values_task['value']

                # print(f"TEXT: {value_text_task}")

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if values_task['id'] in ["id_elemento", "stato_19", "registro_di_creazione8", "data", "persone",
                                         "priorit_", "collega_schede"]:
                    row_task.append(values_task['text'])

                    if value_id_task == "collega_schede":
                        linked_pulse_id = None

                        if value_task is not None:
                            try:
                                # Parse the JSON string in 'value_text'
                                data_task = json.loads(value_task)
                                # print("Parsed JSON data:", data)

                                if "linkedPulseIds" in data_task:
                                    linked_pulse_ids = data_task["linkedPulseIds"]

                                    if linked_pulse_ids:
                                        linked_pulse_id = linked_pulse_ids[0].get("linkedPulseId")
                                        # print("Linked Pulse ID: ", linked_pulse_id)

                            except json.JSONDecodeError:
                                pass
                        row_task.append(linked_pulse_id)
                    else:
                        pass
                        # APPEND None TO row IF linked_pulse_id IS None
                        # row.append(None)

            # print("\n")
            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_task.append(row_task)

    return table_data_task

def fetch_mcd_contratti():
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_contratti = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_contratti = "https://api.monday.com/v2"
    headers_contratti = {"Authorization": apiKey_contratti}

    # TASK
    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_contratti = [['NAME', 'ULTIMO AGGIORNAMENTO', 'DATA CREAZIONE', "COMMESSA", "SOGGETTO ATTIVO", "SOGGETTO PASSIVO", "ID"]]

    # CODICE DELLA BOARD DI NOME SPORTELLO STUDIO
    id_board_contratti = '1641120827'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_contratti = ' { boards (ids: ' + id_board_contratti + ' ) { items (limit:10) { id  name column_values (ids: ["id_elemento0", "ultimo_aggiornamento", "registro_di_creazione_1", "collega_schede7", "collega_schede", "collega_schede0"]) { id type value text } }  } }'
    data_contratti = {'query': query_contratti}

    # FACCIAMO UNA RICHIESTA JSON
    r_contratti = requests.post(url=apiUrl_contratti, json=data_contratti, headers=headers_contratti)

    # DEFINIAMO IL NOSTRO JSON CON LA VARIABILE response_data
    response_data_contratti = r_contratti.json()
    #print(r_contratti.json())

    # ESSENDO UN DIZIONARIO SELEZIONIAMO I DATI CHE CI SERVIRANNO, OVVERO DATA E BOARDS
    boards_contratti = response_data_contratti['data']['boards']

    # ITERIAMO DA I BOARD E PER ITEM,
    for board_contratti in boards_contratti:
        items_contratti = board_contratti['items']

        # PRENDIAMO I VALORI DI OGNI ITEM
        for item_contratti in items_contratti:
            # item_id_contratti = item_contratti['id']
            item_name_contratti = item_contratti['name']
            column_contratti = item_contratti['column_values']
            # print(f"Name: {item_name}")
            # print(f"ID: {item_id}, Name: {item_name}")

            # ANDIAMO A DEFINIRE ROW, OVVERO UNA LISTA CON PRESENTE SOLTANTO IL NOME, PER ADESSO...
            row_contratti = [item_name_contratti]

            # PER OGNI VALORE PRESENTE IN item['column_values'] PRENDIAMO SOLTANTO IL VALORE TEXT
            for values_contratti in column_contratti:
                value_text_contratti = values_contratti['text']
                # print(f"TEXT: {value_text}")

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if values_contratti['id'] in ["id_elemento0", "ultimo_aggiornamento", "registro_di_creazione_1", "collega_schede7", "collega_schede", "collega_schede0"]:
                    row_contratti.append(values_contratti['text'])

            # print("\n")
            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_contratti.append(row_contratti)

    return table_data_contratti
    # for row in table_data:
    # print("\t".join(str(cell) for cell in row))

    # FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA
    #print(tabulate(table_data_contratti, headers="firstrow", tablefmt="fancy_grid"))

def fetch_mcd_servizi():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_servizi = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_servizi = "https://api.monday.com/v2"
    headers_servizi = {"Authorization": apiKey_servizi}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_servizi = [['NAME', 'UTENTE', 'TIPOLOGIA', 'LINK FONTE', 'DOCUMENTI', 'ID']]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_servizi= '937015673'



    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_servizi= ' { boards (ids: '+id_board_servizi+' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "persone", "stato_1", "link", "file"]) { id type value text } }  } }'
    data_servizi = {'query' : query_servizi}

    #FACCIAMO UNA RICHIESTA JSON
    r_servizi = requests.post(url=apiUrl_servizi, json=data_servizi, headers=headers_servizi)
    #print(r_servizio.json())
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



            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_servizi.append(row_servizi)
    return table_data_servizi

    #FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA

    #print(tabulate(table_data_servizio, headers="firstrow", tablefmt="fancy_grid"))

def fetch_mcd_contatti():

    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey_contatti = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl_contatti = "https://api.monday.com/v2"
    headers_contatti = {"Authorization": apiKey_contatti}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_contatti = [['NAME', 'IN QUALITA DI', 'LEGALE RAPPRESENTANTE', 'AZIENDE', 'ID']]

    #CODICE DELLA BOARD DI NOME GESTIONE COMMESSE
    id_board_contatti= '1986160544'



    #ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO, AD ESEMPIO dup__of_priorit_ INDICA LA PRIORITA' (BASSA,MEDIA,ALTA)
    query_contatti= ' { boards (ids: '+id_board_contatti+' ) { items (limit:10) { id  name column_values (ids: ["text0", "collega_schede", "dup__of_legale_rappresentante_di", "collega_schede3", "id_elemento"]) { id type value text } }  } }'
    data_contatti = {'query' : query_contatti}

    #FACCIAMO UNA RICHIESTA JSON
    r_contatti = requests.post(url=apiUrl_contatti, json=data_contatti, headers=headers_contatti)
    #print(r_servizio.json())
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
                if value_id_contatti in ["text0", "collega_schede", "dup__of_legale_rappresentante_di", "collega_schede3", "id_elemento"]:
                    row_contatti.append(value_text_contatti)



            #GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_contatti.append(row_contatti)
    return table_data_contatti

    #FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA

    #print(tabulate(table_data_contatti, headers="firstrow", tablefmt="fancy_grid"))








def write_aziende(table_data_aziende):
    """
    Function which gets table_data of aziende, iterate through them and saves them in django db

    Args:
        -table_data_aziende: table data of aziende fetche from monday.com

    """
    for row_az in table_data_aziende[1:]:  # Start from index 1 to skip headers
        #mappo variabili
        nome_az = row_az[0]
        nome_com = row_az[2]
        id_commessa_az = row_az[3]
        p_iva_az = row_az[4]
        cod_fis_az = row_az[5]
        id_monday_az = row_az[6]
        #elaboro variabili che  necessitano elaborazione

        if p_iva_az != '':
            try:
                # Attempt to convert p_iva_az to a numeric format (e.g., int or float)
                p_iva_az = int(p_iva_az)  # You can use int() or float() depending on your data type
            except ValueError:
                # Handle the case where p_iva_az is not a valid number
                p_iva_az = None
        else:
            p_iva_az = None

        if id_monday_az:
            try:
                id_monday_az = int(id_monday_az)
            except ValueError:
                continue


#################################################################################################


        # aziende_queryset = Aziende.objects.filter(
        #     Q(id_monday=id_monday_az) | Q(nome=nome_az)
        # )
        #
        # # Iterate over the queryset
        # for aziende_instance in aziende_queryset:
        #     commessa_instance, created = Commessa.objects.get_or_create(
        #         id_monday=id_commessa_az,
        #         nome=nome_com
        #     )
        #
        #     # Add the Commessa instance to the aziende's commesse relationship
        #     aziende_instance.commesse.add(commessa_instance)
        #
        #     # Save the aziende instance
        #     aziende_instance.save()
####################################################################################################


        a, created = Aziende.objects.get_or_create(nome=nome_az,
                                                   id_monday=id_monday_az,
                                                   cod_fis=cod_fis_az,
                                                   p_iva=p_iva_az,
                                                   id_commessa=id_commessa_az)
        a.save()

def write_commesse(table_data_commesse):
    """
    Function which gets table_data of commesse, iterate through them and saves them in django db

    Args:
        -table_data_commesse: table data of commesse fetched from monday.com

    """
    # Iterate through the data and update the Commessa model
    for row in table_data_commesse[1:]:  # Start from index 1 to skip headers
        nome = row[0]  # Assuming the name is in the first column
        id_monday = row[1]  # Assuming the id_monday is in the second column
        tipo = row[2]
        priority = row[3]
        date = row[4][0:10]
        aziende_name = row[5]
        aziende_value = row[6]


        if aziende_value != '':
            try:
                # Convert aziende_value to an integer
                aziende_value = int(aziende_value)
            except ValueError:
                # Handle the case where aziende_value is not a valid number
                continue
        else:
            continue

        if id_monday:
            try:
                id_monday = int(id_monday)
            except ValueError:
                continue
##########################################################################################
        # aziende_queryset = Aziende.objects.filter(
        #     Q(id_monday=aziende_value) | Q(nome=aziende_name)
        # )
        #
        # # Iterate over the queryset
        # for aziende_instance in aziende_queryset:
        #     c, created = Commessa.objects.get_or_create(
        #         nome=nome,
        #         id_monday=id_monday,
        #         tipologia=tipo,
        #         ultimo_aggiornamento=date,
        #         priorità=priority
        #     )
        #
        #     # Set the cliente_finale field of the Commessa instance
        #     c.cliente_finale = aziende_instance
        #
        #     # Save the Commessa instance
        #     c.save()



        c, created = Commessa.objects.get_or_create(nome=nome,
                                                     id_monday=id_monday,
                                                     tipologia=tipo,
                                                     ultimo_aggiornamento=date,
                                                     priorità=priority,
                                                    id_azienda=aziende_value)
        c.save()

def commesse_aziende_pair():

    for aziende_instance in Aziende.objects.all():

        id_commessa_az = aziende_instance.id_commessa

        # Check if id_commessa_az is not None
        if id_commessa_az is not None:
            # Find the matching Commessa instance based on id_monday
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_az).first()

            # If a matching Commessa instance is found, assign it to commesse field of Aziende
            if matching_commessa is not None:
                aziende_instance.commesse.add(matching_commessa)
                aziende_instance.save()

###########################################################################################################

    # for commessa_instance in Commessa.objects.all():
    #
    #     aziende_value = commessa_instance.id_azienda
    #
    #     # Check if id_commessa_az is not None
    #     if aziende_value is not None:
    #         # Find the matching Commessa instance based on id_monday
    #         matching_azienda = Aziende.objects.filter(id_monday=aziende_value).first()
    #
    #         # If a matching Azienda instance is found, assign it to  field of Commesse
    #         if matching_azienda is not None:
    #             commessa_instance.cliente_finale.add(matching_azienda)
    #             commessa_instance.save()

    commesse = Commessa.objects.all()

    for commessa in commesse:
        id_azienda = commessa.id_azienda

        if id_azienda:
            # Find the matching Aziende instance by id_monday
            matching_aziende = Aziende.objects.filter(id_monday=id_azienda).first()

            if matching_aziende:
                # Assign the matching Aziende instance to the cliente_finale field of the Commessa instance
                commessa.cliente_finale = matching_aziende
                commessa.save()

def write_task(table_data_task):

    """
        Function which gets table_data of task, iterate through them and saves them in django db

        Args:
            -table_data_task: table data of task fetched from monday.com

        """
    # Iterate through the data and update the Commessa model
    for row_task in table_data_task[1:]:  # Start from index 1 to skip headers
        nome_task = row_task[0]
        tipo_task = row_task[1]
        priorita_task = row_task[2]
        data_creazione_task = row_task[3][0:10]
        data_sollecito_task = row_task[4][0:10]
        responsabile_task = row_task[5]
        id_commessa_task = row_task[7]
        id_task = row_task[8]


        t, created = Task.objects.get_or_create(nome=nome_task,
                                                id_monday=id_task,
                                                tipo=tipo_task,
                                                data_creazione=data_creazione_task,
                                                sollecito=data_sollecito_task,
                                                priorità=priorita_task,
                                                id_commessa=id_commessa_task)
        t.save()

def task_commesse_pair():

    for task_instance in Task.objects.all():

        id_commessa_task = task_instance.id_commessa

        # Check if id_commessa_az is not None
        if id_commessa_task is not None:
            # Find the matching Commessa instance based on id_monday
            matching_commessa = Commessa.objects.filter(id_monday=id_commessa_task).first()

            # If a matching Commessa instance is found, assign it to commesse field of Aziende
            if matching_commessa is not None:
                task_instance.commesse.add(matching_commessa)
                task_instance.save()






def write_contratti(table_data_contratti):
    for row_contratti in table_data_contratti[1:]:  # Start from index 1 to skip headers
        nome_contratti = row_contratti[0]
        ultimo_aggiornamento_contratti = row_contratti[1][0:10]
        data_creazione_contratti = row_contratti[2][0:10]
        id_contratti = row_contratti[6]

        contratti_instance, created = Contratti.objects.get_or_create(nome=nome_contratti,
                                                                 id_monday=id_contratti,
                                                                 ultimo_aggiornamento=ultimo_aggiornamento_contratti,
                                                                 data_creazione=data_creazione_contratti,
                                                                 )
        contratti_instance.save()


def write_servizi(table_data_servizi):
    for row in table_data_servizi[1:]:  # Start from index 1 to skip headers
        nome = row[0]


def write_contatti(table_data_contatti):
    for row in table_data_contatti[1:]:  # Start from index 1 to skip headers
        nome = row[0]





