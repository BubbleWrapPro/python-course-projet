from collections import Counter
from itertools import combinations
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "potions-craft.xlsx"
OUTPUT = ROOT / "data" / "processed_csv" / "ingredients_cooccurrence.csv"
TOP_N = 10


def load_recipes():
    recipes = pd.read_excel(SOURCE, sheet_name="potions")
    recipes = recipes.rename(columns={"quantite_ 2": "quantite_2"})
    return recipes


def get_top_ingredients(recipes, limit=TOP_N):
    ingredient_counter = Counter()

    for _, recipe in recipes.iterrows():
        for i in range(1, 5):
            ingredient = recipe.get(f"ingredient_{i}")
            if pd.notna(ingredient):
                ingredient_counter[str(ingredient).strip()] += 1

    return [ingredient for ingredient, _ in ingredient_counter.most_common(limit)]


def build_cooccurrence_matrix(recipes, top_ingredients):
    selected = set(top_ingredients)
    ingredient_counts = {ingredient: 0 for ingredient in top_ingredients}
    pair_counts = Counter()

    for _, recipe in recipes.iterrows():
        ingredients = []
        for i in range(1, 5):
            ingredient = recipe.get(f"ingredient_{i}")
            if pd.notna(ingredient):
                ingredients.append(str(ingredient).strip())

        unique_ingredients = list(dict.fromkeys(ingredient for ingredient in ingredients if ingredient in selected))
        for ingredient in unique_ingredients:
            ingredient_counts[ingredient] += 1

        for ingredient_a, ingredient_b in combinations(sorted(unique_ingredients), 2):
            pair_counts[(ingredient_a, ingredient_b)] += 1
            pair_counts[(ingredient_b, ingredient_a)] += 1

    # Limit the matrix to 10 ingredients for readability and to emphasize the diagonal.
    matrix = pd.DataFrame(0, index=top_ingredients, columns=top_ingredients, dtype=int)

    for ingredient, count in ingredient_counts.items():
        matrix.at[ingredient, ingredient] = count

    for (ingredient_a, ingredient_b), count in pair_counts.items():
        if ingredient_a in selected and ingredient_b in selected:
            matrix.at[ingredient_a, ingredient_b] = count

    cooccurrence_scores = {
        ingredient: sum(
            matrix.at[ingredient, other]
            for other in matrix.columns
            if other != ingredient
        )
        for ingredient in matrix.index
    }
    ordered_ingredients = [
        ingredient for ingredient, _ in sorted(cooccurrence_scores.items(), key=lambda item: item[1])
    ]

    return matrix.loc[ordered_ingredients, ordered_ingredients]


def prepare_heatmap_data():
    recipes = load_recipes()
    top_ingredients = get_top_ingredients(recipes, limit=TOP_N)
    matrix = build_cooccurrence_matrix(recipes, top_ingredients)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(OUTPUT)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    prepare_heatmap_data()