from score_planning import score_planning
from check_data import controleer_koppels
from DataFrames import dataframes
import random
import pandas as pd

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


def two_opt(planning):
    planning = pd.read_excel(planning)
    strafpunten = score_planning(planning)
    
    oude_planning = planning
    # planning_strafpunten = score_planning()
    logger.debug(msg=f"2-opt starts with tour having total distance: {strafpunten}")

    Voor = planning['Voor']       # Lijst maken werkt niet, dit moet in functie score_planning
    Hoofd = planning['Hoofd']
    Na = planning['Na']
    improved = True
    iteration = 0
    while improved:
        improved = False
        i = 1
        while ((i <= len(Voor)-2) and not(improved)):
            j = i+1
            while((j <= len(Voor)) and not(improved)): 
                if j - i == 1:
                    j += 1
                    continue  # No need to reverse two consecutive edges

                nieuwe_planning = Voor[:]
                nieuwe_planning.iloc[i:j] = reversed(Voor.iloc[i:j])          # reversed werkt niet voor series, iloc nodig voor series
                if score_planning(nieuwe_planning) < score_planning(Voor):
                    Voor = nieuwe_planning
                    current_distance = score_planning(Voor)
                    improved = True
                    logger.debug(msg=f"Iteration {iteration+1:3n}, distance (curr): {current_distance:.2f}")
                    iteration += 1
                j += 1
            i += 1



    for i in range(1, len(strafpunten)):
        x1, y1 = strafpunten[oude_planning[i - 1]]
        x2, y2 = strafpunten[oude_planning[i]]
        plt.plot([x1, x2], [y1, y2], 'g-',linewidth=1)  
    x1, y1 = strafpunten[oude_planning[len(strafpunten)-1]]
    x2, y2 = strafpunten[oude_planning[0]]
    plt.plot([x1, x2], [y1, y2], 'g-',linewidth=1)  
    for i in range(1, len(strafpunten)):
        x1, y1 = strafpunten[planning[i - 1]]
        x2, y2 = strafpunten[planning[i]]
        plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
    x1, y1 = strafpunten[planning[len(strafpunten)-1]]
    x2, y2 = strafpunten[planning[0]]
    plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
    plt.title(f'Tours after applying 2-opt')

    logger.debug(msg=f"2-opt ends with tour having total distance: {strafpunten}")

    return planning, score_planning() 





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

print(two_opt(planning))