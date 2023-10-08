from wensen import *

#functie om de score steeds te bepalen voor elke planning (di e voldoet aan de eisen), gebaseerd op de wensen.
def score_planning(planning, df_buren, dubbel_trippel=True, buurhuis=True) -> int:
    """ voor elke feasible solution bepalen we een score voor die planning. we zoeken de planning met de laagste score
    arguments: planning? (2-opt heuristic is het verwisselen van twee dingen)
    output: score int (we moeten verschil tussen de scores tussen het verschil meten, maar hoeft niet)
    """
    punten_buren_dubbel = 0
    punten_buren_trippel = 0
    punten_dubbel_hoofdgerecht = 0
    punten_voorkeur_gangen = 0
    punten_zelfde_tafelgenoot = 0
    punten_buren_meeten = 0
    punten_zelfde_tafelgenoot_twee_jaar_geleden = 0
    
    dubbel = 0
    trippel = 0
    hoofd_dubbel = 0
    niet_voorkeur_gang = 0
    zelfde_tafelgenoot = 0
    buur = 0
    zelfde_tafelgenoot_twee_jaar_geleden = 0
    
    if dubbel_trippel:
        punten_buren_dubbel = 12
        punten_buren_trippel = 28
        dubbel, trippel = check_meeting(planning)
    
    # if hoofd_check:
    #     punten_dubbel_hoofdgerecht = 8
    #     hoofd_dubbel = dubbel_hoofd(planning, 'Running Dinner eerste oplossing 2022.xlsx')    # Moet nog veranderen hoe excel word ingelezen
    
    # if gang:
    #     niet_voorkeur_gang = voorkeur_gang(planning)
    #     punten_voorkeur_gangen = 6
    
    # if tafelgenoot:
    #     zelfde_tafelgenoot = kennissen(planning)
    #     punten_zelfde_tafelgenoot = 4
    
    if buurhuis:
        buur = buren(planning, df_buren)
        punten_buren_meeten = 2
    
    # if twee_tafelgenoot:
    #     zelfde_tafelgenoot_twee_jaar_geleden = ouwe_kennissen(planning)
    #     punten_zelfde_tafelgenoot_twee_jaar_geleden = 1
    
    strafpunten = punten_buren_dubbel * dubbel + punten_buren_trippel * trippel + punten_dubbel_hoofdgerecht * hoofd_dubbel + punten_voorkeur_gangen * niet_voorkeur_gang + punten_zelfde_tafelgenoot * zelfde_tafelgenoot + buur * punten_buren_meeten + punten_zelfde_tafelgenoot_twee_jaar_geleden * zelfde_tafelgenoot_twee_jaar_geleden
    return strafpunten
     