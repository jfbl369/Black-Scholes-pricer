import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from pricing import black_scholes_prix, black_scholes_greeks


st.set_page_config(layout="wide")

# =======================
# 🎨 STYLE GÉNÉRAL
# =======================
st.markdown("""
    <style>
    .greek-box {
        border: 1px solid #444;
        background-color: #0f1117;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .greek-title {
        font-weight: bold;
        color: #FF9500;  /* Orange Streamlit / Bloomberg */
        font-size: 18px;
        margin-bottom: 0.5rem;
    }
    .orange-latex {
        font-size: 15px;
        color: #FF9500 !important;
    }
    .orange-code {
        color: #FF9500 !important;
    }
    </style>
""", unsafe_allow_html=True)


# Titre
st.markdown("<h2 class='orange-code' style='text-align: left;'>Black-Scholes Pricer</h2>", unsafe_allow_html=True)


# =======================
# ⚙️ FONCTIONS GÉNÉRIQUES
# =======================
def calc_d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def create_styled_plot(x, y, title, color):
    fig, ax = plt.subplots(figsize=(3.5, 2.3), facecolor="#0f1117")
    ax.plot(x, y, color=color, linewidth=1.5)
    #ax.set_title(title, fontsize=10, color="white")
    #ax.set_xlabel("S", fontsize=8, color="white")
    #ax.set_ylabel(title, fontsize=8, color="white")
    ax.tick_params(colors="white", labelsize=7)
    ax.grid(True, linestyle='--', linewidth=0.5, color="#444444")
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")
    fig.tight_layout()
    return fig

def make_greek_plot(S_range, func, *args):
    return [func(s, *args) for s in S_range]

