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
# PDF EXPORT (MORE PROFESSIONAL)
# =========================
def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=12,
        textColor=colors.HexColor("#1d4ed8")
    )

    subtitle_style = ParagraphStyle(
        "subtitle",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=20
    )

    normal = ParagraphStyle(
        "normal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14
    )

    elements = []

    # COVER
    elements.append(Paragraph("LAPORAN ANALISIS SISTEM ENGSETPRO", title_style))
    elements.append(Paragraph("Analisis Probabilitas Blocking Sistem Telekomunikasi", subtitle_style))

    elements.append(Spacer(1, 10))

    # SECTION 1
    elements.append(Paragraph("1. Parameter Sistem", styles["Heading2"]))

    param = f"""
    Sumber (S): {data['S']}<br/>
    Kanal (N): {data['N']}<br/>
    Traffic per Sumber (ρ): {data['rho']}<br/>
    Traffic Idle (M): {data['M']:.6f}<br/>
    Probabilitas Blocking: {data['Pb']:.6f}<br/>
    Status Sistem: {data['status']}<br/>
    Jumlah Iterasi: {data['iter']}
    """

    elements.append(Paragraph(param, normal))
    elements.append(Spacer(1, 15))

    # SECTION 2 TABLE
    elements.append(Paragraph("2. Konvergensi Iterasi", styles["Heading2"]))

    table_data = [["Iterasi", "M", "Pb", "Selisih"]]
    table_data += [[str(x) for x in row] for row in data["iter_data"]]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # SECTION 3 GRAPH
    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=250, bbox_inches='tight')
    img.seek(0)

    elements.append(Paragraph("3. Grafik Analisis Probabilitas Blocking", styles["Heading2"]))
    elements.append(Image(img, width=450, height=260))

    elements.append(Spacer(1, 15))

    # SECTION 4 CONCLUSION
    elements.append(Paragraph("4. Kesimpulan", styles["Heading2"]))

    elements.append(Paragraph(
        f"Sistem berada dalam kondisi <b>{data['status']}</b> berdasarkan hasil analisis probabilitas blocking. Model menunjukkan karakteristik sistem telekomunikasi berbasis sumber terbatas.",
        normal
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# =========================
# UI HEADER
# =========================
st.markdown("""
<style>

html, body {
    background: #f8fafc;
    font-family: Inter;
}

.header {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    padding: 18px;
    border-radius: 14px;
    color: white;
    text-align: center;
    margin-bottom: 15px;
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header'>
<h2>📡 EngsetPro Simulator</h2>
<p>Sistem Analisis Telekomunikasi Profesional</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Navigasi")
page = st.sidebar.radio("Pilih Menu", ["🏠 Dashboard", "📈 Analisis", "📁 Riwayat"])

# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown("### Input Parameter Sistem")

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Jumlah Sumber (S)", min_value=1, value=10)
    with col2:
        N = st.number_input("Jumlah Kanal (N)", min_value=1, value=3)
    with col3:
        rho = st.number_input("Traffic (ρ)", min_value=0.0, value=0.5)

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

        st.markdown("### Hasil Analisis")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Blocking Probability", f"{r['Pb']:.6f}")
        c2.metric("Idle Traffic", f"{r['M']:.6f}")
        c3.metric("Iterasi", r["iter"])
        c4.metric("Status", r["status"])

# =========================
# ANALISIS (GRAPH IMPROVED)
# =========================
elif page == "📈 Analisis":

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

        ax.axhline(0.2, linestyle="--")

        ax.set_title("Kurva Probabilitas Blocking")
        ax.set_xlabel("Jumlah Kanal")
        ax.set_ylabel("Probabilitas Blocking")

        ax.grid(True, alpha=0.4)

        st.pyplot(fig)

# =========================
# RIWAYAT + DOWNLOAD FIX
# =========================
elif page == "📁 Riwayat":

    st.markdown("### Riwayat Simulasi")

    if st.session_state.history:
        st.dataframe(st.session_state.history, use_container_width=True)

        if st.button("📄 Generate Laporan PDF"):

            last = st.session_state.history[-1]

            S = last["S"]
            rho = last["rho"]

            x = list(range(1, S))
            y = [engset_pb(S, n, rho) for n in x]

            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.axhline(0.2, linestyle="--")
            ax.grid(True, alpha=0.4)

            pdf = export_pdf(last, fig)

            st.download_button(
                "⬇ Unduh PDF Profesional",
                data=pdf,
                file_name="EngsetPro_Report.pdf",
                mime="application/pdf"
            )

    else:
        st.info("Belum ada riwayat")
