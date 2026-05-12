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
# UI STYLE (FIXED + CLEAN)
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;500;600;700&display=swap');

/* GLOBAL */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #dbeafe 0%, #EEF4FF 40%, #f0f9ff 100%);
    font-family: 'Nunito', sans-serif;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1d4ed8 0%, #1e3a8a 100%) !important;
    overflow-x: hidden;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: #e0eaff !important;
}

/* HEADER FIX */
.unpix-header {
    position: relative;
    overflow: hidden;
    z-index: 1;
    background: linear-gradient(135deg, #1d4ed8, #2563eb, #3b82f6);
    border-radius: 24px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(29,78,216,0.28);
}

.unpix-header::before,
.unpix-header::after {
    content: "";
    position: absolute;
    background: rgba(255,255,255,0.07);
    border-radius: 50%;
    z-index: 0;
}

.unpix-header::before {
    width: 180px;
    height: 180px;
    top: -40px;
    right: -40px;
}

.unpix-header::after {
    width: 240px;
    height: 240px;
    bottom: -60px;
    right: 60px;
}

.unpix-header > div {
    position: relative;
    z-index: 2;
}

/* SIDEBAR MENU CARD */
.sidebar-box {
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.08);
    margin-bottom: 16px;
}

/* BUTTON */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    width: 100%;
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
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# HEADER
# =========================
st.markdown("""
<div class="unpix-header">
    <div>
        <div style="font-size:13px;letter-spacing:2px;color:#bfdbfe;font-weight:700;">
            📡 ENGSETPRO
        </div>
        <div style="font-size:28px;font-weight:800;color:white;">
            Engset Simulator
        </div>
        <div style="font-size:14px;color:#dbeafe;">
            Professional Blocking Probability Analysis System
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR FIXED MENU
# =========================
st.sidebar.markdown("""
<div class="sidebar-box">
    <div style="font-size:14px;font-weight:800;">📡 MENU</div>
    <div style="font-size:12px;opacity:0.8;">Navigation Panel</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["🏠 Dashboard", "📊 Analysis", "📁 History"],
    label_visibility="collapsed"
)


# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    S = st.number_input("Sources (S)", min_value=1, value=10)
    N = st.number_input("Channels (N)", min_value=1, value=3)
    rho = st.number_input("Traffic (ρ)", min_value=0.0, value=0.5)

    if st.button("🚀 RUN ANALYSIS"):

        if N >= S:
            st.error("N harus lebih kecil dari S")
        else:
            M, Pb, data, iters = iterate(S, N, rho)

            status = "OPTIMAL" if Pb < 0.2 else "CONGESTED"

            st.session_state.result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "status": status,
                "iter": iters,
                "iter_data": data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.session_state.history.append(st.session_state.result)

    if "result" in st.session_state:
        r = st.session_state.result

        st.success(f"Blocking Probability: {r['Pb']:.6f}")
        st.info(f"Status: {r['status']}")


# =========================
# ANALYSIS
# =========================
elif page == "📊 Analysis":

    if "result" not in st.session_state:
        st.warning("Belum ada data")
    else:
        r = st.session_state.result

        st.dataframe(r["iter_data"], use_container_width=True)

        x = list(range(1, r["S"]))
        y = [engset_pb(r["S"], n, r["rho"]) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.axhline(0.2, linestyle="--", color="red")
        ax.grid()

        st.pyplot(fig)


# =========================
# HISTORY
# =========================
elif page == "📁 History":

    st.subheader("History")

    if st.session_state.history:
        st.dataframe(st.session_state.history)
    else:
        st.info("Kosong")
