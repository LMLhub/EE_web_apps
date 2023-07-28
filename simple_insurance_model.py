# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.optimize import root_scalar


def min_func(x, w, p, risk):
    return p * np.log((w + x - risk)/w) + (1-p)*np.log((w + x)/w) if w + x - risk > 0 else -np.inf

def insurance_simulation(T = 1000, N = 5, c = 0.95, p = 0.05):
    #*******************************
    #******** Simulate *************
    w_no_ins = np.ones((T,N)) #initialize wealth array
    w_ins = np.ones((T,N)) #initialize wealth array

    for t in range(T-1):
        w_ins[t+1] = w_ins[t] #carry everyone's wealth forward
        w_no_ins[t+1] = w_no_ins[t] #carry everyone's wealth forward
        i=np.random.randint(0, N) #select random agent to expose to risk
        risk_ins=w_ins[t][i]*c              #set magnitude of risk
        risk_no_ins=w_no_ins[t][i]*c              #set magnitude of risk

        #find fees at which agents offer to insure the risk
        offer = np.zeros(N)
        for n in range(N):
            offer[n] = root_scalar(min_func,args=(w_ins[t][n], p, risk_ins), method='brentq', bracket=[0, risk_ins],xtol=2e-300).root
        offer[i] = np.inf     #exclude self-insurance


        cheapest_offer = np.min(offer) #find minimum fee
        j = np.argmin(offer)      #find agent offering minimum fee

        #find highest fee insurance-seeking agent would pay to remove risk
        max_bid=w_ins[t][i]*(1-np.exp(p*(np.log(1-c))))

        #update wealths
        win = np.random.uniform(0,1)>p  #determine if loss occurs

        #update insurers
        if max_bid>cheapest_offer:   #if a contract is made
            fee=cheapest_offer #set fee at lowest offer
            w_ins[t+1][i]= w_ins[t][i] - fee # deterministic wealth change for insured agent
            if win:
                w_ins[t+1][j]=w_ins[t][j] + fee #update wealth for insurance seller if no losss
            else:
                w_ins[t+1][j] = w_ins[t][j] + fee - risk_ins #update wealth for insurance seller if loss
        #if no contract is made, then i plays the gamble, everyone else stays unchanged.
        else:
            if not win:
                w_ins[t+1][i] = w_ins[t][i] -risk_ins #update wealth if loss for agent i

        #update non_insurers
        if not win:
            w_no_ins[t+1][i] = w_no_ins[t][i] -risk_no_ins #update wealth if loss for agent i
    return w_ins, w_no_ins

def main():
    # User inputs
    N = 2
    T = 2500
    c = 0.95
    p = 0.05
    t = np.arange(0,T)
    t2 = np.arange(0, T/N, 1/N)

    if st.button('Simulate'):
        w_ins, w_no_ins = insurance_simulation(T,N,c,p)

        # Display results
        fig, ax = plt.subplots()
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

# Hide the bottom spine and ticks
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        plt.semilogy(t,w_ins,color='blue',linewidth=.5)
        plt.semilogy(t,w_no_ins,color='orange',linewidth=.5)
        plt.semilogy(t,np.exp(t2*(np.log(1-c*p))), color='red', linewidth=1, linestyle='--',alpha=1,label='expected value uninsured') #plot expected wealth
        plt.semilogy(t,np.exp(t2*(p*np.log(1-c))), color='black', linewidth=1, linestyle=':',alpha=1,label='time average uninsured')
        plt.xlabel('time step (round)')
        plt.ylabel('wealth')
        st.pyplot(plt)

if __name__ == '__main__':
    main()

