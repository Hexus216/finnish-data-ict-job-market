import requests

API_URL = (
    "https://pxdata.stat.fi/PxWeb/api/v1/fi/"
    "StatFin/tyonv/12tu.px"
)

try:
    # Haetaan API:n metatiedot
    response = requests.get(API_URL, timeout=30)

    # Tarkistetaan, onnistuiko HTTP-pyyntö
    response.raise_for_status()

    print("Yhteys onnistui!")
    print("HTTP status:", response.status_code)

except requests.exceptions.ConnectionError:
    print("Virhe: Internet-yhteyttä ei saatu muodostettua.")

except requests.exceptions.Timeout:
    print("Virhe: Palvelin ei vastannut ajoissa.")

except requests.exceptions.HTTPError as error:
    print("Virhe: Palvelin palautti HTTP-virheen:", error)

else:
    # Muutetaan API:n vastaus Pythonin sanakirjaksi
    metadata = response.json()

    # Tulostetaan API:n tarjoamat muuttujat ja niiden vaihtoehdot
    for variable in metadata["variables"]:
        print(f"\nMuuttuja: {variable['text']}")

        for code, label in zip(
            variable["values"],
            variable["valueTexts"]
        ):
            print(f"{code}: {label}")
