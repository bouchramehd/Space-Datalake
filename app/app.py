import streamlit as st

st.set_page_config(
    page_title="Space Data Lake",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Space Data Lake")
st.subheader("Gaia DR3 + NASA NeoWs")

st.markdown(
    """
    Bienvenue dans le dashboard du **Space Data Lake**.

    Cette application permet d'explorer les données provenant de :

    - ⭐ **Gaia DR3** — source Batch
    - ☄️ **NASA NeoWs** — source Streaming

    ### Architecture

    ```text
    Gaia DR3
        ↓
    HDFS Bronze
        ↓
    Spark Silver
        ↓
    Spark Gold
        ↓
    Dashboard

    NASA NeoWs
        ↓
    Kafka
        ↓
    Spark Structured Streaming
        ↓
    HDFS Bronze
        ↓
    Spark Silver
        ↓
    Spark Gold
        ↓
    Dashboard
    ```
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⭐ Source Batch", "Gaia DR3")

with col2:
    st.metric("☄️ Source Streaming", "NASA NeoWs")

with col3:
    st.metric("🏗️ Architecture", "Bronze → Silver → Gold")

st.info(
    "Utilisez le menu à gauche pour explorer Gaia, NeoWs "
    "ou l'architecture du Data Lake."
)