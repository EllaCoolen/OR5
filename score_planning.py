#functie om de score steeds te bepalen voor elke planning (di e voldoet aan de eisen), gebaseerd op de wensen.
def score_planning(planning) -> int:
    """ voor elke feasible solution bepalen we een score voor die planning. we zoeken de planning met de laagste score
    arguments: planning? (2-opt heuristic is het verwisselen van twee dingen)
    output: score int (we moeten verschil tussen de scores tussen het verschil meten, maar hoeft niet)
    """
    buren_samen = 1
     