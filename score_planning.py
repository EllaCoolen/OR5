from check_data import check_meeting


planning = 'Running Dinner eerste oplossing 2022.xlsx'

#functie om de score steeds te bepalen voor elke planning (di e voldoet aan de eisen), gebaseerd op de wensen.
def score_planning(planning) -> int:
    """ voor elke feasible solution bepalen we een score voor die planning. we zoeken de planning met de laagste score
    arguments: planning? (2-opt heuristic is het verwisselen van twee dingen)
    output: score int (we moeten verschil tussen de scores tussen het verschil meten, maar hoeft niet)
    """
    buren_dubbel = 12
    buren_trippel = 28
    dubbel, trippel = check_meeting(planning)
    
    
    strafpunten = buren_dubbel * dubbel + buren_trippel * trippel
    return strafpunten
     
print(score_planning())