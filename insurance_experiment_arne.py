import streamlit as st
from streamlit import session_state
import pandas as pd
import random
import os

def random_description():
    descriptions = ["Lorem Ipsum ...", "Dolor Sit Amet ...", "Consectetur Adipiscing ...", "Elit Sed Do ..."]
    return random.choice(descriptions)

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
        session_state.page = "main_app_page"
        st.experimental_rerun()

loss_prob=1./6
initial_wealth=100
def end_page():
    st.title('Thank You')
    random_code = "".join([str(random.randint(0, 9)) if i=='X' else i for i in "XXXABCXXLMLXXEEXXXX"])
    st.write("Your code:")
    st.code(random_code)

def main_app_page():
    user_id = session_state.user_id

# Initialize session state variables
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

    st.write(f'Wealth: {session_state.wealth:.2f}')
    st.write(f'Gain: {session_state.gain:.2f}')
    st.write(f'Loss: {session_state.loss:.2f}')
    st.write(f'Fee: {session_state.fee:.2f}')
 

    if not os.path.isfile('data.csv'):
        df = pd.DataFrame(columns=['UserID', 'Die Face', 'Outcome', 'Time', 'Capital'])
        df.to_csv('data.csv', index=False)
        time = 1
        capital = 1000
    else:
        df = pd.read_csv('data.csv')
        user_data = df[df['UserID'] == user_id]
        if user_data.empty:
            time = 1
            capital = 1000
        else:
            time = user_data.iloc[-1]['Time']
            capital = user_data.iloc[-1]['Capital']

    st.title('Main App')

#    dice_df = pd.DataFrame({
#        "Outcomes": [ round(random.uniform(1, 2), 2), round(random.uniform(0, 1), 2)]
#        "Die Face": [ "1, 2, 3, 4, 5", "6"],
#    })

    def highlight_cells(data, color='white'):
        attr = f'background-color: {color}'
        other = 'background-color: white'
        mask = pd.DataFrame(other, index=data.index, columns=data.columns)
        mask.iloc[0, 0] = mask.iloc[0, 1] = 'background-color: green'
        mask.iloc[1, 0] = mask.iloc[1, 1] = 'background-color: red'
        return mask


    option = st.radio('Make a choice', ('Buy insurance', 'Take the risk'))

    if st.button('Confirm'):
        #and session_state.t < 10:
        session_state.t=session_state.t+1
        if option == 'Buy insurance':
            session_state.wealth = session_state.wealth - session_state.fee + session_state.gain
        else:
            session_state.wealth = session_state.wealth+random.choices([session_state.gain, -session_state.loss], [1-session_state.loss_probability, session_state.loss_probability], k=1)[0]
        # new_row = pd.DataFrame({'UserID': [user_id], 'Die Face': [dice_df.iloc[1:, 0].to_list()], 'Outcome': [dice_df.iloc[1:, 1].to_list()], 'Time': [time], 'Capital': [capital]})
        # df = pd.concat([df, new_row], ignore_index=True)
        # df.to_csv('data.csv', index=False)
        session_state.loss = .9*session_state.wealth
        session_state.gain = .1*session_state.wealth
        session_state.fee = 1.1*session_state.loss_probability*session_state.loss

        # Rerun after each confirmed choice to generate new random outcomes and update the time and capital.
        st.experimental_rerun()

        # dice_df = pd.DataFrame({
        #     "Die Face": [ "1, 2, 3, 4, 5", "6"],
        #     "Outcomes": [ round(session_state.wealth+session_state.gain, 2), round(session_state.wealth-session_state.loss, 2)]
        #     })
        # st.write("Dice Table:")
        # st.dataframe(dice_df.style.apply(highlight_cells, axis=None))

    if session_state.t >= 5:
        st.session_state.page = "end_page"
        st.experimental_rerun()

PAGES = {
    "start_page": start_page,
    "user_id_page": user_id_page,
    "main_app_page": main_app_page,
    "end_page": end_page
}

st.session_state.page = st.session_state.get("page", "start_page")

PAGES[st.session_state.page]()


