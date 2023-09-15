import pandas as pd

def dataframes(a,b):
    """ 
    Inladen van de datafiles en planning (in juiste format)
    
    arg: a = running dinner dataset, b=eerste oplossing dataset
    output: alle dataframes zijn ingeladen, adressm bewoners, planning etc
    """
    
    df_bewoners = pd.read_excel(a, sheet_name = 'Bewoners')
    #print(df_bewoners)
    
    df_adressen = pd.read_excel(a, sheet_name = 'Adressen')
    #print(df_adressen)

    df_paren = pd.read_excel(a, skiprows=[0], sheet_name = 'Paar blijft bij elkaar')
    #print(df_paren)

    df_buren = pd.read_excel(a, skiprows=[0], sheet_name = 'Buren')
    #print(df_buren)

    df_kookte_2021 = pd.read_excel(a, skiprows=[0], sheet_name = 'Kookte vorig jaar')
    #print(df_kookte_2021)

    df_tafelgenoot_2021 = pd.read_excel(a, skiprows=[0], sheet_name = 'Tafelgenoot vorig jaar')
    #print(df_tafelgenoot_2021)

    df_planning = pd.read_excel(b, usecols = ['Bewoner', 'Huisadres', 'Voor', 'Hoofd', 'Na', 'kookt', 'aantal'])
    #print(df_planning)
    
    
    return df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021, df_planning
#Running Dinner eerste oplossing 2022.xlsx'
   
#print(dataframes('Running Dinner dataset 2022.xlsx', 'Running Dinner eerste oplossing 2022.xlsx'))

############# VERZAMELINGEN EN INDICES ####################

def verzameling(df_bewoners, df_adressen, df_paren):
    
    set_deelnemers = set(df_bewoners['Bewoner'])
    #print(set_deelnemers)

    set_huisadressen = set(df_adressen['Huisadres'])
    #print(set_huisadressen)

    dict_koppels = df_paren.to_dict('index')
    # #print(dict_koppels)

    set_gangen = {'Voor', 'Hoofd', 'Na'}
    # #print(set_gangen)
    return 'Feest'



# ################### PARAMETERS ####################

# dict_tafelgenoot_vorigjaar = df_tafelgenoot_2021.to_dict('index')
# #print(dict_tafelgenoot_vorigjaar)

# dict_gang_vorigjaar = dict(zip(df_kookte_2021['Huisadres'], df_kookte_2021['Gang']))
# #print(dict_gang_vorigjaar)

# dict_gang_ditjaar = dict(zip(df_planning['Huisadres'], df_planning['kookt']))
# #print(dict_gang_ditjaar)

# dict_buren = df_buren.to_dict('index')
# #print(dict_buren)
