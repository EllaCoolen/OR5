import pandas as pd
from DataFrames import dataframes
#################### hier zal ik functies proberen (m)
df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2022.xlsx')
# Vervang met dit jaar data
planning = 'Running Dinner eerste oplossing 2022.xlsx'

def controleer_lege_cellen(planning, kolommen):
    """
    is iedereen een locatie voor elk gerecht toegewezen
    arg: planning (feasible of infeasible)
    output: niks of infeasible-melding
    """
    df = pd.read_excel(planning) #mogelijk overbodige regel

    for kolom in kolommen:
        lege_cellen = df[df[kolom].isnull()]

        if not lege_cellen.empty:
            for index, rij in lege_cellen.iterrows():
                lege_cel = rij[kolom]
                print(f"Het is infeasible want cel '{kolom}' in rij {index + 2} is leeg. Inhoud: {lege_cel}")
                

def controleer_adressen(df_koppels, planning):
    """
    controleert of paren altijd samen zijn.
    """
    # Laad de koppelgegevens in een DataFrame

    # Laad de adresgegevens in een DataFrame
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

def check_niet_koken(df_bewoners, planning):
    # Selecteer rijen waarin 'NietKoken' gelijk is aan 1 (niet hoeven te koken)
    niet_kokers = df_bewoners[df_bewoners['NietKoken'] == 1]
    # Loop door de rijen van niet-kokers
    for index, rij in niet_kokers.iterrows():
        persoon = rij['Persoon']
        adres = rij['Adres']

        # Controleer of het adres van de niet-koker voorkomt in de planning
        if (adres in df_planning['Voor'].values) or (adres in df_planning['Hoofd'].values) or (adres in df_planning['Na'].values):
            print(f"Fout: {persoon} hoeft niet te koken, maar zijn/haar adres staat in de planning.")
    

# Definieer de kolommen om te controleren op lege cellen
kolommen_te_controleren = ['Voor', 'Hoofd', 'Na']

# Roep de functie aan om de controle uit te voeren
print(controleer_lege_cellen(planning, kolommen_te_controleren))
print(controleer_adressen(df_paren, planning))

