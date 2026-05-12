import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io
import base64

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngsetPro Simulator",
    page_icon="📡",
    layout="wide"
)


# =========================
# STYLE UI (lebih clean)
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #2563eb;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #f4f7ff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
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
# SIDEBAR NAV (lebih bagus)
# =========================
st.sidebar.title("📡 EngsetPro Menu")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📊 Analisis", "🕘 Riwayat"]
)

st.sidebar.divider()
st.sidebar.info("Blocking Probability Simulator")


# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown("<div class='main-title'>ENGSETPRO DASHBOARD</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Source (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Channel (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic (ρ)", min_value=0.0, value=0.5)

    st.divider()

    if st.button("🚀 RUN SIMULATION"):

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

        st.success("HASIL SIMULASI")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Pb", f"{r['Pb']:.6f}")
        c2.metric("M", f"{r['M']:.6f}")
        c3.metric("Iterasi", r["iter"])
        c4.metric("Status", r["status"])


# =========================
# ANALISIS
# =========================
elif page == "📊 Analisis":

    st.markdown("## 📊 Analisis Sistem Engset")

    if "result" not in st.session_state:
        st.warning("Belum ada data")
    else:

        r = st.session_state.result

        st.subheader("🔁 Iterasi Konvergensi")
        st.table(r["iter_data"])

        # ================= GRAPH =================
        st.subheader("📈 Grafik Blocking Probability")

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, marker="o", linewidth=2)
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_xlabel("Channel")
        ax.set_ylabel("P(b)")
        ax.grid()

        st.pyplot(fig)


# =========================
# RIWAYAT
# =========================
elif page == "🕘 Riwayat":

    st.markdown("## 🕘 History Simulasi")

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
        st.info("Belum ada history")


# =========================
# PDF EXPORT (FULL REPORT + GRAPH)
# =========================
def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    # COVER
    elements.append(Paragraph("ENGSETPRO SIMULATOR REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    # PARAMETER
    param = f"""
    S: {data['S']}<br/>
    N: {data['N']}<br/>
    ρ: {data['rho']}<br/>
    M: {data['M']:.6f}<br/>
    P(b): {data['Pb']:.6f}<br/>
    Status: {data['status']}<br/>
    Iterasi: {data['iter']}<br/>
    """

    elements.append(Paragraph(param, styles["BodyText"]))
    elements.append(Spacer(1, 12))

    # ITERATION TABLE
    elements.append(Paragraph("TABEL ITERASI", styles["Heading2"]))

    iter_table = [["Iterasi", "M", "P(b)", "Selisih"]]
    iter_table += [[str(x) for x in row] for row in data["iter_data"]]

    table = Table(iter_table)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.blue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # GRAPH INSERT
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    elements.append(Paragraph("GRAFIK BLOCKING PROBABILITY", styles["Heading2"]))
    elements.append(Image(img_buffer, width=400, height=250))

    elements.append(Spacer(1, 12))

    # KESIMPULAN
    conclusion = f"""
    Sistem dalam kondisi <b>{data['status']}</b> berdasarkan nilai blocking probability.
    """

    elements.append(Paragraph(conclusion, styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer


# =========================
# EXPORT BUTTON (FIXED)
# =========================
if page == "🕘 Riwayat":

    if st.button("📥 EXPORT PDF") and st.session_state.history:

        last = st.session_state.history[-1]

        # recreate graph for PDF
        S = last["S"]
        rho = last["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        pdf = export_pdf(last, fig)

        st.download_button(
            "Download PDF Report",
            data=pdf,
            file_name="EngsetPro_Report.pdf",
            mime="application/pdf"
        )
