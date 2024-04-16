import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import altair as alt
import pandas as pd
import plotly.express as px


# Set page configuration with title and stats icon
st.set_page_config(page_title="Stats Dashboard'", page_icon="📊", layout="wide")

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

    # If the Game_Statistics DataFrame is empty, set the game_winner and rounds_total to 0
    # This is error handling. There should always be at least one row in the DataFrame if this part of the page is loading.
    try:
        game_winner = st.session_state.Game_Statistics['Round Winner'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        game_winner = 0
    try:
        rounds_total = int(st.session_state.Game_Statistics['Round Number'].iloc[-1])
    except IndexError:  # Catching the case where the DataFrame is empty
        rounds_total = 0

    # Set text colors for markdown text
    if game_winner == 1:
        color = '#429EBD'
    elif game_winner == 2:
        color = '#F7AD19'
    else:
        # color is black
        color = '#000000'

    st.markdown("<h1 style='text-align:center;font-size:50px;'>Game Statistics</h1>", unsafe_allow_html=True)
    st.write("Please pardon our dust! This page is currently under construction.")

    tab1, tab2, tab3 = st.tabs(["Game Data", "Player 1 Data", "Player 2 Data"])

    with tab1:
        st.subheader('Game Data', divider='gray')

        if game_winner == 1 or game_winner == 2:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} won the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
        
        if not game_winner:
            st.write("No winner to declare or data to display for the Game.")
            if st.button("Go to the War Room", key='leave_from_game_stats_dashboard'):
                st.switch_page("pages/1War_Room.py")

        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            st.metric(label='During the Game There Were:', value=f"{Game_Statistics['Total Wars In Game'].iloc[-1]} Wars")
        with row1_col2:
            st.metric(label="The Player who Won the Game:", value=f'Player {game_winner}!')
        with row1_col3:
            st.metric(label='Most Wars in a Single Round:', value=Game_Statistics['Total Wars In Round'].max())
        
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1:
            st.metric(label='The Players Played:', value=f"{int(Game_Statistics['Round Number'].iloc[-1])} Rounds")
        with row2_col2:
            if Player_1_Statistics['Player 1 Rounds Won'].max() > Player_2_Statistics['Player 2 Rounds Won'].max():
                most_rounds = 'Player 1'
            else:
                most_rounds = 'Player 2'
            
            st.metric(label="The Player Who Won the Most Rounds:", value=most_rounds)
        with row2_col3:

            if Player_1_Statistics['Player 1 Wars Won'].max() > Player_2_Statistics['Player 2 Wars Won'].max():
                most_wars = 'Player 1'
            else:
                most_wars = 'Player 2'
            
            st.metric(label="The Player Who Won the Most Wars:", value=most_wars)

        row3_col1, row3_col2, row3_col3 = st.columns(3)
        val1 = Game_Statistics['Total NonWar Cards Dealt In Game'].iloc[-1]
        val2 = Game_Statistics['Total War Cards Dealt In Game'].iloc[-1]
        val3 = Game_Statistics['Total Cards Dealt In Game'].iloc[-1]
        perc1 = (val1 / val3) * 100
        perc2 = (val2 / val3) * 100

        with row3_col1:
            st.metric(label='The Players Dealt', value=f"{Game_Statistics['Total Cards Dealt In Game'].iloc[-1]} Cards")
        with row3_col2:
            st.metric(label="How Many Cards Dealt in Normal Play?", value=f"{Game_Statistics['Total NonWar Cards Dealt In Game'].iloc[-1]} Cards ({perc1:.1f}%)")
        with row3_col3:
            st.metric(label="How Many Cards Dealt During Wars?", value=f"{Game_Statistics['Total War Cards Dealt In Game'].iloc[-1]} Cards ({perc2:.1f}%)")

            # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
        try:
            Player_1_Card_Count = Player_1_Statistics['Total Player 1 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_1_Card_Count = 26
        try:
            Player_2_Card_Count = Player_2_Statistics['Total Player 2 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_2_Card_Count = 26


        # For the Line chart
        # Create a DataFrame with the Round Number and Total Player Cards columns
        Card_Distributions = pd.DataFrame(columns=['Round Number', 'Total Player 1 Cards', 'Total Player 2 Cards'])
        Card_Distributions['Round Number'] = st.session_state.Game_Statistics['Round Number'].astype(float)
        Card_Distributions['Total Player 1 Cards'] = st.session_state.Player_1_Statistics['Total Player 1 Cards'].astype(int)
        Card_Distributions['Total Player 2 Cards'] = st.session_state.Player_2_Statistics['Total Player 2 Cards'].astype(int)
        Card_Distributions['Total NonWar Cards Dealt In Round'] = st.session_state.Game_Statistics['Total NonWar Cards Dealt In Round'].astype(int)
        Card_Distributions['Total War Cards Dealt In Round'] = st.session_state.Game_Statistics['Total War Cards Dealt In Round'].astype(int)
        Card_Distributions['Total Cards Dealt In Round'] = st.session_state.Game_Statistics['Total Cards Dealt In Round'].astype(int)
        Card_Distributions.drop_duplicates(subset=['Round Number'], keep='last')

        current_winner = None
        players_switched = 0
        for i in range(0, len(Card_Distributions)):
            if (int(Card_Distributions['Total Player 1 Cards'].iloc[i]) > int(Card_Distributions['Total Player 2 Cards'].iloc[i])) and current_winner == None:
                current_winner = 1
            elif (int(Card_Distributions['Total Player 1 Cards'].iloc[i]) > int(Card_Distributions['Total Player 2 Cards'].iloc[i])) and current_winner != 1:
                current_winner = 1
                players_switched += 1
            elif (int(Card_Distributions['Total Player 2 Cards'].iloc[i]) > int(Card_Distributions['Total Player 1 Cards'].iloc[i])) and current_winner == None:
                current_winner = 2
            elif (int(Card_Distributions['Total Player 2 Cards'].iloc[i]) > int(Card_Distributions['Total Player 1 Cards'].iloc[i])) and current_winner != 2:
                current_winner = 2
                players_switched += 1


    # For the dealing line chart

        # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
        try:
            Chart_Total_War_Cards_Dealt_In_Game = Game_Statistics['Total War Cards Dealt In Round']
        except IndexError:  # Catching the case where the DataFrame is empty
            Chart_Total_War_Cards_Dealt_In_Game = 0
        try:
            Chart_Total_NonWar_Cards_Dealt_In_Game = Game_Statistics['Total NonWar Cards Dealt In Round']
        except IndexError:  # Catching the case where the DataFrame is empty
            Chart_Total_NonWar_Cards_Dealt_In_Game = 0
        try:
            Chart_Total_Cards_Dealt_In_Game = Game_Statistics['Total Cards Dealt In Round']
        except IndexError:  # Catching the case where the DataFrame is empty
            Chart_Total_Cards_Dealt_In_Game = 0

        # Player names for the chart legends
        values = [Player_1_Card_Count, Player_2_Card_Count]
        # Create a bar chart using streamlit
        # line_chart_placeholder.line_chart(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color=["#429EBD","#F7AD19"])
        fig_line = px.line(Card_Distributions, x='Round Number', y=['Total Cards Dealt In Round'], color_discrete_map={"Total Cards Dealt In Round": "#9AD8E1"}, labels={ "value": "Total Cards", "variable": "Players"}, height=200)
        fig_line.update_layout(legend=dict(x=0.5, xanchor="center", y=1.0, yanchor="bottom", orientation="h"), legend_title_text="")
        st.markdown(f"<h4 style='text-align:center;font-size:28px;'>There were {Game_Statistics['Total Wars In Game'].max()} Wars during the game.</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)


    # For the distribution line chart
        # Player names for the chart legends
        players = ['Player 1', 'Player 2']
        values = [Player_1_Card_Count, Player_2_Card_Count]
        # Create a bar chart using streamlit
        # line_chart_placeholder.line_chart(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color=["#429EBD","#F7AD19"])
        fig_line = px.line(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color_discrete_map={"Total Player 1 Cards": "#429EBD", "Total Player 2 Cards": "#F7AD19"}, labels={ "value": "Total Cards", "variable": "Players"}, height=350)
        # Update legend names
        fig_line.for_each_trace(lambda t: t.update(name=t.name.replace("Total Player 1 Cards", "Player 1's Total Cards")))
        fig_line.for_each_trace(lambda t: t.update(name=t.name.replace("Total Player 2 Cards", "Player 2's Total Cards")))
        # Find the max value for each series
        max_value_player1 = Card_Distributions['Total Player 1 Cards'].max()
        max_value_player2 = Card_Distributions['Total Player 2 Cards'].max()
        # Get the rounds for each max value
        round_max_player1 = Card_Distributions[Card_Distributions['Total Player 1 Cards'] == max_value_player1]['Round Number'].values[0] if max_value_player1 > 0 else 0
        round_max_player2 = Card_Distributions[Card_Distributions['Total Player 2 Cards'] == max_value_player2]['Round Number'].values[0] if max_value_player2 > 0 else 0
        # Add annotations for max values
        fig_line.add_annotation(x=round_max_player1, y=max_value_player1, 
                        text=f"Max Player 1 Cards Held: {max_value_player1}", showarrow=True, arrowhead=6, arrowcolor="#429EBD", font=dict(color='black', size=14), ax=0, ay=-40)
        fig_line.add_annotation(x=round_max_player2, y=max_value_player2, 
                        text=f"Max Player 2 Cards Held: {max_value_player2}", showarrow=True, arrowhead=6, arrowcolor="#F7AD19", font=dict(color='black', size=14), ax=0, ay=-40)

        fig_line.update_layout(legend=dict(x=0.5, xanchor="center", y=1.0, yanchor="bottom", orientation="h"), legend_title_text="")
        st.markdown(f"<h4 style='text-align:center;font-size:28px;'>The Players switched dominance {players_switched} times.</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)


        # st.dataframe(Game_Statistics)

    with tab2:
        st.subheader('Player 1 Data', divider='blue')

        if game_winner == 1:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} won the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
        elif game_winner == 2:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:gray;'>Player 1 lost the Game after {rounds_total} rounds.</h4>", unsafe_allow_html=True)
        
        if not game_winner:
            # st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} Wins the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
            st.write("No winner to declare or data to display for Player 1.")
            if st.button("Go to the War Room", key='leave_from_player_1_stats_dashboard'):
                st.switch_page("pages/1War_Room.py")


        # st.dataframe(Player_1_Statistics)

    with tab3:
        st.subheader('Player 2 Data', divider='blue')

        if game_winner == 2:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} won the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
        elif game_winner == 1:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:black;'>Player 2 lost the Game after {rounds_total} rounds...</h4>", unsafe_allow_html=True)
        
        if not game_winner:
            # st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} Wins the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
            st.write("No winner to declare or data to display for Player 2.")
            if st.button("Go to the War Room", key='leave_from_player_2_stats_dashboard'):
                st.switch_page("pages/1War_Room.py")


        col1, col2, col3 = st.columns(3)
        # st.dataframe(Player_2_Statistics)
    





style_metric_cards(background_color='#FFF', border_size_px=2, border_color='#CCC', border_radius_px=15, border_left_color='#9AD8E1', box_shadow=True)