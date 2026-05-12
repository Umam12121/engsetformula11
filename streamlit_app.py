import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="EngsetPro Simulator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# TEMA STARTUP MODERN
# =========================
st.markdown("""
<style>
html, body, [class*='css'] {
    font-family: 'Inter', sans-serif;
    background: #f8fafc;
}

/* TOP NAVBAR STYLE */
.navbar {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    padding: 14px 20px;
    border-radius: 14px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 8px 20px rgba(29,78,216,0.25);
}

.navbar h1 {
    font-size: 20px;
    margin: 0;
}

.navbar small {
    opacity: 0.9;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

[data-testid="metric-container"] {
    background: #eef2ff;
    border-radius: 14px;
    padding: 12px;
    border: 1px solid #c7d2fe;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 18px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown("""
<div class='navbar'>
    <h1>📡 EngsetPro Simulator</h1>
    <small>Sistem Analisis Telekomunikasi Profesional</small>
</div>
""", unsafe_allow_html=True)

# =========================
# MODEL ENGSET
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
# SIDEBAR MENU (lebih modern)
# =========================
st.sidebar.markdown("## 📊 MENU")
page = st.sidebar.radio("Navigasi", ["🏠 Dashboard", "📈 Analisis", "📁 Riwayat"])

st.sidebar.markdown("---")
st.sidebar.caption("EngsetPro • Startup Simulation Tool")

# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown("### 📥 Input Parameter Sistem")

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Jumlah Sumber (S)", min_value=1, value=10)
    with col2:
        N = st.number_input("Jumlah Kanal (N)", min_value=1, value=3)
    with col3:
        rho = st.number_input("Traffic per Sumber (ρ)", min_value=0.0, value=0.5)

    if st.button("🚀 Jalankan Simulasi"):

        if N >= S:
            st.error("Jumlah kanal harus lebih kecil dari sumber")
        else:
            M, Pb, iter_data, iters = iterate(S, N, rho)

            status = "OPTIMAL" if Pb < 0.2 else "OVERLOAD"

            st.session_state.result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "status": status,
                "iter": iters,
                "iter_data": iter_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M")
            }

            st.session_state.history.append(st.session_state.result)

    if "result" in st.session_state:
        r = st.session_state.result

        st.markdown("### 📊 Hasil Analisis")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Blocking Probability", f"{r['Pb']:.6f}")
        c2.metric("Idle Traffic", f"{r['M']:.6f}")
        c3.metric("Iterasi", r["iter"])
        c4.metric("Status", r["status"])

# =========================
# ANALISIS
# =========================
elif page == "📈 Analisis":

    st.markdown("### 📊 Analisis Sistem")

    if "result" not in st.session_state:
        st.warning("Belum ada data simulasi")
    else:
        r = st.session_state.result

        st.dataframe(r["iter_data"], use_container_width=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2)
        ax.axhline(0.2, linestyle="--", color="red")
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

# =========================
# RIWAYAT + DOWNLOAD PDF (FIXED)
# =========================
elif page == "📁 Riwayat":

    st.markdown("### 📁 Riwayat Simulasi")

    if st.session_state.history:
        st.dataframe(st.session_state.history, use_container_width=True)

        st.markdown("---")

        # ================= EXPORT BUTTON FIX =================
        if st.button("📄 Download Laporan PDF Profesional"):

            last = st.session_state.history[-1]

            S = last["S"]
            rho = last["rho"]

            x = list(range(1, S))
            y = [engset_pb(S, n, rho) for n in x]

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.axhline(0.2, linestyle="--", color="red")
            ax.grid()

            pdf = export_pdf(last, fig)

            st.download_button(
                label="⬇️ Unduh PDF",
                data=pdf,
                file_name="EngsetPro_Report_Professional.pdf",
                mime="application/pdf"
            )

    else:
        st.info("Belum ada riwayat")

# =========================
# PDF PROFESIONAL
# =========================
def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor("#1d4ed8")
    )

    normal = ParagraphStyle(
        "normal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14
    )

    elements = []

    elements.append(Paragraph("LAPORAN ANALISIS ENGSETPRO", title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Simulasi Probabilitas Blocking Sistem Telekomunikasi", normal))
    elements.append(Spacer(1, 15))

    # PARAMETER
    elements.append(Paragraph("1. Parameter Sistem", styles["Heading2"]))

    param = f"""
    Sumber: {data['S']}<br/>
    Kanal: {data['N']}<br/>
    Traffic: {data['rho']}<br/>
    Idle Traffic: {data['M']:.6f}<br/>
    Blocking: {data['Pb']:.6f}<br/>
    Status: {data['status']}<br/>
    Iterasi: {data['iter']}
    """

    elements.append(Paragraph(param, normal))
    elements.append(Spacer(1, 15))

    # TABLE
    table_data = [["Iter", "M", "Pb", "Diff"]]
    table_data += [[str(x) for x in row] for row in data["iter_data"]]

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # GRAPH
    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=250, bbox_inches='tight')
    img.seek(0)

    elements.append(Paragraph("2. Grafik Analisis", styles["Heading2"]))
    elements.append(Image(img, width=450, height=250))

    elements.append(Spacer(1, 15))

    # CONCLUSION
    elements.append(Paragraph("3. Kesimpulan", styles["Heading2"]))

    elements.append(Paragraph(
        f"Sistem berada dalam kondisi <b>{data['status']}</b> berdasarkan analisis probabilitas blocking.",
        normal
    ))

    doc.build(elements)
    buffer.seek(0)

    return buffer
