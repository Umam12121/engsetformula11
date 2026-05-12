import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngsetPro Professional",
    page_icon="📡",
    layout="wide"
)


# =========================
# UNPIX MOBILE-RESPONSIVE UI STYLE
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

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem !important;
}

[data-testid="stSidebar"] * {
    color: #e0eaff !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Sidebar navigation label header ── */
[data-testid="stSidebar"] .stRadio > label {
    color: #93c5fd !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 8px !important;
    display: block;
    margin-bottom: 4px;
}

/* ── Sidebar radio items ── */
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
    color: #93c5fd !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    transition: background 0.2s;
    font-weight: 700 !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    cursor: pointer;
    border: 1.5px solid transparent;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.16) !important;
    border-color: rgba(255,255,255,0.15) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [aria-checked="true"] ~ label {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.3) !important;
}

/* Radio dot color */
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #93c5fd !important;
    font-size: 12px;
    line-height: 1.5;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
    margin: 16px 0 !important;
}

/* Sidebar info box */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    color: #bfdbfe !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #bfdbfe !important;
    font-size: 13px !important;
}

/* ── Header Banner ── */
.unpix-header {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
    border-radius: 24px;
    padding: 28px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
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
    pointer-events: none;
}

.unpix-header::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 60px;
    width: 240px; height: 240px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    pointer-events: none;
}

.header-app-name {
    font-family: 'Poppins', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #93c5fd;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0;
}

