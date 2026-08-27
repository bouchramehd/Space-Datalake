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
    page_title="Gaia Observatory",
    page_icon="⭐",
    layout="wide",
)


# ============================================================
# SPACE THEME
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   BACKGROUND
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(59, 130, 246, 0.15),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(124, 58, 237, 0.15),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(14, 165, 233, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020617 0%,
            #07111f 50%,
            #030712 100%
        );
}


/* ============================================================
   STAR FIELD
   ============================================================ */

.stApp::before {
    content: "";

    position: fixed;

    inset: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(255,255,255,0.65) 1px,
            transparent 1px
        ),
        radial-gradient(
            circle,
            rgba(255,255,255,0.30) 1px,
            transparent 1px
        );

    background-size:
        150px 150px,
        230px 230px;

    background-position:
        20px 30px,
        80px 120px;

    opacity: 0.20;

    pointer-events: none;

    z-index: 0;
}


/* ============================================================
   CONTENT
   ============================================================ */

.block-container {
    position: relative;

    z-index: 1;

    padding-top: 2rem;

    padding-bottom: 3rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #020617,
            #07101f,
            #030712
        );

    border-right:
        1px solid rgba(96,165,250,0.25);
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1,
h2,
h3 {
    
}


/* ============================================================
   MAIN TITLE
   ============================================================ */

.main-title {
    font-size: 3.4rem;

    font-weight: 900;

    letter-spacing: 3px;

    text-align: center;

    color: #ffffff;

    text-shadow:
        0 0 10px rgba(96,165,250,0.90),
        0 0 30px rgba(59,130,246,0.55);

    margin-bottom: 0;
}


.main-subtitle {
    text-align: center;

    color: #a5b4fc;

    font-size: 0.95rem;

    letter-spacing: 3px;

    margin-top: 0.3rem;

    margin-bottom: 2rem;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    color: #f8fafc;

    font-size: 1.55rem;

    font-weight: 800;

    letter-spacing: 0.5px;

    margin-top: 0.5rem;

    margin-bottom: 1rem;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.98),
            rgba(15,23,42,0.78)
        );

    border:
        1px solid rgba(96,165,250,0.38);

    border-radius: 18px;

    padding: 1.15rem;

    min-height: 115px;

    box-shadow:
        0 8px 28px rgba(0,0,0,0.30);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}


div[data-testid="stMetric"]:hover {

    transform: translateY(-3px);

    border-color:
        rgba(96,165,250,0.80);
}


/* ============================================================
   KPI LABELS
   ============================================================ */

div[data-testid="stMetricLabel"] {

    color: #ffffff !important;

    font-size: 0.90rem !important;

    font-weight: 900 !important;

    letter-spacing: 1px !important;

    opacity: 1 !important;
}


div[data-testid="stMetricLabel"] p {

    color: #ffffff !important;

    font-weight: 900 !important;
}


/* ============================================================
   KPI VALUES
   ============================================================ */

div[data-testid="stMetricValue"] {

    color: #ffffff !important;

    font-size: 1.70rem !important;

    font-weight: 900 !important;

    text-shadow:
        0 0 12px rgba(96,165,250,0.25);
}


/* ============================================================
   TOTAL STARS
   ============================================================ */

.total-stars-box {

    background:
        linear-gradient(
            135deg,
            rgba(30,64,175,0.38),
            rgba(15,23,42,0.95)
        );

    border:
        1px solid rgba(96,165,250,0.55);

    border-radius: 20px;

    padding: 1.4rem 1.6rem;

    margin-bottom: 1rem;

    box-shadow:
        0 10px 35px rgba(37,99,235,0.18);
}


.total-stars-label {

    color: #dbeafe;

    font-size: 1rem;

    font-weight: 900;

    letter-spacing: 1.5px;
}


.total-stars-number {

    color: #ffffff;

    font-size: 2.8rem;

    font-weight: 900;

    margin-top: 0.2rem;

    text-shadow:
        0 0 15px rgba(96,165,250,0.65);
}


