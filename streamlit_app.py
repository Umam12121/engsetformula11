import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngsetPro Simulator",
    page_icon="📡",
    layout="wide"
)


# =========================
# STYLE (simple clean UI)
# =========================
st.markdown("""
<style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #1f4fff;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f5f7ff;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# ENGSET LOGIC
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

        data.append([i, round(M, 6), round(Pb, 6), round(diff, 6)])

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
# HEADER
# =========================
st.markdown("<div class='main-title'>📡 EngsetPro Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Blocking Probability Analysis System</div>", unsafe_allow_html=True)

st.divider()


# =========================
# SIDEBAR NAVIGATION
# =========================
menu = st.sidebar.radio("Navigation", ["Home", "Analisis", "Riwayat"])


# =========================
# HOME PAGE
# =========================
if menu == "Home":

    st.markdown("## 📥 Input Parameter")

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Source (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Channel (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic (ρ)", min_value=0.0, value=0.5)

    st.divider()

    if st.button("🚀 HITUNG SEKARANG"):

        if N >= S:
            st.error("N harus lebih kecil dari S")
        else:
            M, Pb, iter_data, iters = iterate(S, N, rho)

            status = "OPTIMAL" if Pb < 0.2 else "PADAT"

            st.session_state.result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "status": status,
                "iter": iters,
                "iter_data": iter_data,
                "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            st.session_state.history.append(st.session_state.result)

    # RESULT CARD
    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("### 📊 Hasil")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Blocking Prob", f"{r['Pb']:.6f}")
        col2.metric("Traffic Idle", f"{r['M']:.6f}")
        col3.metric("Iterasi", r["iter"])
        col4.metric("Status", r["status"])


# =========================
# ANALISIS PAGE
# =========================
elif menu == "Analisis":

    st.markdown("## 📈 Analisis Sistem")

    if "result" not in st.session_state:
        st.warning("Belum ada data perhitungan")
    else:
        r = st.session_state.result

        # ITERATION TABLE
        st.markdown("### 🔁 Iterasi Konvergensi")
        st.table(r["iter_data"])

        # GRAPH
        st.markdown("### 📊 Grafik Blocking Probability")

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, marker="o", linewidth=2)
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_xlabel("Channel")
        ax.set_ylabel("P(b)")
        ax.grid(True)

        st.pyplot(fig)


# =========================
# HISTORY PAGE
# =========================
elif menu == "Riwayat":

    st.markdown("## 🕘 Riwayat Simulasi")

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
        st.info("Belum ada riwayat")


# =========================
# PDF EXPORT (STREAMLIT SAFE)
# =========================
def export_pdf(data):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ENGSETPRO REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    text = f"""
    S: {data['S']}<br/>
    N: {data['N']}<br/>
    ρ: {data['rho']}<br/>
    M: {data['M']:.6f}<br/>
    P(b): {data['Pb']:.6f}<br/>
    Status: {data['status']}<br/>
    Iterasi: {data['iter']}<br/>
    """

    elements.append(Paragraph(text, styles["BodyText"]))

    doc.build(elements)

    buffer.seek(0)
    return buffer


# =========================
# DOWNLOAD PDF BUTTON
# =========================
if menu == "Riwayat":

    if st.button("📥 EXPORT PDF"):

        if st.session_state.history:

            pdf = export_pdf(st.session_state.history[-1])

            st.download_button(
                label="Download Report PDF",
                data=pdf,
                file_name="engset_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Tidak ada data untuk diexport")
