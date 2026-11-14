import sqlite3
from pathlib import Path

import pandas as pd


# Luetaan käsitelty CSV-tiedosto
csv_file = Path("data/processed/job_market_data.csv")
df = pd.read_csv(csv_file)

# Luodaan tietokantakansio, jos sitä ei ole
Path("database").mkdir(exist_ok=True)

# Yhdistetään SQLite-tietokantaan
connection = sqlite3.connect("database/job_market.db")

# Tallennetaan Pandas-taulukko tietokantaan
df.to_sql(
    "job_market",
    connection,
    if_exists="replace",
    index=False
)

# Luetaan tietokannasta viisi ensimmäistä riviä
result = pd.read_sql(
    "SELECT * FROM job_market LIMIT 5",
    connection
)

print("\nTietokannan ensimmäiset rivit:")
print(result)

# Suljetaan tietokantayhteys
connection.close()

print("Data tallennettu SQLite-tietokantaan!")
