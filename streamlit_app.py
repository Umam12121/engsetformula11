import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngsetPro Professional",
    page_icon="📡",
    layout="wide"
)


# =========================
# UNPIX MOBILE-INSPIRED UI STYLE
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;500;600;700&display=swap');

/* ── Global Reset ── */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #EEF4FF;
    font-family: 'Nunito', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #dbeafe 0%, #EEF4FF 40%, #f0f9ff 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 60%, #1e3a8a 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(29,78,216,0.18);
}

[data-testid="stSidebar"] * {
    color: #e0eaff !important;
    font-family: 'Nunito', sans-serif !important;
}

[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 10px 16px !important;
    margin-bottom: 6px;
    transition: background 0.2s;
    font-weight: 600 !important;
    font-size: 15px !important;
    display: block;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.18) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #93c5fd !important;
    font-size: 13px;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── Header Banner ── */
.unpix-header {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
    border-radius: 24px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(29,78,216,0.28);
    position: relative;
    overflow: hidden;
}

.unpix-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.07);
    border-radius: 50%;
}

.unpix-header::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 60px;
    width: 240px; height: 240px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}

.header-left {}

.header-app-name {
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #93c5fd;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0;
}

.header-subtitle {
    font-size: 14px;
    color: #bfdbfe;
    margin-top: 6px;
    font-weight: 500;
}

.header-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 8px 20px;
    color: white;
    font-size: 13px;
    font-weight: 700;
    backdrop-filter: blur(8px);
}

/* ── Section Title ── */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #1e40af;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Card ── */
.unpix-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(219,234,254,0.8);
    box-shadow: 0 4px 20px rgba(29,78,216,0.07);
    margin-bottom: 16px;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 16px 0;
}

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 20px 16px;
    border: 1.5px solid #dbeafe;
    box-shadow: 0 4px 16px rgba(29,78,216,0.07);
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(29,78,216,0.13);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #1d4ed8, #3b82f6);
    border-radius: 18px 18px 0 0;
}

.metric-icon {
    width: 44px; height: 44px;
    border-radius: 14px;
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    margin: 0 auto 10px auto;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #1e40af;
    line-height: 1;
}

