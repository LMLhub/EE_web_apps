import streamlit as st
from streamlit import session_state as SessionState
import random
import pandas as pd

# Defining the gamble pairs for additive and multiplicative dynamics
additive_gambles = additive = [
    [[-308, 291], [-88, 71]],
    [[-543, 554], [100, -89]],
    [[692, -523], [-254, 423]],
    [[683, -670], [-114, 127]],
    [[-454, 481], [304, -277]],
    [[636, -549], [-371, 458]],
    [[-394, 367], [-9, -18]],
    [[-232, 372], [240, -100]],
    [[524, -498], [447, -421]],
    [[-183, 272], [-32, 121]],
    [[446, -344], [-181, 283]],
    [[379, -226], [28, 125]],
    [[-226, 282], [-121, 177]],
    [[-464, 308], [229, -385]],
    [[3, 121], [24, 100]],
    [[-673, 629], [-118, 74]],
    [[-235, 74], [-53, -108]],
    [[-455, 585], [-147, 277]],
    [[-479, 523], [332, -288]],
    [[542, -469], [-124, 197]],
    [[56, -177], [-148, 27]],
    [[66, -190], [53, -177]],
    [[-54, 128], [102, -28]],
    [[-170, 237], [67, 0]],
    [[-82, 146], [5, 59]],
    [[-312, 402], [143, -53]],
    [[478, -441], [-39, 76]],
    [[-661, 630], [461, -492]],
    [[-350, 334], [-233, 217]],
    [[-331, 333], [-256, 258]],
    [[340, -501], [232, -393]],
    [[-237, 303], [-25, 91]],
    [[492, -454], [45, -7]],
    [[-628, 456], [-50, -122]],
    [[-482, 612], [489, -359]]
]

multiplicative_gambles = multiplicative = [
    [[0.74, 1.23], [0.89, 1.08]],
    [[0.77, 1.18], [0.84, 1.11]],
    [[1.2, 0.8], [1.1, 0.9]],
    [[1.23, 0.77], [1.13, 0.87]],
    [[1.26, 0.73], [0.78, 1.21]],
    [[0.73, 1.25], [1.12, 0.86]],
    [[1.3, 0.75], [0.86, 1.19]],
    [[1.23, 0.8], [0.95, 1.08]],
    [[0.74, 1.16], [0.84, 1.06]],
    [[1.19, 0.73], [0.81, 1.11]],
    [[1.28, 0.84], [0.92, 1.2]],
    [[0.77, 1.25], [0.86, 1.16]],
    [[0.83, 1.26], [1.17, 0.92]],
    [[1.26, 0.72], [0.86, 1.12]],
    [[1.2, 0.71], [0.79, 1.12]],
    [[1.23, 0.7], [0.8, 1.13]],
    [[0.82, 1.3], [1.19, 0.93]],
    [[1.29, 0.88], [0.93, 1.24]],
    [[1.29, 0.73], [0.91, 1.11]],
    [[1.24, 0.74], [1.14, 0.84]],
    [[0.76, 1.19], [0.81, 1.14]],
    [[1.3, 0.83], [1.22, 0.91]],
    [[0.75, 1.22], [0.89, 1.08]],
    [[0.78, 1.2], [0.83, 1.15]],
    [[1.28, 0.74], [0.86, 1.16]],
    [[0.77, 1.28], [0.87, 1.18]],
    [[1.23, 0.73], [0.89, 1.07]],
    [[1.19, 0.74], [0.85, 1.08]],
    [[1.17, 0.71], [1.09, 0.79]],
    [[1.26, 0.78], [1.14, 0.9]],
    [[1.28, 0.78], [1.13, 0.91]],
    [[1.19, 0.76], [1.17, 0.81]],
    [[1.22, 0.79], [0.94, 1.06]],
    [[0.8, 1.26], [0.86, 1.14]],
    [[1.21, 0.77], [0.88, 1.11]]
]

