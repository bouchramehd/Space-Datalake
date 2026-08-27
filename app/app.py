import streamlit as st
from textwrap import dedent


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
    page_title="Space Data Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SPACE THEME
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
       STREAMLIT TOP HEADER
       Hide only the white Streamlit header / Deploy bar.
       The application design and sidebar remain unchanged.
    ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
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

        font-size: 4rem;

        font-weight: 800;

        letter-spacing: 3px;

        color: #ffffff;

        text-shadow:
            0 0 10px rgba(96, 165, 250, 0.8),
            0 0 25px rgba(59, 130, 246, 0.55),
            0 0 50px rgba(37, 99, 235, 0.30);

        margin-bottom: 0.5rem;
    }


    .space-subtitle {
        text-align: center;

        font-size: 1.1rem;

        letter-spacing: 3px;

        color: #94a3b8;

        margin-bottom: 3rem;
    }


    /* ========================================================
       MISSION STATUS
    ======================================================== */

    .mission-status {
        max-width: 950px;

        margin: 0 auto 3rem auto;

        padding: 1.8rem 2rem;

        text-align: center;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(15, 23, 42, 0.95),
                rgba(15, 23, 42, 0.70)
            );

        border:
            1px solid rgba(96, 165, 250, 0.35);

        box-shadow:
            0 0 35px rgba(37, 99, 235, 0.12);
    }


    .mission-title {
        font-size: 0.8rem;

        letter-spacing: 3px;

        color: #60a5fa;

        margin-bottom: 0.5rem;
    }


    .mission-ready {
        font-size: 1.6rem;

        font-weight: 700;

        color: #f8fafc;
    }


    .online {
        color: #4ade80;

        text-shadow:
            0 0 10px rgba(74, 222, 128, 0.8);
    }


    .mission-info {
        margin-top: 0.5rem;

        color: #64748b;

        font-size: 0.85rem;
    }


    /* ========================================================
       SECTION TITLES
    ======================================================== */

    .section-title {
        font-size: 1.7rem;

        font-weight: 700;

        color: #e2e8f0;

        margin-top: 2rem;

        margin-bottom: 1.5rem;
    }


    /* ========================================================
       SOURCE CARDS
    ======================================================== */

    .source-card {
        min-height: 250px;

        padding: 2rem;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(15, 23, 42, 0.65)
            );

        border:
            1px solid rgba(96, 165, 250, 0.25);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.30);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }


    .source-card:hover {
        transform: translateY(-5px);

        border-color:
            rgba(96, 165, 250, 0.70);

        box-shadow:
            0 15px 45px rgba(37, 99, 235, 0.18);
    }


    .source-icon {
        font-size: 3rem;

        margin-bottom: 0.8rem;
    }


    .source-title {
        font-size: 1.5rem;

        font-weight: 700;

        color: #f8fafc;

        margin-bottom: 0.7rem;
    }


    .source-description {
        color: #94a3b8;

        line-height: 1.6;

        font-size: 0.95rem;
    }


    .source-tag {
        display: inline-block;

        margin-top: 1.2rem;

        padding: 0.4rem 0.9rem;

        border-radius: 999px;

        background:
            rgba(59, 130, 246, 0.12);

        border:
            1px solid rgba(96, 165, 250, 0.25);

        color: #93c5fd;

        font-size: 0.72rem;

        font-weight: 600;

        letter-spacing: 1.5px;
    }


    /* ========================================================
       PIPELINE
    ======================================================== */

    .architecture {
        margin-top: 3rem;

        padding: 2rem;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.88),
                rgba(2, 6, 23, 0.88)
            );

        border:
            1px solid rgba(96, 165, 250, 0.22);

        text-align: center;
    }


    .architecture-title {
        font-size: 1.3rem;

        font-weight: 700;

        color: #e2e8f0;

        margin-bottom: 1.5rem;
    }


    .pipeline {
        display: flex;

        justify-content: center;

        align-items: center;

        gap: 0.7rem;

        flex-wrap: wrap;
    }


    .pipeline-step {
        padding: 0.8rem 1rem;

        border-radius: 12px;

        background:
            rgba(30, 41, 59, 0.9);

        border:
            1px solid rgba(96, 165, 250, 0.25);

        color: #cbd5e1;

        font-size: 0.85rem;

        font-weight: 600;

        transition: 0.2s ease;
    }


    .pipeline-step:hover {
        border-color:
            rgba(96, 165, 250, 0.75);

        transform: translateY(-2px);
    }


    .pipeline-arrow {
        color: #60a5fa;

        font-size: 1.4rem;

        font-weight: bold;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .space-footer {
        text-align: center;

        margin-top: 3rem;

        padding-top: 2rem;

        border-top:
            1px solid rgba(148, 163, 184, 0.10);

        color: #64748b;

        font-size: 0.75rem;

        letter-spacing: 1.5px;

        line-height: 1.8;
    }

    </style>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        html_block("""
        <div style="
            text-align:center;
            padding:1rem 0 1.5rem 0;
        ">
            <div style="
                font-size:3rem;
            ">
                🚀
            </div>
            <div style="
                font-size:1.15rem;
                font-weight:700;
                letter-spacing:2px;
            ">
                SPACE DATA
            </div>
            <div style="
                color:#64748b;
                font-size:0.7rem;
                letter-spacing:3px;
            ">
                CENTER
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        html_block("""
        <div style="
            color:#60a5fa;
            font-size:0.7rem;
            font-weight:600;
            letter-spacing:2px;
            margin-bottom:0.8rem;
        ">
            MISSION CONTROL
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.success("● DATA LAKE ONLINE")

    st.markdown(
        html_block("""
        <div style="
            margin-top:1rem;
            color:#94a3b8;
            line-height:2;
            font-size:0.9rem;
        ">
            ⭐ Gaia Observatory<br>
            ☄️ NEO Tracker<br>
            🏗️ Data Lake Architecture
        </div>
        """),
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="space-title">🚀 SPACE DATA CENTER</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="space-subtitle">EXPLORE THE UNIVERSE THROUGH DATA</div>',
    unsafe_allow_html=True,
)


# ============================================================
# MISSION STATUS
# ============================================================

st.markdown(
    html_block("""
    <div class="mission-status">
        <div class="mission-title">
            MISSION STATUS
        </div>
        <div class="mission-ready">
            <span class="online">●</span>
            DATA CENTER OPERATIONAL
        </div>
        <div class="mission-info">
            Bronze → Silver → Gold → Visualization
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# MISSION OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">🛰️ Mission Overview</div>',
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


# ============================================================
# GAIA
# ============================================================

with col1:

    st.markdown(
        html_block("""
        <div class="source-card">
            <div class="source-icon">
                ⭐
            </div>
            <div class="source-title">
                Gaia Observatory
            </div>
            <div class="source-description">
                Explore stellar data from
                <b>Gaia DR3</b>.
                <br><br>
                Analyse millions of stars using:
                <br>
                • Temperature<br>
                • Magnitude<br>
                • Parallax<br>
                • Distance
            </div>
            <div class="source-tag">
                BATCH DATA
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ============================================================
# NASA
# ============================================================

with col2:

    st.markdown(
        html_block("""
        <div class="source-card">
            <div class="source-icon">
                ☄️
            </div>
            <div class="source-title">
                NEO Tracker
            </div>
            <div class="source-description">
                Explore
                <b>Near-Earth Objects</b>
                using NASA NeoWs data.
                <br><br>
                Analyse:
                <br>
                • Asteroid counts<br>
                • Potential hazards<br>
                • Diameter<br>
                • Close approaches
            </div>
            <div class="source-tag">
                STREAMING DATA
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ============================================================
# DATA LAKE ARCHITECTURE
# ============================================================

st.markdown(
    html_block("""
    <div class="architecture">
        <div class="architecture-title">
            🌌 DATA LAKE MISSION PIPELINE
        </div>
        <div class="pipeline">
            <div class="pipeline-step">
                📡 DATA SOURCES
            </div>
            <div class="pipeline-arrow">
                →
            </div>
            <div class="pipeline-step">
                🥉 BRONZE
            </div>
            <div class="pipeline-arrow">
                →
            </div>
            <div class="pipeline-step">
                🥈 SILVER
            </div>
            <div class="pipeline-arrow">
                →
            </div>
            <div class="pipeline-step">
                🥇 GOLD
            </div>
            <div class="pipeline-arrow">
                →
            </div>
            <div class="pipeline-step">
                📊 DASHBOARD
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    html_block("""
    <div class="space-footer">
        SPACE DATA CENTER · DATA LAKE VISUALIZATION SYSTEM
        <br>
        🚀 GAIA DR3 · NASA NEOWS · HDFS · SPARK · KAFKA
    </div>
    """),
    unsafe_allow_html=True,
)