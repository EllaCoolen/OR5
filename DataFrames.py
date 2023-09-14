import pandas as pd

df_bewoners = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name = 'Bewoners')
#rint(df_bewoners)

df_adressen = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name = 'Adressen')
#print(df_adressen)

df_paren = pd.read_excel('Running Dinner dataset 2022.xlsx', skiprows=[0], sheet_name = 'Paar blijft bij elkaar')
#print(df_paren)

df_buren = pd.read_excel('Running Dinner dataset 2022.xlsx', skiprows=[0], sheet_name = 'Buren')
#print(df_buren)

df_kookte_2021 = pd.read_excel('Running Dinner dataset 2022.xlsx', skiprows=[0], sheet_name = 'Kookte vorig jaar')
#print(df_kookte_2021)

df_tafelgenoot_2021 = pd.read_excel('Running Dinner dataset 2022.xlsx', skiprows=[0], sheet_name = 'Tafelgenoot vorig jaar')
#print(df_tafelgenoot_2021)


############# VERZAMELINGEN EN INDICES ####################

set_deelnemers = set(df_bewoners['Bewoner'])
#print(set_deelnemers)

set_huisadressen = set(df_adressen['Huisadres'])
#print(set_huisadressen)

dict_koppels = df_paren.to_dict('index')
#print(dict_koppels)

set_gangen = {'Voor', 'Hoofd', 'Na'}
#print(set_gangen)


################### PARAMETERS ####################

dict_tafelgenoot_vorigjaar = df_tafelgenoot_2021.to_dict('index')
#print(dict_tafelgenoot_vorigjaar)

dict_gang_vorigjaar = df_kookte_2021.to_dict('index')
#print(dict_gang_vorigjaar)

dict_buren = df_buren.to_dict('index')
print(dict_buren)
