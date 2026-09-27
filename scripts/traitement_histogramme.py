import pandas as pd
from pathlib import Path

SOURCE = Path("data") / "potions-craft.xlsx"
OUTPUT = Path("data") / "processed_csv" / "potions_plus_rentables.csv"
OUTPUT_NB_POTIONS = Path("data") / "processed_csv" / "nb_potions_par_competence.csv"

def load_tables():
    """
    Loads the necessary tables from the source Excel file and returns them as pandas DataFrames.
    """
    potions = pd.read_excel(SOURCE, sheet_name="potions")
    ingredients = pd.read_excel(SOURCE, sheet_name="liste-ingredients")
    diluants = pd.read_excel(SOURCE, sheet_name="prix-diluants")
    units = pd.read_excel(SOURCE, sheet_name="unites")
    magic = pd.read_excel(SOURCE, sheet_name="potions-inventeurs")
    competences = pd.read_excel(SOURCE, sheet_name="liste-types-de-magie")

    # faute de frappe dans le fichier source, on corrige le nom de la colonne
    potions = potions.rename(columns={"quantite_ 2": "quantite_2"})

    return potions, ingredients, diluants, units, magic, competences


def build_unit_map(units):
    # unit conversion to pinch
    unit_map = {"Pincée": 1.0}
    unit_map["Soufle"] = units.loc[0, "quantite_1"]
    unit_map["Nuage"] = unit_map["Soufle"] * units.loc[1, "quantite_1"]
    unit_map["Poignée"] = unit_map["Nuage"] * units.loc[2, "quantite_1"]
    unit_map["Once"] = unit_map["Poignée"] * units.loc[3, "quantite_1"]
    return unit_map


def compute_cost(recipe, ingredients, unit_map, diluants):
    """
    Computes the total cost of producing a potion based on its recipe, ingredient prices, and diluant price.
    Returns None if any ingredient is missing from the ingredients DataFrame.
    """
    total_cost = 0

    for i in range(1, 5):
        ingredient_name = recipe[f"ingredient_{i}"]
        # Check if the ingredient name is missing
        if pd.isna(ingredient_name):
            continue
        # Check if the ingredient exists in the ingredients DataFrame
        if ingredient_name not in ingredients.index:
            return None
        # Get the ingredient row from the ingredients DataFrame
        ingredient_row = ingredients.loc[ingredient_name]

        quantity = recipe[f"quantite_{i}"]
        unit = recipe[f"unite_{i}"]
        converted_quantity = quantity * unit_map[unit]

        price_per_pinch = ingredient_row["prix"] / ingredient_row["poids_pincee"]
        total_cost += converted_quantity * price_per_pinch

    # Add the cost of the diluant
    diluant_price = diluants[diluants["diluant"] == recipe["diluant"]].iloc[0]["prix"]
    total_cost += diluant_price

    return total_cost

def count_potions(potions, competences):
    """
    Count the number of potions for each competence that its type is related to
    """
    # on fait un dictionnaire avec toutes les compétences sans doublons initialisées à 0
    all_skills = competences.str.split(";").explode().unique()
    nb_potions_by_competence = {competence: 0 for competence in all_skills}
    for potion in potions:
        magic_type = str(potion)
        if magic_type in competences.index:
            for current_competence in competences[magic_type].split(";"):
                nb_potions_by_competence[current_competence] += 1
        else :
            print(f"Warning: Potion '{potion.index}' has an unknown magic type '{magic_type}'")

    return nb_potions_by_competence

def prepare_histogram():
    """
    Prepares the data for the histogram of the most profitable potions and saves it to a CSV file.
    """
    potions, ingredients, diluants, units, magic, competences = load_tables()

    # Set the index for ingredients, magic, and competences DataFrames for easier lookup
    unit_map = build_unit_map(units)
    ingredients = ingredients.set_index("ingredients")
    magic = magic.set_index("potion")["type-magie-potion"]
    competences = competences.set_index("type_de_magie")["competences"]
    nb_potions = count_potions(magic, competences)

    # Make sure to save the number of potions per competence to a CSV file
    potions_df = pd.DataFrame(list(nb_potions.items()), columns=["competences", "nombre_de_potions"])
    potions_df.to_csv(OUTPUT_NB_POTIONS, index=False)
    print("Saved: " + str(OUTPUT_NB_POTIONS))
    

    valid_rows = []

    # Use the previous function to compute the cost and benefit for each potion, and store the valid results.
    for _, recipe in potions.iterrows():
        cost = compute_cost(recipe, ingredients, unit_map, diluants)
        if cost is None:
            continue

        sale_price = recipe["prix"]
        benefit = sale_price - cost
        competence_potion = competences.get(magic.get(recipe["potion"]))

        valid_rows.append({
            "potion": recipe["potion"],
            "type_magie": magic.get(recipe["potion"]),
            "prix_vente": sale_price,
            "cout_fabrication": cost,
            "benefice": benefit,
            "competences": competence_potion,
        })

    # Create a DataFrame from the valid rows, sort by benefit, and save the top 10 most profitable potions to a CSV file.
    df = pd.DataFrame(valid_rows)
    df = df.sort_values("benefice", ascending=False).head(10).round(2)
    df.to_csv(OUTPUT, index=False)

    print("Saved: " + str(OUTPUT))


if __name__ == "__main__":
    prepare_histogram()