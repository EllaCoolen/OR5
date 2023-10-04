from score_planning import score_planning
from check_data import controleer_koppels
from DataFrames import dataframes
import random
import pandas as pd
from check_data import *
from alle_checks import alle_eisen

df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
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


def two_opt(planning, kolom):
    planning = pd.read_excel(planning)
    strafpunten = score_planning(planning)
    
    oude_planning = planning.copy()
    # planning_strafpunten = score_planning()
    logger.debug(msg=f"2-opt begint met een strafpunten score van: {strafpunten}")


    improved = True
    iteration = 0
    while improved:
        improved = False
        i = 1
        while ((i <= len(planning)-2) and not(improved)):
            j = i+1
            while((j <= len(planning)) and not(improved)): 
                if j - i == 1:
                    j += 1
                    continue  # No need to reverse two consecutive edges
                if alle_eisen(planning) == 0:
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

    return planning, score_planning(planning) 





# def main():
#     # Create a TSP instance based on a given number of cities
#     points, x, y = define_tsp_instance()
    
#     # Create an initial tour (random permutation of points)
#     tour = create_random_tour(points, x, y)

#     # Apply simulated annealing to improve the tour
#     sa_tour, sa_distance = simulated_annealing(tour, points, x, y)

#     # Finally, apply 2-opt to make sure the tour is a local optimal solution
#     optimized_tour, optimized_distance = two_opt(sa_tour, points, x, y)

#     plt.show()

#     print("Optimized tour:", optimized_tour)
#     print("Total distance:", optimized_distance)

    
# if __name__ == "__main__":
#     main()

print(two_opt(planning, 'Voor'))


# Voor = planning['Voor']       # Lijst maken werkt niet, dit moet in functie score_planning
# Hoofd = planning['Hoofd']     # Grote vriend zegt dat dit niet handig is
# Na = planning['Na']