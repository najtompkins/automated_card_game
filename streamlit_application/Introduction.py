import streamlit as st


# """
# This file is the entry-point to the application. The page presents the user with a brief overview of this application, the development of the project, and the rules of the game.
# From here the user can navigate to different pages of the application to play the game.
# Future Versions should link to the pages using buttons at the top of the page as well as in the sidebar for the ease of navigation on mobile phones.
# """

# Establish session state obejct to store which part of the page the user is viewing. Default is Introduction.
if 'intro_choice' not in st.session_state:
    st.session_state.intro_choice = 'Introduction'

# Main Title/introduction for the application/page
st.markdown("<h1 style='text-align:center;font-size:50px;'>Welcome to The Game of War!</h1>", unsafe_allow_html=True)

# Set function for changing which information the user sees when they select a button
def change_intro_choice(choice):
    st.session_state.intro_choice = choice

# Sidebar for selecting which information the user wants to see
st.sidebar.write("What do you want to know about?")
st.sidebar.button('This Application', key='ThisApp_Sidebar', on_click=lambda: change_intro_choice('Introduction'))
st.sidebar.button('Development', key='Development_Sidebar', on_click=lambda: change_intro_choice('Development'))
st.sidebar.button('Game Rules', key='GameRules_Sidebar', on_click=lambda: change_intro_choice('Rules'))

# Buttons at the top of the page for ease of navigation during mobile user experience. 
st.markdown("<p style='text-align:center;font-size:18px;'>What do you want to know about?</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.button('This Application', key='ThisApp', on_click=lambda: change_intro_choice('Introduction'))
with col2:
    st.button('Development', key='Development', on_click=lambda: change_intro_choice('Development'))
with col3:
    st.button('Game Rules', key='GameRules', on_click=lambda: change_intro_choice('Rules'))

# Introduction information content (default and when selected.)
if st.session_state.intro_choice == 'Introduction':
    # Title for the app
    # st.markdown("<h1 style='text-align:center;font-size:50px;'>Welcome to The Game of War!</h1>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align:center;font-size:40px;'>This Application</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # The SideBar
    st.markdown("### The SideBar")
    st.markdown("""
    - The SideBar to your left allows you to navigate between the different pages of this application.
        - The **Introduction** page is what you're reading right now.
        - The **War Room** page is where you will simulate the card game "War" and view, in real-time, some statistics about the game.
        - The **Stats Dashboard** page is where you can view some statistics about the game, who won, how many rounds it took, etc.
        - The **War Data** Page is where all of the game data is populated. See what is going on during each round!
    """)

# Development information content (when selected.)
elif st.session_state.intro_choice == 'Development':
    st.markdown("<h4 style='text-align:center;font-size:40px;'>App Development</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### The Purpose")
    st.markdown("""
    - Designed by Nathan-Andrew Tompkins in late 2023 and deployed early 2024, this application is a labor of love, diligence, and grit. The original purpose of this project was to practice **Python application development**. What started out as a simple exercize in logic and coding has evolved into the application you are interacting with right now. Since the beginning of this project I've developed 3 different versions of this game, all running similar-but-distict logical structures within their code.

    #### The Versions
    - The First is, of course, the Pythonic version, desinged to be run inside of a Jupyter notebook. This version utilizes the PyDeck library to create instances of decks, cards, hands, etc. When running the `set_up_game_environment()` function in its cell, followed immediately by the `play_war()` function in its cell, the program will simulate the entire game of war, from setup to declaring a winner, all while building 3 dataframes of exhaustive data on each round so that the user can see exactly what happened during the game. 
    - The Second is, oddly enough, re-built entirely from the ground up using Visual Basic for Applications (VBA), inside of Microsoft Excel 365. This is a fully-working version of the game and presents the user with a visual dashboard at the end to see the exhaustive statistics gathered during the game's simulation.
    - The Third version of the game is the one you are interactige with now! This version has strengths that the others do not: The ability to access this program from any supported device, A visually appealing way to see the data once the game has been fully simulated, and, last but not least, the ability to step through the game's rounds and see, in real time, how to simulation is progressing for either player!

    #### The Final product
    - Now that you are interacting with a nearly-completed version of this months-long endeavor, please take the time to simulate a war! See how the players fare against each other as the game progresses, and feel free to check out the pages linked to the left of all of the generated data.
    - Thanks for Playing my game! - NA
                
    """)

# Game Rules information content (when selected.)
elif st.session_state.intro_choice == 'Rules':
    # Rules of the Game
    st.markdown("<h4 style='text-align:center;font-size:40px;'>The Game</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Rules of the Game")
    st.markdown("""
    - **The goal** is to be the first player to win all 52 cards

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