.header-subtitle {
    font-size: 13px;
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
    white-space: nowrap;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #1e40af;
    margin: 20px 0 12px 0;
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

/* ── Metric Cards — responsive grid ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0;
}

@media (max-width: 900px) {
    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .metric-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .header-title { font-size: 20px; }
    .unpix-header { padding: 20px 18px; }
}

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 18px 12px;
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
    width: 42px; height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin: 0 auto 10px auto;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #1e40af;
    line-height: 1;
    word-break: break-all;
}

.metric-label {
    font-size: 10px;
    color: #64748b;
    font-weight: 700;
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
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}

.status-congested {
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #b91c1c;
    border: 1.5px solid #fca5a5;
    border-radius: 50px;
    padding: 3px 12px;
    font-size: 11px;
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
    width: 100%;
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

/* ── Input card ── */
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

/* ── Column gap fix for mobile ── */
[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
}

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

        data.append([i, round(M, 16), round(Pb, 16), round(diff, 16)])

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
with st.sidebar:
    st.markdown(
        '<div style="font-family:Poppins,sans-serif;font-size:11px;font-weight:700;'
        'color:#93c5fd;text-transform:uppercase;letter-spacing:2px;'
        'margin-bottom:10px;padding:0 4px;">Navigation</div>',
        unsafe_allow_html=True
    )
    page = st.radio(
        "",
        ["🏠 Dashboard", "📊 Analysis", "📁 History"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.info("Engineering Simulation Tool")


# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown('<div class="input-card"><div class="input-label">📥 Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        S = st.number_input("Number of Sources (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Number of Channels (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5, step=0.01, format="%.2f")

    st.markdown('</div>', unsafe_allow_html=True)

    btn_col, _ = st.columns([1, 2])
    with btn_col:
        run = st.button("🚀 RUN ANALYSIS")

    if run:
        if N >= S:
            st.error("⚠️ Channel (N) must be smaller than Source (S). Please adjust your values.")
        else:
            M, Pb, iter_data, iters = iterate(S, N, rho)
            status = "OPTIMAL" if Pb < 0.2 else "CONGESTED"

            st.session_state.result = {
                "S": S, "N": N, "rho": rho,
                "M": M, "Pb": Pb, "status": status,
                "iter": iters, "iter_data": iter_data,
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
        st.warning("⚠️ No simulation data. Please run an analysis on the Dashboard first.")
    else:
        r = st.session_state.result

        st.markdown('<div class="section-title">🔁 Convergence Iteration Table</div>', unsafe_allow_html=True)

        import pandas as pd
        df = pd.DataFrame(r["iter_data"], columns=["Iter", "M", "Pb", "Diff"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-title">📈 Blocking Probability Graph</div>', unsafe_allow_html=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f8faff')

        ax.fill_between(x, y, alpha=0.15, color="#1d4ed8")
        ax.plot(x, y, linewidth=2.5, color="#1d4ed8", marker='o',
                markersize=5, markerfacecolor='white', markeredgewidth=2)
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
        import pandas as pd

        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                "#": i,
                "Time": r["time"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "M": round(r["M"], 6),
                "Pb": round(r["Pb"], 6),
                "Iter": r["iter"],
                "Status": r["status"]
            })

        df_hist = pd.DataFrame(rows)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

    else:
        st.info("📭 No history yet. Run a simulation on the Dashboard first.")

    st.markdown("---")

    # =========================
    # PROFESSIONAL PDF EXPORT
    # =========================
    def export_pdf(data, fig):
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm,
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=20,
            spaceAfter=6,
            textColor=colors.HexColor("#1d4ed8"),
            alignment=TA_CENTER,
        )

        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            spaceAfter=20,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_CENTER,
        )

        heading2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#1e40af"),
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=18,
            textColor=colors.HexColor("#374151"),
        )

        label_style = ParagraphStyle(
            'LabelStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=18,
            textColor=colors.HexColor("#1e40af"),
        )

        elements = []

        # ── Title block ──
        elements.append(Paragraph("ENGSETPRO SIMULATION REPORT", title_style))
        elements.append(Paragraph("Professional Engset Blocking Probability Analysis", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5,
                                   color=colors.HexColor("#1d4ed8"), spaceAfter=12))

        # ── 1. System Parameters ──
        elements.append(Paragraph("1. System Parameters", heading2_style))

        param_data = [
            ["Parameter", "Value"],
            ["Sources (S)", str(data['S'])],
            ["Channels (N)", str(data['N'])],
            ["Traffic per Source (ρ)", str(data['rho'])],
            ["Idle Traffic (M)", f"{data['M']:.6f}"],
            ["Blocking Probability (Pb)", f"{data['Pb']:.6f}"],
            ["System Status", data['status']],
            ["Iterations", str(data['iter'])],
            ["Timestamp", data['time']],
        ]

        param_table = Table(param_data, colWidths=[7*cm, 9*cm])
        param_table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 10),
            ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
            # Data rows
            ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME",     (1, 1), (1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 10),
            ("TEXTCOLOR",    (0, 1), (0, -1), colors.HexColor("#1e40af")),
            ("TEXTCOLOR",    (1, 1), (1, -1), colors.HexColor("#374151")),
            # Zebra rows
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.HexColor("#f8faff"), colors.white]),
            # Grid
            ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
            ("LINEBELOW",    (0, 0), (-1, 0), 1.5, colors.HexColor("#1d4ed8")),
            # Padding
            ("TOPPADDING",   (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            # Status color
            ("TEXTCOLOR",    (1, 6), (1, 6),
             colors.HexColor("#15803d") if data['status'] == "OPTIMAL"
             else colors.HexColor("#b91c1c")),
            ("FONTNAME",     (1, 6), (1, 6), "Helvetica-Bold"),
        ]))

        elements.append(param_table)
        elements.append(Spacer(1, 16))

        # ── 2. Iteration Convergence ──
        elements.append(Paragraph("2. Iteration Convergence", heading2_style))

        col_widths = [2*cm, 5*cm, 5*cm, 4*cm]
        iter_header = [["Iter", "M", "Pb", "Diff"]]
        iter_rows = [[str(row[0]),
                      f"{row[1]:.10f}",
                      f"{row[2]:.10f}",
                      f"{row[3]:.2e}"] for row in data["iter_data"]]
        table_data = iter_header + iter_rows

        iter_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        iter_table.setStyle(TableStyle([
            # Header
            ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 9),
            ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
            # Data
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("ALIGN",        (0, 1), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1),
             [colors.HexColor("#f8faff"), colors.white]),
            ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#dbeafe")),
            ("LINEBELOW",    (0, 0), (-1, 0), 1.5, colors.HexColor("#1d4ed8")),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(iter_table)
        elements.append(Spacer(1, 16))

        # ── 3. Blocking Probability Graph ──
        elements.append(Paragraph("3. Blocking Probability Graph", heading2_style))

        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", dpi=180, bbox_inches='tight',
                    facecolor='#f8faff')
        img_buf.seek(0)

        chart_img = Image(img_buf, width=16*cm, height=8*cm)
        elements.append(chart_img)
        elements.append(Spacer(1, 16))

        # ── 4. Conclusion ──
        elements.append(HRFlowable(width="100%", thickness=1,
                                   color=colors.HexColor("#dbeafe"), spaceAfter=8))
        elements.append(Paragraph("4. Conclusion", heading2_style))

        color_word = "#15803d" if data['status'] == "OPTIMAL" else "#b91c1c"
        conclusion = (
            f'Based on the Engset iterative model with <b>S={data["S"]}</b> sources, '
            f'<b>N={data["N"]}</b> channels, and traffic intensity <b>ρ={data["rho"]}</b>, '
            f'the system converged in <b>{data["iter"]} iterations</b>. '
            f'The calculated blocking probability is <b>{data["Pb"]:.6f}</b> '
            f'with idle traffic <b>M={data["M"]:.6f}</b>. '
            f'The system is classified as '
            f'<font color="{color_word}"><b>{data["status"]}</b></font>.'
        )
        elements.append(Paragraph(conclusion, body_style))

        # Footer spacer
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=0.5,
                                   color=colors.HexColor("#dbeafe"), spaceAfter=4))

        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor("#94a3b8"),
            alignment=TA_CENTER,
        )
        elements.append(Paragraph(
            f"Generated by EngsetPro Professional · {data['time']}",
            footer_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    # Export button
    if st.button("📥 EXPORT PROFESSIONAL REPORT"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            S = last["S"]
            rho = last["rho"]

            x = list(range(1, S))
            y = [engset_pb(S, n, rho) for n in x]

            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('#f8faff')
            ax.set_facecolor('#f8faff')
            ax.fill_between(x, y, alpha=0.15, color="#1d4ed8")
            ax.plot(x, y, linewidth=2.5, color="#1d4ed8", marker='o',
                    markersize=5, markerfacecolor='white', markeredgewidth=2)
            ax.axhline(0.2, linestyle="--", color="#ef4444",
                       linewidth=1.5, label="Threshold (0.2)")
            ax.set_xlabel("Number of Channels", fontsize=11,
                          color="#374151", fontweight='bold')
            ax.set_ylabel("Blocking Probability", fontsize=11,
                          color="#374151", fontweight='bold')
            ax.grid(True, color='#dbeafe', linewidth=1)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#dbeafe')
            ax.spines['bottom'].set_color('#dbeafe')
            ax.tick_params(colors='#64748b')
            ax.legend(fontsize=10)

            pdf = export_pdf(last, fig)

            st.download_button(
                "⬇️ Download Professional PDF",
                data=pdf,
                file_name="EngsetPro_Professional_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("⚠️ No data to export. Run a simulation first.")
