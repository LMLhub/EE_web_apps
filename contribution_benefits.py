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

def investment_process(sigma, mu_e, contribution, start_pay,end_pay,life_exp,N):
    # Simulate investment process
    T=end_pay-start_pay #number of time steps
    dt=1
    constant=contribution*12 #annual pension contribution   
    M = T  # Number of time steps
    mu=0
    # Generate standard normal random variables for each path
    S=np.zeros((N, M+1))
    epsilon = np.random.normal(size=(N, M))
    # Calculate increment factors for each path
 #   increments = np.exp((mu +mu_e - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * epsilon)
    increments = (mu +mu_e) * dt + sigma * np.sqrt(dt) * epsilon

    for t in range(T):
#        S[:,t+1]=constant+S[:,t]*increments[:,t]
        S[:,t+1]=S[:,t]+constant+S[:,t]*increments[:,t]

    S=S/(12*(life_exp-end_pay))

    return S



def main():
#    st.title('Retirement simulation')
    life_exp=80
    salary=1000
    N=10000
    
    # Add an image
#    st.image("./images/logo_twitter_banner_faint.jpg", caption="<a href="https://www.ergodicityeconomics.com" target="_blank">Part of the ergodicity economics project.</a>", unsafe_allow_html=True", use_column_width=True)
#    st.image("./images/logo_twitter_banner_faint.jpg", caption='<a href="https://www.ergodicityeconomics.com" target="_blank"></a>', unsafe_allow_html=True, use_column_width=True)
    st.image("./images/logo_twitter_banner_faint.jpg", use_column_width=True)
    st.markdown('<a href="https://www.ergodicityeconomics.com" target="_blank">Part of the ergodicity economics project.</a>', unsafe_allow_html=True)

    
    # User inputs
    sigma = st.slider('Volatility:', min_value=0.0, max_value=.5, step=.01, value=.15)
    mu_e = st.slider('Extra growth:', min_value=-0.1, max_value=.1, step=.01, value=.0)
#    salary = st.slider('Monthly salary:', min_value=0, max_value=20000, step=100, value=1000)
    contribution_perc = st.slider('Pension contribution (\% of income):', min_value=0, max_value=100, step=1, value=20)
    start_pay = st.slider('Start work age:', min_value=20, step=1, value=30,max_value=100)
    end_pay = st.slider('Retirement age:', min_value=start_pay, step=1, value=65,max_value=life_exp)
#    life_exp = st.slider('Life expectancy:', min_value=40, step=1, max_value=100, value=80)

    contribution=salary*contribution_perc/100

    if st.button('Simulate'):
        S = investment_process(sigma, mu_e, contribution, start_pay,end_pay,life_exp,N)
#        DB_pension=salary*(contribution_perc/100)*(end_pay-start_pay)/(life_exp-end_pay)   
        DB_pension=(contribution_perc)*(end_pay-start_pay)/(life_exp-end_pay)   

        time=range(start_pay,end_pay+1)
        FEW=100

        # Plot results
#        st.subheader('Accrued retirement income')
        fig, ax=plt.subplots()
        for n in range(FEW):
            ax.plot(time,100*S[n,:]/salary,linewidth=.5,alpha=.5)
        plt.axhline(DB_pension,color='k',linestyle=':',label=f'Defined-benefit level, {DB_pension:.0f}% of working income')
        
        plt.xlabel('Age (years)')
        plt.ylabel('Accrued retirement income (% of working income)')
        ax.grid(False)
        plt.legend()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlim(start_pay,end_pay)
        st.pyplot(fig)

        count_below_DB = np.sum(100*S[:,-1]/salary < DB_pension)
        percentage_poorer=100.*count_below_DB/N
        ranking=np.sort(100*S[:,-1]/salary)
        one_perc=ranking[int(99*N/100)]
        ten_perc=ranking[int(9*N/10)]
        median=ranking[int(5*N/10)]
        ninety_perc=ranking[int(N/10)]
        ninety_nine_perc=ranking[int(N/100)]
        st.write(f"{percentage_poorer:.0f} out of 100 retirees are worse off under defined contributions.")
        st.write(f"Richest 1\%: more than {one_perc:.0f}% of working income.")
        st.write(f"Richest 10\%: more than {ten_perc:.0f}% of working income.")
        st.write(f"Median: {median:.0f}% of working income.")
        st.write(f"Poorest 10\%: less than {ninety_perc:.0f}% of working income.")
        st.write(f"Poorest 1\%: less than {ninety_nine_perc:.0f}% of working income.")
if __name__ == '__main__':
    main()

