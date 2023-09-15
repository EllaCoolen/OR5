from DataFrames import dataframes, verzameling
#import verzameling

def main(a, b):
    kaas = dataframes(a, b)
    salami = verzameling(kaas)
    return salami


print(main('Running Dinner dataset 2022.xlsx', 'Running Dinner eerste oplossing 2022.xlsx'))