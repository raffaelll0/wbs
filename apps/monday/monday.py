import requests
import json
import pandas as pd
import numpy as np
from tabulate import tabulate
from django.db import models



def dump_mdc_to_django():
    #CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    #CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data = [['NAME', 'ID', 'TIPO', 'PRIOR', 'DATA', "CLIENTE FINALE", "MISURA FINANZIARIA"]]

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
                #print(f"TEXT: {value_text}")

                #SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if values['id'] in ["id_elemento", "stato_1", "dup__of_priorit_", "ultimo_aggiornamento", "cliente_1", "collega_schede9"]:
                    row.append(values['text'])


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

#print(dump_mdc_to_django())

def dump_aziende():
    # AZIENDE
    # CHIAVE DI ACCESSO PER COLLEGARSI A MONDAY
    apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIzNDMyMjYwNSwiYWFpIjoxMSwidWlkIjozNDE1NDI1NCwiaWFkIjoiMjAyMy0wMi0wM1QwODozOTowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzI3OTI3OCwicmduIjoidXNlMSJ9.ocXATYHEMQUjny7c3VRGwM7T0N4xwzC7fBGloNzuVYM"
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    # CREAZIONE DI UNA TABELLA CON I TITOLI, IN SEGUITO VERRANNO AGGIUNTI I VALORI CON LA FUNZIONE APPEND
    table_data_aziende = [
        ['NAME', 'RESPONSABILE', "COMMESSE", "PARTITA IVA", "CODICE FISCALE", "ID"]]

    # CODICE DELLA BOARD DI NOME LISTA CLIENTI
    id_board_aziende = '813707989'

    # ALL' INTERNO DELLA QUERY ANDIAMO A SPECIFICARE I VALORI CHE CI SERVONO
    query_aziende = ' { boards (ids: ' + id_board_aziende + ' ) { items (limit:10) { id  name column_values (ids: ["id_elemento", "persone", "link_to_attivit_", "p_iva1", "testo9", "collega_schede0"]) { id type value text } }  } }'
    data_aziende = {'query': query_aziende}

    # FACCIAMO UNA RICHIESTA JSON
    r_aziende = requests.post(url=apiUrl, json=data_aziende, headers=headers)

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
                # print(f"TEXT: {value_text}")

                # SE L'ID DEL VALORE è PRESENTE IN QUESTA LISTA, ALLORA AGGIUNGI A ROW
                if values_aziende['id'] in ["id_elemento", "persone", "link_to_attivit_", "p_iva1", "testo9", "collega_schede0"]:
                    row_aziende.append(values_aziende['text'])

            # print("\n")
            # GIUSTAMENTE QUESTA LISTA VERRA' AGGIUNTA ALLA TABELLA OGNI VOLTA CHE FINISCE IL LOOP
            table_data_aziende.append(row_aziende)

    return table_data_aziende

    # for row in table_data:
    # print("\t".join(str(cell) for cell in row))

    # FACCIAMO USCIRE IN OUTPUT LA TABELLA CON INTERFACCIA
    #print(tabulate(table_data_aziende, headers="firstrow", tablefmt="fancy_grid"))
    #print(row_aziende[5])

#print(dump_aziende())