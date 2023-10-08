from DataFrames import dataframes
import pandas as pd
import numpy as np

planning = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')


def check_meeting(planning):
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
    
    dubbel = 0
    trippel = 0

    # Maak dictionaries om de lijsten van bewoners per adres in de kolommen 'Voor', 'Hoofd', en 'Na' op te slaan
    bewoners_per_adres_voor = {}
    bewoners_per_adres_hoofd = {}
    bewoners_per_adres_na = {}

    # Loop door de rijen van het DataFrame
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Voor'
        if adres_voor not in bewoners_per_adres_voor:
            bewoners_per_adres_voor[adres_voor] = []
        bewoners_per_adres_voor[adres_voor].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Hoofd'
        if adres_hoofd not in bewoners_per_adres_hoofd:
            bewoners_per_adres_hoofd[adres_hoofd] = []
        bewoners_per_adres_hoofd[adres_hoofd].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Na'
        if adres_na not in bewoners_per_adres_na:
            bewoners_per_adres_na[adres_na] = []
        bewoners_per_adres_na[adres_na].append(bewoner)

    # Maak een lege dictionary om de lijsten van bewoners per bewoner op te slaan
    bewoners_per_bewoner = {}

    # Loop door de rijen van het DataFrame om de lijsten van bewoners te genereren
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']

        # Haal de lijsten van bewoners op hetzelfde adres in de kolommen 'Voor', 'Hoofd', en 'Na' op
        bewoners_op_hetzelfde_adres_voor = bewoners_per_adres_voor.get(adres_voor, [])
        bewoners_op_hetzelfde_adres_hoofd = bewoners_per_adres_hoofd.get(adres_hoofd, [])
        bewoners_op_hetzelfde_adres_na = bewoners_per_adres_na.get(adres_na, [])

        # Combineer de lijsten van bewoners van 'Voor', 'Hoofd', en 'Na'
        bewoners_tijdens_voorgerecht = list(bewoners_op_hetzelfde_adres_voor)
        bewoners_tijdens_hoofdgerecht = list(bewoners_op_hetzelfde_adres_hoofd)
        bewoners_tijdens_nagerecht = list(bewoners_op_hetzelfde_adres_na)

        # Voeg de lijsten samen tot één lijst voor de bewoner
        bewoners_tijdens_alle_gangen = list(bewoners_tijdens_voorgerecht + bewoners_tijdens_hoofdgerecht + bewoners_tijdens_nagerecht)
        # Sla de lijst op in de dictionary met bewoners
        bewoners_per_bewoner[bewoner] = bewoners_tijdens_alle_gangen

    # Loop door de bewoners en print de lijsten
    for bewoner, bewoners in bewoners_per_bewoner.items():
        tafelgenoten = bewoners_per_bewoner[bewoner] 
        tafelgenoten = [i for i in tafelgenoten if i != bewoner]   # Bewoner zelf uit eigen tafelgenoten lijst verwijderd
        
        for index, rij in df_paren.iterrows():
            bewoner1 = rij['Bewoner1']
            bewoner2 = rij['Bewoner2']
            
            if bewoner == bewoner1 and bewoner2 in tafelgenoten:
                tafelgenoten.remove(bewoner2)
            elif bewoner == bewoner2 and bewoner1 in tafelgenoten:
                tafelgenoten.remove(bewoner1)
        
        dubbel += len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners) == 2])/2
        trippel += len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners) == 3])/3
        
    dubbel = dubbel/2
    trippel = trippel/2 
        
    return dubbel, trippel





# def dubbel_hoofd(planning, voorgaand_jaar):
#     """
#     Functie kijkt of bewoners van vorig jaar, dit jaar weer hoofdgerecht koken.
#     8 strafpunten
#     """    
#     voorgaand_jaar = pd.read_excel(voorgaand_jaar)
#     planning['Huisadres'] = planning['Huisadres'].str.replace('_', '')
#     voorgaand_jaar['Huisadres'] = voorgaand_jaar['Huisadres'].str.replace('_', '')  # Maakt het generiek
    
#     hoofd_dubbel = []