.metric-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 600;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-card.green::before { background: linear-gradient(90deg, #16a34a, #4ade80); }
.metric-card.green .metric-value { color: #15803d; }
.metric-card.red::before { background: linear-gradient(90deg, #dc2626, #f87171); }
.metric-card.red .metric-value { color: #b91c1c; }
.metric-card.orange::before { background: linear-gradient(90deg, #d97706, #fbbf24); }
.metric-card.orange .metric-value { color: #b45309; }

/* ── Status Badge ── */
.status-optimal {
    display: inline-block;
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    color: #15803d;
    border: 1.5px solid #86efac;
    border-radius: 50px;
    padding: 4px 16px;
    font-size: 13px;
    font-weight: 700;
}

.status-congested {
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #b91c1c;
    border: 1.5px solid #fca5a5;
    border-radius: 50px;
    padding: 4px 16px;
    font-size: 13px;
    font-weight: 700;
}

/* ── Input styling ── */
[data-testid="stNumberInput"] input {
    border-radius: 14px !important;
    border: 2px solid #dbeafe !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: #1e40af !important;
    background: #f8faff !important;
    padding: 10px 14px !important;
    font-size: 16px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

[data-testid="stNumberInput"] label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #374151 !important;
    font-size: 14px !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 36px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 16px rgba(29,78,216,0.30) !important;
    transition: all 0.2s !important;
    width: 100%;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    box-shadow: 0 8px 24px rgba(29,78,216,0.40) !important;
    transform: translateY(-2px);
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    color: white !important;
    border-radius: 16px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(15,118,110,0.30) !important;
}

/* ── Divider ── */
hr {
    border-color: #dbeafe !important;
    margin: 20px 0 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden;
    border: 1.5px solid #dbeafe !important;
}

/* ── Alert / Info ── */
[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: none !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Plot ── */
[data-testid="stImage"] {
    border-radius: 16px;
}

/* ── Fast Menu Cards (input area) ── */
.input-card {
    background: white;
    border-radius: 20px;
    padding: 20px 24px 24px;
    border: 1.5px solid #dbeafe;
    box-shadow: 0 4px 20px rgba(29,78,216,0.06);
    margin-bottom: 20px;
}

.input-label {
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #1d4ed8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── History table rows ── */
.history-row {
    background: white;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 8px;
    border: 1.5px solid #dbeafe;
    display: flex;
    align-items: center;
    gap: 16px;
}

/* ── Page Headings ── */
h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    color: #1e40af !important;
    font-weight: 700 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #eff6ff; }
::-webkit-scrollbar-thumb { background: #93c5fd; border-radius: 10px; }

</style>
""", unsafe_allow_html=True)


# =========================
# ENGSET MODEL
# =========================
def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, M):
    num = nCr(S - 1, N) * (M ** N)
    den = sum(nCr(S - 1, k) * (M ** k) for k in range(N + 1))
    return num / den if den != 0 else 0


def iterate(S, N, rho):
    M = rho
    tol = 0.0001
    data = []

    i = 1
    while True:
        Pb = engset_pb(S, N, M)
        M_new = rho * (1 - Pb)
        diff = abs(M_new - M)

        data.append([i, M, Pb, diff])

        if diff < tol:
            break

        M = M_new
        i += 1

    return M_new, Pb, data, i


# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# HEADER — UNPIX style
# =========================
st.markdown("""
<div class="unpix-header">
    <div class="header-left">
        <div class="header-app-name">📡 EngsetPro</div>
        <div class="header-title">Engset Simulator</div>
        <div class="header-subtitle">Professional Blocking Probability Analysis System</div>
    </div>
    <div class="header-badge">✦ Pro Edition</div>
</div>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR NAV
# =========================
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📊 Analysis", "📁 History"]
)

st.sidebar.markdown("---")
st.sidebar.info("Engineering Simulation Tool")


# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown('<div class="input-card"><div class="input-label">📥 Input Parameter</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Number of Sources (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Number of Channels (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 RUN ANALYSIS"):

        if N >= S:
            st.error("Channel must be smaller than Source (N < S)")
        else:
            M, Pb, iter_data, iters = iterate(S, N, rho)

            status = "OPTIMAL" if Pb < 0.2 else "CONGESTED"

            st.session_state.result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "status": status,
                "iter": iters,
                "iter_data": iter_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.session_state.history.append(st.session_state.result)

    # RESULT DASHBOARD
    if "result" in st.session_state:

        r = st.session_state.result

        status_class = "status-optimal" if r['status'] == "OPTIMAL" else "status-congested"

        st.markdown('<div class="section-title">📊 Results Overview</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card {'green' if r['status'] == 'OPTIMAL' else 'red'}">
                <div class="metric-icon">🔒</div>
                <div class="metric-value">{r['Pb']:.6f}</div>
                <div class="metric-label">Blocking Prob.</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📶</div>
                <div class="metric-value">{r['M']:.6f}</div>
                <div class="metric-label">Traffic Idle (M)</div>
            </div>
            <div class="metric-card orange">
                <div class="metric-icon">🔄</div>
                <div class="metric-value">{r['iter']}</div>
                <div class="metric-label">Iterations</div>
            </div>
            <div class="metric-card {'green' if r['status'] == 'OPTIMAL' else 'red'}">
                <div class="metric-icon">{'✅' if r['status'] == 'OPTIMAL' else '⚠️'}</div>
                <div class="metric-value"><span class="{status_class}">{r['status']}</span></div>
                <div class="metric-label">System Status</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# ANALYSIS PAGE
# =========================
elif page == "📊 Analysis":

    st.markdown('<div class="section-title">📊 System Analysis</div>', unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.warning("No simulation data available. Please run an analysis on the Dashboard first.")
    else:

        r = st.session_state.result

        st.markdown('<div class="section-title">🔁 Convergence Iteration Table</div>', unsafe_allow_html=True)
        st.dataframe(r["iter_data"], use_container_width=True)

        st.markdown('<div class="section-title">📈 Blocking Probability Graph</div>', unsafe_allow_html=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f8faff')

        ax.fill_between(x, y, alpha=0.15, color="#1d4ed8")
        ax.plot(x, y, linewidth=2.5, color="#1d4ed8", marker='o', markersize=5, markerfacecolor='white', markeredgewidth=2)
        ax.axhline(0.2, linestyle="--", color="#ef4444", linewidth=1.5, label="Threshold (0.2)")

        ax.set_xlabel("Number of Channels", fontsize=12, color="#374151", fontweight='bold')
        ax.set_ylabel("Blocking Probability", fontsize=12, color="#374151", fontweight='bold')
        ax.grid(True, color='#dbeafe', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dbeafe')
        ax.spines['bottom'].set_color('#dbeafe')
        ax.tick_params(colors='#64748b')
        ax.legend(fontsize=11)

        st.pyplot(fig)


# =========================
# HISTORY PAGE
# =========================
elif page == "📁 History":

    st.markdown('<div class="section-title">📁 Simulation History</div>', unsafe_allow_html=True)

    if st.session_state.history:

        table = []

        for i, r in enumerate(st.session_state.history, 1):
            table.append([
                i,
                r["time"],
                r["S"],
                r["N"],
                r["rho"],
                round(r["M"], 6),
                round(r["Pb"], 6),
                r["iter"],
                r["status"]
            ])

        st.dataframe(table, use_container_width=True)

    else:
        st.info("No history yet. Run a simulation on the Dashboard first.")


# =========================
# PROFESSIONAL PDF EXPORT
# =========================
def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ENGSETPRO SIMULATION REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Professional Engset Blocking Probability Analysis", styles["BodyText"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("1. System Parameters", styles["Heading2"]))

    param = f"""
    <b>Sources (S):</b> {data['S']}<br/>
    <b>Channels (N):</b> {data['N']}<br/>
    <b>Traffic per Source (ρ):</b> {data['rho']}<br/>
    <b>Idle Traffic (M):</b> {data['M']:.6f}<br/>
    <b>Blocking Probability:</b> {data['Pb']:.6f}<br/>
    <b>Status:</b> {data['status']}<br/>
    <b>Iterations:</b> {data['iter']}<br/>
    """

    elements.append(Paragraph(param, styles["BodyText"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("2. Iteration Convergence", styles["Heading2"]))

    table_data = [["Iter", "M", "Pb", "Diff"]]
    table_data += [[str(x) for x in row] for row in data["iter_data"]]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=200)
    img.seek(0)

    elements.append(Paragraph("3. Blocking Probability Graph", styles["Heading2"]))
    elements.append(Image(img, width=450, height=250))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("4. Conclusion", styles["Heading2"]))

    conclusion = f"""
    The system is classified as <b>{data['status']}</b> based on the calculated blocking probability.
    """

    elements.append(Paragraph(conclusion, styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer


# =========================
# EXPORT BUTTON
# =========================
if page == "📁 History":

    st.markdown("---")

    if st.button("📥 EXPORT PROFESSIONAL REPORT"):

        if st.session_state.history:

            last = st.session_state.history[-1]

            S = last["S"]
            rho = last["rho"]

            x = list(range(1, S))
            y = [engset_pb(S, n, rho) for n in x]

            fig, ax = plt.subplots()
            ax.plot(x, y, color="#1d4ed8")
            ax.axhline(0.2, linestyle="--", color="red")
            ax.grid()

            pdf = export_pdf(last, fig)

            st.download_button(
                "⬇️ Download Professional PDF",
                data=pdf,
                file_name="EngsetPro_Professional_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No data to export")
