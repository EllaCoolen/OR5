from eisen import *



# def alle_eisen(planning):
#     df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
#     errors = 0
#     while errors ==0:
#         errors += check_kookt_gang(planning)
#         while errors == 0:
#             errors += controleer_koppels(df_paren, planning)
#             while errors == 0:
#                 # errors += check_koken(df_bewoners, planning)
#                 # while errors == 0:
#                 #     errors += check_niet_koken(df_bewoners, planning)
#                 #     while errors == 0:
#                 #         errors += check_groepsgrootte(df_adressen, planning)
#                 #         while errors == 0:
#                 #             errors += controleer_lege_cellen(planning)
#                 return 0
        
        
def alle_eisen(planning):
    df_paren = pd.read_excel('Running Dinner dataset 2023 v2.xlsx', skiprows=[0], sheet_name = 'Paar blijft bij elkaar')
    errors = 0

    # Voer alle eisencontroles uit zonder de lussen te verlaten
    errors += check_kookt_gang(planning)
    errors += controleer_koppels(df_paren, planning)
    # Voeg hier andere eisencontroles toe

    return errors
    

