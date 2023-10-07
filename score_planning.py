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
    
    # if hoofd_check:
    #     hoofd_dubbel = dubbel_hoofd(planning, 'Running Dinner eerste oplossing 2022.xlsx')    # Moet nog veranderen hoe excel word ingelezen
    #     dubbel_hoofdgerecht = 8
    
    # niet_voorkeur_gang = voorkeur_gang(planning)
    # voorkeur_gangen = 6
    
    zelfde_tafelgenoot = kennissen(planning)
    punten_zelfde_tafelgenoot = 4
    
    buur = buren(planning)
    buren_meeten = 2
    
    zelfde_tafelgenoot_twee_jaar_geleden = ouwe_kennissen(planning)
    punten_zelfde_tafelgenoot_twee_jaar_geleden = 1
    
    strafpunten = buren_dubbel * dubbel + buren_trippel * trippel + punten_zelfde_tafelgenoot * zelfde_tafelgenoot + buur * buren_meeten + punten_zelfde_tafelgenoot_twee_jaar_geleden * zelfde_tafelgenoot_twee_jaar_geleden
    return strafpunten
     