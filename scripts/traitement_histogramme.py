import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "potions-craft.xlsx"
OUTPUT = ROOT / "data" / "processed_csv" / "potions_plus_rentables.csv"

def load_tables():
    potions = pd.read_excel(SOURCE, sheet_name="potions")
    ingredients = pd.read_excel(SOURCE, sheet_name="liste-ingredients")
    diluants = pd.read_excel(SOURCE, sheet_name="prix-diluants")
    units = pd.read_excel(SOURCE, sheet_name="unites")
    magic = pd.read_excel(SOURCE, sheet_name="potions-inventeurs")

    # faute de frappe dans le fichier source, on corrige le nom de la colonne
    potions = potions.rename(columns={"quantite_ 2": "quantite_2"})

    return potions, ingredients, diluants, units, magic


def build_unit_map(units):
    # unit conversion to pinch
    unit_map = {"Pincée": 1.0}
    unit_map["Soufle"] = units.loc[0, "quantite_1"]
    unit_map["Nuage"] = unit_map["Soufle"] * units.loc[1, "quantite_1"]
    unit_map["Poignée"] = unit_map["Nuage"] * units.loc[2, "quantite_1"]
    unit_map["Once"] = unit_map["Poignée"] * units.loc[3, "quantite_1"]
    return unit_map


def compute_cost(recipe, ingredients, unit_map, diluants):
    total_cost = 0

    for i in range(1, 5):
        ingredient_name = recipe[f"ingredient_{i}"]
        if pd.isna(ingredient_name):
            continue

        if ingredient_name not in ingredients.index:
            print(f"Excluded: {recipe['potion']} -> missing ingredient {ingredient_name}")
            return None
        
        ingredient_row = ingredients.loc[ingredient_name]

        quantity = recipe[f"quantite_{i}"]
        unit = recipe[f"unite_{i}"]
        converted_quantity = quantity * unit_map[unit]

        price_per_pinch = ingredient_row["prix"] / ingredient_row["poids_pincee"]
        total_cost += converted_quantity * price_per_pinch

    diluant_price = diluants[diluants["diluant"] == recipe["diluant"]].iloc[0]["prix"]
    total_cost += diluant_price

    return total_cost


def prepare_histogram():
    potions, ingredients, diluants, units, magic = load_tables()

    unit_map = build_unit_map(units)
    ingredients = ingredients.set_index("ingredients")
    magic = magic.set_index("potion")["type-magie-potion"]

    valid_rows = []

    for _, recipe in potions.iterrows():
        cost = compute_cost(recipe, ingredients, unit_map, diluants)
        if cost is None:
            continue

        sale_price = recipe["prix"]
        benefit = sale_price - cost

        valid_rows.append({
            "potion": recipe["potion"],
            "type_magie": magic.get(recipe["potion"]),
            "prix_vente": sale_price,
            "cout_fabrication": cost,
            "benefice": benefit
        })

    df = pd.DataFrame(valid_rows)
    df = df.sort_values("benefice", ascending=False).head(10).round(2)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    print("Saved: " + str(OUTPUT))


if __name__ == "__main__":
    prepare_histogram()