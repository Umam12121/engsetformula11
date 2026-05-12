import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
from io import BytesIO

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EngsetPro Simulator", layout="wide")

# =========================
# FUNCTION
# =========================
def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, M):
    numerator = nCr(S - 1, N) * (M ** N)
    denominator = 0

    for k in range(N + 1):
        denominator += nCr(S - 1, k) * (M ** k)

    return numerator / denominator if denominator != 0 else 0


# =========================
# SESSION STATE (HISTORY)
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "last_iter" not in st.session_state:
    st.session_state.last_iter = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# =========================
# SIDEBAR MENU (NAVBAR STYLE)
# =========================
menu = st.sidebar.selectbox(
    "📌 MENU",
    ["🏠 Dashboard", "📊 Analisis", "🕘 Riwayat"]
)


# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":

    st.title("📡 EngsetPro Simulator")

    S = st.number_input("Jumlah Source (S)", min_value=1, step=1)
    N = st.number_input("Jumlah Channel (N)", min_value=1, step=1)
    rho = st.number_input("Traffic per Source (ρ)", value=1.0)

    if st.button("🚀 HITUNG"):

        if N >= S:
            st.error("N harus lebih kecil dari S")
            st.stop()

        M = rho
        tol = 0.0001
        iterasi = []

        i = 1

        while True:
            Pb = engset_pb(S, N, M)
            M_new = rho * (1 - Pb)
            diff = abs(M_new - M)

            iterasi.append([i, M, Pb, diff])

            if diff < tol:
                break

            M = M_new
            i += 1

        status = "OPTIMAL" if Pb < 0.2 else "PADAT"

        result = {
            "S": S,
            "N": N,
            "rho": rho,
            "M": M_new,
            "Pb": Pb,
            "status": status,
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "iter": i
        }

        st.session_state.last_result = result
        st.session_state.last_iter = iterasi
        st.session_state.history.append(result)

        st.success(f"Status: {status}")

        st.metric("P(b)", f"{Pb:.6f}")
        st.metric("Traffic Idle (M)", f"{M_new:.6f}")
        st.metric("Iterasi", i)


# =========================
# ANALISIS
# =========================
elif menu == "📊 Analisis":

    st.title("📊 Analisis Sistem")

    if st.session_state.last_result:

        data = st.session_state.last_iter

        df = pd.DataFrame(
            data,
            columns=["Iterasi", "M", "P(b)", "Selisih"]
        )

        st.subheader("Tabel Iterasi")
        st.dataframe(df, use_container_width=True)

        S = st.session_state.last_result["S"]
        rho = st.session_state.last_result["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, marker="o")
        ax.axhline(0.2, linestyle="--", color="red")
        ax.set_title("Blocking Probability")
        ax.set_xlabel("Channel")
        ax.set_ylabel("P(b)")
        ax.grid(True)

        st.pyplot(fig)

    else:
        st.warning("Belum ada data. Jalankan simulasi dulu.")


# =========================
# RIWAYAT
# =========================
elif menu == "🕘 Riwayat":

    st.title("🕘 Riwayat Simulasi")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "engset_history.csv",
            "text/csv"
        )

    else:
        st.info("Belum ada riwayat")

