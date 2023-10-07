import pandas as pd
import logging
import sys
from score_planning import score_planning
from DataFrames import dataframes
from alle_checks import alle_eisen

def two_opt(planning, kolommen, output_filename):
    planning = pd.read_excel(planning)
    strafpunten = score_planning(planning)
    
    logger.debug(msg=f"2-opt begint met een strafpunten score van: {strafpunten}")

    improved = True
    iteration = 0
    planning_len = len(planning)
    while improved:
        improved = False
        for kolom in kolommen:
            for i in range(1, planning_len - 1):
                for j in range(i + 2, planning_len):
                    if alle_eisen(planning) == 0:
                        nieuwe_planning = planning.copy()
                        nieuwe_planning.loc[i, kolom], nieuwe_planning.loc[j, kolom] = nieuwe_planning.loc[j, kolom], nieuwe_planning.loc[i, kolom]
                        new_score = score_planning(nieuwe_planning)
                        if new_score < strafpunten:
                            planning = nieuwe_planning
                            strafpunten = new_score
                            improved = True
                            logger.debug(msg=f"Iteration {iteration + 1:3n}, score (curr): {new_score:.2f}")
                            iteration += 1
                            print(i, j)

    logger.debug(msg=f"2-opt ends with tour having total distance: {strafpunten}")
    planning.to_excel(output_filename, index=False)
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
    planning, score = two_opt(planning, kolommen, output_filename)

    print(f"Uiteindelijke score: {score}")
    print(f"Uiteindelijke planning is opgeslagen in '{output_filename}'")


