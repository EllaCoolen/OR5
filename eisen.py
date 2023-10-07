import pandas as pd
from DataFrames import dataframes

# def controleer_lege_cellen(df):
#     """
#     is iedereen een locatie voor elk gerecht toegewezen, of andere lege cellen in de planning.
#     arg: planning (feasible of infeasible)
#     output: niks of infeasible-melding
#     """ 
#     kolommen = ['Voor', 'Hoofd', 'Na']
#     for kolom in kolommen: 
#         lege_cellen = df[df[kolom].isnull()]

#         if not lege_cellen.empty:
#             for index, rij in lege_cellen.iterrows():
#                 lege_cel = rij[kolom]
#             return 1
#         else:
#             return 0
                
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
        
        elif adres_a_hoofd != adres_b_hoofd:
            return 1

        elif adres_a_na != adres_b_na:
            return 1
            
        else:
            return 0

# def check_koken(df_bewoners, planning_df):
#     """
#     Functie zorgt dat niet-kokers precies 0 keer koken en de rest precies 1 keer kookt.
#     """

#     # Selecteer alleen de rijen waarin 'Kookt niet' gelijk is aan 0 (kokers)
#     kokers = df_bewoners[df_bewoners['Kookt niet'] != 1]

#     # Maak een dictionary om bij te houden hoe vaak elke bewoner moet koken
#     maal_koken_dict = {}

#     # Loop door de rijen van de bewoners die wel moeten koken
#     for index, rij in kokers.iterrows():
#         persoon = rij['Bewoner']
#         adres = rij['Huisadres']
        
#         maal_koken = 0
        
#         # Controleer of het adres van de koker voorkomt in de planning en hoe vaak
#         if (adres in planning_df['Voor'].values):
#             maal_koken += 1
#         if (adres in planning_df['Hoofd'].values):
#             maal_koken += 1
#         if (adres in planning_df['Na'].values):
#             maal_koken += 1

#         # Sla het aantal keren koken op in de dictionary
#         maal_koken_dict[persoon] = maal_koken

#     # Controleer of de kokers precies 1 keer moeten koken
#     for persoon, maal_koken in maal_koken_dict.items():
#         if maal_koken != 1:
#             return 1
#         else:
#             return 0

# def check_niet_koken(df_bewoners, planning):
#     """
#     Functie zorgt dat iedereen die niet kookt, daadwerkelijk niet kookt.
#     arg: df_bewoners, planning_filename (filename as a string)
#     output: hopelijk none, or the place where it goes wrong.
#     """
    
#     # Selecteer rijen waarin 'Kookt niet' gelijk is aan 1 
#     niet_kokers = df_bewoners[df_bewoners['Kookt niet'] == 1]
    
#     # Loop door de rijen van niet-kokers
#     for index, rij in niet_kokers.iterrows():
#         persoon = rij['Bewoner']
#         adres = rij['Huisadres']

#         # Controleer of het adres van de niet-koker voorkomt in de planning
#         if (adres in planning['Voor'].values) or (adres in planning['Hoofd'].values) or (adres in planning['Na'].values):
#             return 1
#         else:
#             return 0            

# def check_groepsgrootte(df_adressen, planning):
    
#     for index, rij in df_adressen.iterrows():
#         adres = rij['Huisadres']
#         if planning.loc[planning['Huisadres'] == adres, 'aantal'].empty:
#             planning.loc[planning['Huisadres'] == adres, 'aantal'] = 0
        
#         aantal = planning.loc[planning['Huisadres'] == adres, 'aantal'].values[0]
        
#         min_aantal = rij['Min groepsgrootte']
#         max_aantal = rij['Max groepsgrootte']
        
#         if aantal < min_aantal or aantal > max_aantal:
#             return 1
#         else:
#             return 0
        
def check_kookt_gang(planning):
    """
    Functie controleert of de bewoners de juiste gang koken op hun eigen adres.
    arg: df_bewoners (DataFrame met kolommen 'Bewoner', 'Huisadres', 'Kookt gang')
    output: 1 als de gang niet overeenkomt met het adres, anders 0
    """
    
    # Loop door de rijen van de DataFrame
    for index, rij in planning.iterrows():
        persoon = rij['Bewoner']
        adres = rij['Huisadres']
        kookt_gang = rij['kookt']
        
        # Controleer of de gang overeenkomt met het adres
        if kookt_gang == 'Voor' and adres not in planning.loc[planning['Bewoner'] == persoon]['Voor'].values:
            return 1
        elif kookt_gang == 'Hoofd' and adres not in planning.loc[planning['Bewoner'] == persoon]['Hoofd'].values:
            return 1
        elif kookt_gang == 'Na' and adres not in planning.loc[planning['Bewoner'] == persoon]['Na'].values:
            return 1
    
    # Als alle controles geslaagd zijn, return 0
    return 0

