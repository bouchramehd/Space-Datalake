import streamlit as st

from utils.hdfs import (
    read_neows_global,
    read_neows_by_date,
    read_neows_hazard,
)


st.set_page_config(
    page_title="NASA NeoWs",
    page_icon="☄️",
    layout="wide",
)


st.title("☄️ NASA NeoWs Explorer")

st.markdown(
    """
    Analyse des objets géocroiseurs provenant de **NASA NeoWs**.

    ```text
    NASA API
        ↓
    Kafka
        ↓
    Spark Streaming
        ↓
    Bronze
        ↓
    Silver
        ↓
    Gold
    ```
    """
)


# ============================================================
# GLOBAL KPIs
# ============================================================

try:

    global_df = read_neows_global()

    st.subheader("📊 Global KPIs")

    st.dataframe(
        global_df.toPandas(),
        use_container_width=True
    )

except Exception as e:

    st.error("Impossible de lire les NeoWs Global KPIs.")
    st.exception(e)


# ============================================================
# BY DATE
# ============================================================

try:

    by_date_df = read_neows_by_date()

    st.subheader("📅 Asteroids by Date")

    st.dataframe(
        by_date_df.toPandas(),
        use_container_width=True
    )

except Exception as e:

    st.error("Impossible de lire NeoWs By Date.")
    st.exception(e)


# ============================================================
# HAZARD ANALYSIS
# ============================================================

try:

    hazard_df = read_neows_hazard()

    st.subheader("☄️ Hazard Analysis")

    st.dataframe(
        hazard_df.toPandas(),
        use_container_width=True
    )

except Exception as e:

    st.error("Impossible de lire NeoWs Hazard Analysis.")
    st.exception(e)