# =======================
# 🎛️ SIDEBAR
# =======================
with st.sidebar:
    st.markdown("""
        <div style="margin-top: -1rem; margin-bottom: 1rem;">
            <a href="https://github.com/jfbl369/Black-Scholes-pricer" target="_blank" style="color:white; text-decoration:none; font-size:16px;">
                🔗 GitHub
            </a>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.header("Paramètres de l'option")
option_type = st.sidebar.selectbox("Type d'option", ["call", "put"])
S = st.sidebar.slider("Prix du sous-jacent (S)", 10, 200, 100)
K = st.sidebar.slider("Strike (K)", 10, 200, 100)
T = st.sidebar.slider("Maturité (T, en années)", 0.01, 2.0, 1.0, 0.01)
r = st.sidebar.slider("Taux sans risque (r, %)", 0.0, 10.0, 5.0) / 100
sigma = st.sidebar.slider("Volatilité (σ, %)", 1.0, 100.0, 20.0) / 100


# Calculs
prix = black_scholes_prix(S, K, T, r, sigma, option_type)
delta, gamma, vega, theta, rho = black_scholes_greeks(S, K, T, r, sigma, option_type)

# Résultats formatés
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Prix<br><b>{prix:.2f} €</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Delta<br><b>{delta:.4f}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Gamma<br><b>{gamma:.4f}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Vega<br><b>{vega:.2f}</b></div>", unsafe_allow_html=True)
col5.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Theta<br><b>{theta:.2f}</b></div>", unsafe_allow_html=True)
col6.markdown(f"<div class='orange-code' style='text-align:center; font-size:16px;'>Rho<br><b>{rho:.2f}</b></div>", unsafe_allow_html=True)

# =======================
# 📈 COURBE S
# =======================
S_range = np.linspace(0.5 * K, 1.5 * K, 100)

# =======================
# 📦 CALCUL DELTA
# =======================
d1, d2 = calc_d1_d2(S, K, T, r, sigma)
delta = stats.norm.cdf(d1) if option_type == "call" else stats.norm.cdf(d1) - 1

def delta_func(s, K, T, r, sigma, opt_type):
    d1, _ = calc_d1_d2(s, K, T, r, sigma)
    return stats.norm.cdf(d1) if opt_type == "call" else stats.norm.cdf(d1) - 1

delta_curve = make_greek_plot(S_range, delta_func, K, T, r, sigma, option_type)

# =======================
# 📤 AFFICHAGE DELTA
# =======================
st.markdown("<div class='greek-box'>", unsafe_allow_html=True)
st.markdown("<div class='greek-title'>Delta</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.pyplot(create_styled_plot(S_range, delta_curve, "Delta", "blue"))

with col2:
    toggle = st.radio("Afficher :", ["Formules mathématiques", "Code Python"],
                      horizontal=True, label_visibility="collapsed", key="delta")

    if toggle == "Formules mathématiques":
        st.latex(r"\Delta_{\text{call}} = N(d_1), \quad \Delta_{\text{put}} = N(d_1) - 1")
        st.latex(r"d_1 = \frac{\ln(S/K) + (r + \frac{1}{2} \sigma^2) T}{\sigma \sqrt{T}}")
        st.latex(rf"d_1 = \frac{{\ln({S}/{K}) + ({r:.2f} + 0.5 \cdot {sigma:.2f}^2) \cdot {T}}}{{{sigma:.2f} \cdot \sqrt{{{T}}}}} = {d1:.4f}")
        st.latex(rf"\Delta = {delta:.4f}")
    else:
        st.code("""d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
delta = stats.norm.cdf(d1) if option_type == "call" else stats.norm.cdf(d1) - 1""")
        st.code(f"""d1 = (np.log({S} / {K}) + ({r:.2f} + 0.5 * {sigma:.2f}**2) * {T}) / ({sigma:.2f} * np.sqrt({T}))
delta = {delta:.4f}""")

st.markdown("</div>", unsafe_allow_html=True)

# Gamma
gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
gammas = []
for s in S_range:
    d1_s = (np.log(s / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    gammas.append(stats.norm.pdf(d1_s) / (s * sigma * np.sqrt(T)))

st.markdown("<div class='greek-box'>", unsafe_allow_html=True)
st.markdown("<div class='greek-title'>Gamma</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1.8])
with col1:
    st.pyplot(create_styled_plot(S_range, gammas, "Gamma", "blue"))

with col2:
    toggle = st.radio("Afficher :", ["Formules mathématiques", "Code Python"], horizontal=True, label_visibility="collapsed", key="gamma")

    if toggle == "Formules mathématiques":
        st.latex(r"\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}")
        st.latex(rf"\Gamma = \frac{{N'({d1:.4f})}}{{{S} \cdot {sigma:.2f} \cdot \sqrt{{{T}}}}} = {gamma:.5f}")
    else:
        st.code("gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))")
        st.code(f"gamma = stats.norm.pdf({d1:.4f}) / ({S} * {sigma:.2f} * np.sqrt({T})) = {gamma:.5f}")

st.markdown("</div>", unsafe_allow_html=True)

# Vega
vega = S * stats.norm.pdf(d1) * np.sqrt(T)
vegas = []
for s in S_range:
    d1_s = (np.log(s / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vegas.append(s * stats.norm.pdf(d1_s) * np.sqrt(T))

st.markdown("<div class='greek-box'>", unsafe_allow_html=True)
st.markdown("<div class='greek-title'>Vega</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1.8])
with col1:
    st.pyplot(create_styled_plot(S_range, vegas, "Vega", "blue"))

with col2:
    toggle = st.radio("Afficher :", ["Formules mathématiques", "Code Python"], horizontal=True, label_visibility="collapsed", key="vega")

    if toggle == "Formules mathématiques":
        st.latex(r"\text{Vega} = S \cdot N'(d_1) \cdot \sqrt{T}")
        st.latex(rf"\text{{Vega}} = {S} \cdot N'({d1:.4f}) \cdot \sqrt{{{T}}} = {vega:.2f}")
    else:
        st.code("vega = S * stats.norm.pdf(d1) * np.sqrt(T)")
        st.code(f"vega = {S} * stats.norm.pdf({d1:.4f}) * np.sqrt({T}) = {vega:.2f}")

st.markdown("</div>", unsafe_allow_html=True)

# Theta
theta = -(S * stats.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * stats.norm.cdf(d2)
thetas = []
for s in S_range:
    d1_s = (np.log(s / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2_s = d1_s - sigma * np.sqrt(T)
    theta_s = -(s * stats.norm.pdf(d1_s) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * stats.norm.cdf(d2_s)
    thetas.append(theta_s)

st.markdown("<div class='greek-box'>", unsafe_allow_html=True)
st.markdown("<div class='greek-title'>Theta</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1.8])
with col1:
    st.pyplot(create_styled_plot(S_range, thetas, "Theta", "blue"))

with col2:
    toggle = st.radio("Afficher :", ["Formules mathématiques", "Code Python"], horizontal=True, label_visibility="collapsed", key="theta")

    if toggle == "Formules mathématiques":
        st.latex(r"\Theta = -\frac{S N'(d_1) \sigma}{2 \sqrt{T}} - r K e^{-rT} N(d_2)")
        st.latex(rf"\Theta = {theta:.2f}")
    else:
        st.code("theta = -(S * N'(d1) * sigma)/(2√T) - r*K*e^{-rT}*N(d2)")
        st.code(f"theta = {theta:.2f}", language="python")

st.markdown("</div>", unsafe_allow_html=True)

# Rho
rho = K * T * np.exp(-r*T) * stats.norm.cdf(d2)
rhos = []
for s in S_range:
    d1_s = (np.log(s / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2_s = d1_s - sigma * np.sqrt(T)
    rho_s = K * T * np.exp(-r*T) * stats.norm.cdf(d2_s)
    rhos.append(rho_s)

st.markdown("<div class='greek-box'>", unsafe_allow_html=True)
st.markdown("<div class='greek-title'>Rho</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1.8])
with col1:
    st.pyplot(create_styled_plot(S_range, rhos, "Rho", "blue"))

with col2:
    toggle = st.radio("Afficher :", ["Formules mathématiques", "Code Python"], horizontal=True, label_visibility="collapsed", key="rho")

    if toggle == "Formules mathématiques":
        st.latex(r"\rho = K T e^{-rT} N(d_2)")
        st.latex(rf"\rho = {K} \cdot {T:.2f} \cdot e^{{-{r:.2f} \cdot {T:.2f}}} \cdot N({d2:.4f}) = {rho:.2f}")
    else:
        st.code("rho = K * T * np.exp(-r*T) * stats.norm.cdf(d2)")
        st.code(f"rho = {rho:.2f}", language="python")

st.markdown("</div>", unsafe_allow_html=True)
