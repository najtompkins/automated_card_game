import streamlit as st

# Set page configuration with title and stats icon
st.set_page_config(page_title="Stats Dashboard'", page_icon="📊", layout="wide")

# st.write("This page is currently under construction.")

st.markdown("<h1 style='text-align:center;font-size:50px;'>Game Statistics</h1>", unsafe_allow_html=True)
st.write("Please pardon our dust! This page is currently under construction.")

tab1, tab2, tab3 = st.tabs(["Game Data", "Player 1 Data", "Player 2 Data"])

with tab1:
    st.subheader('Game Data', divider='gray')
    col1, col2, col3 = st.columns(3)

with tab2:
    st.subheader('Player 1 Data', divider='blue')
    col1, col2, col3 = st.columns(3)

with tab3:
    st.subheader('Player 2 Data', divider='blue')
    col1, col2, col3 = st.columns(3)

