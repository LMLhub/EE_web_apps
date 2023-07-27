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

def coin_toss_experiment(N, T):
#    np.random.seed(127)

    factor = np.random.choice([0.6,1.5], size=(T, N))
    x_N=np.ones([T+1,N])

    for step in range(T):
        x_N[step+1,:]=x_N[step,:]*factor[step]

    return x_N

def main():
    # User inputs
    T=10
    N = st.slider('Number of players, N:', value=20, min_value=1, max_value=100)
    t = np.arange(0,T+1)
#    T = st.slider('Simulated rounds, T:', value=500,min_value=1,max_value=2000)

    if st.button('Simulate'):
        x = coin_toss_experiment(N,T)

        # Display results
        gt=.5*(np.log(1.5)+np.log(.6))
        ge=np.log(1.05)
        fig, ax = plt.subplots()
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

# Hide the bottom spine and ticks
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        plt.semilogy(t,x,color='black',linewidth=.1,alpha=.1)
        plt.semilogy(t, np.mean(x,1),color='blue')
        plt.semilogy(t, np.exp(t*ge),color='red')        
#        plt.semilogy(t, np.exp(t*gt),color='green')        
        plt.xlabel('time step (round)')
        plt.ylabel('wealth')
        st.pyplot(plt)
        
if __name__ == '__main__':
    main()

