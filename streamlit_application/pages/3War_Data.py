import streamlit as st
import numpy as np
import pandas as pd

# st Game_Statistics
Game_Statistics = st.session_state.Game_Statistics
# global Player_1_Statistics
Player_1_Statistics = st.session_state.Player_1_Statistics
# global Player_2_Statistics
Player_2_Statistics = st.session_state.Player_2_Statistics

st.title("Game and Round Data / Player Statistics")
st.write("Here are the game statistics:")
st.write(Game_Statistics)
st.write("Here are the player 1 statistics:")
st.write(Player_1_Statistics)
st.write("Here are the player 2 statistics:")
st.write(Player_2_Statistics)
