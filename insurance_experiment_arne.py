import streamlit as st
from streamlit import session_state
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors 
import os


if not os.path.exists('choices.xlsx'):
    df = pd.DataFrame(columns=['UserID', 'Choice', 'Wealth'])
    df.to_excel('choices.xlsx', index=False)
else:
    df = pd.read_excel('choices.xlsx')
    if df.empty or 'UserID' not in df.columns or 'Choice' not in df.columns or 'Wealth' not in df.columns:
        df = pd.DataFrame(columns=['UserID', 'Choice', 'Wealth'])
        df.to_excel('choices.xlsx', index=False)


loss_prob=1./6
initial_wealth=100

def start_page():
    st.title('Welcome to the App')
    if st.button('Start'):
        session_state.page = "user_id_page"
        st.experimental_rerun()

def user_id_page():
    st.title("Enter User ID")
    user_id = st.number_input('Enter your user ID (0-10)', min_value=0, max_value=10, step=1)
    if st.button("Confirm User ID"):
        session_state.user_id = user_id
        df = pd.read_excel('choices.xlsx')
        user_data = df[df['UserID'] == user_id]
        if not user_data.empty:
            session_state.wealth = user_data.iloc[-1]['Wealth']
            session_state.t = len(user_data)
            session_state.df = user_data
            session_state.loss = .9 * session_state.wealth
            session_state.gain = .1 * session_state.wealth
            session_state.loss_probability = loss_prob
            session_state.fee = 1.1 * session_state.loss_probability * session_state.loss
        else:
            session_state.t = 0
            session_state.wealth = initial_wealth
            session_state.loss = .9*session_state.wealth
            session_state.gain = .1*session_state.wealth
            session_state.loss_probability = loss_prob
            session_state.fee = 1.1*session_state.loss_probability*session_state.loss
            session_state.rolled = 0
            session_state.df = pd.DataFrame(columns=['UserID', 'Choice', 'Wealth'])
        session_state.page = "main_app_page"
        st.experimental_rerun()

def end_page():
    st.title('Thank You')
    random_code = "".join([str(random.randint(0, 9)) if i=='X' else i for i in "XXXABCXXLMLXXEEXXXX"])
    st.write("Your code:")
    st.code(random_code)



die_face_layouts = [
    np.array([[0, 0, 0], [0, 1,0 ], [0, 0, 0]]),  # layout for die face 1
    np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),  # layout for die face 2
    np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]),  # layout for die face 3
    np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]),  # layout for die face 4
    np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]]),  # layout for die face 5
    np.array([[1, 0, 1], [1, 0, 1], [1, 0, 1]])   # layout for die face 6
]

def draw_diefaces_explanation(positive, negative, rolled):
    fig = plt.figure(figsize=(11, 3), dpi=80)

    gs = gridspec.GridSpec(4, 14, figure=fig)
    ax_dice = [plt.subplot(gs[0:2, i], aspect='equal') for i in range(5)]
    ax_dice.append(plt.subplot(gs[2:4, 0],aspect='equal'))

    ax_bar = [plt.subplot(gs[i, 7:9]) for i in range(4)]

    ax_text = plt.subplot(gs[:, 9:])

    for i, ax in enumerate(ax_dice):
        ax.set(xticks=[], yticks=[])
        ax.axis('off')

        if i+1 == rolled and i+1 == 6:
            face_color = 'lightsalmon' 
        elif i+1 == rolled:
            face_color = 'lightgreen'
        else:
            face_color = 'white'

        rect = patches.Rectangle((0, 0), 1, 1, facecolor=face_color, edgecolor='black')
        ax.add_patch(rect)

        for r in range(3):
            for c in range(3):
                if die_face_layouts[i][r, c] == 1:
                    circle = patches.Circle((c/3.0+0.17, 2/3.0-r/3.0+0.17), 0.1, color='black')
                    ax.add_patch(circle)
                    
    bar_values = [session_state.wealth + positive - session_state.fee, session_state.wealth + positive, session_state.wealth - session_state.fee, session_state.wealth - negative]
    max_val = max(bar_values)
    
    text = ["Uninsured", "Insured", "Uninsured", "Insured"]

    for i, ax in enumerate(ax_bar):
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
        bar_length = bar_values[i]/max_val  # scale the bar lengths relative to the max value
        
        ax.barh(0, bar_length, height=0.3, color='red' if bar_values[i] < session_state.wealth else 'green', edgecolor='none')  # Use horizontal bars without edges
        
        wealth_scaled = session_state.wealth / max_val
        ax.axvline(x=wealth_scaled, color='black')  # Draw a vertical line representing the current wealth
        
        ax.set(xticks=[], yticks=[])
        ax.set_xlim(0, 1)  # x-limits are now between 0 and 1 since the bar lengths are scaled
        ax.text(bar_length/2, 0, f'{bar_values[i]:.2f}', ha='center', va='center', fontsize=8, color='black')

        # Add corresponding text
        ax_text.text(0.0, i / 4.0 + 0.125, text[i], ha='center', va='center', fontsize=8, color='black')



    ax_text.axis('off')
    plt.tight_layout()
    st.pyplot(fig)






