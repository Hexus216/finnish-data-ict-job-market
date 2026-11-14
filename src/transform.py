import json
from itertools import product
from pathlib import Path

import pandas as pd


def load_json_data():
    """Lukee alkuperäisen JSON-tiedoston."""

    input_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "raw"
        / "job_market_data.json"
    )

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def transform_data(data):
    """Muuttaa JSON-stat2-datan Pandas-taulukoksi."""

    dimension_ids = data["id"]
    values = data["value"]

    # Selvitetään jokaisen ulottuvuuden kategoriat
    # oikeassa järjestyksessä.
    categories = []

    for dimension_id in dimension_ids:
        category = data["dimension"][dimension_id]["category"]
        index = category.get("index")

        if isinstance(index, dict):
            category_ids = sorted(index, key=index.get)
        elif isinstance(index, list):
            category_ids = index
        else:
            category_ids = list(category.get("label", {}).keys())

        categories.append(category_ids)

    # Muodostetaan kaikki mahdolliset yhdistelmät.
    combinations = product(*categories)

    rows = []

    for position, combination in enumerate(combinations):

        row = {}

        for dimension_id, category_id in zip(
            dimension_ids, combination
        ):
            category_labels = (
                data["dimension"][dimension_id]["category"].get(
                    "label", {}
                )
            )

            row[dimension_id + "_code"] = category_id
            row[dimension_id] = category_labels.get(
                category_id, category_id
            )

        row["value"] = values[position]

        rows.append(row)

    df = pd.DataFrame(rows)

    df = df.sort_values(
    [
        "Alue_code",
        "Ammattiryhmä_code",
        "Työmarkkina-asema_code",
        "contentscode_code",
        "timeperiod_m_code"
    ]
    )

    # Haetaan edellisen kuukauden arvo samalle ryhmälle
    previous_value = df.groupby(
    [
        "Alue_code",
        "Ammattiryhmä_code",
        "Työmarkkina-asema_code",
        "contentscode_code"
    ]
    )["value"].shift(1)

    # Lasketaan muutos prosentteina
    df["muutos_prosenttia"] = (
    (df["value"] - previous_value) / previous_value * 100
    ).where(previous_value != 0).round(1)


    return df

def save_processed_data(df):
    """Tallentaa muunnetun datan CSV-tiedostoksi."""

    output_folder = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processed"
    )

    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "job_market_data.csv"

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nMuunnettu data tallennettu: {output_file}")

def main():
    data = load_json_data()
    df = transform_data(data)

    print("\nMuunnetun datan ensimmäiset rivit:")
    print(df.head(10))

    print("\nDatan koko:")
    print(df.shape)

    print("\nPuuttuvien arvojen määrä:")
    print(df.isnull().sum())

    print("\nEsimerkkejä puuttuvista havainnoista:")
    print(df[df["value"].isnull()].head(10))

    print("\nPuuttuvat arvot mittareittain:")
    print(
    df.groupby("contentscode")["value"]
    .apply(lambda column: column.isnull().sum())
)

    print("\nPuuttuvat arvot ammattiryhmittäin:")
    print(
    df.groupby("Ammattiryhmä")["value"]
    .apply(lambda column: column.isnull().sum())
)
    print("\nDuplikaattien määrä:")
    print(df.duplicated().sum())

    save_processed_data(df)

if __name__ == "__main__":
    main()
