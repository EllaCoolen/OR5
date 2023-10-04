from DataFrames import dataframes



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





def dubbel_hoofd(planning):
    """
    Functie kijkt of bewoners van vorig jaar, dit jaar weer hoofdgerecht koken.
    8 strafpunten
    """    
    
    
    return



def voorkeur_gang(planning):
    """
    Functie kijkt of bewoner een voorkeursgang heeft opgegeven en of desbetreffende persoon bij die gang diens eigen adres heeft staan.
    6 strafpunten
    """
    
    return



def kennissen_voorgaand_jaar(planning, voorgaand_jaar):
    """
    Functie kijkt of bewoner bij zelfde bewoner zit als voorgaand jaar.
    4 strafpunten
    """
    
    return


def buren(planning):
    """
    Functie kijkt of bewoner een buur heeft als tafelgenoot.
    2 strafpunten
    """
    
    return



def kennissen_twee_jaar(planning, twee_jaar):
    """
    Functie kijkt of bewoner bij zelfde bewoner zit als twee jaar daarvoor.
    1 strafpunt
    """
    
    return