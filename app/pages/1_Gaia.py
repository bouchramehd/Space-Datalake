import streamlit as st
import plotly.express as px

from utils.hdfs import (
    read_gaia_global,
    read_gaia_temperature,
    read_gaia_magnitude,
    read_gaia_distance,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Gaia DR3 Explorer",
    page_icon="⭐",
    layout="wide",
)

st.title("⭐ Gaia DR3 Explorer")

st.markdown(
    """
    Analyse interactive des données **Gaia DR3** présentes
    dans la couche **Gold** du Data Lake.
    """
)

st.divider()


# ============================================================
# GLOBAL KPIs
# ============================================================

st.header("📊 Global KPIs")

try:

    global_df = read_gaia_global()
    row = global_df.first()

    if row is None:
        st.warning("Aucune donnée KPI Gaia disponible.")
    else:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total_stars = row["total_stars"]

            st.metric(
                label="⭐ Total Stars",
                value=f"{total_stars:,}" if total_stars is not None else "N/A",
            )

        with col2:
            avg_parallax = row["avg_parallax"]

            st.metric(
                label="📐 Avg Parallax",
                value=(
                    f"{avg_parallax:.2f} mas"
                    if avg_parallax is not None
                    else "N/A"
                ),
            )

        with col3:
            avg_magnitude = row["avg_g_magnitude"]

            st.metric(
                label="💡 Avg Magnitude",
                value=(
                    f"{avg_magnitude:.2f}"
                    if avg_magnitude is not None
                    else "N/A"
                ),
            )

        with col4:
            avg_temperature = row["avg_temperature"]

            st.metric(
                label="🌡️ Avg Temperature",
                value=(
                    f"{avg_temperature:,.0f} K"
                    if avg_temperature is not None
                    else "N/A"
                ),
            )

        with col5:
            avg_distance = row["avg_distance"]

            st.metric(
                label="📏 Avg Distance",
                value=(
                    f"{avg_distance:,.2f} pc"
                    if avg_distance is not None
                    else "N/A"
                ),
            )

except Exception as e:

    st.error("Impossible de lire les KPIs Gaia.")
    st.exception(e)


st.divider()


# ============================================================
# TEMPERATURE
# ============================================================

st.header("🌡️ Stars by Temperature")

try:

    temperature_df = read_gaia_temperature()
    temperature_pdf = temperature_df.toPandas()

    if temperature_pdf.empty:

        st.warning("Aucune donnée de température disponible.")

    else:

        col1, col2 = st.columns([2, 1])

        with col1:

            fig = px.bar(
                temperature_pdf,
                x="temperature_band",
                y="star_count",
                title="Distribution des étoiles par température",
                labels={
                    "temperature_band": "Temperature Band",
                    "star_count": "Number of Stars",
                },
                text="star_count",
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
            )

            fig.update_layout(
                height=450,
                xaxis_title="Temperature Band",
                yaxis_title="Number of Stars",
                showlegend=False,
                margin=dict(l=40, r=20, t=70, b=40),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            st.subheader("📋 Data")

            st.dataframe(
                temperature_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de charger les données de température.")
    st.exception(e)


st.divider()


# ============================================================
# MAGNITUDE
# ============================================================

st.header("💡 Stars by Magnitude")

try:

    magnitude_df = read_gaia_magnitude()
    magnitude_pdf = magnitude_df.toPandas()

    if magnitude_pdf.empty:

        st.warning("Aucune donnée de magnitude disponible.")

    else:

        col1, col2 = st.columns([2, 1])

        with col1:

            fig = px.bar(
                magnitude_pdf,
                x="magnitude_band",
                y="star_count",
                title="Distribution des étoiles par magnitude",
                labels={
                    "magnitude_band": "Magnitude Band",
                    "star_count": "Number of Stars",
                },
                text="star_count",
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
            )

            fig.update_layout(
                height=450,
                xaxis_title="Magnitude Band",
                yaxis_title="Number of Stars",
                showlegend=False,
                margin=dict(l=40, r=20, t=70, b=40),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            st.subheader("📋 Data")

            st.dataframe(
                magnitude_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de charger les données de magnitude.")
    st.exception(e)


st.divider()


# ============================================================
# DISTANCE
# ============================================================

st.header("📏 Stars by Distance")

try:

    distance_df = read_gaia_distance()
    distance_pdf = distance_df.toPandas()

    if distance_pdf.empty:

        st.warning("Aucune donnée de distance disponible.")

    else:

        col1, col2 = st.columns([2, 1])

        with col1:

            fig = px.bar(
                distance_pdf,
                x="distance_band_pc",
                y="star_count",
                title="Distribution des étoiles par distance",
                labels={
                    "distance_band_pc": "Distance Band",
                    "star_count": "Number of Stars",
                },
                text="star_count",
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
            )

            fig.update_layout(
                height=450,
                xaxis_title="Distance Band (pc)",
                yaxis_title="Number of Stars",
                showlegend=False,
                margin=dict(l=40, r=20, t=70, b=40),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        with col2:

            st.subheader("📋 Data")

            st.dataframe(
                distance_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de charger les données de distance.")
    st.exception(e)


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "⭐ Gaia DR3 Explorer — Space Data Lake / Gold Layer"
)