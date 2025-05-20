import streamlit as st
import numpy as np
import pandas as pd

# """
# This page displays the data generated from the game in it's raw format,
# which is accessible and explorable using Pandas' dataframes populated during the simulation.
# """

# Set page configuration with title and spades icon
st.set_page_config(page_title="War Data", page_icon="♠️", layout="wide")

if "Game_Statistics" not in st.session_state or len(st.session_state.Game_Statistics) == 0:
    st.markdown("<h1 style='text-align:center;font-size:50px;'>Game and Player Data</h1>", unsafe_allow_html=True)
    st.markdown("<i><h6 style='text-align:center;font-size:20px;'>Please simulate a game in the War Room to see the data</h6></i>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Go to the War Room"):
            st.switch_page("pages/1War_Room.py")
else:

    # Assign the game statistics session_State object (pandas DF) to the variable 'Game_Statistics'
    Game_Statistics = st.session_state.Game_Statistics
    # Do the same for Player_1_Statistics
    Player_1_Statistics = st.session_state.Player_1_Statistics
    # Do the same for Player_2_Statistics
    Player_2_Statistics = st.session_state.Player_2_Statistics

    # Set the title of the page
    st.markdown("<h1 style='text-align:center;font-size:50px;'>Game and Round Data / Player Statistics</h1>", unsafe_allow_html=True)

    st.info(
    """
    **Thank you for checking out the data page. To better understand what the simulation has generated, here is how to interact with the data tables:**
    - **Resize**: Drag the bottom right corner of the table to resize it.
    - **View in full screen**: Click on the double arrow icon in the upper right corner of the table.
    - **Download data**: Hover over the table and use the download icon that appears in the top right to download the data.
    """
    )

    tab1, tab2, tab3 = st.tabs(["Game Data", "Player 1 Data", "Player 2 Data"])

    with tab1:
        st.subheader('Game Data')
        st.divider()
        st.dataframe(Game_Statistics)

    with tab2:
        st.subheader('Player 1 Data')
        st.divider()
        st.dataframe(Player_1_Statistics)

    with tab3:
        st.subheader('Player 2 Data')
        st.divider()
        st.dataframe(Player_2_Statistics)
