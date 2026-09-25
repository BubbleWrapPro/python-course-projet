import pandas as pd

# Returns a DataFrame
potions_data = pd.read_excel("./data/potions-craft.xlsx", sheet_name="potions")

print(potions_data.values)