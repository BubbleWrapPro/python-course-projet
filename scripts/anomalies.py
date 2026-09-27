import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

# Workbook path and names of the sheets to inspect.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "potions-craft.xlsx"
SHEET_NAMES = (
    "potions",
    "prix-diluants",
    "unites",
    "potions-inventeurs",
    "liste-ingredients",
    "liste-inventeurs",
    "liste-types-de-magie",
)


def _normaliser(value: object) -> str:
    # Standardize text to compare accents, capitalization, and spacing without false differences.
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(character for character in text if not unicodedata.combining(character))
    return " ".join(text.casefold().split())


def _cle_orthographique(value: object) -> str:
    # Also remove spaces and punctuation to identify spelling variants.
    return "".join(character for character in _normaliser(value) if character.isalnum())


def _est_renseigne(value: object) -> bool:
    # Treat a field containing only whitespace as empty.
    return bool(_normaliser(value))


def detect_anomalies(source: Path = SOURCE) -> pd.DataFrame:
    """Recense les références absentes, variantes d'orthographe et champs incomplets."""
    # Load the seven workbook sheets and correct the misspelled header in memory.
    tables = {
        sheet: pd.read_excel(source, sheet_name=sheet)
        for sheet in SHEET_NAMES
    }
    tables["potions"] = tables["potions"].rename(
        columns={"quantite_ 2": "quantite_2"}
    )

    # Columns that must be present and populated in each sheet.
    required_columns = {
        "potions": (
            "potion", "diluant", "prix",
        ),
        "prix-diluants": ("diluant", "prix"),
        "unites": ("quantite_1", "unite_1", "quantite_2", "unite_2"),
        "potions-inventeurs": ("potion", "type-magie-potion", "inventeur"),
        "liste-ingredients": ("ingredients", "poids_pincee", "prix", "type"),
        "liste-inventeurs": (
            "pseudo", "lignee", "numero_permis", "type_magie_1",
            "elements", "benediction",
        ),
        "liste-types-de-magie": ("type_de_magie", "competences"),
    }
    # Check that all required columns are present in each sheet.
    for sheet, columns in required_columns.items():
        missing_columns = [column for column in columns if column not in tables[sheet]]
        if missing_columns:
            raise ValueError(
                f"Colonnes manquantes dans la feuille '{sheet}': "
                f"{', '.join(missing_columns)}"
            )

    # Also check the columns for all four possible ingredient slots.
    recipe_slot_columns = tuple(
        f"{field}_{slot}"
        for slot in range(1, 5)
        for field in ("ingredient", "quantite", "unite", "temperature")
    )
    # Check that all recipe columns are present in the "potions" sheet.
    missing_recipe_columns = [
        column for column in recipe_slot_columns if column not in tables["potions"]
    ]
    
    # Raise a specific error if any recipe columns are missing.
    if missing_recipe_columns:
        raise ValueError(
            "Colonnes de recette manquantes dans la feuille 'potions': "
            f"{', '.join(missing_recipe_columns)}"
        )

    # Shared list that will hold one entry for each anomaly found.
    # Each entry is a dictionary with these keys: Sheet, Excel row, Anomaly, Field, Value, and Details.
    findings: list[dict[str, object]] = []

    # Add an anomaly with its sheet, Excel row, and relevant details.
    def add(
        sheet: str,
        row_number: int,
        category: str,
        field: str,
        value: object,
        detail: str,
    ) -> None:
        findings.append({
            "Feuille": sheet,
            "Ligne Excel": row_number,
            "Anomalie": category,
            "Champ": field,
            "Valeur": "" if pd.isna(value) else str(value),
            "Détail": detail,
        })

    # Report missing required fields in the reference and linking sheets.
    for sheet, columns in required_columns.items():
        for index, row in tables[sheet].iterrows():
            for column in columns:
                if not _est_renseigne(row[column]):
                    add(
                        sheet, int(index) + 2, "Ligne incomplète", column,
                        row[column], f"Valeur requise absente dans '{column}'.",
                    )

    # Compare a populated value with the allowed values in its reference list.
    def report_unknown(
        sheet: str,
        row_number: int,
        field: str,
        value: object,
        allowed_values: set[str],
        reference_name: str,
    ) -> None:
        if _est_renseigne(value) and _normaliser(value) not in allowed_values:
            add(
                sheet, row_number, "Référence absente", field, value,
                f"Valeur absente du référentiel '{reference_name}'.",
            )

    # Prepare normalized reference lists for consistency checks.
    # A reference list contains allowed values for a field, such as known ingredients or magic types.
    ingredient_names = {
        _normaliser(value)
        for value in tables["liste-ingredients"]["ingredients"]
        if _est_renseigne(value)
    }
    units = {
        _normaliser(value)
        for column in ("unite_1", "unite_2") # Vérification supplémentaire ici car une équivalence est obligatoire pour les deux colonnes d'unités.
        for value in tables["unites"][column]
        if _est_renseigne(value)
    }
    diluants = {
        _normaliser(value)
        for value in tables["prix-diluants"]["diluant"]
        if _est_renseigne(value)
    }
    potion_names = {
        _normaliser(value)
        for value in tables["potions"]["potion"]
        if _est_renseigne(value)
    }
    magic_types = {
        _normaliser(value)
        for value in tables["liste-types-de-magie"]["type_de_magie"]
        if _est_renseigne(value)
    }

    # Check diluants, then ingredients and their associated fields in each recipe.
    for index, recipe in tables["potions"].iterrows():
        row_number = int(index) + 2
        # Report unknown diluants in the "potions" sheet.
        report_unknown(
            "potions", row_number, "diluant", recipe["diluant"], diluants,
            "prix-diluants.diluant",
        )
        # Check all four ingredient slots for each recipe.
        for slot in range(1, 5):
            ingredient_column = f"ingredient_{slot}"
            quantity_column = f"quantite_{slot}"
            unit_column = f"unite_{slot}"
            temperature_column = f"temperature_{slot}"
            if ingredient_column not in recipe.index:
                continue

            # Check that the associated fields are populated whenever an ingredient is specified.
            slot_fields = (
                ingredient_column, quantity_column, unit_column, temperature_column,
            )
            # Check the other fields if an ingredient is specified or this is the first slot.
            populated = [column for column in slot_fields if _est_renseigne(recipe[column])]
            if slot == 1 or populated:
                for column in slot_fields:
                    if column in recipe.index and not _est_renseigne(recipe[column]):
                        add(
                            "potions", row_number, "Ligne incomplète", column,
                            recipe[column], f"Champ absent pour l'ingrédient {slot}.",
                        )
            # Check that the ingredient and unit are present in their respective reference lists.
            if _est_renseigne(recipe[ingredient_column]):
                report_unknown(
                    "potions", row_number, ingredient_column, recipe[ingredient_column],
                    ingredient_names, "liste-ingredients.ingredients",
                )
            # Check that the unit is present in the units reference list.
            if _est_renseigne(recipe[unit_column]):
                report_unknown(
                    "potions", row_number, unit_column, recipe[unit_column],
                    units, "unites",
                )

    # Build inventors' full names from their pseudonyms and lineages.
    inventor_rows = tables["liste-inventeurs"]
    canonical_inventors = {
        f"{row['pseudo']} {row['lignee']}".strip()
        for _, row in inventor_rows.iterrows()
        if _est_renseigne(row["pseudo"]) and _est_renseigne(row["lignee"]) # Ignore les inventeurs dont le pseudo ou la lignée est manquant, car ils ne peuvent pas être correctement identifiés.
    }
    # Create a dictionary to identify spelling variants of known inventors.
    canonical_by_key = {
        _cle_orthographique(name): name for name in canonical_inventors
    }

    # Check links to potions, magic types, and inventors.
    for index, link in tables["potions-inventeurs"].iterrows():
        row_number = int(index) + 2
        report_unknown(
            "potions-inventeurs", row_number, "potion", link["potion"],
            potion_names, "potions.potion",
        )
        report_unknown(
            "potions-inventeurs", row_number, "type-magie-potion",
            link["type-magie-potion"], magic_types,
            "liste-types-de-magie.type_de_magie",
        )
        inventor = link["inventeur"]
        if not _est_renseigne(inventor):
            continue

        # Skip inventors whose normalized names already match the reference list.
        normalized_name = _normaliser(inventor)
        if normalized_name in {_normaliser(name) for name in canonical_inventors}:
            continue

        # Identify differences limited to accents, spaces, or punctuation.
        key = _cle_orthographique(inventor)
        if key in canonical_by_key:
            add(
                "potions-inventeurs", row_number, "Variante d'orthographe",
                "inventeur", inventor,
                f"Écriture différente de « {canonical_by_key[key]} ».",
            )
            continue

        # Automatic matching is not possible if the reference list is empty.
        if not canonical_inventors:
            add(
                "potions-inventeurs", row_number, "Référence absente",
                "inventeur", inventor,
                "Le référentiel 'liste-inventeurs' ne contient aucun inventeur.",
            )
            continue

        # Find the closest known name to detect likely typos.
        # SequenceMatcher returns a similarity score from 0 to 1, where 1 means an exact match.
        closest_name = max(
            canonical_inventors,
            key=lambda name: SequenceMatcher(
                None, key, _cle_orthographique(name)
            ).ratio(),
        )
        similarity = SequenceMatcher(
            None, key, _cle_orthographique(closest_name)
        ).ratio()
        if similarity >= 0.85: # taux arbitraire pour signaler une faute de frappe probable.
            add(
                "potions-inventeurs", row_number, "Variante d'orthographe",
                "inventeur", inventor,
                f"Écriture proche de « {closest_name} » ({similarity:.0%}).",
            )
        else:
            add(
                "potions-inventeurs", row_number, "Référence absente",
                "inventeur", inventor,
                "Inventeur absent du référentiel 'liste-inventeurs'.",
            )

    # Check that the magic types in inventor records are known.
    for index, inventor in inventor_rows.iterrows():
        row_number = int(index) + 2
        for column in ("type_magie_1", "type_magie_2", "type_magie_3"):
            if column in inventor.index:
                report_unknown(
                    "liste-inventeurs", row_number, column, inventor[column],
                    magic_types, "liste-types-de-magie.type_de_magie",
                )

    # Return the anomalies in a sorted table, ready to display in Streamlit.
    columns = ("Feuille", "Ligne Excel", "Anomalie", "Champ", "Valeur", "Détail")
    return pd.DataFrame(findings, columns=columns).sort_values(
        ["Feuille", "Ligne Excel", "Anomalie", "Champ"],
        ignore_index=True,
    )