#     vorig_jaar_hoofd = voorgaand_jaar[voorgaand_jaar['kookt'] == 'Hoofd']['Huisadres'].values.tolist()

#     for index, rij in planning.iterrows():
#         koken_dit_jaar = rij['kookt']
#         huisadres = rij['Huisadres']
        
#         # Zoek het huisadres in de voorgaand_jaar DataFrame
#         vorig_jaar_rij = voorgaand_jaar[voorgaand_jaar['Huisadres'] == huisadres]
        
#         if not vorig_jaar_rij.empty:            
#             if koken_dit_jaar == 'Hoofd' and huisadres in vorig_jaar_hoofd:
#                 hoofd_dubbel.append(huisadres)
           
#     hoofd_dubbel = len(list(dict.fromkeys(hoofd_dubbel)))
#     return hoofd_dubbel



def voorkeur_gang(planning):
    """
    Functie kijkt of bewoner een voorkeursgang heeft opgegeven en of desbetreffende persoon bij die gang diens eigen adres heeft staan.
    6 strafpunten
    """
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')    
    niet_voorkeur_gang = []

    for index, row in df_adressen.iterrows():
        voorkeur_gang = row['Voorkeur gang']
        huisadres = row['Huisadres']
    
        # Controleer of de voorkeursgang niet NaN is
        if not pd.isna(voorkeur_gang):
            # Zoek het bijbehorende adres in de dataframe planning
            adres_in_planning = planning[planning['Huisadres'] == huisadres]
        
            if not adres_in_planning.empty:
                toegewezen_gang = adres_in_planning['kookt'].values[0]
            
                # Vergelijk de voorkeursgang met de toegewezen gang
                if voorkeur_gang != toegewezen_gang:
                    niet_voorkeur_gang.append(huisadres)
                    
    niet_voorkeur_gang = len(niet_voorkeur_gang)
    
    return niet_voorkeur_gang



def tafelgenoten(planning, data):
    """
    Functie kijkt of bewoner bij zelfde bewoner zit als voorgaand jaar. (in dit geval eerst alleen 2022)
    4 strafpunten
    """
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes(data)
    # Maak dictionaries om de lijsten van bewoners per adres in de kolommen 'Voor', 'Hoofd', en 'Na' op te slaan
    bewoners_per_adres_voor = {}
    bewoners_per_adres_hoofd = {}
    bewoners_per_adres_na = {}
    
    # Loop door de rijen van het DataFrame
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']
        
         # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Voor'
        if adres_voor not in bewoners_per_adres_voor:
            bewoners_per_adres_voor[adres_voor] = []
        bewoners_per_adres_voor[adres_voor].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Hoofd'
        if adres_hoofd not in bewoners_per_adres_hoofd:
            bewoners_per_adres_hoofd[adres_hoofd] = []
        bewoners_per_adres_hoofd[adres_hoofd].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Na'
        if adres_na not in bewoners_per_adres_na:
            bewoners_per_adres_na[adres_na] = []
        bewoners_per_adres_na[adres_na].append(bewoner)

    # Maak een lege dictionary om de lijsten van bewoners per bewoner op te slaan
    bewoners_per_bewoner = {}

    # Loop door de rijen van het DataFrame om de lijsten van bewoners te genereren
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']

        # Haal de lijsten van bewoners op hetzelfde adres in de kolommen 'Voor', 'Hoofd', en 'Na' op
        bewoners_op_hetzelfde_adres_voor = bewoners_per_adres_voor.get(adres_voor, [])
        bewoners_op_hetzelfde_adres_hoofd = bewoners_per_adres_hoofd.get(adres_hoofd, [])
        bewoners_op_hetzelfde_adres_na = bewoners_per_adres_na.get(adres_na, [])

        # Combineer de lijsten van bewoners van 'Voor', 'Hoofd', en 'Na'
        bewoners_tijdens_voorgerecht = list(bewoners_op_hetzelfde_adres_voor)
        bewoners_tijdens_hoofdgerecht = list(bewoners_op_hetzelfde_adres_hoofd)
        bewoners_tijdens_nagerecht = list(bewoners_op_hetzelfde_adres_na)

        # Voeg de lijsten samen tot één lijst voor de bewoner
        bewoners_tijdens_alle_gangen = list(bewoners_tijdens_voorgerecht + bewoners_tijdens_hoofdgerecht + bewoners_tijdens_nagerecht)
        # Sla de lijst op in de dictionary met bewoners
        bewoners_per_bewoner[bewoner] = bewoners_tijdens_alle_gangen

    # Loop door de bewoners en print de lijsten
    for bewoner, bewoners in bewoners_per_bewoner.items():
        tafelgenoten = bewoners_per_bewoner[bewoner] 
        tafelgenoten = [i for i in tafelgenoten if i != bewoner]   # Bewoner zelf uit eigen tafelgenoten lijst verwijderd
        
        for index, rij in df_paren.iterrows():
            bewoner1 = rij['Bewoner1']
            bewoner2 = rij['Bewoner2']
            
            if bewoner == bewoner1 and bewoner2 in tafelgenoten:
                tafelgenoten.remove(bewoner2)
            elif bewoner == bewoner2 and bewoner1 in tafelgenoten:
                tafelgenoten.remove(bewoner1)
                
        bewoners_per_bewoner[bewoner] = tafelgenoten
        
    return bewoners_per_bewoner
            # f'{bewoner} komt de volgende mensen tegen dit jaar: {tafelgenoten}'
            
