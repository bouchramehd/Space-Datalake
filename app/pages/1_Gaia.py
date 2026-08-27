import streamlit as st

from utils.hdfs import (
    read_gaia_global,
    read_gaia_temperature,
    read_gaia_magnitude,
    read_gaia_distance,
)


st.set_page_config(
    page_title="Gaia DR3",
    page_icon="⭐",
    layout="wide",
)

st.title("⭐ Gaia DR3 Explorer")

st.markdown(
    """
    Analyse des données **Gaia DR3** présentes dans la couche Gold.
    """
)

# ============================================================
# GLOBAL KPIs
# ============================================================

try:

    global_df = read_gaia_global()

    row = global_df.first()

    st.subheader("📊 Global KPIs")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "⭐ Total Stars",
            f"{row['total_stars']:,}"
        )

    with col2:
        st.metric(
            "📐 Avg Parallax",
            f"{row['avg_parallax']:.2f}"
            if row["avg_parallax"] is not None
            else "N/A"
        )

    with col3:
        st.metric(
            "💡 Avg Magnitude",
            f"{row['avg_g_magnitude']:.2f}"
            if row["avg_g_magnitude"] is not None
            else "N/A"
        )

    with col4:
        st.metric(
            "🌡️ Avg Temperature",
            f"{row['avg_temperature']:.0f} K"
            if row["avg_temperature"] is not None
            else "N/A"
        )

    with col5:
        st.metric(
            "📏 Avg Distance",
            f"{row['avg_distance']:.2f} pc"
            if row["avg_distance"] is not None
            else "N/A"
        )

except Exception as e:

    st.error("Impossible de lire les KPIs Gaia.")
    st.exception(e)


st.divider()


# ============================================================
# TEMPERATURE
# ============================================================

st.subheader("🌡️ Stars by Temperature")

try:

    temperature_df = read_gaia_temperature()

    st.dataframe(
        temperature_df.toPandas(),
        use_container_width=True,
    )

    chart_df = temperature_df.toPandas()

    if not chart_df.empty:

        st.bar_chart(
            chart_df.set_index("temperature_band")["star_count"]
        )

except Exception as e:

    st.error("Impossible de charger les données de température.")
    st.exception(e)


st.divider()


# ============================================================
# MAGNITUDE
# ============================================================

st.subheader("💡 Stars by Magnitude")

try:

    magnitude_df = read_gaia_magnitude()

    st.dataframe(
        magnitude_df.toPandas(),
        use_container_width=True,
    )

    chart_df = magnitude_df.toPandas()

    if not chart_df.empty:

        st.bar_chart(
            chart_df.set_index("magnitude_band")["star_count"]
        )

except Exception as e:

    st.error("Impossible de charger les données de magnitude.")
    st.exception(e)


st.divider()


# ============================================================
# DISTANCE
# ============================================================

st.subheader("📏 Stars by Distance")

try:

    distance_df = read_gaia_distance()

    st.dataframe(
        distance_df.toPandas(),
        use_container_width=True,
    )

    chart_df = distance_df.toPandas()

    if not chart_df.empty:

        st.bar_chart(
            chart_df.set_index("distance_band_pc")["star_count"]
        )

except Exception as e:

    st.error("Impossible de charger les données de distance.")
    st.exception(e)