import streamlit as st
import plotly.express as px

from utils.hdfs import (
    read_neows_global,
    read_neows_by_date,
    read_neows_hazard,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NASA NeoWs Explorer",
    page_icon="☄️",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("☄️ NASA NeoWs Explorer")

st.markdown(
    """
    Analyse interactive des **Near-Earth Objects (NEOs)** provenant
    de **NASA NeoWs** et stockés dans la couche **Gold** du Data Lake.
    """
)

st.divider()


# ============================================================
# GLOBAL KPIs
# ============================================================

st.header("📊 Global KPIs")

try:

    global_df = read_neows_global()
    global_pdf = global_df.toPandas()

    if global_pdf.empty:

        st.warning("Aucune donnée KPI NeoWs disponible.")

    else:

        row = global_pdf.iloc[0]

        # ----------------------------------------------------
        # Détection des colonnes disponibles
        # ----------------------------------------------------

        def find_column(possible_names):

            for name in possible_names:
                if name in global_pdf.columns:
                    return name

            return None

        total_col = find_column([
            "total_asteroids",
            "total_neos",
            "total_objects",
            "asteroid_count",
            "neo_count",
            "total_count",
        ])

        hazardous_col = find_column([
            "hazardous_count",
            "hazardous_asteroids",
            "hazardous_neos",
            "potentially_hazardous_count",
        ])

        avg_diameter_col = find_column([
            "avg_diameter",
            "avg_diameter_km",
            "average_diameter",
        ])

        avg_velocity_col = find_column([
            "avg_velocity",
            "avg_velocity_kmh",
            "average_velocity",
        ])

        # ----------------------------------------------------
        # KPI values
        # ----------------------------------------------------

        total_value = (
            row[total_col]
            if total_col
            else None
        )

        hazardous_value = (
            row[hazardous_col]
            if hazardous_col
            else None
        )

        avg_diameter_value = (
            row[avg_diameter_col]
            if avg_diameter_col
            else None
        )

        avg_velocity_value = (
            row[avg_velocity_col]
            if avg_velocity_col
            else None
        )

        # ----------------------------------------------------
        # KPI cards
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "☄️ Total NEOs",
                (
                    f"{total_value:,.0f}"
                    if total_value is not None
                    else "N/A"
                ),
            )

        with col2:

            st.metric(
                "⚠️ Hazardous NEOs",
                (
                    f"{hazardous_value:,.0f}"
                    if hazardous_value is not None
                    else "N/A"
                ),
            )

        with col3:

            st.metric(
                "📏 Avg Diameter",
                (
                    f"{avg_diameter_value:.2f} km"
                    if avg_diameter_value is not None
                    else "N/A"
                ),
            )

        with col4:

            st.metric(
                "🚀 Avg Velocity",
                (
                    f"{avg_velocity_value:,.0f} km/h"
                    if avg_velocity_value is not None
                    else "N/A"
                ),
            )

        # ----------------------------------------------------
        # Raw KPI table
        # ----------------------------------------------------

        with st.expander("📋 Voir les données KPI"):

            st.dataframe(
                global_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de lire les NeoWs Global KPIs.")
    st.exception(e)


st.divider()


# ============================================================
# ASTEROIDS BY DATE
# ============================================================

st.header("📅 Asteroids by Date")

try:

    by_date_df = read_neows_by_date()
    by_date_pdf = by_date_df.toPandas()

    if by_date_pdf.empty:

        st.warning("Aucune donnée NeoWs par date disponible.")

    else:

        st.write(
            "Évolution du nombre d'objets géocroiseurs détectés par date."
        )

        # ----------------------------------------------------
        # Detect date column
        # ----------------------------------------------------

        date_column = None

        for column in [
            "date",
            "observation_date",
            "close_approach_date",
            "approach_date",
            "event_date",
        ]:

            if column in by_date_pdf.columns:
                date_column = column
                break

        # ----------------------------------------------------
        # Detect count column
        # ----------------------------------------------------

        count_column = None

        for column in [
            "asteroid_count",
            "neo_count",
            "object_count",
            "count",
            "total_asteroids",
            "total_neos",
        ]:

            if column in by_date_pdf.columns:
                count_column = column
                break

        if date_column and count_column:

            chart_df = by_date_pdf.copy()

            chart_df[date_column] = chart_df[date_column].astype(str)

            fig = px.bar(
                chart_df,
                x=date_column,
                y=count_column,
                title="Nombre de NEOs par date",
                labels={
                    date_column: "Date",
                    count_column: "Number of NEOs",
                },
                text=count_column,
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
            )

            fig.update_layout(
                height=450,
                showlegend=False,
                margin=dict(
                    l=40,
                    r=20,
                    t=70,
                    b=40,
                ),
                xaxis_title="Date",
                yaxis_title="Number of NEOs",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "Les colonnes nécessaires au graphique "
                "n'ont pas été trouvées."
            )

        # ----------------------------------------------------
        # Data table
        # ----------------------------------------------------

        with st.expander("📋 Voir les données par date"):

            st.dataframe(
                by_date_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de lire NeoWs By Date.")
    st.exception(e)


st.divider()


# ============================================================
# HAZARD ANALYSIS
# ============================================================

st.header("☄️ Hazard Analysis")

try:

    hazard_df = read_neows_hazard()
    hazard_pdf = hazard_df.toPandas()

    if hazard_pdf.empty:

        st.warning(
            "Aucune donnée d'analyse de danger disponible."
        )

    else:

        # ----------------------------------------------------
        # Detect category column
        # ----------------------------------------------------

        hazard_column = None

        for column in [
            "is_potentially_hazardous",
            "hazardous",
            "hazard_status",
            "hazard",
            "hazard_category",
            "category",
        ]:

            if column in hazard_pdf.columns:
                hazard_column = column
                break

        # ----------------------------------------------------
        # Detect count column
        # ----------------------------------------------------

        count_column = None

        for column in [
            "asteroid_count",
            "neo_count",
            "object_count",
            "count",
            "total_asteroids",
            "total_neos",
        ]:

            if column in hazard_pdf.columns:
                count_column = column
                break

        if hazard_column and count_column:

            chart_df = hazard_pdf.copy()

            chart_df[hazard_column] = (
                chart_df[hazard_column]
                .astype(str)
            )

            fig = px.pie(
                chart_df,
                names=hazard_column,
                values=count_column,
                title="Répartition des NEOs selon le niveau de danger",
                hole=0.45,
            )

            fig.update_traces(
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Count: %{value:,}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=450,
                margin=dict(
                    l=20,
                    r=20,
                    t=70,
                    b=20,
                ),
                showlegend=True,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "Les colonnes nécessaires au graphique "
                "d'analyse de danger n'ont pas été trouvées."
            )

        # ----------------------------------------------------
        # Hazard table
        # ----------------------------------------------------

        with st.expander("📋 Voir les données Hazard Analysis"):

            st.dataframe(
                hazard_pdf,
                use_container_width=True,
                hide_index=True,
            )

except Exception as e:

    st.error("Impossible de lire NeoWs Hazard Analysis.")
    st.exception(e)


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "☄️ NASA NeoWs Explorer — Space Data Lake / Gold Layer"
)