import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pricing import black_scholes_price, black_scholes_greeks

st.title("🧮 Black-Scholes Pricer avec Visualisation des Greeks")

# Sidebar : paramètres de l'option
st.sidebar.header("Paramètres de l'option")

option_type = st.sidebar.selectbox("Type d'option", ["call", "put"])
S = st.sidebar.slider("Prix du sous-jacent (S)", 10, 200, 100)
K = st.sidebar.slider("Prix d'exercice (K)", 10, 200, 100)
T = st.sidebar.slider("Temps avant maturité (en années)", 0.01, 2.0, 1.0, 0.01)
r = st.sidebar.slider("Taux d'intérêt sans risque (%)", 0.0, 10.0, 5.0) / 100
sigma = st.sidebar.slider("Volatilité (%)", 1.0, 100.0, 20.0) / 100

# Calcul du prix et des greeks
price = black_scholes_price(S, K, T, r, sigma, option_type)
delta, gamma, vega, theta, rho = black_scholes_greeks(S, K, T, r, sigma, option_type)

# Affichage des résultats
st.subheader("Résultats")
st.write(f"**Prix de l'option {option_type}** : {price:.2f} €")
st.write(f"**Delta** : {delta:.4f}")
st.write(f"**Gamma** : {gamma:.4f}")
st.write(f"**Vega** : {vega:.2f}")
st.write(f"**Theta** : {theta:.2f}")
st.write(f"**Rho** : {rho:.2f}")

# Graphiques des Greeks en fonction de S
st.subheader("Variation des Greeks en fonction du prix du sous-jacent")

S_range = np.linspace(0.5 * K, 1.5 * K, 100)
deltas, gammas, vegas, thetas, rhos = [], [], [], [], []

for s in S_range:
    d, g, v, t, r_ = black_scholes_greeks(s, K, T, r, sigma, option_type)
    deltas.append(d)
    gammas.append(g)
    vegas.append(v)
    thetas.append(t)
    rhos.append(r_)

def plot_greek(y, title):
    fig, ax = plt.subplots()
    ax.plot(S_range, y)
    ax.set_title(title)
    ax.set_xlabel("Prix du Spot")
    ax.set_ylabel(title)
    ax.grid(True)
    st.pyplot(fig)

plot_greek(deltas, "Delta")
plot_greek(gammas, "Gamma")
plot_greek(vegas, "Vega")
plot_greek(thetas, "Theta")
plot_greek(rhos, "Rho")