.total-stars-info {

    color: #94a3b8;

    font-size: 0.82rem;

    margin-top: 0.2rem;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {

    color: #cbd5e1 !important;

    font-size: 0.95rem !important;

    font-weight: 800 !important;
}


button[data-baseweb="tab"][aria-selected="true"] {

    color: #ffffff !important;
}


/* ============================================================
   SPACE TABLE
   ============================================================ */

.space-table-wrapper {

    width: 100%;

    overflow-x: auto;

    border-radius: 15px;

    border:
        1px solid rgba(96,165,250,0.35);

    box-shadow:
        0 8px 30px rgba(0,0,0,0.30);
}


.space-table {

    width: 100%;

    border-collapse: separate;

    border-spacing: 0;

    background:
        rgba(7, 15, 30, 0.95);

    color: #e2e8f0;

    font-size: 0.85rem;
}


/* TABLE HEADER */

.space-table th {

    background:
        linear-gradient(
            180deg,
            rgba(30,41,59,0.98),
            rgba(15,23,42,0.98)
        );

    color: #93c5fd;

    font-weight: 900;

    letter-spacing: 0.5px;

    padding: 13px 12px;

    text-align: left;

    border-bottom:
        1px solid rgba(96,165,250,0.35);
}


/* TABLE CELLS */

.space-table td {

    background:
        rgba(15,23,42,0.78);

    color: #e2e8f0;

    padding: 12px;

    border-bottom:
        1px solid rgba(148,163,184,0.10);
}


/* LAST ROW */

.space-table tr:last-child td {

    border-bottom: none;
}


/* HOVER */

.space-table tbody tr:hover td {

    background:
        rgba(30,64,175,0.28);

    color: #ffffff;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    color: #64748b;

    font-size: 0.78rem;

    letter-spacing: 1.5px;

    margin-top: 1rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">⭐ GAIA OBSERVATORY</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    'STELLAR DATA ANALYSIS · GAIA DR3 · GOLD LAYER'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# MISSION OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">🌌 Mission Overview</div>',
    unsafe_allow_html=True,
)


try:

    global_df = read_gaia_global()

    row = global_df.first()


    if row is None:

        st.warning(
            "Aucune donnée KPI Gaia disponible."
        )

    else:

        total_stars = row["total_stars"]

        avg_parallax = row["avg_parallax"]

        avg_magnitude = row["avg_g_magnitude"]

        avg_temperature = row["avg_temperature"]

        avg_distance = row["avg_distance"]


        # ====================================================
        # TOTAL STARS
        # ====================================================

        total_display = (
            f"{total_stars:,}"
            if total_stars is not None
            else "N/A"
        )


        st.markdown(
            f"""<div class="total-stars-box"><div class="total-stars-label">⭐ TOTAL STARS OBSERVED</div><div class="total-stars-number">{total_display}</div><div class="total-stars-info">Gaia DR3 · Gold Layer</div></div>""",
            unsafe_allow_html=True,
        )


        # ====================================================
        # OTHER KPIs
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                label="📐 AVG PARALLAX",
                value=(
                    f"{avg_parallax:.2f} mas"
                    if avg_parallax is not None
                    else "N/A"
                ),
            )


        with col2:

            st.metric(
                label="💡 AVG MAGNITUDE",
                value=(
                    f"{avg_magnitude:.2f}"
                    if avg_magnitude is not None
                    else "N/A"
                ),
            )


        with col3:

            st.metric(
                label="🌡️ AVG TEMPERATURE",
                value=(
                    f"{avg_temperature:,.0f} K"
                    if avg_temperature is not None
                    else "N/A"
                ),
            )


        with col4:

            st.metric(
                label="📏 AVG DISTANCE",
                value=(
                    f"{avg_distance:,.2f} pc"
                    if avg_distance is not None
                    else "N/A"
                ),
            )


except Exception as e:

    st.error(
        "Impossible de lire les KPIs Gaia."
    )

    st.exception(e)


st.divider()


# ============================================================
# STELLAR ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🔭 Stellar Analysis</div>',
    unsafe_allow_html=True,
)


