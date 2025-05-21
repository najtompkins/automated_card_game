import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # ✅ correct import


# Set page configuration with title and books icon
st.set_page_config(page_title="Landing Page", page_icon="📚", layout="centered")

# Main Title/introduction for the application/page
st.markdown("<h1 style='text-align:center;font-size:50px;'>Welcome to The Game of War!</h1>", unsafe_allow_html=True)
st.info("""
        The **SideBar** on your left you will allow you to navigate between the different pages of this application. You are reading the Introduction page.
    - ***On Mobile, please tap the arrow in the upper-left corner to open the **SideBar**.***""")

# Using tabs to organize content
tabs = st.tabs(["This Application", "This Project", "Game Rules"])

with tabs[0]:  # This Application
    st.subheader('This Application')
    st.divider()
    st.write("")
    st.markdown("""
    Hello! Welcome to my application and thank you for playing my game. It means a lot. The information on this page is summarized from the project itself over at my github: [github.com/najtompkins/automated_card_game](https://github.com/najtompkins/automated_card_game). Here are the highlights:
    """)
    # Tabs for learning about each page in the application
    with st.expander("📱 Web Application"):
        st.markdown("""
        **The Web Application**: This is the verison of the project you are experiencing now. It is a fully-deployed web application that simulates the card game War, generating player metric dashboards, comprehensive dataframes, and card distribution charts which help visualize how the game is progressing in real-time.
        """)
        if st.button("Simulate Your Own War Now!"):
            switch_page("War_Room")
    with st.expander("💥 War Room"):
        st.markdown("""
        **The War Room**: Is found on the **SideBar** or by clicking the button below. This page is the crown jewel of this application. It allows you to simulate the game and view (some) of the data generated during the game in real-time, and the rest of the data after a winner has been declared.
            """)
        if st.button("Visit the War Room!"):
            switch_page("War_Room")
        st.image("images/streamlit_images/IncrementThroughGameApp.png")
    with st.expander("🎛️ The Stats Dashboard"):
        st.markdown("""
        **The Stats Dashboard**: This page is where you can view some very unique metrics and statistics about the game as a whole, or by player, who won, how many rounds they played, etc. The dashboards are designed to easily understand how the game progressed and who was winning at the end of any given round. This page is populated once a War has begun in the **War Room**. 
        """)
        st.image("images/streamlit_images/GameStatsDashboardApp.png")
    with st.expander("📊 War Data"):
        st.markdown("""
        **The War Data**: The War Data page is simple but vital to the purpose of this application, as the dataframes on display there contain over 40 different metrics generated and reported throughout the game. These very metrics power the metrics on the **Stats Dashboard** page. The dataframes are available to the user to puruse, download, or analyze the game in detail for themselves.  This page is populated once a War has begun in the **War Room**.
            """)
        st.image("images/streamlit_images/GameDataframeApp.png")

