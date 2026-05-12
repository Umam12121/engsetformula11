import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# =========================
# LOGIKA ENGSET
# =========================

def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, M):
    num = nCr(S - 1, N) * (M ** N)
    den = sum(nCr(S - 1, k) * (M ** k) for k in range(N + 1))
    return num / den if den != 0 else 0


def iterate_engset(S, N, rho):
    M = rho
    tol = 0.0001
    iter_data = []

    i = 1
    while True:
        Pb = engset_pb(S, N, M)
        M_new = rho * (1 - Pb)
        diff = abs(M_new - M)

        iter_data.append([i, M, Pb, diff])

        if diff < tol:
            break

        M = M_new
        i += 1

    return M_new, Pb, iter_data, i


# =========================
# SESSION STATE
# =========================

if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# UI
# =========================

st.title("📡 EngsetPro Simulator (Streamlit)")

st.sidebar.header("Input Parameter")

S = st.sidebar.number_input("Jumlah Source (S)", min_value=1, value=10)
N = st.sidebar.number_input("Jumlah Channel (N)", min_value=1, value=3)
rho = st.sidebar.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5)


# =========================
# HITUNG
# =========================

if st.button("HITUNG"):

    if N >= S:
        st.error("N harus lebih kecil dari S")
    else:
        M, Pb, iter_data, iters = iterate_engset(S, N, rho)

        status = "OPTIMAL" if Pb < 0.2 else "PADAT"

        result = {
            "S": S,
            "N": N,
            "rho": rho,
            "M": M,
            "Pb": Pb,
            "status": status,
            "iterasi": iters,
            "waktu": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        st.session_state.last_result = result
        st.session_state.iter_data = iter_data
        st.session_state.history.append(result)


# =========================
# HASIL
# =========================

if "last_result" in st.session_state:

    r = st.session_state.last_result

    st.subheader("📊 Hasil Analisis")

    st.write(f"**Blocking Probability:** {r['Pb']:.6f}")
    st.write(f"**Traffic Idle (M):** {r['M']:.6f}")
    st.write(f"**Iterasi:** {r['iterasi']}")
    st.write(f"**Status:** {r['status']}")


# =========================
# ITERATION TABLE
# =========================

if "iter_data" in st.session_state:

    st.subheader("🔁 Iterasi Konvergensi")

    st.table(st.session_state.iter_data)


# =========================
# GRAFIK
# =========================

if "last_result" in st.session_state:

    st.subheader("📈 Grafik Blocking Probability")

    S = st.session_state.last_result["S"]
    rho = st.session_state.last_result["rho"]

    x = list(range(1, S))
    y = [engset_pb(S, n, rho) for n in x]

    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o")
    ax.axhline(0.2, linestyle="--", color="red")
    ax.set_xlabel("Channel")
    ax.set_ylabel("P(b)")
    ax.grid()

    st.pyplot(fig)


# =========================
# HISTORY
# =========================

st.subheader("🕘 History")

if st.session_state.history:
    st.dataframe(st.session_state.history)
else:
    st.info("Belum ada data")


# =========================
# EXPORT PDF
# =========================

def export_pdf(data, filename="report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ENGSETPRO REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    text = f"""
    S: {data['S']} <br/>
    N: {data['N']} <br/>
    ρ: {data['rho']} <br/>
    M: {data['M']:.6f} <br/>
    P(b): {data['Pb']:.6f} <br/>
    Status: {data['status']} <br/>
    """

    elements.append(Paragraph(text, styles["BodyText"]))

    doc.build(elements)


if st.button("EXPORT PDF") and "last_result" in st.session_state:
    export_pdf(st.session_state.last_result)
    st.success("PDF berhasil dibuat!")