def main_app_page():
    user_id = session_state.user_id

    if 't' not in session_state:
        session_state.t = 0

    if 'wealth' not in session_state:
        session_state.wealth=initial_wealth

    if 'loss' not in session_state:
        session_state.loss = .9*session_state.wealth

    if 'gain' not in session_state:
        session_state.gain = .1*session_state.wealth

    if 'loss_probability' not in session_state:
        session_state.loss_probability = loss_prob

    if 'fee' not in session_state:
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss

    if 'rolled' not in session_state:
        session_state.rolled = 0

    st.write(f'Wealth: {session_state.wealth:.2f}')
    st.write(f'Gain: {session_state.gain:.2f}')
    st.write(f'Loss: {session_state.loss:.2f}')
    st.write(f'Fee: {session_state.fee:.2f}')

    option = st.radio('Make a choice', ('Buy insurance', 'Take the risk'))

    if st.button('Roll the Dice'):
        session_state.t=session_state.t+1
        session_state.rolled = random.randint(1, 6)
        
        if option == 'Buy insurance':
            if session_state.rolled < 6:
                session_state.wealth = session_state.wealth - session_state.fee + session_state.gain
            elif session_state.rolled == 6:
                session_state.wealth = session_state.wealth - session_state.fee
        elif option == 'Take the risk':
            if session_state.rolled < 6:
                session_state.wealth = session_state.wealth +  session_state.gain
            else:  # the rolled number is 6, the loss case
                session_state.wealth = session_state.wealth - session_state.loss  # decrease wealth by the loss amount
                
        new_data = pd.DataFrame({'UserID': [session_state.user_id], 'Choice': [option], 'Wealth': [session_state.wealth]})
        session_state.df = pd.concat([session_state.df, new_data], ignore_index=True)

        session_state.loss = .9 * session_state.wealth
        session_state.gain = .1 * session_state.wealth
        session_state.fee = 1.1 * session_state.loss_probability * session_state.loss

        # Read the existing DataFrame from the Excel file
        df = pd.read_excel('choices.xlsx')

        # Append only the new data
        df = pd.concat([df, new_data], ignore_index=True)  # Change this line

        # Write the entire DataFrame back to the Excel file
        df.to_excel('choices.xlsx', index=False, header=True)

        st.experimental_rerun()

    draw_diefaces_explanation(session_state.gain, session_state.loss, session_state.rolled)

    if session_state.t >= 50:
        session_state.page = "end_page"
        st.experimental_rerun()


if 'page' not in st.session_state:
    st.session_state.page = "start_page"

PAGES = {
    "start_page": start_page,
    "user_id_page": user_id_page,
    "main_app_page": main_app_page,
    "end_page": end_page,
}

PAGES[st.session_state.page]()

