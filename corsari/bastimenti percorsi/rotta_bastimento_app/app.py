from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


REQUIRED_COLUMNS = ("nome", "long", "lat")


def read_locations(uploaded_file) -> pd.DataFrame:
    """Read CSV or Excel data, normalize headers, and validate route points."""
    filename = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if filename.endswith(".csv"):
        try:
            frame = pd.read_csv(BytesIO(raw), sep=None, engine="python")
        except UnicodeDecodeError:
            frame = pd.read_csv(BytesIO(raw), sep=None, engine="python", encoding="latin-1")
    elif filename.endswith(".xlsx"):
        frame = pd.read_excel(BytesIO(raw), engine="openpyxl")
    else:
        raise ValueError("Formato non supportato. Carica un file .csv oppure .xlsx.")

    frame.columns = [str(column).strip().lower() for column in frame.columns]
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError("Colonne mancanti: " + ", ".join(missing))

    route = frame.loc[:, REQUIRED_COLUMNS].copy()
    route["nome"] = route["nome"].astype("string").str.strip()
    for column in ("long", "lat"):
        route[column] = pd.to_numeric(route[column], errors="coerce")

    bad_rows = route[
        route["nome"].isna()
        | route["nome"].eq("")
        | route["long"].isna()
        | route["lat"].isna()
        | ~route["long"].between(-180, 180)
        | ~route["lat"].between(-90, 90)
    ].index
    if len(bad_rows):
        rows = ", ".join(str(index + 2) for index in bad_rows[:10])
        suffix = "…" if len(bad_rows) > 10 else ""
        raise ValueError(f"Dati non validi alle righe del foglio: {rows}{suffix}.")
    if len(route) < 2:
        raise ValueError("Servono almeno due località per disegnare uno spostamento.")

    route.insert(0, "tappa", range(1, len(route) + 1))
    return route.reset_index(drop=True)


def build_route_map(route: pd.DataFrame, frame_ms: int) -> go.Figure:
    labels = route["tappa"].astype(str) + ". " + route["nome"].astype(str)
    figure = go.Figure()
    figure.add_trace(
        go.Scattermap(
            lon=route["long"],
            lat=route["lat"],
            mode="lines+markers+text",
            line={"width": 4, "color": "#0b6e75"},
            marker={"size": 10, "color": "#f4a261"},
            text=route["tappa"].astype(str),
            textposition="top center",
            customdata=labels,
            hovertemplate="%{customdata}<br>Lat: %{lat:.5f}<br>Long: %{lon:.5f}<extra></extra>",
            name="Rotta",
        )
    )
    figure.add_trace(
        go.Scattermap(
            lon=[route.iloc[0]["long"]],
            lat=[route.iloc[0]["lat"]],
            mode="text",
            text=["🚢"],
            textfont={"size": 30},
            hovertext=[labels.iloc[0]],
            hoverinfo="text",
            name="Bastimento",
        )
    )

    figure.frames = [
        go.Frame(
            name=str(row.tappa),
            data=[
                go.Scattermap(
                    lon=[row.long], lat=[row.lat], mode="text", text=["🚢"], textfont={"size": 30}
                )
            ],
            traces=[1],
        )
        for row in route.itertuples()
    ]
    steps = [
        {
            "label": str(row.tappa),
            "method": "animate",
            "args": [[str(row.tappa)], {"mode": "immediate", "frame": {"duration": frame_ms, "redraw": True}}],
        }
        for row in route.itertuples()
    ]
    figure.update_layout(
        map={"style": "open-street-map", "center": {"lat": route["lat"].mean(), "lon": route["long"].mean()}},
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        height=650,
        showlegend=False,
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0,
                "y": 0,
                "buttons": [
                    {
                        "label": "▶ Avvia",
                        "method": "animate",
                        "args": [None, {"fromcurrent": True, "frame": {"duration": frame_ms, "redraw": True}, "transition": {"duration": 200}}],
                    },
                    {
                        "label": "⏸ Pausa",
                        "method": "animate",
                        "args": [[None], {"mode": "immediate", "frame": {"duration": 0, "redraw": False}}],
                    },
                ],
            }
        ],
        sliders=[{"active": 0, "currentvalue": {"prefix": "Tappa: "}, "steps": steps, "pad": {"t": 45}}],
    )
    return figure


st.set_page_config(page_title="Rotta del bastimento", page_icon="🚢", layout="wide")
st.title("🚢 Rotta del bastimento")
st.caption("Carica le località: l’ordine delle righe determina l’ordine dello spostamento.")

with st.sidebar:
    st.header("Dati della rotta")
    uploaded = st.file_uploader("Foglio CSV o Excel", type=["csv", "xlsx"])
    speed = st.slider("Durata per tappa (secondi)", 0.3, 3.0, 1.0, 0.1)
    st.info("Colonne richieste: nome, long, lat")

if uploaded is None:
    st.subheader("Come iniziare")
    st.markdown(
        "1. Prepara un foglio con le colonne `nome`, `long`, `lat`.\n"
        "2. Inserisci le tappe nell’ordine del viaggio.\n"
        "3. Carica il file dal pannello laterale."
    )
    sample_path = Path(__file__).with_name("esempio_rotta.csv")
    st.download_button(
        "Scarica il CSV di esempio",
        sample_path.read_bytes(),
        file_name="esempio_rotta.csv",
        mime="text/csv",
    )
else:
    try:
        locations = read_locations(uploaded)
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    st.success(f"Rotta caricata: {len(locations)} tappe, da {locations.iloc[0]['nome']} a {locations.iloc[-1]['nome']}.")
    map_tab, data_tab = st.tabs(["Mappa", "Tappe"])
    with map_tab:
        st.plotly_chart(build_route_map(locations, int(speed * 1000)), use_container_width=True)
    with data_tab:
        st.dataframe(locations, hide_index=True, use_container_width=True)

