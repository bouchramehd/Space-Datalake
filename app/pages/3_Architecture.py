import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Space Data Center — Architecture",
    page_icon="🚀",
    layout="wide",
)


# ============================================================
# SPACE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN BACKGROUND
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(59, 130, 246, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(139, 92, 246, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 50% 85%,
                rgba(14, 165, 233, 0.10),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #071225 50%,
                #020617 100%
            );

        color: #e2e8f0;
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
                rgba(255,255,255,0.65) 1px,
                transparent 1px
            ),
            radial-gradient(
                circle,
                rgba(255,255,255,0.40) 1px,
                transparent 1px
            );

        background-size:
            150px 150px,
            250px 250px;

        background-position:
            20px 30px,
            80px 100px;

        opacity: 0.25;
        pointer-events: none;
        z-index: 0;
    }


    /* ========================================================
       CONTENT
    ======================================================== */

    .block-container {
        position: relative;
        z-index: 1;

        max-width: 1250px;

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
        color: #cbd5e1 !important;
    }


    /* ========================================================
       HEADINGS
    ======================================================== */

    h1,
    h2,
    h3 {
        color: #f8fafc !important;
    }


    /* ========================================================
       PAGE HEADER
    ======================================================== */

    .page-title {
        text-align: center;

        font-size: 3.2rem;
        font-weight: 800;

        letter-spacing: 4px;

        color: #f8fafc;

        text-shadow:
            0 0 12px rgba(96, 165, 250, 0.45),
            0 0 30px rgba(59, 130, 246, 0.20);

        margin-bottom: 0.3rem;
    }

    .page-subtitle {
        text-align: center;

        color: #94a3b8;

        font-size: 0.95rem;

        letter-spacing: 3px;

        margin-bottom: 3rem;
    }


    /* ========================================================
       NATIVE STREAMLIT CONTAINERS
    ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(15, 23, 42, 0.72);

        border:
            1px solid rgba(96, 165, 250, 0.24);

        border-radius: 18px;

        box-shadow:
            0 10px 35px rgba(0,0,0,0.22);
    }


    /* ========================================================
       METRICS
    ======================================================== */

    div[data-testid="stMetric"] {
        background:
            rgba(15, 23, 42, 0.65);

        border:
            1px solid rgba(96, 165, 250, 0.20);

        border-radius: 15px;

        padding: 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* ========================================================
       INFO BOXES
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer-text {
        text-align: center;

        color: #64748b;

        font-size: 0.75rem;

        letter-spacing: 1.5px;

        margin-top: 3rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🚀")

    st.markdown("## SPACE DATA CENTER")

    st.caption("MISSION CONTROL")

    st.divider()

    st.success("🟢 DATA CENTER ONLINE")

    st.markdown("### 🧭 Navigation")

    st.page_link(
        "app.py",
        label="🚀 Space Data Center",
    )

    st.page_link(
        "pages/1_Gaia.py",
        label="⭐ Gaia Observatory",
    )

    st.page_link(
        "pages/2_NeoWs.py",
        label="☄️ NEO Tracker",
    )

    st.page_link(
        "pages/3_Architecture.py",
        label="🏗️ Architecture",
    )

    st.divider()

    st.caption("GAIA DR3")
    st.caption("NASA NEOWS")
    st.caption("HDFS · SPARK · KAFKA")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">🏗️ SPACE DATA ARCHITECTURE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    'EXPLORE THE UNIVERSE THROUGH DATA'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# INTRODUCTION
# ============================================================

st.header("🌌 Data Lake Mission")

st.write(
    "Cette architecture permet de collecter, stocker, "
    "transformer et analyser les données astronomiques "
    "provenant de deux sources complémentaires."
)

st.write("")


# ============================================================
# SOURCE OVERVIEW
# ============================================================

st.header("📡 Data Sources")

source_col1, source_col2 = st.columns(2, gap="large")


with source_col1:

    with st.container(border=True):

        st.markdown("## ⭐ Gaia DR3")

        st.write(
            "Source **Batch** contenant les données "
            "astronomiques de Gaia DR3."
        )

        st.markdown("### 📥 Ingestion")

        st.info(
            "Les fichiers Gaia sont déposés dans "
            "la couche Bronze du Data Lake."
        )

        st.metric(
            "Type de source",
            "BATCH",
        )


with source_col2:

    with st.container(border=True):

        st.markdown("## ☄️ NASA NeoWs")

        st.write(
            "Source **Streaming** fournissant des données "
            "sur les Near-Earth Objects."
        )

        st.markdown("### 📡 Ingestion")

        st.info(
            "Les événements NASA NeoWs transitent par "
            "Kafka avant d'être traités par Spark Streaming."
        )

        st.metric(
            "Type de source",
            "STREAMING",
        )


# ============================================================
# GAIA PIPELINE
# ============================================================

st.header("⭐ Gaia DR3 — Batch Pipeline")

st.write(
    "Le flux Gaia utilise une architecture batch "
    "pour traiter les données astronomiques à grande échelle."
)

gaia1, gaia2, gaia3, gaia4 = st.columns(4)


with gaia1:
    with st.container(border=True):
        st.markdown("### 📡")
        st.markdown("**GAIA DR3**")
        st.caption("Source Batch")


with gaia2:
    with st.container(border=True):
        st.markdown("### 🥉")
        st.markdown("**BRONZE**")
        st.caption("Raw data")


with gaia3:
    with st.container(border=True):
        st.markdown("### 🥈")
        st.markdown("**SILVER**")
        st.caption("Clean & normalized")


with gaia4:
    with st.container(border=True):
        st.markdown("### 🥇")
        st.markdown("**GOLD**")
        st.caption("KPIs & analytics")


st.write("")


st.info(
    "⭐ Gaia DR3 → HDFS Bronze → Spark Silver → "
    "Spark Gold → Gaia Observatory"
)


# ============================================================
# NEOWS PIPELINE
# ============================================================

st.header("☄️ NASA NeoWs — Streaming Pipeline")

st.write(
    "Le flux NASA NeoWs est traité en continu grâce "
    "à Kafka et Spark Structured Streaming."
)

neo1, neo2, neo3, neo4, neo5 = st.columns(5)


with neo1:
    with st.container(border=True):
        st.markdown("### ☄️")
        st.markdown("**NASA NeoWs**")
        st.caption("Real-time source")


with neo2:
    with st.container(border=True):
        st.markdown("### 📨")
        st.markdown("**KAFKA**")
        st.caption("Message broker")


with neo3:
    with st.container(border=True):
        st.markdown("### ⚡")
        st.markdown("**SPARK**")
        st.caption("Structured Streaming")


with neo4:
    with st.container(border=True):
        st.markdown("### 🥉")
        st.markdown("**BRONZE**")
        st.caption("Raw events")


with neo5:
    with st.container(border=True):
        st.markdown("### 🥇")
        st.markdown("**GOLD**")
        st.caption("Analytics")


st.write("")


st.info(
    "☄️ NASA NeoWs → Kafka → Spark Structured Streaming "
    "→ HDFS Bronze → Spark Silver → Spark Gold → NEO Tracker"
)


# ============================================================
# MEDALLION ARCHITECTURE
# ============================================================

st.header("🥉 🥈 🥇 Medallion Architecture")

bronze_col, silver_col, gold_col = st.columns(3, gap="large")


with bronze_col:

    with st.container(border=True):

        st.markdown("## 🥉 Bronze")

        st.markdown("**RAW DATA**")

        st.write(
            "Première couche du Data Lake. "
            "Les données sont conservées dans leur "
            "format d'origine."
        )

        st.markdown(
            """
            **Objectif**

            • Conserver les données originales  
            • Assurer la traçabilité  
            • Éviter les transformations précoces
            """
        )


with silver_col:

    with st.container(border=True):

        st.markdown("## 🥈 Silver")

        st.markdown("**CLEAN DATA**")

        st.write(
            "Couche de transformation contenant "
            "des données nettoyées et normalisées."
        )

        st.markdown(
            """
            **Traitements**

            • Validation du schéma  
            • Nettoyage  
            • Déduplication  
            • Normalisation
            """
        )


with gold_col:

    with st.container(border=True):

        st.markdown("## 🥇 Gold")

        st.markdown("**ANALYTICS READY**")

        st.write(
            "Couche finale contenant les agrégations "
            "et indicateurs prêts pour l'analyse."
        )

        st.markdown(
            """
            **Contenu**

            • KPIs  
            • Agrégations  
            • Statistiques  
            • Visualisations
            """
        )


# ============================================================
# PROCESSING TECHNOLOGIES
# ============================================================

st.header("⚙️ Processing & Infrastructure")

tech_col1, tech_col2 = st.columns(2, gap="large")


with tech_col1:

    with st.container(border=True):

        st.markdown("### 🗄️ HDFS")

        st.write(
            "Stockage distribué des données Bronze, "
            "Silver et Gold."
        )

        st.metric(
            "Role",
            "Distributed Storage",
        )


    with st.container(border=True):

        st.markdown("### ⚡ Apache Spark")

        st.write(
            "Traitement distribué des données et "
            "Spark Structured Streaming pour NeoWs."
        )

        st.metric(
            "Role",
            "Data Processing",
        )


with tech_col2:

    with st.container(border=True):

        st.markdown("### 📨 Apache Kafka")

        st.write(
            "Transport et gestion du flux temps réel "
            "NASA NeoWs."
        )

        st.metric(
            "Role",
            "Streaming",
        )


    with st.container(border=True):

        st.markdown("### 📊 Streamlit")

        st.write(
            "Interface interactive permettant d'explorer "
            "les données présentes dans la Gold Layer."
        )

        st.metric(
            "Role",
            "Visualization",
        )


# ============================================================
# END-TO-END FLOW
# ============================================================

st.header("🛰️ End-to-End Data Flow")

st.write(
    "Vue globale du parcours des données depuis "
    "les sources jusqu'au dashboard."
)

flow_col1, flow_col2 = st.columns(2, gap="large")


with flow_col1:

    with st.container(border=True):

        st.markdown("## ⭐ Batch Mission")

        st.markdown(
            """
            **⭐ Gaia DR3**

            ↓

            **🥉 HDFS Bronze**

            ↓

            **🥈 Spark Silver**

            ↓

            **🥇 Spark Gold**

            ↓

            **📊 Gaia Observatory**
            """
        )


with flow_col2:

    with st.container(border=True):

        st.markdown("## ☄️ Streaming Mission")

        st.markdown(
            """
            **☄️ NASA NeoWs**

            ↓

            **📨 Kafka**

            ↓

            **⚡ Spark Structured Streaming**

            ↓

            **🥉 HDFS Bronze**

            ↓

            **🥈 Spark Silver**

            ↓

            **🥇 Spark Gold**

            ↓

            **📊 NEO Tracker**
            """)


# ============================================================
# SYSTEM STATUS
# ============================================================

st.header("📡 System Status")

status1, status2, status3, status4 = st.columns(4)


with status1:
    st.metric(
        "🟢 HDFS",
        "ONLINE",
    )


with status2:
    st.metric(
        "🟢 SPARK",
        "ONLINE",
    )


with status3:
    st.metric(
        "🟢 KAFKA",
        "ONLINE",
    )


with status4:
    st.metric(
        "🟢 DASHBOARD",
        "ONLINE",
    )


# ============================================================
# SUMMARY
# ============================================================

st.header("🎯 Architecture Summary")

st.success(
    "🚀 **Space Data Center opérationnel** — "
    "les sources Gaia DR3 et NASA NeoWs sont intégrées "
    "dans une architecture Data Lake Bronze → Silver → Gold."
)

st.write(
    "Gaia DR3 alimente le pipeline batch tandis que "
    "NASA NeoWs alimente le pipeline streaming. "
    "Les deux flux convergent vers la Gold Layer pour "
    "alimenter les dashboards analytiques."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    '🚀 SPACE DATA CENTER · '
    'ARCHITECTURE · '
    'BRONZE → SILVER → GOLD · '
    'GAIA DR3 · NASA NEOWS'
    '</div>',
    unsafe_allow_html=True,
)