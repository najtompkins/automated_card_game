import streamlit as st

# Set page configuration with title and books icon
st.set_page_config(page_title="Landing Page", page_icon="📚", layout="centered")

# Main Title/introduction for the application/page
st.markdown("<h1 style='text-align:center;font-size:50px;'>Welcome to The Game of War!</h1>", unsafe_allow_html=True)

# Using tabs to organize content
tabs = st.tabs(["This Application", "App Development", "Game Rules"])

with tabs[0]:  # This Application
    st.markdown("<h4 style='text-align:center;font-size:40px;'>This Application</h4>", unsafe_allow_html=True)
    # st.markdown("<hr>", unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    #### The SideBar
    - To your left you will see a **SideBar** that allows you to navigate between the different pages of this application. ***On Mobile, please tap the arrow in the upper-left corner to open the sidebar.***
        - The **Introduction** page is what you're reading right now.
        - The **War Room** page is where you will simulate the card game "War" and view, in real-time, some statistics about the game.
        - The **Stats Dashboard** page is where you can view some statistics about the game, who won, how many rounds it took, etc.
        - The **War Data** Page is where all of the game data is populated. See what is going on during each round!
    """)

with tabs[1]:  # App Development
    st.markdown("<h4 style='text-align:center;font-size:40px;'>App Development</h4>", unsafe_allow_html=True)
    # st.markdown("<hr>", unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    
    #### The History            
    - Designed by Nathan-Andrew Tompkins in late 2023 and deployed early 2024, this application is a labor of love, diligence, and grit. The original purpose of this project was to practice **Python application development**. What started out as a simple exercise in logic and coding has evolved into the application you are interacting with right now. Since the beginning of this project I've developed 3 different versions of this game, all running similar-but-distinct logical structures within their code.

    #### The Versions
    - The First is, of course, the Pythonic version, designed to be run inside of a Jupyter notebook. This version utilizes the PyDeck library to create instances of decks, cards, hands, etc. When running the `set_up_game_environment()` function in its cell, followed immediately by the `play_war()` function in its cell, the program will simulate the entire game of war, from setup to declaring a winner, all while building 3 dataframes of exhaustive data on each round so that the user can see exactly what happened during the game. 
    - The Second is, oddly enough, re-built entirely from the ground up using Visual Basic for Applications (VBA), inside of Microsoft Excel 365. This is a fully-working version of the game and presents the user with a visual dashboard at the end to see the exhaustive statistics gathered during the game's simulation.
    - The Third version of the game is the one you are interacting with now! This version has strengths that the others do not: The ability to access this program from any supported device, a visually appealing way to see the data once the game has been fully simulated, and, last but not least, the ability to step through the game's rounds and see, in real time, how the simulation is progressing for either player!

    #### The Final Product
    - Now that you are interacting with a nearly-completed version of this months-long endeavor, please take the time to simulate a war! See how the players fare against each other as the game progresses, and feel free to check out the pages linked to the left of all of the generated data.
    - Thanks for Playing my game! - NA
    """)

with tabs[2]:  # Game Rules
    st.markdown("<h4 style='text-align:center;font-size:40px;'>Game Rules</h4>", unsafe_allow_html=True)
    # st.markdown("<hr>", unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    #### The Goal
    - The goal is to be the first player to win all 52 cards

    #### The Deal
    - The deck is divided evenly, with each player receiving 26 cards, dealt one at a time, face down. Anyone may deal first. Each player places their stack of cards face down, in front of them.

    #### The Play
    - Each player turns up a card at the same time and the player with the higher card takes both cards and puts them, face down, on the bottom of his stack.
    - If the cards are the same rank, it is War. Each player turns up three cards face down and one card face up. The player with the higher cards takes both piles (10 cards). If the turned-up cards are again the same rank, each player places another card face down and turns another card face up. The player with the higher card takes all cards, and so on.

    #### How to Keep Score
    - The game ends when one player has won all the cards.

    *Source: [https://bicyclecards.com/how-to-play/war](https://bicyclecards.com/how-to-play/war)*
    *Note: Original (cited) rules include players dealing 2 more cards in 'war'. This program deals 3 cards face down, and one face up to then compare.* 
    """)
