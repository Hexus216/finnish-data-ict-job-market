import json
from pathlib import Path

import requests


API_URL = (
    "https://pxdata.stat.fi/PxWeb/api/v1/fi/"
    "StatFin/tyonv/12tu.px"
)

# Valitut data- ja ICT-alan ammattiryhmät
OCCUPATION_CODES = [
    "2153",
    "2511",
    "2512",
    "2514",
    "2521",
    "2522",
    "2529",
    "2120",
    "3314",
    "3512",
    "3513",
]


def fetch_data():
    """Hakee työmarkkinatilaston tiedot PxWeb API:sta."""

    # Haetaan ensin API:n metatiedot, jotta tiedämme
    # mitä kuukausia aineistossa on saatavilla.
    metadata_response = requests.get(API_URL, timeout=30)
    metadata_response.raise_for_status()

    metadata = metadata_response.json()

    # Valitaan kaikki saatavilla olevat kuukaudet vuodesta 2019 alkaen.
    time_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "timeperiod_m"
    )

    months = [
        month
        for month in time_variable["values"]
        if month >= "2019M01"
    ]

    query = {
        "query": [
            {
                "code": "Alue",
                "selection": {
                    "filter": "item",
                    "values": ["MK01", "SSS"],
                },
            },
            {
                "code": "Ammattiryhmä",
                "selection": {
                    "filter": "item",
                    "values": OCCUPATION_CODES,
                },
            },
            {
                "code": "Työmarkkina-asema",
                "selection": {
                    "filter": "item",
                    "values": ["SSS"],
                },
            },
            {
                "code": "timeperiod_m",
                "selection": {
                    "filter": "item",
                    "values": months,
                },
            },
            {
                "code": "contentscode",
                "selection": {
                    "filter": "item",
                    "values": ["AVPAIKATYHT", "HAKIJAYHT"],
                },
            },
        ],
        "response": {
            "format": "json-stat2"
        },
    }

    response = requests.post(
        API_URL,
        json=query,
        timeout=60,
    )

    if not response.ok:
        print("API:n tarkempi virheviesti:")
        print(response.text)

    response.raise_for_status()

    return response.json()


def save_raw_data(data):
    """Tallentaa alkuperäisen API-vastauksen JSON-tiedostoksi."""

    output_folder = Path(__file__).resolve().parent.parent / "data" / "raw"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "job_market_data.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Data tallennettu tiedostoon: {output_file}")


def main():
    try:
        data = fetch_data()
        save_raw_data(data)
        print("Datan haku onnistui!")

        inspect_saved_data()

    except requests.exceptions.RequestException as error:
        print("Datan hakeminen epäonnistui:", error)

def inspect_saved_data():
    """Tulostaa tallennetun JSON-datan rakenteen."""

    input_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "raw"
        / "job_market_data.json"
    )

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("\nJSON-tiedoston pääavaimet:")
    print(data.keys())

    print("\nDatan rakenne:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])


if __name__ == "__main__":
    main()
