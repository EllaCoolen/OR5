import pandas as pd
from DataFrames import dataframes
#################### hier zal ik functies proberen (m)
df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2022.xlsx')

def check_allocation(kolom_van_sheet): #df_bewoners[0] in ons geval
    """
    komt iedere persoon precies 1 keer voor in kolommen 'voor' 'hoofd' en 'na'
    """
    lijst_bewoners = list(kolom_van_sheet)
    for bewoner in lijst_bewoners:
        count(bewoner)
    return lijst_bewoners
    
print(check_allocation(df_bewoners.iloc[:, 0]))




