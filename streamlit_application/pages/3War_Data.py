import streamlit as st
import numpy as np
import pandas as pd

# """
# This page displays the data generated from the game in it's raw format,
# which is accessible and explorable using Pandas' dataframes populated during the simulation.
# """

if "Game_Statistics" not in st.session_state:
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

    st.write("Game Statistics:")
    st.write(Game_Statistics)
    st.write("Player 1 Statistics:")
    st.write(Player_1_Statistics)
    st.write("Player 2 Statistics:")
    st.write(Player_2_Statistics)