def get_gamble_index():
    return SessionState.gamble_index if hasattr(SessionState, 'gamble_index') else 0

def get_safe_bet_counts():
    return SessionState.safe_bet_counts if hasattr(SessionState, 'safe_bet_counts') else [0, 0]

def get_total_bet_counts():
    return SessionState.total_bet_counts if hasattr(SessionState, 'total_bet_counts') else [0, 0]

def get_wealth():
    return SessionState.wealth if hasattr(SessionState, 'wealth') else 1000

def get_gambles_order():
    return SessionState.gambles_order if hasattr(SessionState, 'gambles_order') else None

# Get or set up the state of the app
SessionState.wealth = get_wealth()
SessionState.gambles_order = get_gambles_order()
SessionState.gamble_index = get_gamble_index()
SessionState.safe_bet_counts = get_safe_bet_counts()
SessionState.total_bet_counts = get_total_bet_counts()

# If this is the first run of the app, randomly select the order of the gambles
if SessionState.gambles_order is None:
    SessionState.gambles_order = [additive_gambles, multiplicative_gambles]
    random.shuffle(SessionState.gambles_order)

# Get the current gamble
gambles = SessionState.gambles_order[0] if SessionState.gamble_index < len(SessionState.gambles_order[0]) else SessionState.gambles_order[1]
gamble = gambles[SessionState.gamble_index % len(gambles)]

st.title('Gamble selection')

# Check if all the gambles have been played
if SessionState.gamble_index == len(additive_gambles) + len(multiplicative_gambles):
    for i, gamble_type in enumerate(['additive', 'multiplicative']):
        if SessionState.gambles_order[i] == additive_gambles:
            st.write(f'You took the safe bet {SessionState.safe_bet_counts[i] / SessionState.total_bet_counts[i] * 100:.2f}% of the time in the {gamble_type} setting.')
        else:
            st.write(f'You took the safe bet {SessionState.safe_bet_counts[i] / SessionState.total_bet_counts[i] * 100:.2f}% of the time in the {gamble_type} setting.')
    
    if st.button('Restart the Experiment'):
        SessionState.wealth = 1000
        SessionState.gambles_order = None
        SessionState.gamble_index = 0
        SessionState.safe_bet_counts = [0, 0]
        SessionState.total_bet_counts = [0, 0]
else:
    show_wealth = st.checkbox('Show wealth', value=True)

    # Show the current wealth if the checkbox is checked
    if show_wealth:
        st.write(f'Current wealth: {SessionState.wealth}')
    else:
        st.write("Wealth is hidden.")

    for i, bet in enumerate(gamble, 1):
        df = pd.DataFrame([bet], columns=['Outcome 1', 'Outcome 2'])
        st.write(f' Bet {i}:')
        st.markdown(df.to_html(index=False), unsafe_allow_html=True)
        if st.button(f'Play Bet {i}'):
            # Simulate gamble outcome
            outcome = random.choice(bet)
            # Update wealth
            if isinstance(outcome, int):
                SessionState.wealth += outcome  # For additive gambles
            else:
                SessionState.wealth *= outcome  # For multiplicative 

            order_index = 0 if SessionState.gamble_index < len(SessionState.gambles_order[0]) else 1
            SessionState.total_bet_counts[order_index] += 1

            # Determine if the selected bet is the safer one
            safe_bet_index = 0 if (isinstance(gamble[0][0], int) and abs(gamble[0][0] - gamble[0][1]) < abs(gamble[1][0] - gamble[1][1])) or \
                                 (isinstance(gamble[0][0], float) and abs((gamble[0][0] / gamble[0][1]) - 1) < abs((gamble[1][0] / gamble[1][1]) - 1)) else 1
            if i - 1 == safe_bet_index:
                SessionState.safe_bet_counts[order_index] += 1

            # Go to the next gamble
            SessionState.gamble_index += 1

