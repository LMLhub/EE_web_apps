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
    st.title("Collect and Write User Choices")
    st.header(f"Choice")

   # Initialize session state variable 't' to 0
    if 't' not in session_state:
        session_state.t = 0
    if 'wealth' not in session_state:
        session_state.wealth=100

    if st.button("Buy insurance"):
        session_state.t += 1
        session_state.wealth += -10
        st.write(f"time step: {session_state.t}, wealth: {session_state.wealth}")

        wealth=wealth-1
        write_to_file(str(session_state.t)+' buy')
#        st.success(f"User chose: {user_choice}")
 
    if st.button("Take the risk"):
        session_state.t += 1
        session_state.wealth += 10
        st.write(f"time step: {session_state.t}, wealth: {session_state.wealth}")
        write_to_file('risk')
#        st.success(f"User chose: {user_choice}")

 
    if session_state.t>10:
        if st.button("Close App"):
            st.experimental_rerun()  # Rerun the app to reset the state


if __name__ == "__main__":
    main()