tab_temperature, tab_magnitude, tab_distance = st.tabs(
    [
        "🌡️ Temperature",
        "💡 Magnitude",
        "📏 Distance",
    ]
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def show_space_table(df):
    """
    Display a DataFrame as a dark space-themed HTML table.
    """

    html = df.to_html(
        index=False,
        escape=False,
        classes="space-table",
    )

    st.markdown(
        f'<div class="space-table-wrapper">{html}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# TEMPERATURE
# ============================================================

with tab_temperature:

    st.subheader(
        "🌡️ Distribution des étoiles par température"
    )


    try:

        temperature_df = read_gaia_temperature()

        temperature_pdf = temperature_df.toPandas()


        if temperature_pdf.empty:

            st.warning(
                "Aucune donnée de température disponible."
            )


        else:

            total = temperature_pdf[
                "star_count"
            ].sum()


            temperature_pdf[
                "percentage"
            ] = (
                temperature_pdf["star_count"]
                / total
                * 100
            )


            col1, col2 = st.columns(
                [2.2, 1]
            )


            with col1:

                fig = px.bar(

                    temperature_pdf,

                    x="temperature_band",

                    y="star_count",

                    text="star_count",

                    labels={
                        "temperature_band":
                            "Temperature Band",

                        "star_count":
                            "Number of Stars",
                    },

                )


                fig.update_traces(

                    texttemplate="%{text:,.0f}",

                    textposition="outside",

                    hovertemplate=
                        "<b>%{x}</b><br>"
                        "Stars: %{y:,.0f}"
                        "<extra></extra>",

                )


                fig.update_layout(

                    template="plotly_dark",

                    height=500,

                    showlegend=False,

                    margin=dict(
                        l=40,
                        r=20,
                        t=30,
                        b=50,
                    ),

                    plot_bgcolor="rgba(0,0,0,0)",

                    paper_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#cbd5e1"
                    ),

                )


                st.plotly_chart(

                    fig,

                    use_container_width=True,

                )


            with col2:

                st.subheader(
                    "📊 Distribution"
                )


                display_df = temperature_pdf[
                    [
                        "temperature_band",
                        "star_count",
                        "percentage",
                    ]
                ].copy()


                display_df["star_count"] = (
                    display_df["star_count"]
                    .map(
                        lambda x:
                        f"{x:,.0f}"
                    )
                )


                display_df["percentage"] = (
                    display_df["percentage"]
                    .map(
                        lambda x:
                        f"{x:.2f}%"
                    )
                )


                show_space_table(
                    display_df
                )


    except Exception as e:

        st.error(
            "Impossible de charger "
            "les données de température."
        )

        st.exception(e)


# ============================================================
# MAGNITUDE
# ============================================================

with tab_magnitude:

    st.subheader(
        "💡 Distribution des étoiles par magnitude"
    )


    try:

        magnitude_df = read_gaia_magnitude()

        magnitude_pdf = magnitude_df.toPandas()


        if magnitude_pdf.empty:

            st.warning(
                "Aucune donnée de magnitude disponible."
            )


        else:

            total = magnitude_pdf[
                "star_count"
            ].sum()


            magnitude_pdf[
                "percentage"
            ] = (
                magnitude_pdf["star_count"]
                / total
                * 100
            )


            col1, col2 = st.columns(
                [2.2, 1]
            )


            with col1:

                fig = px.bar(

                    magnitude_pdf,

                    x="magnitude_band",

                    y="star_count",

                    text="star_count",

                    labels={
                        "magnitude_band":
                            "Magnitude Band",

                        "star_count":
                            "Number of Stars",
                    },

                )


                fig.update_traces(

                    texttemplate="%{text:,.0f}",

                    textposition="outside",

                    hovertemplate=
                        "<b>%{x}</b><br>"
                        "Stars: %{y:,.0f}"
                        "<extra></extra>",

                )


                fig.update_layout(

                    template="plotly_dark",

                    height=500,

                    showlegend=False,

                    margin=dict(
                        l=40,
                        r=20,
                        t=30,
                        b=50,
                    ),

                    plot_bgcolor="rgba(0,0,0,0)",

                    paper_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#cbd5e1"
                    ),

                )


                st.plotly_chart(

                    fig,

                    use_container_width=True,

                )


            with col2:

                st.subheader(
                    "📊 Distribution"
                )


                display_df = magnitude_pdf[
                    [
                        "magnitude_band",
                        "star_count",
                        "percentage",
                    ]
                ].copy()


                display_df["star_count"] = (
                    display_df["star_count"]
                    .map(
                        lambda x:
                        f"{x:,.0f}"
                    )
                )


                display_df["percentage"] = (
                    display_df["percentage"]
                    .map(
                        lambda x:
                        f"{x:.2f}%"
                    )
                )


                show_space_table(
                    display_df
                )


    except Exception as e:

        st.error(
            "Impossible de charger "
            "les données de magnitude."
        )

        st.exception(e)


# ============================================================
# DISTANCE
# ============================================================

with tab_distance:

    st.subheader(
        "📏 Distribution des étoiles par distance"
    )


    try:

        distance_df = read_gaia_distance()

        distance_pdf = distance_df.toPandas()


        if distance_pdf.empty:

            st.warning(
                "Aucune donnée de distance disponible."
            )


        else:

            total = distance_pdf[
                "star_count"
            ].sum()


            distance_pdf[
                "percentage"
            ] = (
                distance_pdf["star_count"]
                / total
                * 100
            )


            col1, col2 = st.columns(
                [2.2, 1]
            )


            with col1:

                fig = px.bar(

                    distance_pdf,

                    x="distance_band_pc",

                    y="star_count",

                    text="star_count",

                    labels={
                        "distance_band_pc":
                            "Distance Band (pc)",

                        "star_count":
                            "Number of Stars",
                    },

                )


                fig.update_traces(

                    texttemplate="%{text:,.0f}",

                    textposition="outside",

                    hovertemplate=
                        "<b>%{x}</b><br>"
                        "Stars: %{y:,.0f}"
                        "<extra></extra>",

                )


                fig.update_layout(

                    template="plotly_dark",

                    height=500,

                    showlegend=False,

                    margin=dict(
                        l=40,
                        r=20,
                        t=30,
                        b=50,
                    ),

                    plot_bgcolor="rgba(0,0,0,0)",

                    paper_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#cbd5e1"
                    ),

                )


                st.plotly_chart(

                    fig,

                    use_container_width=True,

                )


            with col2:

                st.subheader(
                    "📊 Distribution"
                )


                display_df = distance_pdf[
                    [
                        "distance_band_pc",
                        "star_count",
                        "percentage",
                    ]
                ].copy()


                display_df["star_count"] = (
                    display_df["star_count"]
                    .map(
                        lambda x:
                        f"{x:,.0f}"
                    )
                )


                display_df["percentage"] = (
                    display_df["percentage"]
                    .map(
                        lambda x:
                        f"{x:.2f}%"
                    )
                )


                show_space_table(
                    display_df
                )


    except Exception as e:

        st.error(
            "Impossible de charger "
            "les données de distance."
        )

        st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    '🟢 GAIA OBSERVATORY ONLINE · '
    'GOLD LAYER CONNECTED · '
    'GAIA DR3'
    '</div>',
    unsafe_allow_html=True,
)