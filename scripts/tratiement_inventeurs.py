from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_XLSX = ROOT / "data" / "potions-craft.xlsx"
OUT_DIR = ROOT / "data" / "processed_csv"
OUT_DIR.mkdir(parents=True, exist_ok=True)

NODES_CSV = OUT_DIR / "network_nodes.csv"
EDGES_CSV = OUT_DIR / "network_edges.csv"


def generate_network_csv_files():
    excel_workbook = pd.ExcelFile(DATA_XLSX)

    inventors_dataframe = pd.read_excel(excel_workbook, sheet_name="liste-inventeurs")
    # Normalize column names that may contain blank spaces
    inventors_dataframe = inventors_dataframe.rename(columns=lambda column_name: column_name.strip())

    potion_links_dataframe = pd.read_excel(excel_workbook, sheet_name="potions-inventeurs")
    potion_links_dataframe = potion_links_dataframe.rename(columns=lambda column_name: column_name.strip())

    # Build lineage nodes from the inventeurs list
    lineage_names = sorted(inventors_dataframe["lignee"].dropna().unique().astype(str))

    network_nodes = []
    network_edges = []

    # Add lineage nodes
    for lineage_name in lineage_names:
        lineage_node_id = f"lignee::{lineage_name}"
        network_nodes.append({
            "id": lineage_node_id,
            "label": lineage_name,
            "type": "lignee",
            "group": lineage_name,
            "magic_types_count": "",
            "primary_magic": "",
            "parent": "",
        })

    # Add special node for inventors without matching lineage
    no_lineage_node_id = "lignee::Sans lignée"
    network_nodes.append({
        "id": no_lineage_node_id,
        "label": "Sans lignée",
        "type": "lignee",
        "group": "Sans lignée",
        "magic_types_count": "",
        "primary_magic": "",
        "parent": "",
    })

    # Index inventeurs by pseudo for matching
    inventor_lookup_by_pseudo = {}
    for _, inventor_row in inventors_dataframe.iterrows():
        pseudo = str(inventor_row.get("pseudo")).strip()
        lineage_name = inventor_row.get("lignee") if pd.notna(inventor_row.get("lignee")) else "Sans lignée"
        
        # Count distinct magic types
        magic_type_values = [inventor_row.get(column_name) for column_name in ["type_magie_1", "type_magie_2", "type_magie_3"] if column_name in inventor_row.index]
        # Remove NaN values and get unique magic types
        magic_type_values = [magic_type for magic_type in magic_type_values if pd.notna(magic_type)]
        unique_magic_types = list(dict.fromkeys(magic_type_values))
        # Determine primary magic type (first in the list) and count of unique magic types
        primary_magic_type = unique_magic_types[0] if unique_magic_types else ""
        magic_type_count = len(unique_magic_types)
        
        
        # Create inventor node
        inventor_node_id = f"inventeur::{pseudo}"
        inventor_lookup_by_pseudo[pseudo] = {
            "id": inventor_node_id,
            "pseudo": pseudo,
            "lignee": lineage_name,
            "primary_magic": primary_magic_type,
            "magic_types_count": magic_type_count,
        }
        network_nodes.append({
            "id": inventor_node_id,
            "label": pseudo,
            "type": "inventeur",
            "group": lineage_name,
            "magic_types_count": magic_type_count,
            "primary_magic": primary_magic_type,
            "parent": f"lignee::{lineage_name}",
        })
        # add the edge that connects lignee to inventeur
        network_edges.append({"source": f"lignee::{lineage_name}", "target": inventor_node_id, "relation": "has_inventor"})



    # Now add potions as leaf nodes connected to inventeur.
    # If inventor in potions sheet doesn't match any pseudo, assign to 'Sans lignée' as inventor node created on-the-fly.
    dynamically_created_inventors = {}

    for _, potion_row in potion_links_dataframe.iterrows():
        potion_label = str(potion_row.get("potion")).strip()
        inventor_name = potion_row.get("inventeur")
        if pd.isna(inventor_name):
            inventor_name = "Inconnu"
        inventor_name = str(inventor_name).strip()

        # find a pseudo that appears in the inventor_name string
        matching_pseudo = None
        for pseudo in inventor_lookup_by_pseudo.keys():
            if pseudo in inventor_name:
                matching_pseudo = pseudo
                break

        if matching_pseudo:
            inventor_record = inventor_lookup_by_pseudo[matching_pseudo]
            inventor_node_id = inventor_record["id"]
        else:
            # create dynamic inventor node under special lineage
            # this is for inventors from potions-inventeurs that are not in liste-inventeurs
            inventor_label = inventor_name
            inventor_node_id = f"inventeur::{inventor_label}"
            if inventor_node_id not in dynamically_created_inventors:
                network_nodes.append({
                    "id": inventor_node_id,
                    "label": inventor_label,
                    "type": "inventeur",
                    "group": "Sans lignée",
                    "magic_types_count": "",
                    "primary_magic": "",
                    "parent": no_lineage_node_id,
                })
                network_edges.append({"source": no_lineage_node_id, "target": inventor_node_id, "relation": "has_inventor"})
                dynamically_created_inventors[inventor_node_id] = True



        # create potion node
        potion_node_id = f"potion::{potion_label}"
        network_nodes.append({
            "id": potion_node_id,
            "label": potion_label,
            "type": "potion",
            "group": potion_row.get("type-magie-potion") if pd.notna(potion_row.get("type-magie-potion")) else "",
            "magic_types_count": "",
            "primary_magic": potion_row.get("type-magie-potion") if pd.notna(potion_row.get("type-magie-potion")) else "",
            "parent": inventor_node_id,
        })
        network_edges.append({"source": inventor_node_id, "target": potion_node_id, "relation": "created"})

    # Save CSVs
    network_nodes_df = pd.DataFrame(network_nodes)
    network_edges_df = pd.DataFrame(network_edges)

    network_nodes_df.to_csv(NODES_CSV, index=False)
    network_edges_df.to_csv(EDGES_CSV, index=False)
    print(f"Wrote nodes -> {NODES_CSV}")
    print(f"Wrote edges -> {EDGES_CSV}")


if __name__ == "__main__":
    generate_network_csv_files()
