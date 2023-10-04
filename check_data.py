import pandas as pd
from DataFrames import dataframes
from collections import Counter
df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
planning = 'Running Dinner eerste oplossing 2023 v2.xlsx'

def controleer_lege_cellen(df):
    """
    is iedereen een locatie voor elk gerecht toegewezen, of andere lege cellen in de planning.
    arg: planning (feasible of infeasible)
    output: niks of infeasible-melding
    """ 
    kolommen = ['Voor', 'Hoofd', 'Na']
    for kolom in kolommen: 
        lege_cellen = df[df[kolom].isnull()]

        if not lege_cellen.empty:
            for index, rij in lege_cellen.iterrows():
                lege_cel = rij[kolom]
            return 1
        else:
            return 0
                # print(f"Het is infeasible want cel '{kolom}' in rij {index + 2} is leeg. Inhoud: {lege_cel}")
                

def controleer_koppels(df_koppels, planning):
    """
    controleert of paren altijd samen zijn.
    arg: df_koppels en planning
    output: hopelijk none, anders waar het mis zit
    """
    

    # Loop door de koppelgegevens en controleer adressen
    for index, rij in df_koppels.iterrows():
        persoon_a = rij['Bewoner1']
        persoon_b = rij['Bewoner2']

        adres_a_voor = planning.loc[planning['Bewoner'] == persoon_a, 'Voor'].values[0]
        adres_b_voor = planning.loc[planning['Bewoner'] == persoon_b, 'Voor'].values[0]

        adres_a_hoofd = planning.loc[planning['Bewoner'] == persoon_a, 'Hoofd'].values[0]
        adres_b_hoofd = planning.loc[planning['Bewoner'] == persoon_b, 'Hoofd'].values[0]

        adres_a_na = planning.loc[planning['Bewoner'] == persoon_a, 'Na'].values[0]        
        adres_b_na = planning.loc[planning['Bewoner'] == persoon_b, 'Na'].values[0]

        if adres_a_voor != adres_b_voor:
            return 1
            # print(f"Fout: Het adres in 'Voor' voor {persoon_a} verschilt van dat voor {persoon_b}.")
        
        elif adres_a_hoofd != adres_b_hoofd:
            return 1
            # print(f"Fout: Het adres in 'Hoofd' voor {persoon_a} verschilt van dat voor {persoon_b}.")

        elif adres_a_na != adres_b_na:
            return 1
            # print(f"Fout: Het adres in 'Na' voor {persoon_a} verschilt van dat voor {persoon_b}.")
            
        else:
            return 0

def check_koken(df_bewoners, planning_df):
    """
    Functie zorgt dat niet-kokers precies 0 keer koken en de rest precies 1 keer kookt.
    """
    # Read the planning Excel file into a DataFrame
    

    # Selecteer alleen de rijen waarin 'Kookt niet' gelijk is aan 0 (kokers)
    kokers = df_bewoners[df_bewoners['Kookt niet'] != 1]

    # Maak een dictionary om bij te houden hoe vaak elke bewoner moet koken
    maal_koken_dict = {}

    # Loop door de rijen van de bewoners die wel moeten koken
    for index, rij in kokers.iterrows():
        persoon = rij['Bewoner']
        adres = rij['Huisadres']
        
        maal_koken = 0
        
        # Controleer of het adres van de koker voorkomt in de planning en hoe vaak
        if (adres in planning_df['Voor'].values):
            maal_koken += 1
        if (adres in planning_df['Hoofd'].values):
            maal_koken += 1
        if (adres in planning_df['Na'].values):
            maal_koken += 1

        # Sla het aantal keren koken op in de dictionary
        maal_koken_dict[persoon] = maal_koken

    # Controleer of de kokers precies 1 keer moeten koken
    for persoon, maal_koken in maal_koken_dict.items():
        if maal_koken != 1:
            return 1
        else:
            return 0


def check_niet_koken(df_bewoners, planning):
    """
    Functie zorgt dat iedereen die niet kookt, daadwerkelijk niet kookt.
    arg: df_bewoners, planning_filename (filename as a string)
    output: hopelijk none, or the place where it goes wrong.
    """
    # Read the planning Excel file into a DataFrame
    

    # Selecteer rijen waarin 'Kookt niet' gelijk is aan 1 
    niet_kokers = df_bewoners[df_bewoners['Kookt niet'] == 1]
    # Loop door de rijen van niet-kokers
    for index, rij in niet_kokers.iterrows():
        persoon = rij['Bewoner']
        adres = rij['Huisadres']

        # Controleer of het adres van de niet-koker voorkomt in de planning
        if (adres in planning['Voor'].values) or (adres in planning['Hoofd'].values) or (adres in planning['Na'].values):
            return 1
        else:
            return 0            
            
# Definieer de kolommen om te controleren op lege cellen


def check_groepsgrootte(df_adressen, planning):
    for index, rij in df_adressen.iterrows():
        adres = rij['Huisadres']
        if planning.loc[planning['Huisadres'] == adres, 'aantal'].empty:
            planning.loc[planning['Huisadres'] == adres, 'aantal'] = 0
        
        aantal = planning.loc[planning['Huisadres'] == adres, 'aantal'].values[0]
        
        min_aantal = rij['Min groepsgrootte']
        max_aantal = rij['Max groepsgrootte']
        
        if aantal < min_aantal or aantal > max_aantal:
            return 1
        else:
            return 0

    





############# WENSEN ###################################################





def check_meeting(planning_filename):
    # Lees het Excel-bestand met de informatie over wie waar eet in
    # df = pd.read_excel(planning_filename)
    df = planning_filename
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
        # print(len(tafelgenoten))
        # print(f"Bewoner {bewoner} komt de volgende bewoners tegen bij alle 3 de gangen: {', '.join(tafelgenoten)}")
        
        dubbel += len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners) == 2])/2
        trippel += len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners) == 3])/3
        
    dubbel = dubbel/2
    trippel = trippel/2 
        
    return dubbel, trippel
        





    
