import streamlit as st


st.set_page_config(
    page_title="Architecture",
    page_icon="🏗️",
    layout="wide",
)


st.title("🏗️ Space Data Lake Architecture")


st.subheader("📡 Global Architecture")

st.code(
    """
                         SOURCES
                            │
              ┌─────────────┴─────────────┐
              │                           │
           Gaia DR3                   NASA NeoWs
            Batch                     Streaming
              │                           │
              │                         Kafka
              │                           │
              │                  Spark Structured
              │                     Streaming
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                         BRONZE
                            │
                         Apache
                          Spark
                            │
                            ▼
                         SILVER
                            │
                         Apache
                          Spark
                            │
                            ▼
                          GOLD
                            │
                            ▼
                       STREAMLIT
                        DASHBOARD
    """,
    language="text",
)


st.divider()


st.subheader("🥉 Bronze")

st.markdown(
    """
    La couche Bronze conserve les données proches de leur format source.

    **Gaia :**

    `/bronze/source=gaia/year=2026/month=08/`

    **NeoWs :**

    `/bronze/source=neows/year=2026/month=8/day=27/`
    """
)


st.divider()


st.subheader("🥈 Silver")

st.markdown(
    """
    La couche Silver contient les données nettoyées et structurées.

    **Gaia :**

    `/silver/source=gaia`

    **NeoWs :**

    `/silver/source=neows`

    Les données sont stockées en **Parquet**.
    """
)


st.divider()


st.subheader("🥇 Gold")

st.markdown(
    """
    La couche Gold contient les données préparées pour l'analyse.

    **Gaia :**

    - Global KPIs
    - Temperature bands
    - Magnitude bands
    - Distance bands

    **NeoWs :**

    - KPIs des astéroïdes
    - Statistiques de dangerosité
    - Statistiques de distance
    - Statistiques de vitesse
    """
)


st.divider()


st.subheader("⚙️ Technologies")

cols = st.columns(6)

technologies = [
    "Docker",
    "HDFS",
    "Spark",
    "Kafka",
    "Airflow",
    "Streamlit",
]

for col, technology in zip(cols, technologies):

    with col:
        st.info(technology)