def kennissen(planning):
    
    voorgaand_jaar = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')
    data_dit_jaar = 'Running Dinner dataset 2023 v2.xlsx'
    data_vorig_jaar = 'Running Dinner dataset 2022.xlsx'
    voorgaand_jaar_bewoners = voorgaand_jaar['Bewoner'].tolist()
    bewoners_per_bewoner = tafelgenoten(planning, data_dit_jaar)
    bewoners_per_bewoner_2 = tafelgenoten(voorgaand_jaar, data_vorig_jaar)
    
    zelfde_tafelgenoot = 0
    
    for bewoner in bewoners_per_bewoner:
        if bewoner in voorgaand_jaar_bewoners:
            contacten = bewoners_per_bewoner[bewoner]
            contacten = list(set(contacten))
            contacten_2 = bewoners_per_bewoner_2[bewoner]
            contacten_2 = list(set(contacten_2))
            alle_contacten = contacten + contacten_2
            set_alle_contacten = set(alle_contacten)
            if len(set_alle_contacten) != len(alle_contacten):
                verschil = len(alle_contacten)-len(set_alle_contacten)
                zelfde_tafelgenoot += verschil
            
    zelfde_tafelgenoot = zelfde_tafelgenoot/2
    return zelfde_tafelgenoot
    

            


