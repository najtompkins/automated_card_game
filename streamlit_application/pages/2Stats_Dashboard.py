import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import plotly.express as px


# Set page configuration with title and stats icon
st.set_page_config(page_title="Stats Dashboard'", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

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


    streak_statistics = pd.DataFrame()
    streak_statistics['Round Number'] = Game_Statistics['Round Number']
    streak_statistics['Round Winner'] = Game_Statistics['Round Winner']

    # Initialize tracking dictionaries
    streak_info = {
        1: {'max_streak': 0, 'current_streak': 0, 'start_round': None, 'best_rounds': []},
        2: {'max_streak': 0, 'current_streak': 0, 'start_round': None, 'best_rounds': []}
    }
    # Variables to track the current winner and current streak
    current_winner = None

    # Iterate over the DataFrame
    for index, row in streak_statistics.iterrows():
        winner = row['Round Winner']
        
        # Check if the winner is NaN or 0 before proceeding
        if pd.isna(winner) or winner == 0:
            if current_winner is not None:
                # Update the streak info if it was the longest and then reset
                info = streak_info[current_winner]
                if info['current_streak'] > info['max_streak']:
                    info['max_streak'] = info['current_streak']
                    info['best_rounds'] = [info['start_round'], row['Round Number'] - 1]
                streak_info[current_winner]['current_streak'] = 0
            current_winner = None  # Reset current winner
            continue  # Skip the rest of the loop

        if winner != current_winner:
            # If streak ends or winner changes
            if current_winner is not None:
                # Update the streak info if it was the longest
                info = streak_info[current_winner]
                if info['current_streak'] > info['max_streak']:
                    info['max_streak'] = info['current_streak']
                    info['best_rounds'] = [info['start_round'], row['Round Number'] - 1]
                # Reset the current streak
                info['current_streak'] = 0
            
            # This check ensures that only valid winners (1 or 2) initialize new streaks
            if winner in streak_info:
                current_winner = winner  # Update current winner
                # Initialize new streak
                streak_info[winner]['start_round'] = row['Round Number']
                streak_info[winner]['current_streak'] = 1
        else:
            # Continue the current streak
            streak_info[winner]['current_streak'] += 1


    # Final check for ongoing streak at the end of DataFrame
    for winner, info in streak_info.items():
        if info['current_streak'] > info['max_streak']:
            info['max_streak'] = info['current_streak']
            info['best_rounds'] = [info['start_round'], streak_statistics.iloc[-1]['Round Number']]
    streak_tuples = []
    # Output results
    for winner, info in streak_info.items():
        # st.write(f"Player {winner} had a maximum streak of {info['max_streak']} during rounds {info['best_rounds'][0]} and {info['best_rounds'][1]}")
        streak_tuples.append((winner, int(info['max_streak']), int(info['best_rounds'][0]), int(info['best_rounds'][1])))

    # Set text colors for markdown text
    if game_winner == 1:
        color = '#429EBD'
    elif game_winner == 2:
        color = '#F7AD19'
    else:
        # color is black
        color = '#000000'

    st.markdown("<h1 style='text-align:center;font-size:50px;'>Game Statistics</h1>", unsafe_allow_html=True)
    # st.write("Please pardon our dust! This page is currently under construction.")

    tab1, tab2, tab3 = st.tabs(["Game Data", "Player 1 Data", "Player 2 Data"])

    with tab1:
        st.subheader('Game Data', divider='gray')

        if game_winner == 1 or game_winner == 2:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} won the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
        
        if not game_winner:
            st.write("No winner to declare or data to display for the Game.")
            if st.button("Go to the War Room", key='leave_from_game_stats_dashboard'):
                st.switch_page("pages/1War_Room.py")

        row2_col1, row2_col2= st.columns(2)
        with row2_col1:
            if Player_1_Statistics['Player 1 Wars Won'].max() > Player_2_Statistics['Player 2 Wars Won'].max():
                most_wars = 'Player 1'
            else:
                most_wars = 'Player 2'
            st.metric(label="The Player Who Won the Most Wars:", value=most_wars)   
        with row2_col2:
            if Player_1_Statistics['Player 1 Rounds Won'].max() > Player_2_Statistics['Player 2 Rounds Won'].max():
                most_rounds = 'Player 1'
            else:
                most_rounds = 'Player 2'
            
            st.metric(label="The Player Who Won the Most Rounds:", value=most_rounds)     

        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.metric(label='During the Game There Were:', value=f"{Game_Statistics['Total Wars In Game'].iloc[-1]} Wars")
        with row1_col2:
            st.metric(label='Most Wars in a Single Round:', value=Game_Statistics['Total Wars In Round'].max())

        row4_col1, row4_col2 = st.columns(2)
        with row4_col1:
            st.metric(label='The Players Dealt', value=f"{Game_Statistics['Total Cards Dealt In Game'].iloc[-1]} Cards")
        with row4_col2:
            st.metric(label='The Players Played:', value=f"{int(Game_Statistics['Round Number'].iloc[-1])} Rounds")



        row3_col1, row3_col2 = st.columns(2)
        val1 = Game_Statistics['Total NonWar Cards Dealt In Game'].iloc[-1]
        val2 = Game_Statistics['Total War Cards Dealt In Game'].iloc[-1]
        val3 = Game_Statistics['Total Cards Dealt In Game'].iloc[-1]
        perc1 = (val1 / val3) * 100
        perc2 = (val2 / val3) * 100

        with row3_col1:
            st.metric(label="How Many Cards Dealt in Normal Play?", value=f"{Game_Statistics['Total NonWar Cards Dealt In Game'].iloc[-1]} Cards ({perc1:.1f}%)")
        with row3_col2:
            st.metric(label="How Many Cards Dealt During Wars?", value=f"{Game_Statistics['Total War Cards Dealt In Game'].iloc[-1]} Cards ({perc2:.1f}%)")

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
        

        row3_col1, row3_col2, row3_col3 = st.columns(3)
        with row3_col1:
            st.metric(label='Maximum cards held:', value=f"{Player_1_Statistics['Total Player 1 Cards'].max()} Cards", delta=f"{Player_1_Statistics['Total Player 1 Cards'].max() - Player_2_Statistics['Total Player 2 Cards'].max()} from {Player_2_Statistics['Total Player 2 Cards'].max()} (Pl.2)")
        with row3_col2:
            # Get the number of times Player_1_Statistics['Player 1 Ran Out of Cards'] is True
            st.metric(label="How many times was their hand depleted?", value=f"{(Player_1_Statistics['Player 1 Ran Out of Cards'] == True).sum()} Times", delta=f"{(Player_1_Statistics['Player 1 Ran Out of Cards'] == True).sum() - (Player_2_Statistics['Player 2 Ran Out of Cards'] == True).sum()} from {(Player_2_Statistics['Player 2 Ran Out of Cards'] == True).sum()} (Pl.2)")
        with row3_col3:
            st.metric(label="Cards dealt back into hand:", value=f"{Player_1_Statistics['Cards Dealt Back to Player 1'].sum()} Cards", delta=f"{Player_1_Statistics['Cards Dealt Back to Player 1'].sum() - Player_2_Statistics['Cards Dealt Back to Player 2'].sum()} from {Player_2_Statistics['Cards Dealt Back to Player 2'].sum()} (Pl.2)", delta_color="inverse")

        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            val1 = Player_1_Statistics['Player 1 Rounds Won'].max()
            val2 = Player_2_Statistics['Player 2 Rounds Won'].max()
            val3 = val1 + val2
            perc1 = (val1 / val3) * 100
            perc2 = (val2 / val3) * 100
            st.metric(label='How many rounds did Player 1 win?', value=f"{Player_1_Statistics['Player 1 Rounds Won'].max()} Rounds ({perc1:.1f}%)", delta=f"{(perc1-perc2):.1f}% from {perc2:.1f}% (Pl.2)")
        with row1_col2:
            val1 = Player_1_Statistics['Player 1 Wars Won'].max()
            val2 = Player_2_Statistics['Player 2 Wars Won'].max()
            val3 = val1 + val2
            perc1 = (val1 / val3) * 100
            perc2 = (val2 / val3) * 100            
            st.metric(label="How many wars did Player 1 win?", value=f'{Player_1_Statistics["Player 1 Wars Won"].max()} Wars ({perc1:.1f}%)', delta=f"{(perc1-perc2):.1f}% from {perc2:.1f}% (Pl. 2)")
        
        dropped_duplicates = Player_1_Statistics.drop_duplicates(subset=['Round Number'], keep='last')
        most_common_value_counts_card = dropped_duplicates['Player 1 Card'].value_counts()
        most_common_value = most_common_value_counts_card.index[0]
        occurrences_card = most_common_value_counts_card.iloc[0]
        second_most_common_value_counts_card = dropped_duplicates['Player 1 Card'].value_counts()
        second_most_common_value = second_most_common_value_counts_card.index[1]
        second_occurrences_card = second_most_common_value_counts_card.iloc[1]
        st.metric(label='What was their most common card?', value=f"{most_common_value} ({occurrences_card} Times)", delta=f"{second_most_common_value} ({second_occurrences_card} Times)")
        
        row2_col1, row2_col2,  = st.columns(2)
        with row2_col1:
            most_common_value_counts_card = dropped_duplicates['Player 1 Card Face'].value_counts()
            most_common_value = most_common_value_counts_card.index[0]
            occurrences_card = most_common_value_counts_card.iloc[0]
            second_most_common_value_counts_card = dropped_duplicates['Player 1 Card Face'].value_counts()
            second_most_common_value = second_most_common_value_counts_card.index[1]
            second_occurrences_card = second_most_common_value_counts_card.iloc[1]
            st.metric(label='What was their most common face?', value=f"{most_common_value} ({occurrences_card} Times)", delta=f"'{second_most_common_value}' ({second_occurrences_card} Times)")
        with row2_col2:
            most_common_value_counts_card = dropped_duplicates['Player 1 Card Suit'].value_counts()
            most_common_value = most_common_value_counts_card.index[0]
            occurrences_card = most_common_value_counts_card.iloc[0]
            second_most_common_value_counts_card = dropped_duplicates['Player 1 Card Suit'].value_counts()
            second_most_common_value = second_most_common_value_counts_card.index[1]
            second_occurrences_card = second_most_common_value_counts_card.iloc[1]
            st.metric(label="What was their most common suit?'", value=f"{most_common_value} ({occurrences_card} Times)", delta=f"'{second_most_common_value}' ({second_occurrences_card} Times)")


        # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
        try:
            Player_1_Card_Count = Player_1_Statistics['Total Player 1 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_1_Card_Count = 26
        try:
            Player_2_Card_Count = Player_2_Statistics['Total Player 2 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_2_Card_Count = 26
        style_metric_cards(background_color='#FFF', border_size_px=2, border_color='#CCC', border_radius_px=15, border_left_color=color, box_shadow=True)


    with tab3:
        st.subheader('Player 2 Data', divider='orange')

        if game_winner == 2:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:{color};'>Player {game_winner} won the Game after {rounds_total} rounds!</h4>", unsafe_allow_html=True)
        elif game_winner == 1:
            st.markdown(f"<h4 style='text-align:center;font-size:30px;color:gray;'>Player 2 lost the Game after {rounds_total} rounds.</h4>", unsafe_allow_html=True)
        
        if not game_winner:
            st.write("No winner to declare or data to display for Player 2.")
            if st.button("Go to the War Room", key='leave_from_player_2_stats_dashboard'):
                st.switch_page("pages/1War_Room.py")

        row3_col1, row3_col2, row3_col3 = st.columns(3)
        with row3_col1:
            st.metric(label='Maximum cards held:', value=f"{Player_2_Statistics['Total Player 2 Cards'].max()} Cards", delta=f"{Player_2_Statistics['Total Player 2 Cards'].max() - Player_1_Statistics['Total Player 1 Cards'].max()} from {Player_1_Statistics['Total Player 1 Cards'].max()} (Pl.1)")
        with row3_col2:
            st.metric(label="How many times was their hand depleted?", value=f"{(Player_2_Statistics['Player 2 Ran Out of Cards'] == True).sum()} Times", delta=f"{(Player_2_Statistics['Player 2 Ran Out of Cards'] == True).sum() - (Player_1_Statistics['Player 1 Ran Out of Cards'] == True).sum()} from {(Player_1_Statistics['Player 1 Ran Out of Cards'] == True).sum()} (Pl.1)" , delta_color="inverse")
        with row3_col3:
            st.metric(label="Cards dealt back into hand:", value=f"{Player_2_Statistics['Cards Dealt Back to Player 2'].sum()} Cards", delta=f"{Player_2_Statistics['Cards Dealt Back to Player 2'].sum() - Player_1_Statistics['Cards Dealt Back to Player 1'].sum()} from {Player_1_Statistics['Cards Dealt Back to Player 1'].sum()} (Pl.1)", delta_color="inverse")

        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            val1 = Player_2_Statistics['Player 2 Rounds Won'].max()
            val2 = Player_1_Statistics['Player 1 Rounds Won'].max()
            val3 = val1 + val2
            perc1 = (val1 / val3) * 100
            perc2 = (val2 / val3) * 100
            st.metric(label='How many rounds did Player 2 win?', value=f"{val1} Rounds ({perc1:.1f}%)", delta=f"{(perc1-perc2):.1f}% from {perc2:.1f}% (Pl.1)")
        with row1_col2:
            val1 = Player_2_Statistics['Player 2 Wars Won'].max()
            val2 = Player_1_Statistics['Player 1 Wars Won'].max()
            val3 = val1 + val2
            perc1 = (val1 / val3) * 100
            perc2 = (val2 / val3) * 100            
            st.metric(label="How many wars did Player 2 win?", value=f'{val1} Wars ({perc1:.1f}%)', delta=f"{(perc1-perc2):.1f}% from {perc2:.1f}% (Pl.1)")

        dropped_duplicates = Player_2_Statistics.drop_duplicates(subset=['Round Number'], keep='last')
        most_common_value_counts_card = dropped_duplicates['Player 2 Card'].value_counts()
        most_common_value = most_common_value_counts_card.index[0]
        occurrences_card = most_common_value_counts_card.iloc[0]
        second_most_common_value_counts_card = dropped_duplicates['Player 2 Card'].value_counts()
        second_most_common_value = second_most_common_value_counts_card.index[1]
        second_occurrences_card = second_most_common_value_counts_card.iloc[1]
        st.metric(label='What was their most common card?', value=f"{most_common_value} ({occurrences_card} Times)", delta=f"Second most commmon: '{second_most_common_value}' ({second_occurrences_card} Times)")

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            most_common_value_counts_card = dropped_duplicates['Player 2 Card Face'].value_counts()
            most_common_value = most_common_value_counts_card.index[0]
            occurrences_card = most_common_value_counts_card.iloc[0]
            second_most_common_value_counts_card = dropped_duplicates['Player 2 Card Face'].value_counts()
            second_most_common_value = second_most_common_value_counts_card.index[1]
            second_occurrences_card = second_most_common_value_counts_card.iloc[1]
            st.metric(label='What was their most common face?', value=f"{most_common_value} ({occurrences_card} Times)", delta=f"Second most common: '{second_most_common_value}' ({second_occurrences_card} Times)")
        with row2_col2:
            most_common_value_counts_card = dropped_duplicates['Player 2 Card Suit'].value_counts()
            most_common_value = most_common_value_counts_card.index[0]
            occurrences_card = most_common_value_counts_card.iloc[0]
            second_most_common_value_counts_card = dropped_duplicates['Player 2 Card Suit'].value_counts()
            second_most_common_value = second_most_common_value_counts_card.index[1]
            second_occurrences_card = second_most_common_value_counts_card.iloc[1]
            st.metric(label="What was their most common suit?'", value=f"{most_common_value} ({occurrences_card} Times)", delta=f"Second most common: '{second_most_common_value}' ({second_occurrences_card} Times)")

        # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
        try:
            Player_1_Card_Count = Player_1_Statistics['Total Player 1 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_1_Card_Count = 26
        try:
            Player_2_Card_Count = Player_2_Statistics['Total Player 2 Cards'].iloc[-1]
        except IndexError:  # Catching the case where the DataFrame is empty
            Player_2_Card_Count = 26
    

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
        # If Player 1 wins at the beginning of the game (current_winner == None) then set the current_winner to 1
        if (int(Card_Distributions['Total Player 1 Cards'].iloc[i]) > int(Card_Distributions['Total Player 2 Cards'].iloc[i])) and current_winner == None:
            current_winner = 1
        # If player 1 wins after player 2 has won, then set the current_winner to 1 and increase the times that the players have switched dominance
        elif (int(Card_Distributions['Total Player 1 Cards'].iloc[i]) > int(Card_Distributions['Total Player 2 Cards'].iloc[i])) and current_winner != 1:
            current_winner = 1
            players_switched += 1
        # If Player 2 wins at the beginning of the game (current_winner == None) then set the current_winner to 2
        elif (int(Card_Distributions['Total Player 2 Cards'].iloc[i]) > int(Card_Distributions['Total Player 1 Cards'].iloc[i])) and current_winner == None:
            current_winner = 2
        # If player 2 wins after player 1 has won, then set the current_winner to 2 and increase the times that the players have switched dominance
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
                    text=f"Max Player 1 Cards Held: {max_value_player1}", showarrow=True, arrowhead=4, arrowcolor="#429EBD", font=dict(color='black', size=12), ax=-60, ay=-40, borderwidth=2, bordercolor="#429EBD")
    fig_line.add_annotation(x=round_max_player2, y=max_value_player2, 
                    text=f"Max Player 2 Cards Held: {max_value_player2}", showarrow=True, arrowhead=4, arrowcolor="#F7AD19", font=dict(color='black', size=12), ax=-60, ay=-40, borderwidth=2, bordercolor="#F7AD19")

    fig_line.add_vrect(x0=streak_tuples[0][2], x1=streak_tuples[0][3], fillcolor="#429EBD", opacity=0.25, line_width=0)
    fig_line.add_annotation(x=(streak_tuples[0][2] + streak_tuples[0][3]) / 2, y=0.2, yref="paper",
                    text="Longest Player 1 Win Streak", showarrow=False, font=dict(color='black', size=12),
                    bgcolor="white", bordercolor="#429EBD", borderwidth=2, opacity=0.85)
    fig_line.add_vrect(x0=streak_tuples[1][2], x1=streak_tuples[1][3], fillcolor="#F7AD19", opacity=0.25, line_width=0)
    fig_line.add_annotation(x=(streak_tuples[1][2] + streak_tuples[1][3]) / 2, y=0.3, yref="paper",
                    text="Longest Player 2 Win Streak", showarrow=False, font=dict(color='black', size=12),
                    bgcolor="white", bordercolor="#F7AD19", borderwidth=2, opacity=0.85)

    fig_line.update_layout(legend=dict(x=0.5, xanchor="center", y=1.0, yanchor="bottom", orientation="h"), legend_title_text="")
    if players_switched > 1:
        st.markdown(f"<h4 style='text-align:center;font-size:28px;'>The Players switched dominance {players_switched} times.</h4>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h4 style='text-align:center;font-size:28px;'>The Players switched dominance {players_switched} time.</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # Add buttons to navigate to the War Data page
    button_col1, button_col2, button_col3= st.columns(3)


    with button_col1:
        with st.expander("Peek at the Game Data"):
            st.dataframe(Game_Statistics)
    with button_col2:
        with st.expander("Peek at the Player 1 Data"):
            st.dataframe(Player_1_Statistics)
        if st.button("See All of the Datasets", key='leave_from_player_1_stats_dashboard_after_game'):
            st.switch_page("pages/3War_Data.py")
    with button_col3:
        with st.expander("Peek at the Player 2 Data"):
            st.dataframe(Player_2_Statistics)
    style_metric_cards(background_color='#FFF', border_size_px=2, border_color='#CCC', border_radius_px=15, border_left_color=color, box_shadow=True)