with tabs[1]:  # This Project
    st.subheader('This Project')
    st.divider()

    st.write("**Developer:** Nathan-Andrew Tompkins")
    st.write(f"**LinkedIn:** [Nathan-Andrew Tompkins](https://www.linkedin.com/in/nathan-andrew-tompkins/)")
    st.write(f"**Project Repository:** [https://github.com/najtompkins/automated_card_game](https://github.com/najtompkins/automated_card_game)")
    st.write("")
    st.subheader('Purpose and History')
    st.markdown("""
    Designed by Nathan-Andrew Tompkins in late 2023 and deployed early 2024, this application is a labor of love, diligence, and grit. The original purpose of this project was to practice **Python application development**. What started out as a simple exercise in logic and coding has evolved into the very thing you are interacting with right now. Since the beginning of this project I've developed 3 different versions of this game, all running similar-but-distinct logical frameworks to house their code. This web-based version is what will be on display whenenever this project is represented.
    """)
    st.subheader('Project Versions (in order of development)')
    project_tabs = st.tabs(["📝 Jupyter Notebook", "📊 Excel VBA", "📱 Streamlit Web App"])
    with project_tabs[0]:
        st.markdown("""
        ### **Jupyter Notebook:** 
        The un-refined first version of this project was first uploaded on **March 5th, 2024** and further developed through **April 2nd**, nearly a month later. This is, of course, a Pythonic version, designed to be run inside of a Jupyter Notebook environment. This version utilizes the PyDeck library to create instances of decks, cards, hands, etc. When running the `set_up_game_environment()` function in its cell, followed immediately by the `play_war()` function in its cell, the program will simulate the entire game of war from setup to declaring a winner. During this, the program will build 3 dataframes of exhaustive metrics on each round so that the user can see exactly what happened during the game.
        - While this is absolutely a 'War Simulator' in functionality. This version of the program is, simply put, not designed to be used outside of development. The Jupyter environment was instrumental in the early developement of the logic and execution of the simulation, but while the file can be found [here](https://github.com/najtompkins/automated_card_game/blob/main/ipynb_files/war_v6_data.ipynb), it is not intended for general use as it is simply a peek at development in this project's early stages.
        """)
        with st.expander("Jupyter: Notebook Imports"):
            st.image("images/ipynb_images/Imports.png", )
        with st.expander("Jupyter: Compare Function"):
            st.image("images/ipynb_images/CompareFunction.png", )
        with st.expander("Jupyter: Quick Dataframe"):
            st.image("images/ipynb_images/QuickDataframe.png", )
        with st.expander("Jupyter: Set Up and Play"):
            st.image("images/ipynb_images/SetupAndPlay.png", )

    with project_tabs[1]:
        st.markdown("""
        ### **Excel 365/VBA:** 
        This second version was oddly enough, re-built entirely from the ground up using Visual Basic for Applications (VBA) inside of Microsoft Excel 365. This is a fully-working version of the game and presents the user with a visual dashboard at the end to see the exhaustive statistics gathered during the game's simulation. Why do I also have a version of this program written in a completely different coding language, running in a program designed for a thousand other uses than playing a card game? Because Excel is ubiquitous in the Data Analytics and Business Intelligence industry (especially for smaller businesses) and I used this same project to further refine my Excel skills by building it out in a different and unique way. Download the workbook [here](https://github.com/najtompkins/automated_card_game/blob/main/excel_files/WarCardGame.xlsm).
        - ***Note: This version is a proof of concept, first and foremost. It does not have the same functionality as the web application, nor is it able to run on MacOS systems. It requires the workbook to be trusted by the user (more information in the project README) and for macros to be enabled within the workbook itself before it is able to run. I am proud of this version, but it is certainly not intended for general use and is, again a proof-of-concept.***
        """)
        with st.expander("VBA: Deal Cards to Players"):
            st.image("images/excel_images/DealCards2Msg.png")
        with st.expander("VBA: Front-End Layout"):
            st.image("images/excel_images/FrontEnd.png")
        with st.expander("VBA: Player Stats Dashboard"):
            st.image("images/excel_images/GamePlayerStats.png")
        with st.expander("VBA: Game Dataframe"):
            st.image("images/excel_images/GameDataTable.png")

    with project_tabs[2]:
        st.markdown("""
        ### **Streamlit Web App:** 
        The third and final version of the game is the one you are interacting with now! This web-application has strengths that the others do not: The ability to access this program from any supported device, a visually appealing way to see the data once the game has been fully simulated, and, last but not least, the ability to step through the game's rounds and see how the simulation is progressing for either player in real time!
        """)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        #### Play the Game for Yourself
        Once you've read up on each version of this program, you can play the game yourself. You are interacting with a nearly-completed version of this months-long endeavor, so please take the time to simulate your own War in the **War Room** or visit the project repository [here](https://github.com/najtompkins/automated_card_game) to learn more about this project in depth.
        - Thanks for Playing my game!
        """)
    if st.button("Simulate Your Own War Now!", key="from_thank_you_1"):
        switch_page("War_Room")


with tabs[2]:  # Game Rules
    st.subheader('Game Rules')
    st.divider()
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
    The game ends when one player has won all the cards.

    - *Source: [https://bicyclecards.com/how-to-play/war](https://bicyclecards.com/how-to-play/war)*
    - *Note: Cited rules include players dealing 2 more cards when a  'war' occurs, one face down, another face up. This program deals 3 cards face down, and one face up.* 
    """)


