import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# Sivun asetukset
st.set_page_config(
    page_title="Data- ja ICT-alan työmarkkinat",
    layout="wide"
)

# Luetaan tiedot SQLite-tietokannasta
database = Path(__file__).resolve().parent.parent / "database" / "job_market.db"

with sqlite3.connect(database) as connection:
    df = pd.read_sql_query("SELECT * FROM job_market", connection)

# Muotoillaan kuukaudet selkeämmin
df["Kuukausi"] = df["timeperiod_m_code"].apply(
    lambda x: f"{x[:4]}/{int(x[-2:])}"
)

# Otsikko
st.title("Suomen data- ja ICT-alan työmarkkinat")
st.caption(
    "Tarkastele työnhakijoiden ja avoimien työpaikkojen kehitystä "
    "eri ammattiryhmissä ja alueilla."
)

# Suodattimet
st.sidebar.header("Rajaa tilastoja")

area = st.sidebar.selectbox(
    "Alue",
    sorted(df["Alue"].dropna().unique())
)

occupations = sorted(df["Ammattiryhmä"].dropna().unique())

selected_occupations = st.sidebar.multiselect(
    "Ammattiryhmät",
    occupations,
    default=occupations
)

measure = st.sidebar.selectbox(
    "Mittari",
    sorted(df["contentscode"].dropna().unique())
)

# Suodatetaan aineisto valintojen mukaan
data = df[
    (df["Alue"] == area)
    & (df["Ammattiryhmä"].isin(selected_occupations))
    & (df["contentscode"] == measure)
].copy()

# Näytetään kaavio
st.subheader(measure)

chart_data = data.dropna(subset=["value"]).copy()

if not chart_data.empty:
    chart_data["Päivämäärä"] = pd.to_datetime(
        chart_data["timeperiod_m_code"].str.replace("M", "-"),
        format="%Y-%m"
    )

    chart_data = chart_data.sort_values("Päivämäärä")

    y_title = (
        "Työnhakijoita"
        if "Työnhakijoita" in measure
        else "Avoimia työpaikkoja"
    )

    fig = px.line(
        chart_data,
        x="Päivämäärä",
        y="value",
        color="Ammattiryhmä",
        markers=True,
        labels={
            "Päivämäärä": "Kuukausi",
            "value": y_title,
            "Ammattiryhmä": "Ammattiryhmä"
        }
    )

    fig.update_layout(
        height=500,
        hovermode="x unified",
        legend_title="Ammattiryhmä"
    )

    fig.update_xaxes(tickformat="%Y/%m")

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Valituilla suodattimilla ei löytynyt näytettäviä arvoja.")

# Näytetään taulukko
st.subheader("Tilastotiedot")

display_data = data[
    ["Alue", "Ammattiryhmä", "Kuukausi", "contentscode", "value", "muutos_prosenttia"]
].rename(
    columns={
        "contentscode": "Mittari",
        "value": "Määrä",
        "muutos_prosenttia": "Kuukausimuutos (%)"
    }
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)
