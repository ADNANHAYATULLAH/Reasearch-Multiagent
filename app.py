
import streamlit as st
from crew import run_research

st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(91, 33, 182, .18), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(6, 182, 212, .15), transparent 25%),
        linear-gradient(135deg, #070b16 0%, #0d1222 48%, #111827 100%);
    color: #f8fafc;
}
.block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem; }
.hero {
    padding: 2.2rem 2.4rem;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(124,58,237,.22), rgba(8,145,178,.13));
    box-shadow: 0 25px 70px rgba(0,0,0,.28);
    margin-bottom: 1.4rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    line-height: 1;
    margin: 0 0 .7rem 0;
    letter-spacing: -2px;
}
.hero p { color: #cbd5e1; font-size: 1.05rem; max-width: 780px; }
.badge {
    display: inline-block;
    padding: .38rem .75rem;
    border-radius: 999px;
    background: rgba(34,197,94,.12);
    color: #86efac;
    border: 1px solid rgba(134,239,172,.18);
    font-size: .8rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
.card {
    padding: 1rem 1.15rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(15,23,42,.72);
    backdrop-filter: blur(12px);
    margin-bottom: .8rem;
}
.card-title { font-weight: 700; font-size: 1rem; margin-bottom: .25rem; }
.card-sub { color: #94a3b8; font-size: .85rem; }
.working {
    border: 1px solid rgba(34,211,238,.42);
    background: linear-gradient(135deg, rgba(8,145,178,.20), rgba(30,41,59,.72));
    box-shadow: 0 0 30px rgba(34,211,238,.08);
}
.done { border-color: rgba(34,197,94,.25); }
.waiting { opacity: .62; }
.status-dot {
    display:inline-block; width:10px; height:10px; border-radius:50%;
    margin-right:8px; background:#22d3ee; box-shadow:0 0 14px #22d3ee;
}
.done .status-dot { background:#22c55e; box-shadow:0 0 12px #22c55e; }
.waiting .status-dot { background:#64748b; box-shadow:none; }
.stButton > button {
    border: 0;
    border-radius: 14px;
    min-height: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #0891b2);
    color: white;
    box-shadow: 0 12px 28px rgba(124,58,237,.24);
}
.stButton > button:hover {
    border: 0;
    transform: translateY(-1px);
    box-shadow: 0 15px 35px rgba(8,145,178,.22);
}
textarea, input {
    border-radius: 14px !important;
}
.source {
    padding: .8rem 1rem;
    margin: .45rem 0;
    border-radius: 12px;
    background: rgba(30,41,59,.55);
    border: 1px solid rgba(255,255,255,.08);
}
.small { color:#94a3b8; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)

AGENTS = [
    ("🧭", "Research Manager", "Breaks the question into a focused research plan"),
    ("🌐", "Web Researcher", "Searches the live web for relevant evidence"),
    ("📚", "Source Analyst", "Reads useful pages and extracts evidence"),
    ("🛡️", "Fact Checker", "Checks claims, gaps and contradictions"),
    ("✍️", "Report Writer", "Builds the final research report"),
]

def render_agent_panel(container, current_index, completed):
    html = '<div style="margin-top:1rem;">'
    for i, (icon, name, desc) in enumerate(AGENTS):
        if i in completed:
            cls, state = "card done", "DONE"
        elif i == current_index:
            cls, state = "card working", "WORKING NOW"
        else:
            cls, state = "card waiting", "QUEUED"
        html += f"""
        <div class="{cls}">
          <div class="card-title"><span class="status-dot"></span>{icon} {name}
          <span style="float:right;font-size:.72rem;color:#94a3b8;">{state}</span></div>
          <div class="card-sub">{desc}</div>
        </div>
        """
    html += "</div>"
    container.markdown(html, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔬 ResearchForge")
    st.caption("CrewAI × Groq research team")
    st.markdown("---")
    st.markdown("### Team")
    for icon, name, _ in AGENTS:
        st.markdown(f"**{icon} {name}**")
    st.markdown("---")
    st.caption("Live web research • source analysis • fact checking")

st.markdown("""
<div class="hero">
  <div class="badge">● MULTI-AGENT RESEARCH LAB</div>
  <h1>ResearchForge AI</h1>
  <p>Ask a research question and let a focused CrewAI team investigate the web, inspect sources, challenge claims, and assemble a structured report.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown("### What should the team research?")
    question = st.text_area(
        "Research question",
        placeholder="Example: What are the latest developments in AI-assisted PLC programming in 2026?",
        height=150,
        label_visibility="collapsed",
    )
    depth = st.select_slider(
        "Research depth",
        options=["Quick", "Standard", "Deep"],
        value="Standard",
    )
    start = st.button("🚀 Start Research", use_container_width=True)

with right:
    st.markdown("### How it works")
    st.markdown("""
    <div class="card"><b>01</b> 🧭 Plan the investigation</div>
    <div class="card"><b>02</b> 🌐 Search live sources</div>
    <div class="card"><b>03</b> 📚 Read & extract evidence</div>
    <div class="card"><b>04</b> 🛡️ Challenge the findings</div>
    <div class="card"><b>05</b> ✍️ Write the report</div>
    """, unsafe_allow_html=True)

if start:
    if not question.strip():
        st.warning("Please enter a research question first.")
        st.stop()

    st.markdown("---")
    progress = st.progress(0)
    status = st.empty()
    panel = st.empty()
    completed = set()

    def ui_callback(index, name):
        status.markdown(
            f'<div class="card working"><b>⚡ Working now:</b> {name}</div>',
            unsafe_allow_html=True,
        )
        render_agent_panel(panel, index, completed)
        progress.progress(index / len(AGENTS))

    try:
        result = run_research(
            question=question.strip(),
            depth=depth,
            on_agent_start=ui_callback,
            on_agent_done=lambda index: completed.add(index),
        )

        progress.progress(1.0)
        status.markdown(
            '<div class="card done"><b>✅ Research complete.</b> The team has finished the investigation.</div>',
            unsafe_allow_html=True,
        )
        render_agent_panel(panel, -1, set(range(len(AGENTS))))

        st.markdown("---")
        st.markdown("## 📄 Final Research Report")
        st.markdown(result["report"])

        if result.get("sources"):
            st.markdown("## 🔗 Key Sources")
            for src in result["sources"]:
                title = src.get("title", "Source")
                url = src.get("url", "")
                if url:
                    st.markdown(
                        f'<div class="source"><b>{title}</b><br><a href="{url}" target="_blank">{url}</a></div>',
                        unsafe_allow_html=True,
                    )
    except Exception as exc:
        status.error("The research run stopped because an error occurred.")
        st.exception(exc)
