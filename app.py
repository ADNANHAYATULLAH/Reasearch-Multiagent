import streamlit as st
from crew import run_research


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@500;600;700;800&display=swap');

    :root {
        --rf-ink: #0b1220;
        --rf-muted: #52647d;
        --rf-brand: #1a56db;
        --rf-accent: #0ea5e9;
        --rf-success: #16a34a;
        --rf-warning: #d97706;
        --rf-surface: rgba(255, 255, 255, 0.72);
        --rf-surface-strong: rgba(255, 255, 255, 0.9);
        --rf-border: rgba(255, 255, 255, 0.9);
        --rf-line: #dbe7ff;
        --rf-shadow: 0 18px 50px -22px rgba(26, 86, 219, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.95);
    }

    html, body, [class*="css"] {
        font-family: "Manrope", sans-serif;
    }

    .stApp {
        color: var(--rf-ink);
        background:
            radial-gradient(circle at 8% 7%, rgba(26, 86, 219, 0.2), transparent 28rem),
            radial-gradient(circle at 92% 18%, rgba(14, 165, 233, 0.18), transparent 31rem),
            radial-gradient(circle at 55% 100%, rgba(124, 58, 237, 0.1), transparent 34rem),
            linear-gradient(145deg, #f7faff 0%, #eef4ff 48%, #f4f8ff 100%);
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3,
    [data-testid="stHeadingWithActionElements"] {
        font-family: "Sora", sans-serif !important;
        color: var(--rf-ink) !important;
        letter-spacing: 0 !important;
    }

    h1 {
        font-size: clamp(2.15rem, 4vw, 3.35rem) !important;
        line-height: 1.08 !important;
        font-weight: 800 !important;
        margin-bottom: 0.75rem !important;
    }

    h2 { font-weight: 750 !important; }
    h3 { font-weight: 700 !important; }

    p, label, .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--rf-muted);
    }

    [data-testid="stMarkdownContainer"] p {
        line-height: 1.72;
    }

    hr {
        border-color: rgba(26, 86, 219, 0.12) !important;
        margin: 1.65rem 0 !important;
    }

    /* Sidebar: polished specialist console */
    section[data-testid="stSidebar"] {
        background: rgba(247, 250, 255, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.92);
        box-shadow: 18px 0 45px -34px rgba(26, 86, 219, 0.45);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.25rem;
    }

    section[data-testid="stSidebar"] h2 {
        color: var(--rf-brand) !important;
        font-size: 1.35rem !important;
        padding-bottom: 0.3rem;
    }

    section[data-testid="stSidebar"] h3 {
        margin-top: 0.55rem;
        font-size: 0.76rem !important;
        text-transform: uppercase;
        letter-spacing: 0.12em !important;
        color: #60708a !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        padding: 0.32rem 0;
        color: #41536d;
    }

    /* Frosted panels */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--rf-border) !important;
        border-radius: 18px !important;
        background: var(--rf-surface) !important;
        box-shadow: var(--rf-shadow) !important;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-1px);
        border-color: rgba(14, 165, 233, 0.28) !important;
        box-shadow: 0 22px 55px -25px rgba(26, 86, 219, 0.38), inset 0 1px 0 #ffffff !important;
    }

    /* Research prompt */
    [data-testid="stTextArea"] label,
    [data-testid="stSelectSlider"] label {
        font-family: "Sora", sans-serif !important;
        color: var(--rf-ink) !important;
        font-weight: 650 !important;
    }

    textarea {
        min-height: 180px !important;
        padding: 1.15rem 1.2rem !important;
        border: 1px solid var(--rf-line) !important;
        border-radius: 16px !important;
        background: var(--rf-surface-strong) !important;
        color: var(--rf-ink) !important;
        font-family: "Manrope", sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.65 !important;
        box-shadow: 0 10px 30px -24px rgba(26, 86, 219, 0.55), inset 0 1px 0 #ffffff !important;
        caret-color: var(--rf-brand);
        transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
    }

    textarea::placeholder {
        color: #7a8aa1 !important;
        opacity: 1 !important;
    }

    textarea:focus {
        border-color: var(--rf-accent) !important;
        background: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.13), 0 16px 36px -22px rgba(26, 86, 219, 0.42) !important;
    }

    /* Research depth control */
    [data-testid="stSelectSlider"] {
        padding: 0.35rem 0.15rem 0.15rem;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: linear-gradient(135deg, var(--rf-brand), var(--rf-accent)) !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 4px 14px rgba(26, 86, 219, 0.35) !important;
    }

    [data-testid="stSlider"] > div > div > div {
        color: var(--rf-ink) !important;
    }

    /* Primary and link buttons */
    .stButton > button,
    .stLinkButton > a {
        min-height: 3.25rem;
        border: 1px solid rgba(255, 255, 255, 0.66) !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, var(--rf-brand) 0%, var(--rf-accent) 100%) !important;
        color: #ffffff !important;
        font-family: "Sora", sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
        box-shadow: 0 15px 30px -14px rgba(26, 86, 219, 0.62), inset 0 1px 0 rgba(255, 255, 255, 0.28) !important;
        transition: transform 170ms ease, box-shadow 170ms ease, filter 170ms ease !important;
    }

    .stButton > button:hover,
    .stLinkButton > a:hover {
        transform: translateY(-2px);
        filter: saturate(1.08) brightness(1.03);
        box-shadow: 0 20px 36px -15px rgba(26, 86, 219, 0.72), inset 0 1px 0 rgba(255, 255, 255, 0.34) !important;
    }

    .stButton > button:focus-visible,
    .stLinkButton > a:focus-visible {
        outline: 3px solid rgba(14, 165, 233, 0.28) !important;
        outline-offset: 3px !important;
    }

    /* Progress and states */
    [data-testid="stProgress"] > div,
    [data-testid="stProgressBar"] > div {
        border-radius: 999px !important;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.78) !important;
        border: 1px solid rgba(219, 231, 255, 0.9);
    }

    [data-testid="stProgress"] > div > div,
    [data-testid="stProgressBar"] > div > div {
        border-radius: 999px !important;
        background: linear-gradient(90deg, var(--rf-brand), var(--rf-accent), #7c3aed) !important;
        background-size: 180% 100% !important;
        animation: rf-shimmer 2.8s linear infinite;
    }

    [data-testid="stAlert"] {
        border: 1px solid rgba(255, 255, 255, 0.88) !important;
        border-radius: 16px !important;
        box-shadow: 0 15px 38px -28px rgba(26, 86, 219, 0.52);
        backdrop-filter: blur(16px);
    }

    /* Report typography and links */
    [data-testid="stMarkdownContainer"] a {
        color: var(--rf-brand) !important;
        text-decoration-color: rgba(26, 86, 219, 0.32) !important;
        text-underline-offset: 3px;
    }

    code {
        border: 1px solid var(--rf-line);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.74) !important;
        color: #12469f !important;
    }

    @keyframes rf-shimmer {
        0% { background-position: 180% 0; }
        100% { background-position: -180% 0; }
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1.35rem 1rem 3.5rem;
        }

        h1 {
            font-size: 2.15rem !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT DEFINITIONS
# ============================================================

AGENTS = [
    (
        "🧭",
        "Research Manager",
        "Creates the research plan and identifies the important questions.",
    ),
    (
        "🌐",
        "Web Researcher",
        "Searches the live web for relevant evidence and sources.",
    ),
    (
        "📚",
        "Source Analyst",
        "Reads important webpages and extracts useful evidence.",
    ),
    (
        "🛡️",
        "Fact Checker",
        "Checks claims, contradictions, gaps and outdated information.",
    ),
    (
        "✍️",
        "Report Writer",
        "Combines the research into the final structured report.",
    ),
]


# ============================================================
# AGENT STATUS PANEL
# ============================================================

def render_agent_panel(container, current_index, completed):
    """
    Render agent status using native Streamlit components.

    No raw HTML is used here.
    """

    with container:

        st.markdown("### 🤖 Research Team")

        for i, (icon, name, description) in enumerate(AGENTS):

            if i in completed:
                state = "✅ DONE"
                state_color = "🟢"

            elif i == current_index:
                state = "⚡ WORKING NOW"
                state_color = "🔵"

            else:
                state = "⏳ QUEUED"
                state_color = "⚪"

            with st.container(border=True):

                col1, col2 = st.columns([5, 1])

                with col1:
                    st.markdown(
                        f"### {icon} {name}"
                    )

                    st.caption(description)

                with col2:
                    st.markdown(
                        f"**{state_color}**"
                    )
                    st.caption(state)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔬 ResearchForge AI")

    st.caption(
        "A multi-agent research team powered by "
        "CrewAI + Groq"
    )

    st.divider()

    st.markdown("### 🤖 AI Team")

    for icon, name, _ in AGENTS:
        st.markdown(f"{icon} **{name}**")

    st.divider()

    st.markdown("### 🧰 Team capabilities")

    st.markdown(
        """
        🌐 Live web research

        📚 Source inspection

        🛡️ Fact verification

        🧠 Multi-agent reasoning

        📄 Structured reports
        """
    )

    st.divider()

    st.caption(
        "ResearchForge AI • CrewAI Research Team"
    )


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("# 🔬 ResearchForge AI")

st.markdown(
    """
    ### Your AI research team

    Ask a research question and let five specialized AI agents
    investigate the web, inspect sources, verify important claims,
    and produce a structured research report.
    """
)

st.divider()


# ============================================================
# MAIN INPUT AREA
# ============================================================

left, right = st.columns(
    [1.65, 1],
    gap="large",
)


# ------------------------------------------------------------
# LEFT SIDE
# ------------------------------------------------------------

with left:

    st.markdown("### 🎯 What should the team research?")

    question = st.text_area(
        "Research question",
        placeholder=(
            "Example:\n\n"
            "What are the latest developments in "
            "AI-assisted PLC programming in 2026?"
        ),
        height=180,
        label_visibility="collapsed",
    )

    st.markdown("### 📊 Research depth")

    depth = st.select_slider(
        "Research depth",
        options=[
            "Quick",
            "Standard",
            "Deep",
        ],
        value="Standard",
        label_visibility="collapsed",
    )

    st.caption(
        "Quick = faster investigation • "
        "Standard = balanced research • "
        "Deep = broader investigation"
    )

    start = st.button(
        "🚀  START RESEARCH",
        use_container_width=True,
    )


# ------------------------------------------------------------
# RIGHT SIDE
# ------------------------------------------------------------

with right:

    st.markdown("### ⚙️ How it works")

    with st.container(border=True):
        st.markdown("**01  🧭 Plan**")
        st.caption(
            "The Research Manager breaks your question "
            "into research tasks."
        )

    with st.container(border=True):
        st.markdown("**02  🌐 Search**")
        st.caption(
            "The Web Researcher searches live sources."
        )

    with st.container(border=True):
        st.markdown("**03  📚 Analyze**")
        st.caption(
            "The Source Analyst reads important webpages."
        )

    with st.container(border=True):
        st.markdown("**04  🛡️ Verify**")
        st.caption(
            "The Fact Checker challenges important claims."
        )

    with st.container(border=True):
        st.markdown("**05  ✍️ Report**")
        st.caption(
            "The Report Writer creates the final report."
        )


# ============================================================
# RESEARCH EXECUTION
# ============================================================

if start:

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question.strip():

        st.warning(
            "⚠️ Please enter a research question first."
        )

        st.stop()


    # --------------------------------------------------------
    # Research section
    # --------------------------------------------------------

    st.divider()

    st.markdown("## 🧠 Research in progress")

    progress = st.progress(0)

    status_message = st.empty()

    agent_panel = st.empty()

    completed = set()


    # --------------------------------------------------------
    # Agent started callback
    # --------------------------------------------------------

    def ui_callback(index, name):

        status_message.info(
            f"⚡ **Currently working:** {name}"
        )

        render_agent_panel(
            agent_panel,
            index,
            completed,
        )

        progress.progress(
            int((index / len(AGENTS)) * 100)
        )


    # --------------------------------------------------------
    # Agent completed callback
    # --------------------------------------------------------

    def agent_done(index):

        completed.add(index)

        # Refresh panel immediately
        render_agent_panel(
            agent_panel,
            -1,
            completed,
        )


    # --------------------------------------------------------
    # Run research
    # --------------------------------------------------------

    try:

        result = run_research(
            question=question.strip(),
            depth=depth,
            on_agent_start=ui_callback,
            on_agent_done=agent_done,
        )


        # ----------------------------------------------------
        # Research complete
        # ----------------------------------------------------

        progress.progress(100)

        status_message.success(
            "✅ **Research complete!** "
            "All five agents have finished."
        )

        render_agent_panel(
            agent_panel,
            -1,
            set(range(len(AGENTS))),
        )


        # ----------------------------------------------------
        # Final report
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            "## 📄 Final Research Report"
        )

        st.markdown(
            result["report"]
        )


        # ----------------------------------------------------
        # Sources
        # ----------------------------------------------------

        sources = result.get("sources", [])

        if sources:

            st.divider()

            st.markdown(
                "## 🔗 Key Sources"
            )

            for number, source in enumerate(
                sources,
                start=1,
            ):

                title = source.get(
                    "title",
                    "Research Source",
                )

                url = source.get(
                    "url",
                    "",
                )

                if url:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{number}. {title}**"
                        )

                        st.link_button(
                            "🔗 Open source",
                            url,
                        )


    # --------------------------------------------------------
    # Error handling
    # --------------------------------------------------------

    except Exception as exc:

        status_message.error(
            "❌ The research run stopped because "
            "an error occurred."
        )

        st.error(
            "Something went wrong while running "
            "the research team."
        )

        st.exception(exc)
