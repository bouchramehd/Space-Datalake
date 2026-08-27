import streamlit as st
import plotly.express as px
import pandas as pd
from textwrap import dedent

from utils.hdfs import (
    read_neows_global,
    read_neows_by_date,
    read_neows_hazard,
)


# ============================================================
# HTML HELPER
# ============================================================

def html_block(s: str) -> str:
    """Strip leading whitespace from every line (not just the common
    prefix) so Streamlit's markdown parser never mistakes indented
    HTML for a 4-space code block."""
    return "\n".join(line.lstrip() for line in dedent(s).strip().splitlines())


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NASA NeoWs Explorer",
    page_icon="☄️",
    layout="wide",
)


# ============================================================
# SPACE THEME (same as home page)
# ============================================================

st.markdown(
    html_block("""
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(59, 130, 246, 0.16),
                transparent 25%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(139, 92, 246, 0.14),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 85%,
                rgba(14, 165, 233, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #071225 50%,
                #030712 100%
            );

        color: #f8fafc;
    }


    /* ========================================================
       STAR BACKGROUND
    ======================================================== */

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;

        background-image:
            radial-gradient(
                circle,
                rgba(255,255,255,0.75) 1px,
                transparent 1px
            ),
            radial-gradient(
                circle,
                rgba(255,255,255,0.45) 1px,
                transparent 1px
            ),
            radial-gradient(
                circle,
                rgba(255,255,255,0.30) 1px,
                transparent 1px
            );

        background-size:
            120px 120px,
            190px 190px,
            270px 270px;

        background-position:
            10px 20px,
            50px 80px,
            100px 40px;

        opacity: 0.30;

        pointer-events: none;

        z-index: 0;
    }


    .block-container {
        position: relative;
        z-index: 1;

        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #071225 55%,
                #020617 100%
            );

        border-right:
            1px solid rgba(96, 165, 250, 0.25);
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .space-title {
        text-align: center;

        font-size: 3.2rem;

        font-weight: 800;

        letter-spacing: 2px;

        color: #ffffff;

        text-shadow:
            0 0 10px rgba(96, 165, 250, 0.8),
            0 0 25px rgba(59, 130, 246, 0.55),
            0 0 50px rgba(37, 99, 235, 0.30);

        margin-bottom: 0.5rem;
    }


    .space-subtitle {
        text-align: center;

        font-size: 1rem;

        letter-spacing: 1px;

        color: #94a3b8;

        margin-bottom: 2.5rem;

        line-height: 1.6;
    }


    /* ========================================================
       SECTION HEADERS (st.header replacement)
    ======================================================== */

    .section-title {
        font-size: 1.6rem;

        font-weight: 700;

        color: #e2e8f0;

        margin-top: 1rem;

        margin-bottom: 1.2rem;

        display: flex;

        align-items: center;

        gap: 0.6rem;
    }


    /* Native Streamlit headers, in case any remain */
    h1, h2, h3 {
        color: #f8fafc !important;
    }


    /* ========================================================
       DIVIDER GLOW
    ======================================================== */

    hr {
        border-color: rgba(96, 165, 250, 0.20) !important;
    }


    /* ========================================================
       METRIC CARDS
    ======================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(15, 23, 42, 0.65)
            );

        border:
            1px solid rgba(96, 165, 250, 0.25);

        border-radius: 16px;

        padding: 1rem 1.2rem;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        border-color:
            rgba(96, 165, 250, 0.65);
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;

        text-shadow:
            0 0 12px rgba(96, 165, 250, 0.35);
    }


    /* ========================================================
       EXPANDER / DATAFRAME CONTAINERS
    ======================================================== */

    div[data-testid="stExpander"] {
        background:
            rgba(15, 23, 42, 0.75);

        border:
            1px solid rgba(96, 165, 250, 0.20);

        border-radius: 14px;
    }


    /* ========================================================
       ALERT BOXES (warning / info / error)
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;

        border: 1px solid rgba(96, 165, 250, 0.20);
    }


    /* ========================================================
       FOOTER / CAPTION
    ======================================================== */

    .stCaption, [data-testid="stCaptionContainer"] {
        text-align: center;

        color: #64748b !important;

        letter-spacing: 1px;
    }

    </style>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="space-title">☄️ NASA NEOWS EXPLORER</div>',
    unsafe_allow_html=True,
)

st.markdown(
    html_block("""
    <div class="space-subtitle">
        Analyse interactive des <b>Near-Earth Objects (NEOs)</b>
        provenant de <b>NASA NeoWs</b>, stockés dans la couche
        <b>Gold</b> du Data Lake.
    </div>
    """),
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# GLOBAL KPIs
# ============================================================

st.markdown(
    '<div class="section-title">📊 Global KPIs</div>',
    unsafe_allow_html=True,
)

try:

    global_df = read_neows_global()
    global_pdf = global_df.toPandas()

    if global_pdf.empty:

        st.warning("Aucune donnée KPI NeoWs disponible.")

    else:

        row = global_pdf.iloc[0]

        # ----------------------------------------------------
        # Helper function
        # ----------------------------------------------------

        def find_column(possible_names):

            for name in possible_names:

                if name in global_pdf.columns:
                    return name

            return None

        # ----------------------------------------------------
        # Detect columns
        # ----------------------------------------------------

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
            "average_velocity_kmh",
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
        # Hazard percentage
        # ----------------------------------------------------

        if (
            total_value is not None
            and hazardous_value is not None
            and float(total_value) > 0
        ):

            hazard_percentage = (
                float(hazardous_value)
                / float(total_value)
                * 100
            )

        else:

            hazard_percentage = None

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4, col5 = st.columns(5)

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

        with col5:

            st.metric(
                "⚠️ Hazard Rate",
                (
                    f"{hazard_percentage:.2f}%"
                    if hazard_percentage is not None
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

st.markdown(
    '<div class="section-title">📅 Asteroids by Date</div>',
    unsafe_allow_html=True,
)

try:

    by_date_df = read_neows_by_date()
    by_date_pdf = by_date_df.toPandas()

    if by_date_pdf.empty:

        st.warning(
            "Aucune donnée NeoWs par date disponible."
        )

    else:

        st.write(
            "Évolution du nombre d'objets géocroiseurs "
            "détectés par date."
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

            chart_df[date_column] = pd.to_datetime(
                chart_df[date_column],
                errors="coerce",
            )

            chart_df = chart_df.dropna(
                subset=[date_column]
            )

            chart_df = chart_df.sort_values(
                date_column
            )

            # ------------------------------------------------
            # Chart
            # ------------------------------------------------

            fig = px.bar(
                chart_df,
                x=date_column,
                y=count_column,
                title="☄️ Nombre de NEOs par date",
                labels={
                    date_column: "Date",
                    count_column: "Nombre de NEOs",
                },
                text=count_column,
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_color="#60a5fa",
                hovertemplate=(
                    "<b>Date:</b> %{x}<br>"
                    "<b>NEOs:</b> %{y:,}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=500,
                showlegend=False,
                margin=dict(
                    l=40,
                    r=20,
                    t=70,
                    b=40,
                ),
                xaxis_title="Date",
                yaxis_title="Nombre de NEOs",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                title_font=dict(color="#f8fafc", size=18),
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

st.markdown(
    '<div class="section-title">☄️ Hazard Analysis</div>',
    unsafe_allow_html=True,
)

st.write(
    "Répartition des objets géocroiseurs selon leur "
    "niveau de danger potentiel."
)

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
        # IMPORTANT:
        # Your Gold data uses:
        # potentially_hazardous
        # ----------------------------------------------------

        hazard_column = None

        for column in [
            "potentially_hazardous",
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

        # ----------------------------------------------------
        # Create chart
        # ----------------------------------------------------

        if hazard_column and count_column:

            chart_df = hazard_pdf.copy()

            # Convert values into readable labels
            def format_hazard(value):

                value = str(value).strip().lower()

                if value in [
                    "true",
                    "1",
                    "yes",
                    "oui",
                ]:

                    return "⚠️ Hazardous"

                if value in [
                    "false",
                    "0",
                    "no",
                    "non",
                ]:

                    return "✅ Non-Hazardous"

                return str(value).title()

            chart_df["Hazard Status"] = (
                chart_df[hazard_column]
                .apply(format_hazard)
            )

            # Make sure count is numeric
            chart_df[count_column] = pd.to_numeric(
                chart_df[count_column],
                errors="coerce",
            )

            chart_df = chart_df.dropna(
                subset=[count_column]
            )

            # ------------------------------------------------
            # PIE CHART
            # ------------------------------------------------

            fig = px.pie(
                chart_df,
                names="Hazard Status",
                values=count_column,
                title=(
                    "⚠️ Répartition des NEOs "
                    "selon le niveau de danger"
                ),
                hole=0.45,
                color_discrete_sequence=[
                    "#60a5fa",
                    "#f87171",
                    "#4ade80",
                    "#a78bfa",
                ],
            )

            fig.update_traces(
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Nombre: %{value:,}<br>"
                    "Pourcentage: %{percent}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=500,
                margin=dict(
                    l=20,
                    r=20,
                    t=70,
                    b=20,
                ),
                showlegend=True,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                title_font=dict(color="#f8fafc", size=18),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            # ------------------------------------------------
            # Additional summary
            # ------------------------------------------------

            total_hazard = chart_df[count_column].sum()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "☄️ Total NEOs analysés",
                    f"{total_hazard:,.0f}",
                )

            with col2:

                hazardous_rows = chart_df[
                    chart_df["Hazard Status"]
                    == "⚠️ Hazardous"
                ]

                hazardous_total = (
                    hazardous_rows[count_column].sum()
                    if not hazardous_rows.empty
                    else 0
                )

                st.metric(
                    "⚠️ NEOs potentiellement dangereux",
                    f"{hazardous_total:,.0f}",
                )

        else:

            st.info(
                "Les colonnes nécessaires au graphique "
                "d'analyse de danger n'ont pas été trouvées."
            )

        # ----------------------------------------------------
        # Hazard table
        # ----------------------------------------------------

        with st.expander(
            "📋 Voir les données Hazard Analysis"
        ):

            st.dataframe(
                hazard_pdf,
                use_container_width=True,
                hide_index=True,
            )


except Exception as e:

    st.error(
        "Impossible de lire NeoWs Hazard Analysis."
    )

    st.exception(e)


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "☄️ NASA NeoWs Explorer — Space Data Lake / Gold Layer"
)