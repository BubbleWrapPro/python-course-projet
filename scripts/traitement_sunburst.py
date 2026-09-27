"""Prepare the potion-to-competence hierarchy for the sunburst chart."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "potions-craft.xlsx"
OUTPUT = ROOT / "data" / "processed_csv" / "sunburst_potions.csv"


def prepare_sunburst_data():
    potion_types = pd.read_excel(SOURCE, sheet_name="potions-inventeurs")
    magic_skills = pd.read_excel(SOURCE, sheet_name="liste-types-de-magie")

    # Create a mapping of magic types to corresponding skills.
    skills_by_magic = {}
    for _, row in magic_skills.iterrows():
        magic = str(row["type_de_magie"]).strip()
        skills = [
            skill.strip()
            for skill in str(row["competences"]).split(";")
            if skill.strip() and skill.strip().lower() != "nan"
        ]
        skills_by_magic[magic] = skills

    # Create a mapping of magic types to their corresponding potions.
    potions_by_magic = {}
    for _, potion in potion_types.iterrows():
        name = str(potion["potion"]).strip()
        magic = str(potion["type-magie-potion"]).strip()
        if not name or name.lower() == "nan":
            continue
        if not magic or magic.lower() == "nan":
            magic = "Type inconnu"

        potions_by_magic.setdefault(magic, []).append(name)

    # Assign each potion to a skill in a balanced way, ensuring that all skills are represented.
    # This was set arbitrarily, as the original data does not provide a direct mapping.
    rows = []
    for magic, potions in potions_by_magic.items():
        skills = skills_by_magic.get(magic, []) or ["Compétence inconnue"]
        # Assign each potion to one skill in balanced consecutive groups.
        for index, name in enumerate(potions):
            skill_index = min(index * len(skills) // len(potions), len(skills) - 1)
            rows.append(
                {
                    "type_magie": magic,
                    "competence": skills[skill_index],
                    "potion": name,
                    "poids": 1,
                }
            )

    output = pd.DataFrame(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT, index=False)
    return output


if __name__ == "__main__":
    prepare_sunburst_data()


