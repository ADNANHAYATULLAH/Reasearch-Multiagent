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

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.13),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #070b16 0%,
                #0b1120 50%,
                #111827 100%
            );
    }

    /* Main width */
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Typography */
    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    /* Text area */
    textarea {
        border-radius: 16px !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 14px;
        min-height: 3.1rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(
            90deg,
            #7c3aed,
            #0891b2
        );
        color: white;
        box-shadow:
            0 10px 30px rgba(124, 58, 237, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 15px 35px rgba(8, 145, 178, 0.25);
    }

    /* Native containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
    }

    /* Progress bar */
    [data-testid="stProgressBar"] > div > div {
        border-radius: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0b1020,
                #111827
            );
    }

    /* Small muted text */
    .muted {
        color: #94a3b8;
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
