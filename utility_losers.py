# -*- coding: utf-8 -*-
"""CoinToss_BasicInput.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W13FIeqCvAkPXqVHqycruZNbSX3b8Wuo
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def geometric_brownian_motion(mu, sigma, l, T, S0=1, N=1000):
    """
    Simulates a Geometric Brownian Motion (GBM) trajectory.

    Parameters:
    mu (float): Drift coefficient.
    sigma (float): Volatility coefficient.
    S0 (float): Initial asset price (default: 1).
    N (int): Number of time steps.
    T (float): Total time duration.

    Returns:
    tuple: (t, S) where
        t (np.ndarray): Time grid of shape (N,).
        S (np.ndarray): Simulated GBM trajectory of shape (N,).
    """
    mu=l*mu
    sigma=l*sigma
    dt = T / N  # Time step
    t = np.linspace(0, T, N)  # Time grid
    W = np.random.normal(0, np.sqrt(dt), N).cumsum()  # Wiener process
    S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)  # GBM formula    
    return t, S

def iso_u(x,eta):
    if eta==1:
        u=np.log(x)
    else:
        u=(np.power(x,(1-eta))-1)/(1-eta)
    return(u)

# Initialize session state for two plots
if "plot1" not in st.session_state:
    st.session_state.plot1 = None
if "plot2" not in st.session_state:
    st.session_state.plot2 = None

def main():
#    st.title('Utility')

    # User inputs
    eta = st.slider(r'Risk aversion parameter, $\eta$:',min_value=-1.,max_value=3., step=.1, value=0.5)
#    mu = st.slider('drift:', min_value=0.0, max_value=.1, step=0.01, value=0.05)
#    sigma = st.slider('volatility:', min_value=0.05, max_value=.5,step=.01,value=.2)
    mu=0.05
    sigma=0.2

    T = st.slider('max time:', min_value=1000, max_value=10000,step=200,value=5000)

    l_opt=mu/(sigma*sigma)
    if eta==0:
        l_maxu=10000
        st.write(r"Singularity in $l_{\text{opt}}^{\text{EUT}}$ at $\eta=0$ (linear utility). Setting $l_{\text{opt}}^{\text{EUT}}=10,000$.")
    else:
        l_maxu=mu/(eta*sigma*sigma)

    st.write(r"Long-time growth is maximized at leverage $l_{\text{opt}}^{\text{EE}}=$",f"{l_opt:.2f}")

    st.write(r"Expected utility is maximized at leverage $l_{\text{opt}}^{\text{EUT}}=$",f"{l_maxu:.2f}")

    if st.button('Plot utility function'):

        x=np.arange(.1,100,1)
        u=iso_u(x,eta)
        fig1, ax1 = plt.subplots()
        ax1.plot(x, u)
        ax1.set_xlabel('dollar wealth')
        ax1.set_ylabel('utility')
        st.session_state.plot1 = fig1  # Store the first plot


    if st.button('Simulate agents'):

        t, S_e = geometric_brownian_motion(mu, sigma,l_opt,T)
        t, S_u = geometric_brownian_motion(mu, sigma,l_maxu,T)

        u_e=iso_u(S_e,eta)
        u_u=iso_u(S_u,eta)

        fig2, ax2 = plt.subplots()
        ax2.semilogy(t, S_e,label='EE agent\'s wealth',color='C0')
        ax2.semilogy(t, u_e,label='EE agent\'s utility',color='C0',linestyle='--')
        ax2.semilogy(t, S_u,label='EUT agent\'s wealth',color='C1')       
        ax2.semilogy(t, u_u,label='EUT agent\'s utility',color='C1',linestyle='--')       
        ax2.set_xlabel('time')
        ax2.set_ylabel('dollar wealth and corresponding utility')
        ax2.legend()
        st.session_state.plot2 = fig2  # Store the second plot
        
        # Display stored plots
    if st.session_state.plot1:
        st.pyplot(st.session_state.plot1)

    if st.session_state.plot2:
        st.pyplot(st.session_state.plot2)

if __name__ == '__main__':
    main()

