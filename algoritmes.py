from score_planning import score_planning
from check_data import controleer_koppels
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


# def two_opt(planning, strafpunten):
#     oude_planning = planning
#     planning_strafpunten = score_planning(planning,strafpunten)
#     logger.debug(msg=f"2-opt starts with tour having total distance: {planning_strafpunten}")


#     improved = True
#     iteration = 0
#     while improved:
#         improved = False
#         i = 1
#         while ((i <= len(planning)-2) and not(improved)):
#             j = i+1
#             while((j <= len(planning)) and not(improved)): 
#                 if j - i == 1:
#                     j += 1
#                     continue  # No need to reverse two consecutive edges

#                 new_tour = planning[:]
#                 new_tour[i:j] = reversed(planning[i:j])
#                 if score_planning(new_tour, strafpunten) < score_planning(planning, strafpunten):
#                     planning = new_tour
#                     current_distance = score_planning(planning,strafpunten)
#                     improved = True
#                     logger.debug(msg=f"Iteration {iteration+1:3n}, distance (curr): {current_distance:.2f}")
#                     iteration += 1
#                 j += 1
#             i += 1



#     for i in range(1, len(strafpunten)):
#         x1, y1 = strafpunten[oude_planning[i - 1]]
#         x2, y2 = strafpunten[oude_planning[i]]
#         plt.plot([x1, x2], [y1, y2], 'g-',linewidth=1)  
#     x1, y1 = strafpunten[oude_planning[len(strafpunten)-1]]
#     x2, y2 = strafpunten[oude_planning[0]]
#     plt.plot([x1, x2], [y1, y2], 'g-',linewidth=1)  
#     for i in range(1, len(strafpunten)):
#         x1, y1 = strafpunten[planning[i - 1]]
#         x2, y2 = strafpunten[planning[i]]
#         plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
#     x1, y1 = strafpunten[planning[len(strafpunten)-1]]
#     x2, y2 = strafpunten[planning[0]]
#     plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
#     plt.title(f'Tours after applying 2-opt')

#     logger.debug(msg=f"2-opt ends with tour having total distance: {planning_strafpunten}")

#     return planning, total_distance(planning, strafpunten) 

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
        
        # j > i+1, so the 2-exchange based on i and j is relevant 
        # remove arcs (i-1,i) and (j-1,j) and insert arcs (i-1,j-1) and (i,j)
        # resulting tour equals: 0->..->i-1->j-1->..->i->j->n-1->0 

#         new_tour = current_planning[:bewoner_a] + list(reversed(current_planning[bewoner_a:bewoner_b])) + current_planning[bewoner_b:]
#         new_distance = score_planning(new_tour, strafpunten)
#         delta_distance = new_distance - current_strafpunten

#         if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
#             current_planning = new_tour
#             current_strafpunten = new_distance

#             if current_strafpunten < minste_strafpunten:
#                 best_planning = current_planning
#                 minste_strafpunten = current_strafpunten

#         hist_curr_obj_vals.append(current_strafpunten)
#         hist_best_obj_vals.append(minste_strafpunten)
#         hist_temp_vals.append(temperature)

#         logger.debug(msg=f"Iteration {iteration+1:3n}, temp: {temperature:.2f}, distance (curr): {current_strafpunten:.2f}, (best): {minste_strafpunten:.2f}")

#         iteration += 1
#         temperature *= COOLINGRATE

#     # Create a line plot for the constructed tour
#     plt.figure(3)
#     plt.scatter(x, y)
#     plt.xlabel('X-axis Label')
#     plt.ylabel('Y-axis Label')
#     for bewoner_a in range(1, len(strafpunten)):
#         x1, y1 = strafpunten[best_planning[bewoner_a - 1]]
#         x2, y2 = strafpunten[best_planning[bewoner_a]]
#         plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
#     x1, y1 = strafpunten[best_planning[len(strafpunten)-1]]
#     x2, y2 = strafpunten[best_planning[0]]
#     plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
#     plt.title(f'Best solution: tour on {NUMBEROFCITIES} nodes, distance {minste_strafpunten:.2f}')


#     # Create a plot for the solution progress
#     plt.figure(4)
#     x = list(range(len(hist_curr_obj_vals)))
#     y1 = [currobjval for currobjval in hist_curr_obj_vals]
#     y2 = [bestobjval for bestobjval in hist_best_obj_vals]
#     y3 = [tempval for tempval in hist_temp_vals]
#     plt.plot(x, y1)
#     plt.plot(x, y2)
#     plt.plot(x, y3)

#     plt.xlabel('Iteration')
#     plt.ylabel('Distance')
#     plt.title(f'Progress of simulated annealing applied to {len(planning)} nodes')

#     return best_planning, minste_strafpunten

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

simulated_annealing(planning)

