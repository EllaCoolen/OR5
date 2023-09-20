import pandas as pd
from DataFrames import dataframes
df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2022.xlsx')
planning = 'Running Dinner eerste oplossing 2022.xlsx'

def controleer_lege_cellen(planning, kolommen):
    """
    is iedereen een locatie voor elk gerecht toegewezen, of andere lege cellen in de planning.
    arg: planning (feasible of infeasible)
    output: niks of infeasible-melding
    """
    df = pd.read_excel(planning) 

    for kolom in kolommen: 
        lege_cellen = df[df[kolom].isnull()]

        if not lege_cellen.empty:
            for index, rij in lege_cellen.iterrows():
                lege_cel = rij[kolom]
                print(f"Het is infeasible want cel '{kolom}' in rij {index + 2} is leeg. Inhoud: {lege_cel}")
                

def controleer_koppels(df_koppels, planning):
    """
    controleert of paren altijd samen zijn.
    arg: df_koppels en planning
    output: hopelijk none, anders waar het mis zit
    """
    df_adressen = pd.read_excel(planning)

    # Loop door de koppelgegevens en controleer adressen
    for index, rij in df_koppels.iterrows():
        persoon_a = rij['Bewoner1']
        persoon_b = rij['Bewoner2']

        adres_a_voor = df_adressen.loc[df_adressen['Bewoner'] == persoon_a, 'Voor'].values[0]
        adres_b_voor = df_adressen.loc[df_adressen['Bewoner'] == persoon_b, 'Voor'].values[0]

        adres_a_hoofd = df_adressen.loc[df_adressen['Bewoner'] == persoon_a, 'Hoofd'].values[0]
        adres_b_hoofd = df_adressen.loc[df_adressen['Bewoner'] == persoon_b, 'Hoofd'].values[0]

        adres_a_na = df_adressen.loc[df_adressen['Bewoner'] == persoon_a, 'Na'].values[0]        
        adres_b_na = df_adressen.loc[df_adressen['Bewoner'] == persoon_b, 'Na'].values[0]

        if adres_a_voor != adres_b_voor:
            print(f"Fout: Het adres in 'Voor' voor {persoon_a} verschilt van dat voor {persoon_b}.")
        
        if adres_a_hoofd != adres_b_hoofd:
            print(f"Fout: Het adres in 'Hoofd' voor {persoon_a} verschilt van dat voor {persoon_b}.")

        if adres_a_na != adres_b_na:
            print(f"Fout: Het adres in 'Na' voor {persoon_a} verschilt van dat voor {persoon_b}.")
    
# def check_koken(df_bewoners, planning):
#     """
#     Functie zorgt dat iedereen die wel moet koken ook daadwerkelijk 1 keer kookt.
#     """
#     # Maak een dictionary om bij te houden hoe vaak elke bewoner moet koken
#     maal_koken_dict = {}
    
#     # Selecteer rijen waarin 'Kookt niet' gelijk is aan 1 
#     kokers = df_bewoners[df_bewoners['Kookt niet'] != '1']

#     # Loop door de rijen van de bewoners
#     for index, rij in kokers.iterrows():
#         persoon = rij['Bewoner']
#         adres = rij['Huisadres']
        
#         maal_koken = 0
        
#         # Controleer of het adres van de koker voorkomt in de planning en hoevaak
#         if (adres in planning['Voor'].values):
#             maal_koken += 1
#         if (adres in planning['Hoofd'].values):
#             maal_koken += 1
#         if (adres in planning['Na'].values):
#             maal_koken += 1

#         # Sla het aantal keren koken op in de dictionary
#         maal_koken_dict[persoon] = maal_koken

#     # Controleer of iedereen precies 1 keer moet koken
#     for persoon, maal_koken in maal_koken_dict.items():
#         if maal_koken != 1:
#             print(f"Fout: {persoon} moet {maal_koken} keer koken")

def check_niet_koken(df_bewoners, planning_filename):
    """
    Functie zorgt dat iedereen die niet kookt, daadwerkelijk niet kookt.
    arg: df_bewoners, planning_filename (filename as a string)
    output: hopelijk none, or the place where it goes wrong.
    """
    # Read the planning Excel file into a DataFrame
    planning = pd.read_excel(planning_filename)

    # Selecteer rijen waarin 'Kookt niet' gelijk is aan 1 
    niet_kokers = df_bewoners[df_bewoners['Kookt niet'] == '1']
    # Loop door de rijen van niet-kokers
    for index, rij in niet_kokers.iterrows():
        persoon = rij['Bewoner']
        adres = rij['Huisadres']

        # Controleer of het adres van de niet-koker voorkomt in de planning
        if (adres in planning['Voor'].values) or (adres in planning['Hoofd'].values) or (adres in planning['Na'].values):
            print(f"Fout: {persoon} hoeft niet te koken, maar zijn/haar adres staat in de planning.")            
            




# Definieer de kolommen om te controleren op lege cellen
kolommen_te_controleren = ['Voor', 'Hoofd', 'Na']

# Roep de functie aan om de controle uit te voeren
print(controleer_lege_cellen(planning, kolommen_te_controleren))
print(controleer_koppels(df_paren, planning))
print(check_niet_koken(df_bewoners, planning))
print(check_koken(df_bewoners, planning))

