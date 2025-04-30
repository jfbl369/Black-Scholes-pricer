import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from pricing import black_scholes_prix, black_scholes_greeks

# Interface globale
st.set_page_config(layout="wide", page_title="Black-Scholes Pricer", initial_sidebar_state="expanded")


st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Courier New', monospace;
        color: #00ff00;
    }

    .stSlider > div {
        color: #ffaa00;
    }

    .st-bb {
        background-color: #0f1117 !important;
    }

    .block-container {
        padding-top: 1rem;
    }

    h1, h2, h3, h4 {
        color: #ffaa00;
    }
    </style>
""", unsafe_allow_html=True)



# Titre
st.markdown("<h2 style='text-align: left;'>Black-Scholes Pricer</h2>", unsafe_allow_html=True)

# Sidebar - Paramètres de l'option
st.sidebar.header("Paramètres de l'option")
option_type = st.sidebar.selectbox("Type d'option", ["call", "put"])
St = st.sidebar.slider("Prix du sous-jacent (S)", 10, 200, 100)
K = st.sidebar.slider("Prix d'exercice (K)", 10, 200, 100)
T = st.sidebar.slider("Temps avant maturité (en années)", 0.01, 2.0, 1.0, 0.01)
r = st.sidebar.slider("Taux d'intérêt sans risque (%)", 0.0, 10.0, 5.0) / 100
sigma = st.sidebar.slider("Volatilité (%)", 1.0, 100.0, 20.0) / 100

# Calculs
prix = black_scholes_prix(St, K, T, r, sigma, option_type)
delta, gamma, vega, theta, rho = black_scholes_greeks(St, K, T, r, sigma, option_type)

# Résultats formatés
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.markdown(f"<div style='text-align:center; font-size:16px;'>Prix<br><b>{prix:.2f} €</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div style='text-align:center; font-size:16px;'>Delta<br><b>{delta:.4f}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div style='text-align:center; font-size:16px;'>Gamma<br><b>{gamma:.4f}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div style='text-align:center; font-size:16px;'>Vega<br><b>{vega:.2f}</b></div>", unsafe_allow_html=True)
col5.markdown(f"<div style='text-align:center; font-size:16px;'>Theta<br><b>{theta:.2f}</b></div>", unsafe_allow_html=True)
col6.markdown(f"<div style='text-align:center; font-size:16px;'>Rho<br><b>{rho:.2f}</b></div>", unsafe_allow_html=True)

# Données pour graphiques
S_range = np.linspace(0.5 * K, 1.5 * K, 100)
deltas, gammas, vegas, thetas, rhos = [], [], [], [], []

for s in S_range:
    d, g, v, t, r_ = black_scholes_greeks(s, K, T, r, sigma, option_type)
    deltas.append(d)
    gammas.append(g)
    vegas.append(v)
    thetas.append(t)
    rhos.append(r_)




# d1, d2
d1 = (np.log(St / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# Calcul de d1 et d2
d1 = (np.log(St / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)


def create_plot_fixed(x, y, title):
    fig, ax = plt.subplots(figsize=(2.7, 2.3))
    fig.patch.set_facecolor("#000000")  # fond du graphe
    ax.set_facecolor("#000000")         # fond de la zone de tracé

    ax.plot(x, y, color="#00FF00", linewidth=1.5)  # ligne verte fluo
    ax.set_title(title, fontsize=10, color="#FFB000")  # titre jaune/orangé
    ax.set_xlabel("Prix du Spot", fontsize=8, color="white")
    ax.set_ylabel(title, fontsize=8, color="white")
    ax.tick_params(axis='both', colors='white', labelsize=7)
    ax.grid(True, linestyle='--', linewidth=0.5, color="#444444")

    fig.tight_layout()
    return fig


# ----------------------------- DELTA -----------------------------
col_left, col_right = st.columns([2, 3])
with col_left:
    st.pyplot(create_plot_fixed(S_range, deltas, "Delta"))
with col_right:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.latex(r"\Delta = N(d_1)")
    st.latex(r"d_1 = \frac{\ln(S/K) + (r + 0.5\sigma^2)T}{\sigma\sqrt{T}}")
    st.latex(rf"d_1 = \frac{{\ln({St}/{K}) + ({r:.2f} + 0.5\cdot{sigma:.2f}^2)\cdot{T:.2f}}}{{{sigma:.2f}\sqrt{{{T:.2f}}}}} = {d1:.4f}")
    st.latex(rf"\Delta = N({d1:.4f}) = {delta:.4f}")

# ----------------------------- GAMMA -----------------------------
col_left, col_right = st.columns([2, 3])
with col_left:
    st.pyplot(create_plot_fixed(S_range, gammas, "Gamma"))
with col_right:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.latex(r"\Gamma = \frac{N'(d_1)}{S \cdot \sigma \cdot \sqrt{T}}")
    st.latex(rf"\Gamma = \frac{{N'({d1:.4f})}}{{{St} \cdot {sigma:.2f} \cdot \sqrt{{{T:.2f}}}}}")
    st.latex(rf"\Gamma = {gamma:.5f}")

# ----------------------------- VEGA -----------------------------
col_left, col_right = st.columns([2, 3])
with col_left:
    st.pyplot(create_plot_fixed(S_range, vegas, "Vega"))
with col_right:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.latex(r"\text{Vega} = S \cdot N'(d_1) \cdot \sqrt{T}")
    st.latex(rf"\text{{Vega}} = {St} \cdot N'({d1:.4f}) \cdot \sqrt{{{T:.2f}}}")
    st.latex(rf"\text{{Vega}} = {vega:.2f}")

# ----------------------------- THETA -----------------------------
col_left, col_right = st.columns([2, 3])
with col_left:
    st.pyplot(create_plot_fixed(S_range, thetas, "Theta"))
with col_right:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.latex(r"\Theta = -\frac{S N'(d_1) \sigma}{2 \sqrt{T}} - r K e^{-rT} N(d_2)")
    st.latex(rf"\Theta = {theta:.2f}")

# ----------------------------- RHO -----------------------------
col_left, col_right = st.columns([2, 3])
with col_left:
    st.pyplot(create_plot_fixed(S_range, rhos, "Rho"))
with col_right:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.latex(r"\rho = K T e^{-rT} N(d_2)")
    st.latex(rf"\rho = {K} \cdot {T:.2f} \cdot e^{{-{r:.2f} \cdot {T:.2f}}} \cdot N({d2:.4f})")
    st.latex(rf"\rho = {rho:.2f}")
