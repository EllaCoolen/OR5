from wensen import *

#functie om de score steeds te bepalen voor elke planning (di e voldoet aan de eisen), gebaseerd op de wensen.
def score_planning(planning) -> int:
    """ voor elke feasible solution bepalen we een score voor die planning. we zoeken de planning met de laagste score
    arguments: planning? (2-opt heuristic is het verwisselen van twee dingen)
    output: score int (we moeten verschil tussen de scores tussen het verschil meten, maar hoeft niet)
    """
    buren_dubbel = 12
    buren_trippel = 28
    dubbel, trippel = check_meeting(planning)
    
    hoofd_dubbel = dubbel_hoofd(planning, 'Running Dinner eerste oplossing 2022.xlsx')    # Moet nog veranderen hoe excel word ingelezen
    dubbel_hoofdgerecht = 8
    
    niet_voorkeur_gang = voorkeur_gang(planning)
    voorkeur_gang = 6
    
    buren = buren(planning)
    buren_meeten = 2
    
    strafpunten = buren_dubbel * dubbel + buren_trippel * trippel + hoofd_dubbel * dubbel_hoofdgerecht + voorkeur_gang * niet_voorkeur_gang + buren * buren_meeten
    return strafpunten
     