#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:18:39 2023

@author: obp48
"""

import random
import streamlit as st
from streamlit import session_state
import matplotlib.pyplot as plt
import numpy as np

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

    if 'gain' not in session_state:
        session_state.gain = .1*session_state.wealth

    if 'loss_probability' not in session_state:
        session_state.loss_probability = 0.05

    if 'fee' not in session_state:
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss

#    st.title("Collect and Write User Choices")
#    st.header(f"Choice")
    # st.markdown(
    # f'<div style="position: absolute; top: 50px; left: 170px; font-size: 34px;"> Wealth = {session_state.wealth}</div>',
    # unsafe_allow_html=True)

#########################
## If insurance bought ##
#########################
    if st.button("Buy insurance"):
        session_state.t += 1
        session_state.wealth = session_state.wealth-session_state.fee+session_state.gain
        session_state.loss = .9*session_state.wealth
        session_state.gain = .1*session_state.wealth
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss

        write_to_file(str(session_state.t)+' buy')

#try a graphical representation, ciricles with areas equal to dollar amounts
        # Given areas of the circles
        area1 = session_state.wealth
        area2 = session_state.gain
        area3 = session_state.loss
# Calculate radii from the areas (assuming circles are perfect)
        radius1 = np.sqrt(area1 / np.pi)
        radius2 = np.sqrt(area2 / np.pi)
        radius3 = np.sqrt(area3 / np.pi)
# Create a figure and axis
        fig, ax = plt.subplots()
# Draw the circles
        circle1 = plt.Circle((0, 0), radius1, color='blue', alpha=1)
        circle3 = plt.Circle((0, 0), radius3, color='green', alpha=1)
        circle2 = plt.Circle((0, 0), radius2, color='red', alpha=1)
# Add the circles to the axis
        ax.add_patch(circle1)
        ax.add_patch(circle3)
        ax.add_patch(circle2)
# Set axis limits to fit the circles properly
        ax.set_xlim(-100, 100)
        ax.set_ylim(-100, 100)
        plt.xlim([-100,100])
        plt.ylim([-100,100])
# Display the plot
        plt.axis('equal')
        # Turn off spines (axes' lines)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

# Remove ticks and tick labels
        ax.set_xticks([])
        ax.set_yticks([])
        st.pyplot(fig)

##############################
### If no insurance bought ###
############################## 
    if st.button("Take the risk"):
        session_state.t += 1
        session_state.wealth = random.choices([session_state.wealth+session_state.gain, session_state.wealth-session_state.loss], [1-session_state.loss_probability, session_state.loss_probability], k=1)[0]
        session_state.loss = .9*session_state.wealth
        session_state.gain = .1*session_state.wealth
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss
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
    f'<div style="position: absolute; top: 75px; left: 170px; font-size: 34px;"> Likely gain = {session_state.gain:.2f}</div>',
    unsafe_allow_html=True)
    st.markdown(
    f'<div style="position: absolute; top: 100px; left: 170px; font-size: 34px;"> Potential loss = {session_state.loss:.2f}</div>',
    unsafe_allow_html=True)
    st.markdown(
    f'<div style="position: absolute; top: 125px; left: 170px; font-size: 34px;"> Fee = {session_state.fee:.2f}</div>',
    unsafe_allow_html=True)
 
        
    if session_state.t>10:
        if st.button("Close App"):
            st.experimental_rerun()  # Rerun the app to reset the state


if __name__ == "__main__":
    main()