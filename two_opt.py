from score_planning import score_planning
from DataFrames import dataframes
import random
import pandas as pd
from eisen import *
from alle_checks import alle_eisen
import logging
import sys

df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
planning = 'Running Dinner eerste oplossing 2023 v2.xlsx'

# # Constants
# MYVERYBIGNUMBER = 424242424242 
# MYVERYSMALLNUMBER = 1e-5
# NUMBEROFCITIES = 100
# INITIALTEMPERATURE = 2000.0    
# COOLINGRATE = 0.9995

# Initialize random number generator 
# random.seed(42)

logger = logging.getLogger(name='sa-logger')
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("sa.log"),logging.StreamHandler(stream=sys.stdout)])
logging.getLogger('matplotlib.font_manager').disabled = True

def two_opt(planning, kolom, output_filename, dubbel_trippel=True, buurhuis=True):
    planning = pd.read_excel(planning)
    strafpunten = score_planning(planning, dubbel_trippel, buurhuis)
    
    # planning_strafpunten = score_planning()
    logger.debug(msg=f"2-opt begint met een strafpunten score van: {strafpunten}")

    improved = True
    iteration = 0
    while improved:
        improved = False
        i = 1
        while i <= len(planning)-2 :
            j = i+1
            while j <= len(planning): 
                if j - i == 1:
                    j += 1
                    continue  # No need to reverse two consecutive edges
                if 0 <= i < len(planning) and 0 <= j < len(planning):
                    errors = alle_eisen(planning)
                    if errors == 0:
                    # if alle_eisen(planning) == 0:
                        nieuwe_planning = planning.copy()
                        nieuwe_planning.loc[i, kolom], nieuwe_planning.loc[j, kolom] = nieuwe_planning.loc[j, kolom], nieuwe_planning.loc[i, kolom]
                        new_score = score_planning(nieuwe_planning)
                        if new_score < score_planning(planning):
                            planning = nieuwe_planning
                            improved = True
                            logger.debug(msg=f"Iteration {iteration + 1:3n}, score (curr): {new_score:.2f}")
                            iteration += 1
                j += 1
            i += 1

    logger.debug(msg=f"2-opt ends with tour having total distance: {strafpunten}")
    planning.to_excel(output_filename, index=False)
    return planning, score_planning(planning) 

output_filename = 'Uiteindelijke_Planning.xlsx'
planning, score = two_opt(planning, ['Voor', 'Hoofd', 'Na'], output_filename, dubbel_trippel=True, buurhuis=True)

print(f"Uiteindelijke score: {score}")
print(f"Uiteindelijke planning is opgeslagen in '{output_filename}'")


# print(two_opt(planning, ['Voor', 'Hoofd', 'Na']))


