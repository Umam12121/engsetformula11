import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# =====================================================
# ENGSET LOGIC (TIDAK DIUBAH)
# =====================================================

def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, M):
    numerator = nCr(S - 1, N) * (M ** N)
    denominator = sum(nCr(S - 1, k) * (M ** k) for k in range(N + 1))
    return numerator / denominator if denominator != 0 else 0


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


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


# =====================================================
# SIDEBAR NAVBAR (mirip navbar kamu)
# =====================================================

st.sidebar.title("ENGSETPRO")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("📈 Analisis"):
    st.session_state.page = "Analisis"

if st.sidebar.button("🕘 Riwayat"):
    st.session_state.page = "Riwayat"


# =====================================================
# HOME PAGE (INPUT + RESULT)
# =====================================================

if st.session_state.page == "Home":

    st.title("ENGSETPRO SIMULATOR")

    st.subheader("Input Parameter")

    S = st.number_input("Jumlah Source (S)", min_value=1, value=10)
    N = st.number_input("Jumlah Channel (N)", min_value=1, value=3)
    rho = st.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5)

    if st.button("HITUNG SEKARANG"):

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

    # RESULT DISPLAY
    if "result" in st.session_state:

        r = st.session_state.result

        st.success("HASIL ANALISIS")

        st.write("Blocking Probability:", round(r["Pb"], 6))
        st.write("Traffic Idle (M):", round(r["M"], 6))
        st.write("Iterasi:", r["iter"])
        st.write("Status:", r["status"])


# =====================================================
# ANALISIS PAGE (TABLE + GRAPH)
# =====================================================

elif st.session_state.page == "Analisis":

    st.title("GRAFIK ANALISIS")

    if "result" not in st.session_state:
        st.warning("Belum ada data")
    else:
        r = st.session_state.result

        st.subheader("Tabel Iterasi")

        st.table(r["iter_data"])

        # GRAPH (SAMA LOGIKA)
        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, marker="o")
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_xlabel("Channel")
        ax.set_ylabel("P(b)")
        ax.grid()

        st.pyplot(fig)


# =====================================================
# HISTORY PAGE
# =====================================================

elif st.session_state.page == "Riwayat":

    st.title("RIWAYAT SIMULASI")

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

        st.table(table)

    else:
        st.info("Belum ada riwayat")


# =====================================================
# EXPORT PDF
# =====================================================

def export_pdf(data, filename="engset_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ENGSETPRO REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    text = f"""
    S: {data['S']}<br/>
    N: {data['N']}<br/>
    ρ: {data['rho']}<br/>
    M: {data['M']}<br/>
    P(b): {data['Pb']}<br/>
    Status: {data['status']}<br/>
    """

    elements.append(Paragraph(text, styles["BodyText"]))

    doc.build(elements)


# BUTTON EXPORT
if st.session_state.page == "Riwayat":

    if st.button("EXPORT PDF"):

        if st.session_state.history:
            export_pdf(st.session_state.history[-1])
            st.success("PDF berhasil dibuat")
        else:
            st.error("Tidak ada data")
