import pandas as pd
import logging
import sys
from score_planning import score_planning
from DataFrames import dataframes
from alle_checks import alle_eisen
import matplotlib as plt

def two_opt(planning, kolommen, output_filename, df_paren):
    planning = pd.read_excel(planning)
    strafpunten = score_planning(planning, df_buren)
    
    logger.debug(msg=f"2-opt begint met een strafpunten score van: {strafpunten}")

    improved = True
    verbetering =0
    iteraties = []
    hist_best_obj_vals = []
    huidige_score = score_planning(planning, df_buren)
    beste_score = huidige_score
    hist_best_obj_vals.append(beste_score)
    planning_len = len(planning)
    while improved:
        improved = False
        for kolom in kolommen:
            for i in range(1, planning_len - 1):
                for j in range(i + 2, planning_len):
                    if alle_eisen(planning, df_paren) == 0:
                        nieuwe_planning = planning.copy()
                        nieuwe_planning.loc[i, kolom], nieuwe_planning.loc[j, kolom] = nieuwe_planning.loc[j, kolom], nieuwe_planning.loc[i, kolom]
                        new_score = score_planning(nieuwe_planning, df_buren)
                        if alle_eisen(nieuwe_planning, df_paren) ==0:
                            if new_score < strafpunten:
                                planning = nieuwe_planning
                                strafpunten = new_score
                                improved = True
                                logger.debug(msg=f"Iteration {iteration + 1:3n}, score (curr): {new_score:.2f}")
                                verbetering += 1
                                print(i, j)
                            hist_best_obj_vals.append(strafpunten)

    plt.figure()
    x = list(range(len(iteraties)))
    y=[bestobjval for bestobjval in hist_best_obj_vals]
    plt.plot(x,y)
    plt.xlabel('Iteraties')
    plt.ylabel('Score/strafpunten')
    plt.title(f'Voortgang van het two-opt algoritme van het Running Dinner probleem')

    logger.debug(msg=f"2-opt ends with tour having total distance: {strafpunten}")
    planning= planning.to_excel(output_filename, index=False)
    return planning, strafpunten 

if __name__ == "__main__":
    df_bewoners, df_adressen, df_paren, df_buren, df_kookte_2021, df_tafelgenoot_2021 = dataframes('Running Dinner dataset 2023 v2.xlsx')
    planning = 'Running Dinner eerste oplossing 2023 v2.xlsx'
    output_filename = 'Uiteindelijke_Planning.xlsx'
    logger = logging.getLogger(name='sa-logger')
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(message)s',
                        handlers=[logging.FileHandler("sa.log"), logging.StreamHandler(stream=sys.stdout)])
    logging.getLogger('matplotlib.font_manager').disabled = True

    kolommen = ['Voor', 'Hoofd', 'Na']
    planning1, score1 = two_opt(planning, kolommen, output_filename, df_paren)
    # planning2, score2 = two_opt(planning1, 'Hoofd', output_filename, df_paren)
    # planning3, score3= two_opt(planning2, 'Na', output_filename, df_paren)

    print(f"Uiteindelijke score: {score1}")
    print(f"Uiteindelijke planning is opgeslagen in '{output_filename}'")


