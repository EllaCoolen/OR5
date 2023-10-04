from score_planning import score_planning
from eisen import controleer_koppels
from DataFrames import dataframes
import random
import pandas as pd

df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2022.xlsx')
planning = 'Running Dinner eerste oplossing 2023 v2.xlsx'

# Constants
MYVERYBIGNUMBER = 424242424242 
MYVERYSMALLNUMBER = 1e-5
NUMBEROFCITIES = 100
INITIALTEMPERATURE = 2000.0    
COOLINGRATE = 0.9995

# Initialize random number generator 
import random
random.seed(42)

import matplotlib.pyplot as plt
import math

import logging
import sys
logger = logging.getLogger(name='sa-logger')
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("sa.log"),logging.StreamHandler(stream=sys.stdout)])
logging.getLogger('matplotlib.font_manager').disabled = True



def simulated_annealing(df_planning):
    planning_strafpunten = score_planning()   # Twee imputs, maar geen imputs in onze functie score_planning
    logger.debug(msg=f"SA starts with tour having total distance: {planning_strafpunten}")
    df_planning = pd.read_excel(planning)
    iteration = 0

    # initialize data for maintaining history of objective values and temperature
    hist_curr_obj_vals = []
    hist_best_obj_vals = []
    hist_temp_vals = [] 

    # initialize current solution and best solution; become initial tour
    current_planning = df_planning 
    # print(current_planning)
    best_planning = df_planning    
    current_strafpunten = score_planning()
    minste_strafpunten = current_strafpunten

    # initialize temperature
    temperature = INITIALTEMPERATURE 

    hist_curr_obj_vals.append(current_strafpunten)
    hist_best_obj_vals.append(minste_strafpunten)
    hist_temp_vals.append(temperature)
    
        # Maak dictionaries om de lijsten van bewoners per adres in de kolommen 'Voor', 'Hoofd', en 'Na' op te slaan
    bewoners_per_adres_voor = {}
    bewoners_per_adres_hoofd = {}
    bewoners_per_adres_na = {}

    # Loop door de rijen van het DataFrame
    for index, rij in df_planning.iterrows():
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
    for index, rij in df_planning.iterrows():
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


    tellen = 0
    while temperature > MYVERYSMALLNUMBER:  # Cooling stops when temperature is close to 0
        while True and tellen < 50:
            
            gang_kiezen = random.choice(['Voor', 'Hoofd', 'Na'])
            gang = df_planning[gang_kiezen].values.tolist()
            bewoner_a, bewoner_b = random.sample(gang, 2)   # draw two random numbers i,j in {0,1,...,n-1}
            print(bewoner_a, bewoner_b)
            tellen += 1
            if (bewoner_a>0) and (bewoner_b > bewoner_a+1) and controleer_koppels(df_paren, planning) is not None:
                break
        


simulated_annealing(planning)

