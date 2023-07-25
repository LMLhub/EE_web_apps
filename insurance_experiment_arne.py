import streamlit as st
import pandas as pd
import random
import os

def random_description():
    descriptions = ["Lorem Ipsum ...", "Dolor Sit Amet ...", "Consectetur Adipiscing ...", "Elit Sed Do ..."]
    return random.choice(descriptions)

def start_page():
    st.title('Welcome to the App')
    if st.button('Start'):
        st.session_state.page = "user_id_page"
        st.experimental_rerun()

def user_id_page():
    st.title("Enter User ID")
    user_id = st.number_input('Enter your user ID (0-10)', min_value=0, max_value=10, step=1)
    if st.button("Confirm User ID"):
        st.session_state.user_id = user_id
        st.session_state.page = "main_app_page"
        st.experimental_rerun()
def main_app_page():
    user_id = st.session_state.user_id
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

    # Generate the random numbers at the start of each iteration
    dice_df = pd.DataFrame({
        "Die Face": [ "1, 2, 3, 4, 5", "6"],
        "Outcomes": [ round(random.uniform(1, 2), 2), round(random.uniform(0, 1), 2)]
    })

    def highlight_cells(data, color='white'):
        attr = f'background-color: {color}'
        other = 'background-color: white'
        mask = pd.DataFrame(other, index=data.index, columns=data.columns)
        mask.iloc[0, 0] = mask.iloc[0, 1] = 'background-color: green'
        mask.iloc[1, 0] = mask.iloc[1, 1] = 'background-color: red'
        return mask

    st.write("Dice Table:")
    st.dataframe(dice_df.style.apply(highlight_cells, axis=None))

    option = st.radio('Make a choice', ('Yes', 'No'))

    if st.button('Confirm') and time < 50:
        if option == 'Yes':
            time += 1
            capital = random.choice([capital * dice_df.loc[0, "Outcomes"] - 0.1 * capital, capital])
        else:
            capital = random.choice([capital * dice_df.loc[0, "Outcomes"], capital * dice_df.loc[1, "Outcomes"]])
        new_row = pd.DataFrame({'UserID': [user_id], 'Die Face': [dice_df.iloc[1:, 0].to_list()], 'Outcome': [dice_df.iloc[1:, 1].to_list()], 'Time': [time], 'Capital': [capital]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data.csv', index=False)

        # Rerun after each confirmed choice to generate new random outcomes and update the time and capital.
        st.experimental_rerun()

    st.write(f'Time: {time}')
    st.write(f'Capital: {capital}')

    if time >= 10:
        st.write("The app has ended for this user.")
        if st.button('Restart', key='restart'):
            st.session_state.page = "start_page"
            st.experimental_rerun()


PAGES = {
    "start_page": start_page,
    "user_id_page": user_id_page,
    "main_app_page": main_app_page
}

st.session_state.page = st.session_state.get("page", "start_page")

PAGES[st.session_state.page]()

