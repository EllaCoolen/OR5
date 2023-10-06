import DataFrames
from collections import defaultdict
from DataFrames import dataframes
import pandas as pd
import numpy as np


# dict_koken_beidejaren = defaultdict(list)

# for d in (dict_gang_vorigjaar, dict_gang_ditjaar): # you can list as many input dicts as you want here
#     for key, value in d.items():
#         dict_koken_beidejaren[key].append(value)
    
# print(dict_koken_beidejaren)

# def koken(vorig_jaar, dit_jaar):
#     if vorig_jaar == dit_jaar:
#         return 1
#     else:
#         return 0


#print(koken('Voor', 'Voor'))
def kennissen_voorgaand_jaar(df, data):
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
    for index, rij in df.iterrows():
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
    for index, rij in df.iterrows():
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
            
def kennissen(planning, voorgaand_jaar, data_dit_jaar, data_vorig_jaar):
    
    voorgaand_jaar_bewoners = voorgaand_jaar['Bewoner'].tolist()
    bewoners_per_bewoner = kennissen_voorgaand_jaar(planning, data_dit_jaar)
    bewoners_per_bewoner_2 = kennissen_voorgaand_jaar(voorgaand_jaar, data_vorig_jaar)
    
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
    

            



planning = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
planning_vorig_jaar = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')
data_vorig_jaar = 'Running Dinner dataset 2022.xlsx'
data_dit_jaar = 'Running Dinner dataset 2023 v2.xlsx'
# print(kennissen_voorgaand_jaar(planning_vorig_jaar, data_vorig_jaar))
# print(kennissen(planning, planning_vorig_jaar, data_dit_jaar, data_vorig_jaar))



def check_meeting(df):
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
    
    dubbel = 0
    trippel = 0

    # Maak dictionaries om de lijsten van bewoners per adres in de kolommen 'Voor', 'Hoofd', en 'Na' op te slaan
    bewoners_per_adres_voor = {}
    bewoners_per_adres_hoofd = {}
    bewoners_per_adres_na = {}

    # Loop door de rijen van het DataFrame
    for index, rij in df.iterrows():
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
    for index, rij in df.iterrows():
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