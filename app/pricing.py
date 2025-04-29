import numpy as np
import scipy.stats as stats

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price

def black_scholes_greeks(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta = stats.norm.cdf(d1) if option_type == "call" else stats.norm.cdf(d1) - 1
    gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * stats.norm.pdf(d1) * np.sqrt(T)
    theta_call = -(S * stats.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * stats.norm.cdf(d2)
    theta_put = -(S * stats.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * stats.norm.cdf(-d2)
    rho_call = K * T * np.exp(-r * T) * stats.norm.cdf(d2)
    rho_put = -K * T * np.exp(-r * T) * stats.norm.cdf(-d2)

    theta = theta_call if option_type == "call" else theta_put
    rho = rho_call if option_type == "call" else rho_put

    return delta, gamma, vega, theta, rho
