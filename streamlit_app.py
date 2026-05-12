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
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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
# TEMA STARTUP MODERN (BIRU - PUTIH)
# =========================
st.markdown("""
<style>

html, body, [class*='css'] {
    font-family: 'Inter', sans-serif;
    background: #f8fafc;
}

.header {
    padding: 28px;
    border-radius: 16px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: white;
    box-shadow: 0 10px 25px rgba(29,78,216,0.25);
}

.header h1 {
    margin: 0;
    font-size: 34px;
    font-weight: 800;
}

.header p {
    margin-top: 6px;
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
    border: none;
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
# HEADER
# =========================
st.markdown("""
<div class='header'>
    <h1>📡 EngsetPro</h1>
    <p>Simulasi Probabilitas Blocking Sistem Telekomunikasi (Gaya Startup Profesional)</p>
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
# SIDEBAR
# =========================
st.sidebar.title("📌 Menu Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Dashboard", "Analisis", "Riwayat"])

st.sidebar.markdown("---")
st.sidebar.caption("EngsetPro v2 • Sistem Simulasi Telekomunikasi")

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":

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

        c1.metric("Probabilitas Blocking", f"{r['Pb']:.6f}")
        c2.metric("Traffic Idle", f"{r['M']:.6f}")
        c3.metric("Iterasi", r["iter"])
        c4.metric("Status Sistem", r["status"])

# =========================
# ANALISIS
# =========================
elif page == "Analisis":

    st.markdown("### 📊 Analisis Sistem")

    if "result" not in st.session_state:
        st.warning("Belum ada data simulasi")
    else:
        r = st.session_state.result

        st.markdown("#### Tabel Konvergensi Iterasi")
        st.dataframe(r["iter_data"], use_container_width=True)

        st.markdown("#### Grafik Probabilitas Blocking")

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2)
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_xlabel("Jumlah Kanal")
        ax.set_ylabel("Probabilitas Blocking")
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

# =========================
# RIWAYAT
# =========================
elif page == "Riwayat":

    st.markdown("### 📁 Riwayat Simulasi")

    if st.session_state.history:
        st.dataframe(st.session_state.history, use_container_width=True)
    else:
        st.info("Belum ada riwayat")

# =========================
# PDF PROFESIONAL EXPORT (DITINGKATKAN)
# =========================
def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor("#1d4ed8")
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14
    )

    elements = []

    # COVER
    elements.append(Paragraph("ENGSETPRO SIMULATION REPORT", title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Laporan Analisis Probabilitas Blocking Sistem Telekomunikasi Berbasis Model Engset",
        normal_style
    ))
    elements.append(Spacer(1, 20))

    # PARAMETER
    elements.append(Paragraph("1. Parameter Sistem", styles['Heading2']))

    param = f"""
    Sumber (S): {data['S']}<br/>
    Kanal (N): {data['N']}<br/>
    Traffic per Sumber (ρ): {data['rho']}<br/>
    Traffic Idle (M): {data['M']:.6f}<br/>
    Probabilitas Blocking: {data['Pb']:.6f}<br/>
    Status: {data['status']}<br/>
    Iterasi: {data['iter']}<br/>
    """

    elements.append(Paragraph(param, normal_style))
    elements.append(Spacer(1, 15))

    # TABEL
    elements.append(Paragraph("2. Konvergensi Iterasi", styles['Heading2']))

    table_data = [["Iterasi", "M", "Pb", "Selisih"]]
    table_data += [[str(x) for x in row] for row in data["iter_data"]]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 8)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # GRAFIK
    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=250, bbox_inches='tight')
    img.seek(0)

    elements.append(Paragraph("3. Grafik Probabilitas Blocking", styles['Heading2']))
    elements.append(Image(img, width=450, height=250))

    elements.append(Spacer(1, 15))

    # KESIMPULAN
    elements.append(Paragraph("4. Kesimpulan", styles['Heading2']))

    conclusion = f"Sistem berada dalam kondisi <b>{data['status']}</b> berdasarkan hasil analisis probabilitas blocking."

    elements.append(Paragraph(conclusion, normal_style))

    doc.build(elements)
    buffer.seek(0)

    return buffer