def buren(planning):
    """
    Functie kijkt of bewoner een buur heeft als tafelgenoot.
    2 strafpunten
    """
    
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
    
    buren = []
    
    # Maak dictionaries om de lijsten van bewoners per adres in de kolommen 'Voor', 'Hoofd', en 'Na' op te slaan
    bewoners_per_adres_voor = {}
    bewoners_per_adres_hoofd = {}
    bewoners_per_adres_na = {}

    # Loop door de rijen van het DataFrame
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Voor'
        if adres_voor not in bewoners_per_adres_voor:
            bewoners_per_adres_voor[adres_voor] = []
        bewoners_per_adres_voor[adres_voor].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Hoofd'
        if adres_hoofd not in bewoners_per_adres_hoofd:
            bewoners_per_adres_hoofd[adres_hoofd] = []
        bewoners_per_adres_hoofd[adres_hoofd].append(bewoner)

        # Voeg de bewoner toe aan de lijst van bewoners op hetzelfde adres in de kolom 'Na'
        if adres_na not in bewoners_per_adres_na:
            bewoners_per_adres_na[adres_na] = []
        bewoners_per_adres_na[adres_na].append(bewoner)

    # Maak een lege dictionary om de lijsten van bewoners per bewoner op te slaan
    bewoners_per_bewoner = {}

    # Loop door de rijen van het DataFrame om de lijsten van bewoners te genereren
    for index, rij in planning.iterrows():
        bewoner = rij['Bewoner']
        adres_voor = rij['Voor']
        adres_hoofd = rij['Hoofd']
        adres_na = rij['Na']

        # Haal de lijsten van bewoners op hetzelfde adres in de kolommen 'Voor', 'Hoofd', en 'Na' op
        bewoners_op_hetzelfde_adres_voor = bewoners_per_adres_voor.get(adres_voor, [])
        bewoners_op_hetzelfde_adres_hoofd = bewoners_per_adres_hoofd.get(adres_hoofd, [])
        bewoners_op_hetzelfde_adres_na = bewoners_per_adres_na.get(adres_na, [])

        # Combineer de lijsten van bewoners van 'Voor', 'Hoofd', en 'Na'
        bewoners_tijdens_voorgerecht = list(bewoners_op_hetzelfde_adres_voor)
        bewoners_tijdens_hoofdgerecht = list(bewoners_op_hetzelfde_adres_hoofd)
        bewoners_tijdens_nagerecht = list(bewoners_op_hetzelfde_adres_na)

        # Voeg de lijsten samen tot één lijst voor de bewoner
        bewoners_tijdens_alle_gangen = list(bewoners_tijdens_voorgerecht + bewoners_tijdens_hoofdgerecht + bewoners_tijdens_nagerecht)
        # Sla de lijst op in de dictionary met bewoners
        bewoners_per_bewoner[bewoner] = bewoners_tijdens_alle_gangen

    # Loop door de bewoners en print de lijsten
    for bewoner, bewoners in bewoners_per_bewoner.items():
        tafelgenoten = bewoners_per_bewoner[bewoner] 
        tafelgenoten = [i for i in tafelgenoten if i != bewoner]   # Bewoner zelf uit eigen tafelgenoten lijst verwijderd
        # print(bewoner, '\n', tafelgenoten)
        for index, rij in df_buren.iterrows():
            bewoner1 = rij['Bewoner1']
            bewoner2 = rij['Bewoner2']
            
            if bewoner == bewoner1 and bewoner2 in tafelgenoten:
                buren.append(bewoner)
                buren.append(bewoner2)
                # print(bewoner, bewoner2)
            elif bewoner == bewoner2 and bewoner1 in tafelgenoten:
                buren.append(bewoner)
                buren.append(bewoner1)
                # print(bewoner, bewoner2, bewoner1)
    
    buren = len(list(dict.fromkeys(buren)))
    return buren




def ouwe_kennissen(planning):
    """
    Functie kijkt of bewoner bij zelfde bewoner zit als twee jaar daarvoor.
    1 strafpunt
    """
    twee_jaar_geleden_planning = pd.read_excel('Running Dinner eerste oplossing 2021 - corr.xlsx')
    data_dit_jaar = 'Running Dinner dataset 2023 v2.xlsx'
    data_twee_jaar_geleden = 'Running Dinner dataset 2021.xlsx'
    voorgaand_jaar_bewoners = twee_jaar_geleden_planning['Bewoner'].tolist()
    bewoners_per_bewoner = tafelgenoten(planning, data_dit_jaar)
    bewoners_per_bewoner_2 = tafelgenoten(twee_jaar_geleden_planning, data_twee_jaar_geleden)
    
    zelfde_tafelgenoot_twee_jaar_geleden = 0
    
    for bewoner in bewoners_per_bewoner:
        if bewoner in voorgaand_jaar_bewoners:
            contacten = bewoners_per_bewoner[bewoner]
            contacten = list(set(contacten))
            contacten_2 = bewoners_per_bewoner_2[bewoner]
            contacten_2 = list(set(contacten_2))
            alle_contacten = contacten + contacten_2
            set_alle_contacten = set(alle_contacten)
            if len(set_alle_contacten) != len(alle_contacten):
                verschil = len(alle_contacten)-len(set_alle_contacten)
                zelfde_tafelgenoot_twee_jaar_geleden += verschil
            
    zelfde_tafelgenoot_twee_jaar_geleden = zelfde_tafelgenoot_twee_jaar_geleden/2
    return zelfde_tafelgenoot_twee_jaar_geleden
    
