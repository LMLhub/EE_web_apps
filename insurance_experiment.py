#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:18:39 2023

@author: obp48
"""

import streamlit as st
from streamlit import session_state

def write_to_file(text_to_write):
    with open("user_data.txt", "a") as file:
        file.write(f"choice: {text_to_write}\n")


    
def main():
    wealth=100
    # Initialize session state variables
    if 't' not in session_state:
        session_state.t = 0

    if 'wealth' not in session_state:
        session_state.wealth=100

    if 'loss' not in session_state:
        session_state.loss = .9*session_state.wealth

    if 'loss_probability' not in session_state:
        session_state.loss_probability = 0.05

    if 'fee' not in session_state:
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss

#    st.title("Collect and Write User Choices")
#    st.header(f"Choice")
    # st.markdown(
    # f'<div style="position: absolute; top: 50px; left: 170px; font-size: 34px;"> Wealth = {session_state.wealth}</div>',
    # unsafe_allow_html=True)


    if st.button("Buy insurance"):
        session_state.t += 1
        session_state.wealth = session_state.wealth-session_state.fee
        session_state.loss = .9*session_state.wealth
#        st.write(f"time step: {session_state.t}, wealth: {session_state.wealth}")
#        st.markdown(
#    f'<div style="position: absolute; top: 100px; left: 50px; font-size: 34px;">Wealth = {session_state.wealth}</div>',
#    unsafe_allow_html=True)

        write_to_file(str(session_state.t)+' buy')
#        st.success(f"User chose: {user_choice}")
 
    if st.button("Take the risk"):
        session_state.t += 1
        session_state.wealth += 10      
        session_state.loss = .9*session_state.wealth
#        st.write(f"time step: {session_state.t}, wealth: {session_state.wealth}")
#        st.markdown(
#    f'<div style="position: absolute; top: 100px; left: 50px; font-size: 34px;">Wealth = {session_state.wealth}</div>',
#    unsafe_allow_html=True)
        write_to_file('risk')
#        st.success(f"User chose: {user_choice}")

    st.markdown(
    f'<div style="position: absolute; top: 50px; left: 170px; font-size: 34px;"> Wealth = {session_state.wealth:.2f}</div>',
    unsafe_allow_html=True)
    st.markdown(
    f'<div style="position: absolute; top: 75px; left: 170px; font-size: 34px;"> Potential loss = {session_state.loss:.2f}</div>',
    unsafe_allow_html=True)
    st.markdown(
    f'<div style="position: absolute; top: 100px; left: 170px; font-size: 34px;"> Fee = {session_state.fee:.2f}</div>',
    unsafe_allow_html=True)
 
        
    if session_state.t>10:
        if st.button("Close App"):
            st.experimental_rerun()  # Rerun the app to reset the state


if __name__ == "__main__":
    main()