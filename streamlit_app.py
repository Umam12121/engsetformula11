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
# PAGE CONFIG (PRO LOOK)
# =========================
st.set_page_config(
    page_title="EngsetPro Professional",
    page_icon="📡",
    layout="wide"
)


# =========================
# CLEAN BLUE-WHITE UI STYLE
# =========================
st.markdown("""
<style>

body {
    background-color: #ffffff;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #1d4ed8;
}

.sub-title {
    font-size: 16px;
    color: #64748b;
    margin-bottom: 10px;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

.metric-box {
    background: #f0f6ff;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #dbeafe;
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
# HEADER
# =========================
st.markdown("<div class='main-title'>📡 EngsetPro Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Professional Blocking Probability Analysis System</div>", unsafe_allow_html=True)

st.divider()


# =========================
# SIDEBAR NAV (clean pro)
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

    st.markdown("## 📥 Input Parameter")

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Number of Sources (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Number of Channels (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5)

    st.markdown("---")

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

        st.markdown("### 📊 Results Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Blocking Probability", f"{r['Pb']:.6f}")
        c2.metric("Traffic Idle (M)", f"{r['M']:.6f}")
        c3.metric("Iterations", r["iter"])
        c4.metric("Status", r["status"])


# =========================
# ANALYSIS PAGE
# =========================
elif page == "📊 Analysis":

    st.markdown("## 📊 System Analysis")

    if "result" not in st.session_state:
        st.warning("No simulation data available")
    else:

        r = st.session_state.result

        st.markdown("### 🔁 Convergence Iteration Table")
        st.dataframe(r["iter_data"], use_container_width=True)

        st.markdown("### 📈 Blocking Probability Graph")

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2, color="#1d4ed8")
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_xlabel("Number of Channels")
        ax.set_ylabel("Blocking Probability")
        ax.grid(True)

        st.pyplot(fig)


# =========================
# HISTORY PAGE
# =========================
elif page == "📁 History":

    st.markdown("## 📁 Simulation History")

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
        st.info("No history yet")


# =========================
# PROFESSIONAL PDF EXPORT
# =========================
def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    # ================= COVER =================
    elements.append(Paragraph("ENGSETPRO SIMULATION REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Professional Engset Blocking Probability Analysis", styles["BodyText"]))
    elements.append(Spacer(1, 12))

    # ================= PARAMETERS =================
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

    # ================= ITERATION TABLE =================
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

    # ================= GRAPH =================
    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=200)
    img.seek(0)

    elements.append(Paragraph("3. Blocking Probability Graph", styles["Heading2"]))
    elements.append(Image(img, width=450, height=250))

    elements.append(Spacer(1, 12))

    # ================= CONCLUSION =================
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
                "Download Professional PDF",
                data=pdf,
                file_name="EngsetPro_Professional_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No data to export")
