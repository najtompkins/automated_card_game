import pydealer as pyd # For card/stack/deck classes
from time import sleep # For optional delay between rounds
import pandas as pd # For dataframes
import streamlit as st # For Streamlit application framework
import plotly.graph_objects as go # For plotting graphs
import plotly.express as px
import warnings # For suppressing warnings in the terminal

# """
# This War Room page sets up the needed functions to simulate the game of war, then builds the streamlit page which allows the user to interact with and 
# simulate the game for themselves. Data is generated throughout the many funcitons in this page and then added to the Game_Statistics, Player_1_Statistics, and Player_2_Statistics Pandas Dataframes.
# """

# Set page configuration with title and burst icon
st.set_page_config(page_title="War Room", page_icon="💥", layout="centered")

# Suppress FutureWarnings so the terminal is not flooded with warnings during a simulation
warnings.simplefilter(action='ignore', category=FutureWarning)

# Raises error when player's hand is empty
class NoCards(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def create_global_variables():
    # Initialize variables if they don't already exist in the session state
    # Some variables needed at one point, but unneeded now. Kept in case.

    # Establish dictionary of global variables needed to report on and simulate the game.
    variables = {
    # Game data generation variables
        'Data_Round_Number': 0,
        'Data_Round_Winner': 0,
        'Data_War_Number': 0,
        'Local_War_Count': 0,
        'Data_War_Winner': None,
        # 'Data_Total_Cards_In_Play': 0,
        # 'Data_Total_War_Cards_Dealt_In_Round': 0,
        # 'Data_Total_NonWar_Cards_Dealt_In_Round': 0,
        # 'Data_Total_Cards_Dealt_In_Round': 0,
        'Data_War_Happened': False,
        'Data_Total_Wars_In_Round': 0,
        # 'Data_Total_War_Cards_Dealt_In_Game': 0,
        # 'Data_Total_NonWar_Cards_Dealt_In_Game': 0,
        # 'Data_Total_Cards_Dealt_In_Game': 0,
        'Data_Total_Wars_In_Game': 0,
        'Result_Value': None, # Reports a variable value, mostly for debugging.
    # Player 1 data generation variables
        'Data_Player_1_Card': None, # Player 1 Data
        'Data_Player_1_Card_Face': "",
        'Data_Player_1_Card_Suit': "",
        'Data_Player_1_Card_Value': 0,
        'Data_Player_1_Hand_Size': 0,
        'Data_Player_1_War_Stack_Size': 0,
        'Data_Player_1_Discard_Pile_Size': 0,
        'Data_Total_Player_1_Cards': 0,
        'Data_Total_Player_1_War_Cards_Dealt_In_Round': 0,
        'Data_Total_Player_1_NonWar_Cards_Dealt_In_Round': 0,
        # 'Data_Total_Player_1_Cards_Dealt_In_Round': 0,
        'Data_Total_Player_1_War_Cards_Dealt_In_Game': 0,
        'Data_Total_Player_1_NonWar_Cards_Dealt_In_Game': 0,
        # 'Data_Total_Player_1_Cards_Dealt_In_Game': 0,
        'Data_Player_1_Ran_Out_of_Cards': False,
        'Data_Cards_Dealt_Back_to_Player_1': 0,
        'Data_Player_1_Rounds_Won': 0,
        'Data_Player_1_Wars_Won': 0,
    # Player 2 data generation variables
        'Data_Player_2_Card': None,
        'Data_Player_2_Card_Face': "",
        'Data_Player_2_Card_Suit': "",
        'Data_Player_2_Card_Value': 0,
        'Data_Player_2_Hand_Size': 0,
        'Data_Player_2_War_Stack_Size': 0,
        'Data_Player_2_Discard_Pile_Size': 0,
        'Data_Total_Player_2_Cards': 0,
        'Data_Total_Player_2_War_Cards_Dealt_In_Round': 0,
        'Data_Total_Player_2_NonWar_Cards_Dealt_In_Round': 0,
        # 'Data_Total_Player_2_Cards_Dealt_In_Round': 0,
        'Data_Total_Player_2_War_Cards_Dealt_In_Game': 0,
        'Data_Total_Player_2_NonWar_Cards_Dealt_In_Game': 0,
        # 'Data_Total_Player_2_Cards_Dealt_In_Game': 0,
        'Data_Player_2_Ran_Out_of_Cards': False,
        'Data_Cards_Dealt_Back_to_Player_2': 0,
        'Data_Player_2_Rounds_Won': 0,
        'Data_Player_2_Wars_Won': 0,
    # Dataframe variables
        'Game_Statistics': None,
        'Player_1_Statistics': None,
        'Player_2_Statistics': None,
    # Other variables needed for the game
        'Is_Dealing_In_War': False,
        'player_1_hand': None,
        'player_1_war': None,
        'player_1_discard': None,
        'player_2_hand': None,
        'player_2_war': None,
        'player_2_discard': None,
        'result': None,
        'playing_game_increment': 0
    }

    # Iterate through the global variables needed and add those to the Streamlit's session_state
    for key, initial_value in variables.items():
        if key not in st.session_state:
            st.session_state[key] = initial_value

# Deals card(s) to specified player's war_stack from the top (index -1) of the player's hand
# Returns error code 10 if player's hand is empty. None if deal was successful.
def deal(player_hand, player_war_stack, number_of_cards):
    # player_hand:      pyd.Stack() object.
    # player_war_stack: pyd.Stack() object.
    # number_of_cards:  Integer.
    
    # Returns error code 10 if player's hand is empty

    # Try to deal, catch error if player's hand is empty
    try:
        if len(player_hand) == 0:
            raise NoCards("Player's hand is empty")
    
    # If player's hand is not empty, deal the card(s) to the war_stack
        elif len(player_hand) > 0:

        # Get the top card from the player's hand and place it in the war stack
            temp_card = player_hand.deal(number_of_cards)
            player_war_stack.add(temp_card)
            
        # Pulls in and updates global variables based on which player_hand was passed through
            # Update global variables for Player 1
            if player_hand.name == "Player 1's Hand":
                st.session_state.Data_Player_1_Card = st.session_state.player_1_war[-1]
                st.session_state.Data_Player_1_Card_Face = st.session_state.player_1_war[-1].value
                st.session_state.Data_Player_1_Card_Suit = st.session_state.player_1_war[-1].suit
                st.session_state.Data_Player_1_Card_Value = get_face_value(st.session_state.player_1_war[-1])

            # Increase card counters by an increment of 1
                # During a war
                if st.session_state.Data_War_Happened == True:
                    # Cards in game
                    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game += 1
                    # Cards in round
                    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round += 1

                # During a non-war round
                elif st.session_state.Data_War_Happened == False:
                    # Cards in game
                    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game += 1
                    # Cards in round
                    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round += 1

            # Update global variables for Player 2
            elif player_hand.name == "Player 2's Hand":
                st.session_state.Data_Player_2_Card = st.session_state.player_2_war[-1]
                st.session_state.Data_Player_2_Card_Face =  st.session_state.player_2_war[-1].value
                st.session_state.Data_Player_2_Card_Suit = st.session_state.player_2_war[-1].suit
                st.session_state.Data_Player_2_Card_Value = get_face_value(st.session_state.player_2_war[-1])

            # Increase card counters by an increment of 1
                if st.session_state.Data_War_Happened == True:
                    # Cards in game
                    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game += 1
                    # Cards in round
                    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round += 1
                elif st.session_state.Data_War_Happened == False:
                    # Cards in game
                    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game += 1
                    # Cards in round
                    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round += 1

    # Return error code 10 if player's hand is empty
    except NoCards as e:
        return 10

# Function to get the numerical value of a card object that is passed in so that it can be compared in the compare() function
def get_face_value(card):
    # card: pyd.Card() object

    # Returns the numerical value of the card

    # Dictionary of card face values
    card_face_values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "Jack": 11, "Queen": 12, "King": 13, "Ace": 14
    }

    # Return the numerical value of the card so that it can be compared based on this value
    return card_face_values[card.value]

# Compares the top cards in the player's war_stacks.
def compare():

    # Returns 1 if Player 1's card is greater
    # Returns 2 if Player 2's card is greater
    # Returns 0 if both cards have the same face value
    # Returns error code 10 if either player's hand is empty

    # Assign the top cards in the war stack to variables.
    top_card_1 = st.session_state.player_1_war[-1]
    top_card_2 = st.session_state.player_2_war[-1]

    # Compare the face values of the top cards
    # If Player 1's card is greater, return 1
    if get_face_value(top_card_1) > get_face_value(top_card_2):
        return 1
    # If Player 2's card is greater, return 2
    elif get_face_value(top_card_1) < get_face_value(top_card_2):
        return 2
    # If both cards have the same face value, return 0 (war)
    elif get_face_value(top_card_1) == get_face_value(top_card_2):
        return 0
    
    # Further else statements only show when something went wrong. They should never print in a functioning game.
    # if something went wrong, return the 'someone is out of cards' error code
    else:
        return 10

# Moves all cards from the both player's war stacks into the their respective discard hands
# Based on result value (0, 1, or 2) which is passed into function after comparison function returns a verdict.
def reset_war_stacks(result):
    # result: Integer value of 0, 1, or 2.
        # 0 = war
        # 1 = player 1's card won
        # 2 = player 2's card won

    # Returns None if war stacks are successfully emptied

    # If Player 1 won the round, then move all cards from both player's war stacks into player 1's discard stack
    if st.session_state.result == 1:

        # For every card in player 1's war stack, move it to player 1's discard stack
        for i in range(len(st.session_state.player_1_war)):
            temp_card = st.session_state.player_1_war.deal(1) # deal 1 card
            st.session_state.player_1_discard.add(temp_card) # add to player 1's discard

        # For every card in player 2's war stack, move it to player 2's discard stack
        for i in range(len(st.session_state.player_2_war)):
            temp_card = st.session_state.player_2_war.deal(1) # deal 1 card
            st.session_state.player_1_discard.add(temp_card) # add to player 1's discard
        
        # Change global variables
        st.session_state.Data_Round_Winner = 1 # Player 1 won the round
        st.session_state.Data_Player_1_Rounds_Won += 1 # Increase the total number of times that player 1 won a round
    
    elif st.session_state.result == 2:

        # For every card in player 1's war stack, move it to player 2's discard stack
        for i in range(len(st.session_state.player_1_war)):
            temp_card = st.session_state.player_1_war.deal(1) # deal 1 card
            st.session_state.player_2_discard.add(temp_card) # add to player 2's discard

        # For every card in player 2's war stack, move it to player 2's discard stack
        for i in range(len(st.session_state.player_2_war)):
            temp_card = st.session_state.player_2_war.deal(1) # deal 1 card
            st.session_state.player_2_discard.add(temp_card) # add to player 2's discard
        
        # Change global variables
        st.session_state.Data_Round_Winner = 2 # Player 2 won the round
        st.session_state.Data_Player_2_Rounds_Won += 1 # Increase the total number of times that player 2 won a round

    # Further else statements only show when something went wrong. They should never print in a functioning game.
    elif st.session_state.result == 10:
        print("Cannot reset stacks when comparison errors (value 10) are passed into reset function")
    
    elif st.session_state.result == 0:
        print("Hey there's a war going on! Cannot reset the stacks right now!")

    else: 
        print("Something went wrong when resetting the stacks.")

# Empties discard pile of specified player into hand of specified player.
def empty_discard_pile(player_hand, player_discard_pile):
    # player_hand:          pyd.Stack() object.
    # player_discard_pile:  pyd.Stack() object.

    # Returns error code 10 if player's discard pile is empty
    # Returns None if discard pile is successfully emptied into the player's hand

    # Check if the discard pile is empty
    if len(player_discard_pile) == 0:
        return 10
    
    # Empty discard pile into player hand
    elif len(player_discard_pile) > 0:

        # For every card in player's discard pile, move it to player's hand
        for card in player_discard_pile:
            temp_card = player_discard_pile.deal(1) # deal 1 card
            player_hand.add(temp_card) # add to player's hand

            # Change global variables for reporting round data
            # Player 1 reporting
            if player_discard_pile.name == "Player 1's Discard Pile":
                st.session_state.Data_Player_1_Ran_Out_of_Cards = True # Player 1 ran out of cards
                st.session_state.Data_Cards_Dealt_Back_to_Player_1 += 1 # Increase number of cards dealt back to player 1

            # Player 2 reporting
            elif player_discard_pile.name == "Player 2's Discard Pile":
                st.session_state.Data_Player_2_Ran_Out_of_Cards = True # Player 2 ran out of cards
                st.session_state.Data_Cards_Dealt_Back_to_Player_2 += 1 # Increase number of cards dealt back to player 2

    # Shuffle the player's hand once all discards have been returned to the player
    player_hand.shuffle()

# Performs final check for winner returning Boolean value.
def check_for_winner(player_hand, player_war_stack, player_discard):
    # player_hand:          pyd.Stack() object.
    # player_war_stack:     pyd.Stack() object.
    # player_discard:       pyd.Stack() object.

    # Returns True if all pyd.Stack() objects passed in are empty.

    # Check if all stacks are empty
    if ((len(player_hand)) + (len(player_war_stack)) + (len(player_discard))) == 0:
        # The game has ended
        return True
    else:
        # The game has not ended
        return False

# Creates three empty dataframes for use in game/round data reporting.
def create_game_dataframes():

    # Create dataframe columns. Should be self-explanatory. Added comments for those that aren't as clear.

    # Game Data dataframe columns
    Column_Names_Game_Data = [
        "Round Number",
        "Round Winner",
        "War Number", 
        "War Winner",
        "Total Cards In Play",
        "Total War Cards Dealt In Round",
        "Total NonWar Cards Dealt In Round",
        "Total Cards Dealt In Round",
        "War Happened",
        "Total Wars In Round",
        "Total War Cards Dealt In Game",
        "Total NonWar Cards Dealt In Game",
        "Total Cards Dealt In Game",
        "Total Wars In Game",
        "Result Value"] # Reports a variable value, mostly for debugging

    # Player 1 Data dataframe columns
    Column_Names_Player_1_Data = [
        "Round Number",
        "Player 1 Card", # Full player card string
        "Player 1 Card Face",
        "Player 1 Card Suit",
        "Player 1 Card Value", # Numerical value of card derived from face value using the get_face_value() function
        "Player 1 Hand Size",
        "Player 1 War Stack Size",
        "Player 1 Discard Pile Size",
        "Total Player 1 Cards",
        "Total Player 1 War Cards Dealt In Round",
        "Total Player 1 NonWar Cards Dealt In Round",
        "Total Player 1 Cards Dealt In Round",
        "Total Player 1 War Cards Dealt In Game",
        "Total Player 1 NonWar Cards Dealt In Game",
        "Total Player 1 Cards Dealt In Game",
        "Player 1 Ran Out of Cards",
        "Cards Dealt Back to Player 1",
        "Player 1 Rounds Won",
        "Player 1 Wars Won"]

    # Player 2 Data dataframe columns
    Column_Names_Player_2_Data = [
        "Round Number",
        "Player 2 Card", # Full player card string
        "Player 2 Card Face",
        "Player 2 Card Suit",
        "Player 2 Card Value", # Numerical value of card derived from face value using the get_face_value() function
        "Player 2 Hand Size",
        "Player 2 War Stack Size",
        "Player 2 Discard Pile Size",
        "Total Player 2 Cards",
        "Total Player 2 War Cards Dealt In Round",
        "Total Player 2 NonWar Cards Dealt In Round",
        "Total Player 2 Cards Dealt In Round",
        "Total Player 2 War Cards Dealt In Game",
        "Total Player 2 NonWar Cards Dealt In Game",
        "Total Player 2 Cards Dealt In Game",
        "Player 2 Ran Out of Cards",
        "Cards Dealt Back to Player 2",
        "Player 2 Rounds Won",
        "Player 2 Wars Won"]

    # Create dataframes that are globally available in the streamlit application, and have one row of starting data per column

    # Create the Game_Statistics dataframe
    st.session_state.Game_Statistics = pd.DataFrame(columns=Column_Names_Game_Data)

    # Create the Player_1_Statistics dataframe
    st.session_state.Player_1_Statistics = pd.DataFrame(columns=Column_Names_Player_1_Data)

    # Create the Player_2_Statistics dataframe
    st.session_state.Player_2_Statistics = pd.DataFrame(columns=Column_Names_Player_2_Data)

# Reports the round data and adds that to the dataframe passed in
def report_round_data(Data_DF):
    # Data_DF: Pandas DataFrame object

    # Returns None.

    # Pre-process certain variables before reporting properly begins
    # Assign the lengths of all Player 1's pyd.Stack() objects to global variables
    st.session_state.Data_Player_1_Hand_Size = len(st.session_state.player_1_hand)
    st.session_state.Data_Player_1_Discard_Pile_Size = len(st.session_state.player_1_discard)
    st.session_state.Data_Player_1_War_Stack_Size = len(st.session_state.player_1_war)
    st.session_state.Data_Total_Player_1_Cards = len(st.session_state.player_1_hand) + len(st.session_state.player_1_war) + len(st.session_state.player_1_discard)

    # Assign the lengths of all Player 2's pyd.Stack() objects to global variables
    st.session_state.Data_Player_2_Hand_Size = len(st.session_state.player_2_hand)
    st.session_state.Data_Player_2_Discard_Pile_Size = len(st.session_state.player_2_discard)
    st.session_state.Data_Player_2_War_Stack_Size = len(st.session_state.player_2_war)
    st.session_state.Data_Total_Player_2_Cards = len(st.session_state.player_2_hand) + len(st.session_state.player_2_war) + len(st.session_state.player_2_discard)

    # Assign the total number of cards in play to global variable
    Data_Total_Cards_In_Play = len(st.session_state.player_1_hand) + len(st.session_state.player_1_war) + len(st.session_state.player_1_discard) + len(st.session_state.player_2_hand) + len(st.session_state.player_2_war) + len(st.session_state.player_2_discard)

    # leftover code. refactoring may remove these without issue. or not.
    global Data_Total_Player_1_Cards_Dealt_In_Round
    global Data_Total_Player_1_Cards_Dealt_In_Game
    global Data_Total_Player_2_Cards_Dealt_In_Round
    global Data_Total_Player_2_Cards_Dealt_In_Game

    # Assign the total number of cards dealt in the rounds and game (aggregate) to global variables
    Data_Total_Player_1_Cards_Dealt_In_Round = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
    Data_Total_Player_1_Cards_Dealt_In_Game = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
    Data_Total_Player_2_Cards_Dealt_In_Round = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
    Data_Total_Player_2_Cards_Dealt_In_Game = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game

    # Report the round and game data to the Game_Statistics dataframe
    if Data_DF is st.session_state.Game_Statistics:
        
        # Get the current dataframe
        df = st.session_state.Game_Statistics

        # Generate an empty row of data at the last index of the dataframe
        new_row_index = len(df)
        df.loc[new_row_index] = pd.NA

        # Report the round data in a non-war context (End-of-the-round)
        if st.session_state.Is_Dealing_In_War == False:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            df.at[new_row_index, "Round Winner"] = st.session_state.Data_Round_Winner
            if st.session_state.Local_War_Count > 0:
                df.at[new_row_index, "War Number"] = st.session_state.Data_War_Number
            else:
                df.at[new_row_index, "War Number"] = None
            df.at[new_row_index, "War Winner"] = st.session_state.Data_War_Winner
            df.at[new_row_index, "Total Cards In Play"] = Data_Total_Cards_In_Play
            df.at[new_row_index, "Total War Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Cards Dealt In Round"] = Data_Total_Player_1_Cards_Dealt_In_Round + Data_Total_Player_2_Cards_Dealt_In_Round
            df.at[new_row_index, "War Happened"] = st.session_state.Data_War_Happened
            df.at[new_row_index, "Total Wars In Round"] = st.session_state.Data_Total_Wars_In_Round
            df.at[new_row_index, "Total War Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Cards Dealt In Game"] = Data_Total_Player_1_Cards_Dealt_In_Game + Data_Total_Player_2_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Wars In Game"] = st.session_state.Data_Total_Wars_In_Game
            df.at[new_row_index, "Result Value"] = st.session_state.Result_Value

        # Report the round data in a war context (Reporting each deal during a war, not just at the end of the round)
        elif st.session_state.Is_Dealing_In_War == True:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number

            df.at[new_row_index, "War Number"] = st.session_state.Data_War_Number + 1

            df.at[new_row_index, "Total Cards In Play"] = Data_Total_Cards_In_Play
            df.at[new_row_index, "Total War Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Cards Dealt In Round"] = Data_Total_Player_1_Cards_Dealt_In_Round + Data_Total_Player_2_Cards_Dealt_In_Round
            df.at[new_row_index, "War Happened"] = st.session_state.Data_War_Happened
            df.at[new_row_index, "Total Wars In Round"] = st.session_state.Data_Total_Wars_In_Round
            df.at[new_row_index, "Total War Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Cards Dealt In Game"] = Data_Total_Player_1_Cards_Dealt_In_Game + Data_Total_Player_2_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Wars In Game"] = st.session_state.Data_Total_Wars_In_Game + 1

    # Report the round and game data to the Player_1_Statistics dataframe
    elif Data_DF is st.session_state.Player_1_Statistics:
        
        # Get the current dataframe
        df = st.session_state.Player_1_Statistics

        # Generate an empty row of data at the last index of the dataframe
        new_row_index = len(df)
        df.loc[new_row_index] = pd.NA

        # Report the round data in a non-war context (End-of-the-round)
        if st.session_state.Is_Dealing_In_War == False:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            df.at[new_row_index, "Player 1 Card"] = st.session_state.Data_Player_1_Card
            df.at[new_row_index, "Player 1 Card Face"] = st.session_state.Data_Player_1_Card_Face
            df.at[new_row_index, "Player 1 Card Suit"] = st.session_state.Data_Player_1_Card_Suit
            df.at[new_row_index, "Player 1 Card Value"] = st.session_state.Data_Player_1_Card_Value
            df.at[new_row_index, "Player 1 Hand Size"] = st.session_state.Data_Player_1_Hand_Size
            df.at[new_row_index, "Player 1 War Stack Size"] = st.session_state.Data_Player_1_War_Stack_Size
            df.at[new_row_index, "Player 1 Discard Pile Size"] = st.session_state.Data_Player_1_Discard_Pile_Size
            df.at[new_row_index, "Total Player 1 Cards"] = st.session_state.Data_Total_Player_1_Cards
            df.at[new_row_index, "Total Player 1 War Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 Cards Dealt In Round"] = Data_Total_Player_1_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 War Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 1 NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 1 Cards Dealt In Game"] = Data_Total_Player_1_Cards_Dealt_In_Game
            df.at[new_row_index, "Player 1 Ran Out of Cards"] = st.session_state.Data_Player_1_Ran_Out_of_Cards
            df.at[new_row_index, "Cards Dealt Back to Player 1"] = st.session_state.Data_Cards_Dealt_Back_to_Player_1
            df.at[new_row_index, "Player 1 Rounds Won"] = st.session_state.Data_Player_1_Rounds_Won
            df.at[new_row_index, "Player 1 Wars Won"] = st.session_state.Data_Player_1_Wars_Won
        
        # Report the round data in a war context
        if st.session_state.Is_Dealing_In_War == True:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            df.at[new_row_index, "Player 1 Card"] = st.session_state.Data_Player_1_Card
            df.at[new_row_index, "Player 1 Card Face"] = st.session_state.Data_Player_1_Card_Face
            df.at[new_row_index, "Player 1 Card Suit"] = st.session_state.Data_Player_1_Card_Suit
            df.at[new_row_index, "Player 1 Card Value"] = st.session_state.Data_Player_1_Card_Value
            df.at[new_row_index, "Player 1 Hand Size"] = st.session_state.Data_Player_1_Hand_Size
            df.at[new_row_index, "Player 1 War Stack Size"] = st.session_state.Data_Player_1_War_Stack_Size
            df.at[new_row_index, "Player 1 Discard Pile Size"] = st.session_state.Data_Player_1_Discard_Pile_Size
            df.at[new_row_index, "Total Player 1 Cards"] = st.session_state.Data_Total_Player_1_Cards
            df.at[new_row_index, "Total Player 1 War Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 Cards Dealt In Round"] = Data_Total_Player_1_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 1 War Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 1 NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 1 Cards Dealt In Game"] = Data_Total_Player_1_Cards_Dealt_In_Game
            df.at[new_row_index, "Player 1 Ran Out of Cards"] = st.session_state.Data_Player_1_Ran_Out_of_Cards
            df.at[new_row_index, "Cards Dealt Back to Player 1"] = st.session_state.Data_Cards_Dealt_Back_to_Player_1
            df.at[new_row_index, "Player 1 Rounds Won"] = st.session_state.Data_Player_1_Rounds_Won
            df.at[new_row_index, "Player 1 Wars Won"] = st.session_state.Data_Player_1_Wars_Won
        
    # Report the round and game data to the Player_1_Statistics dataframe
    elif Data_DF is st.session_state.Player_2_Statistics:

        # Get the current dataframe
        df = st.session_state.Player_2_Statistics

        # Generate an empty row of data at the last index of the dataframe
        new_row_index = len(df)
        df.loc[new_row_index] = pd.NA

        # Report the round data in a non-war context (End-of-the-round)
        if st.session_state.Is_Dealing_In_War == False:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            df.at[new_row_index, "Player 2 Card"] = st.session_state.Data_Player_2_Card
            df.at[new_row_index, "Player 2 Card Face"] = st.session_state.Data_Player_2_Card_Face
            df.at[new_row_index, "Player 2 Card Suit"] = st.session_state.Data_Player_2_Card_Suit
            df.at[new_row_index, "Player 2 Card Value"] = st.session_state.Data_Player_2_Card_Value
            df.at[new_row_index, "Player 2 Hand Size"] = st.session_state.Data_Player_2_Hand_Size
            df.at[new_row_index, "Player 2 War Stack Size"] = st.session_state.Data_Player_2_War_Stack_Size
            df.at[new_row_index, "Player 2 Discard Pile Size"] = st.session_state.Data_Player_2_Discard_Pile_Size
            df.at[new_row_index, "Total Player 2 Cards"] = st.session_state.Data_Total_Player_2_Cards
            df.at[new_row_index, "Total Player 2 War Cards Dealt In Round"] = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 Cards Dealt In Round"] = Data_Total_Player_2_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 War Cards Dealt In Game"] = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 2 NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 2 Cards Dealt In Game"] = Data_Total_Player_2_Cards_Dealt_In_Game
            df.at[new_row_index, "Player 2 Ran Out of Cards"] = st.session_state.Data_Player_2_Ran_Out_of_Cards
            df.at[new_row_index, "Cards Dealt Back to Player 2"] = st.session_state.Data_Cards_Dealt_Back_to_Player_2
            df.at[new_row_index, "Player 2 Rounds Won"] = st.session_state.Data_Player_2_Rounds_Won
            df.at[new_row_index, "Player 2 Wars Won"] = st.session_state.Data_Player_2_Wars_Won
        
        # Report the round data in a war context
        elif st.session_state.Is_Dealing_In_War == True:
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            df.at[new_row_index, "Player 2 Card"] = st.session_state.Data_Player_2_Card
            df.at[new_row_index, "Player 2 Card Face"] = st.session_state.Data_Player_2_Card_Face
            df.at[new_row_index, "Player 2 Card Suit"] = st.session_state.Data_Player_2_Card_Suit
            df.at[new_row_index, "Player 2 Card Value"] = st.session_state.Data_Player_2_Card_Value
            df.at[new_row_index, "Player 2 Hand Size"] = st.session_state.Data_Player_2_Hand_Size
            df.at[new_row_index, "Player 2 War Stack Size"] = st.session_state.Data_Player_2_War_Stack_Size
            df.at[new_row_index, "Player 2 Discard Pile Size"] = st.session_state.Data_Player_2_Discard_Pile_Size
            df.at[new_row_index, "Total Player 2 Cards"] = st.session_state.Data_Total_Player_2_Cards
            df.at[new_row_index, "Total Player 2 War Cards Dealt In Round"] = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 NonWar Cards Dealt In Round"] = st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 Cards Dealt In Round"] = Data_Total_Player_2_Cards_Dealt_In_Round
            df.at[new_row_index, "Total Player 2 War Cards Dealt In Game"] = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 2 NonWar Cards Dealt In Game"] = st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
            df.at[new_row_index, "Total Player 2 Cards Dealt In Game"] = Data_Total_Player_2_Cards_Dealt_In_Game
            df.at[new_row_index, "Player 2 Ran Out of Cards"] = st.session_state.Data_Player_2_Ran_Out_of_Cards
            df.at[new_row_index, "Cards Dealt Back to Player 2"] = st.session_state.Data_Cards_Dealt_Back_to_Player_2
            df.at[new_row_index, "Player 2 Rounds Won"] = st.session_state.Data_Player_2_Rounds_Won
            df.at[new_row_index, "Player 2 Wars Won"] = st.session_state.Data_Player_2_Wars_Won

# Sets up the game environment (pyd.Deck(), pyd.Stack(), objects, shuffles, deals to players, etc.)
def set_up_game_environment():
    # Set up the game environment using global variables

    # Assign the global variables and their starting values
    create_global_variables()

    # Create the game dataframes as global variables (based on the global variables)
    create_game_dataframes()

    # Create the stacks and give them names

    # Create the starting deck and shuffle the starting deck
    starting_deck = pyd.Deck()
    starting_deck.shuffle()

    # Deal the cards to variables
    player_1_cards = starting_deck.deal(26)
    player_2_cards = starting_deck.deal(26)

    # Create player 1's starting hand
    st.session_state.player_1_hand = pyd.Stack()
    st.session_state.player_1_hand.add(player_1_cards)
    # Create player 2's starting hand
    st.session_state.player_2_hand = pyd.Stack()
    st.session_state.player_2_hand.add(player_2_cards)

    # Create player 1's discard pile
    st.session_state.player_1_discard = pyd.Stack()
    # Create player 2's discard pile
    st.session_state.player_2_discard = pyd.Stack()

    # Create player 1's war stack
    st.session_state.player_1_war = pyd.Stack()
    # Create player 2's war stack
    st.session_state.player_2_war = pyd.Stack()

    # Naming the Stacks for better output readability
    st.session_state.player_1_hand.name = "Player 1's Hand"
    st.session_state.player_1_discard.name = "Player 1's Discard Pile"
    st.session_state.player_1_war.name = "Player 1's War Stack"

    st.session_state.player_2_hand.name = "Player 2's Hand"
    st.session_state.player_2_discard.name = "Player 2's Discard Pile"
    st.session_state.player_2_war.name = "Player 2's War Stack"

# Resets the non-aggregate global variables after each round
def reset_non_aggregate_global_variables():

    # Reset the war winner
    st.session_state.Data_War_Winner = None

    # Reset the round winner
    st.session_state.Data_Round_Winner = None

    # Reset the local war count
    st.session_state.Local_War_Count = 0

    # Reset the war happened
    st.session_state.Data_War_Happened = False

    # Reset the number of cards dealt to player 1 in the round, if they ran out of cards, and the number of cards dealt back to player 1 if so
    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round = 0
    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round = 0
    global Data_Total_Player_1_Cards_Dealt_In_Round # Refactor this
    Data_Total_Player_1_Cards_Dealt_In_Round = 0

    st.session_state.Data_Player_1_Ran_Out_of_Cards = False
    st.session_state.Data_Cards_Dealt_Back_to_Player_1 = 0

    # Reset the number of cards dealt to player 2 in the round, if they ran out of cards, and the number of cards dealt back to player 2 if so 
    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round = 0
    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round = 0
    global Data_Total_Player_2_Cards_Dealt_In_Round # Refactor this
    Data_Total_Player_2_Cards_Dealt_In_Round = 0

    st.session_state.Data_Player_2_Ran_Out_of_Cards = False
    st.session_state.Data_Cards_Dealt_Back_to_Player_2 = 0

    # Reset the number of wars that occured in the round
    st.session_state.Data_Total_Wars_In_Round = 0

    # Reset the result value that is passed into the final reset_war_stacks() function
    st.session_state.result = None

# Only run in play_with_increments() function! Simulates the game of War, sleeping for the specified amount of time between each round
def play_war(sleepy_time = 0.2):
    # sleepy_time: Integer: number of seconds to sleep between each round

    while st.session_state.playing_game_increment > 0:
        # label the round
        st.session_state.Data_Round_Number = int(st.session_state.Data_Round_Number) + 1
        war_result = None
        st.session_state.Local_War_Count = 0
        # print(f"Round {st.session_state.Data_Round_Number}")
        # print("\/\/\/\/\/\/\/\/\/\/\/\/\/")
        
        # deal the cards
        deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)
        # print(f'The result for Deal 1 is: ({deal_1_result}) ')
        deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)
        # print(f'The result for Deal 2 is: ({deal_2_result}) ')
        
        # test the error result, if it is None (no error) then compare the cards
        
        # Check if both hands are empty
        if deal_1_result == 10 and deal_2_result == 10:

            discard_result_1 = empty_discard_pile(st.session_state.player_1_hand, st.session_state.player_1_discard)
            discard_result_2 = empty_discard_pile(st.session_state.player_2_hand, st.session_state.player_2_discard)
            if discard_result_1 == 10:
                # print("Player 2 Wins")
                break
            elif discard_result_2 == 10:
                # print("Player 1 Wins")
                break
            elif discard_result_1 == None and discard_result_2 == None:
                deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)
                deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)

            elif discard_result_1 == None or discard_result_2 == None:
                # print("Something went wrong. Both players ran out of cards, were dealt back their discards, but did not continue.")
                break
            else:
                # print("Something went wrong. Both players ran out of cards, but did not continue.")
                break

        # Check if Player 1 is out of cards but not Player 2
        elif deal_1_result == 10 and deal_2_result == None:
            discard_result = empty_discard_pile(st.session_state.player_1_hand, st.session_state.player_1_discard)
            if discard_result == 10:
                print("Player 2 Wins")
                break
            elif discard_result == None:
                deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)

        # Check if Player 2 is out of cards but not Player 1
        elif deal_2_result == 10 and deal_1_result == None:
            discard_result = empty_discard_pile(st.session_state.player_2_hand, st.session_state.player_2_discard)
            if discard_result == 10:
                print("Player 1 Wins")
                break
            elif discard_result == None:
                deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)
        else:
            print("Something went wrong when re-dealing after players were found without cards.")

        # Compare the cards
        if deal_1_result == None and deal_2_result == None:
            st.session_state.result = compare()
            if st.session_state.result == 0:
                print("There was a war!")
                st.session_state.Local_War_Count += 1 # Add to the local war counter
                st.session_state.Data_War_Happened = True # War Condition for the round is True
                # global Data_Total_Wars_In_Round
                st.session_state.Data_Total_Wars_In_Round += 1
                st.session_state.Data_Round_Number += 0.1 # Increase by 1 to indicate that we're in war round 1
                # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
                st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round -= 1 #These Changes so that if there is a war, the compared cards are considered War Cards, not Non-War Cards
                # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
                st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round -= 1
                # global Data_Total_Player_1_War_Cards_Dealt_In_Round
                st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round += 1
                # global Data_Total_Player_2_War_Cards_Dealt_In_Round
                st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round += 1
                report_round_data(st.session_state.Game_Statistics)
                report_round_data(st.session_state.Player_1_Statistics)
                report_round_data(st.session_state.Player_2_Statistics)

                # While comparison is in war mode (0)
                while st.session_state.result == 0:
                    # Deal 4 times, (0-3) Top card (is the fourth card dealt)
                    st.session_state.Is_Dealing_In_War = True # Flag for reporting to report extra lines during a war
                    for i in range(4):
                        deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)
                        deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)
                        st.session_state.Data_Round_Number += 0.01 # Increase to show this is tthe nth deal of the war

                        # If they're both out of cards, use their discard piles
                        if deal_1_result == 10 and deal_2_result == 10:
                            discard_result_1 = empty_discard_pile(st.session_state.player_1_hand, st.session_state.player_1_discard)
                            discard_result_2 = empty_discard_pile(st.session_state.player_2_hand, st.session_state.player_2_discard)
                            if discard_result_1 == 10:
                                st.session_state.result = 2
                                break
                            elif discard_result_1 == None:
                                deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)
                            
                            if discard_result_2 == 10:
                                st.session_state.result = 1
                                break
                            elif discard_result_2 == None:
                                deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)

                        # If Player 1 is out of cards but not Player 2, set result = 2 (player 2 wins), re-deal for player 1
                        elif deal_1_result == 10 and deal_2_result == None:
                            discard_result_1 = empty_discard_pile(st.session_state.player_1_hand, st.session_state.player_1_discard)
                            if discard_result_1 == 10:
                                st.session_state.result = 2
                                break
                            elif discard_result_1 == None:
                                deal_1_result = deal(st.session_state.player_1_hand, st.session_state.player_1_war, 1)

                        # If Player 2 is out of cards but not Player 1, set result = 1 (player 1 wins) and re-deal for player 2
                        elif deal_2_result == 10 and deal_1_result == None:
                            discard_result_2 = empty_discard_pile(st.session_state.player_2_hand, st.session_state.player_2_discard)
                            if discard_result_2 == 10:    
                                st.session_state.result = 1
                                break
                            elif discard_result_2 == None:
                                deal_2_result = deal(st.session_state.player_2_hand, st.session_state.player_2_war, 1)

                        report_round_data(st.session_state.Game_Statistics)
                        report_round_data(st.session_state.Player_1_Statistics)
                        report_round_data(st.session_state.Player_2_Statistics)
                        
                    # Once neither player is out of cards, compare the cards
                    if deal_1_result == None and deal_2_result == None:
                        war_result = compare()
                        # If player 1 wins, then set result to 1 and break the deal loop
                        if war_result == 1:
                            st.session_state.result = 1
                            print(f"Player 1 Wins The War at round {st.session_state.Data_Round_Number}!")
                            # report_round_data(Game_Statistics)
                            # report_round_data(Player_1_Statistics)
                            # report_round_data(Player_2_Statistics)
                            break
                        # If player 2 wins, then set result to 2 and break the deal loop
                        elif war_result == 2:
                            st.session_state.result = 2
                            print(f"Player 2 Wins The War at round {st.session_state.Data_Round_Number}!")
                            # report_round_data(Game_Statistics)
                            # report_round_data(Player_1_Statistics)
                            # report_round_data(Player_2_Statistics)
                            break
                        # If there was another war, then keep/set result at 0 and continue
                        elif war_result == 0:
                            st.session_state.result = 0
                            st.session_state.Local_War_Count += 1
                            st.session_state.Data_Total_Wars_In_Round += 1
                            st.session_state.Data_Round_Number = float(f'{st.session_state.Data_Round_Number:.1f}') + 0.1 # Reset the deal numbers and increment war numberby 0.1
                            print(f"There was another war at round {st.session_state.Data_Round_Number}!")
                            continue
                        # If there was in error when comparing, this should print
                        elif war_result == 10:
                            print(f"There was an error when performing a war_check comparison at round {st.session_state.Data_Round_Number}.")
                            break

        st.session_state.Is_Dealing_In_War = False # Reset flag before end-of-round reporting

        if war_result == 1 or war_result == 2:
            st.session_state.Data_War_Winner = st.session_state.result
            if war_result == 1:
                # global Data_Player_1_Wars_Won
                st.session_state.Data_Player_1_Wars_Won += 1
            elif war_result == 2:
                # global Data_Player_2_Wars_Won
                st.session_state.Data_Player_2_Wars_Won += 1


        if st.session_state.Local_War_Count > 0:
            # global Data_War_Number
            st.session_state.Data_War_Number += st.session_state.Local_War_Count
            # global Data_Total_Wars_In_Game
            st.session_state.Data_Total_Wars_In_Game += st.session_state.Local_War_Count
            # st.session_state.Data_Total_Wars_In_Round += st.session_state.Local_War_Count

        # Reset the War Stacks after each round
        # Result Parameter assigned abive will always be 1, 2, or 0. 
        print("Before trying to reset war stacks, the result value is: ", st.session_state.result)
        st.session_state.Result_Value = st.session_state.result
        try:
        # Code that might throw an exception
            reset_war_stacks(st.session_state.result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        
        print("****Player Totals****")
        print(f"The total length of {st.session_state.player_1_hand.name} and {st.session_state.player_1_discard.name} is:, {len(st.session_state.player_1_hand)} + {len(st.session_state.player_1_discard)}, or {len(st.session_state.player_1_hand) + len(st.session_state.player_1_discard)}, at the end of round {st.session_state.Data_Round_Number}")
        print(f"The total length of {st.session_state.player_2_hand.name} and {st.session_state.player_2_discard.name} is:, {len(st.session_state.player_2_hand)} + {len(st.session_state.player_2_discard)}, or {len(st.session_state.player_2_hand) + len(st.session_state.player_2_discard)}, at the end of round {st.session_state.Data_Round_Number}")


        # Check for a winner and store boolean values in variables
        did_player_1_win = check_for_winner(st.session_state.player_1_hand, st.session_state.player_1_war, st.session_state.player_1_discard)
        did_player_2_win = check_for_winner(st.session_state.player_2_hand, st.session_state.player_2_war, st.session_state.player_2_discard)
                
        report_round_data(st.session_state.Game_Statistics)
        report_round_data(st.session_state.Player_1_Statistics)
        report_round_data(st.session_state.Player_2_Statistics)
        reset_non_aggregate_global_variables()
        
        # If either player won, break the loop and print the winner
        if did_player_1_win == True:
            print("Player 1 Wins the game!")
            # Add another reporting function here when there is a game winner
            st.session_state.game_state = "after_game"
            break
        elif did_player_2_win == True:
            print("Player 2 Wins the game!")
            st.session_state.game_state = "after_game"
            # Add another reporting function here when there is a game winner
            break

        st.session_state.playing_game_increment -= 1

        # wait 0.25 seconds before continuing
        sleep(sleepy_time)
        build_data_page()

# Function to run the game of war when the user clicks the "player x rounds" buttons (or "finish the game" button)
def play_with_increments(rounds, sleepy_time):
    # rounds: Integer, the number of rounds to play
    # sleepy_time: Float, the number of seconds to wait between rounds

    # Play the game for the specified number of rounds
    st.session_state.playing_game_increment = rounds
    play_war(sleepy_time=sleepy_time)

# Function to handle the "Play Game?" button action
def handle_play_game():
    # Update session state to indicate the game has started
    set_up_game_environment()
    st.session_state.game_state = "in_game"

# Function to updates the charts on display while the user is playing the game
def build_data_page():

    # Assign the dataframes from the session state to variables
    Game_Statistics = st.session_state.Game_Statistics
    Player_1_Statistics = st.session_state.Player_1_Statistics
    Player_2_Statistics = st.session_state.Player_2_Statistics

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

    # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
    try:
        Player_1_Card_Count = Player_1_Statistics['Total Player 1 Cards'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_1_Card_Count = 26
    try:
        Player_2_Card_Count = Player_2_Statistics['Total Player 2 Cards'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_2_Card_Count = 26

    # Player names for the chart legends
    players = ['Player 1', 'Player 2']
    values = [Player_1_Card_Count, Player_2_Card_Count]
    # Create a bar chart using streamlit
    # line_chart_placeholder.line_chart(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color=["#429EBD","#F7AD19"])

    fig_line = px.line(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color_discrete_map={"Total Player 1 Cards": "#429EBD", "Total Player 2 Cards": "#F7AD19"}, labels={ "value": "Total Cards", "variable": "Players"})

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
                    text=f"Max for P1: {max_value_player1}", showarrow=True, arrowhead=6, arrowcolor="#429EBD", font=dict(color='black', size=14), ax=0, ay=-40)
    fig_line.add_annotation(x=round_max_player2, y=max_value_player2, 
                    text=f"Max for P2: {max_value_player2}", showarrow=True, arrowhead=6, arrowcolor="#F7AD19", font=dict(color='black', size=14), ax=0, ay=-40)



    fig_line.update_layout(legend=dict(x=0.5, xanchor="center", y=1.0, yanchor="bottom", orientation="h"), legend_title_text="")

    line_chart_placeholder.plotly_chart(fig_line, use_container_width=True)


    # For the pie chart
    # Get the last values in the player total rounds won columns
    try:
        Player_1_Rounds_Won_Chart = Player_1_Statistics['Player 1 Rounds Won'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_1_Rounds_Won_Chart = 10
    try:
        Player_2_Rounds_Won_Chart = Player_2_Statistics['Player 2 Rounds Won'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_2_Rounds_Won_Chart = 10

    # Create the pie chart using streamlit
    fig_pie = go.Figure(data=[
        go.Pie(labels=players, values=values, marker=dict(colors=['#429EBD','#F7AD19']), sort=False, direction="clockwise")])
    # set the size and removing the legend
    fig_pie.update_layout(width=300, height=400, showlegend=False, title='Card Ownership', title_x=0, margin=dict(l=0, r=0, t=30, b=0))
    # update the pie chart placeholder
    pie_chart_placeholder.plotly_chart(fig_pie)

    # Create the bar chart using streamlit
    fig_bar = go.Figure(data=[
        go.Bar(name='Player 1 Rounds Won', x=['Player 1'], y=[Player_1_Rounds_Won_Chart], marker_color='#429EBD', text=[Player_1_Rounds_Won_Chart], textposition=['outside']),
        go.Bar(name='Player 2 Rounds Won', x=['Player 2'], y=[Player_2_Rounds_Won_Chart], marker_color='#F7AD19', text=[Player_2_Rounds_Won_Chart], textposition=['outside'])
    ])
    # remove the legend
    fig_bar.update_layout(barmode='group', showlegend=False, dragmode=False, title='Rounds Won', title_x=0, margin=dict(l=0, r=0, t=30, b=0))
    # update the bar chart placeholder
    bar_chart_placeholder.plotly_chart(fig_bar, use_container_width=True)

    # # Update Button placeholders
    # if game_data_button_placeholder.button("See the Game Data"): # Change this to Game Stats when that page is built-out
    #         st.switch_page("pages/3War_Data.py")
    # if stats_dashboard_button_placeholder.button("See the Stats Dashboard"): # Change this to Game Stats when that page is built-out
    #         st.switch_page("pages/2War_Stats.py")    # Create placeholders for the pie, bar, and line charts
            

# Initialize 'game_state' in session state if not already present, with the defualt as "before_game"
if 'game_state' not in st.session_state:
    st.session_state.game_state = "before_game"

# Initialize 'first_game' in session state if not already present
if "first_game" not in st.session_state:
    st.session_state.first_game = True

# Initialize 'first_game' in session state if not already present
if st.session_state.first_game == True:
    # set_up_game_environment()
    st.session_state.first_game = False

# Display the title of the page
st.markdown("<h1 style='text-align:center;font-size:50px;'>The War Room</h1>", unsafe_allow_html=True)
# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Initialize columns for the page
col1, col2, col3, col4= st.columns(4)

# Displays the "Play Game?" button only if it's the first run
if st.session_state.game_state == "before_game":
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("<h3 style='text-align:left;font-size:42px;'>Play the Game?</h3>", unsafe_allow_html=True)

        if st.button('Let\'s Go', on_click=handle_play_game):
            pass

# Displays the gameplay page once the "Play Game?" button is clicked
elif st.session_state.game_state == "in_game":
    column1, column2 = st.columns(2)

    # Set player colors
    color1 = '#429EBD' 
    color2 = '#F7AD19'

    # Display player names in their colors
    with column1:
        st.markdown(f"<h4 style='text-align:center;font-size:40px;color:{color1};'>Player 1</h4>", unsafe_allow_html=True)
    with column2:
        st.markdown(f"<h4 style='text-align:center;font-size:40px;color:{color2};'>Player 2</h4>", unsafe_allow_html=True)

    # Display the buttons users use to iterate through the game
    with col1:
        if st.button('Play 1 Round', key='play_1_round_button', on_click=lambda: play_with_increments(1, 0.1)):
            pass
    with col2:
        if st.button('Play 10 Rounds', key='play_10_rounds_button', on_click=lambda: play_with_increments(10, 0.1)):
            pass
    with col3:
        if st.button('Play 50 Rounds', key='play_50_rounds_button', on_click=lambda: play_with_increments(50, 0.025)):
            pass
    with col4:
        if st.button('Finish the Game', key='finish_game_button', on_click=lambda: play_with_increments(10000, 0.001)):
            pass

    # c1, c2, c3, c4 = st.columns(4)
    # with c2:
    #     game_data_button_placeholder = st.empty()
    # with c3:
    #     stats_dashboard_button_placeholder = st.empty()

    # Create placeholders for the pie, bar, and line charts
    # These placeholders keeps the charts updating in the same spot instead of creating new ones above the old ones for every round of the game.
    co1, co2 = st.columns(2)
    with co1:
        pie_chart_placeholder = st.empty()
    with co2:
        bar_chart_placeholder = st.empty()
    
    line_chart_placeholder = st.empty()

    # Build the data page using the build_data_page() function
    build_data_page()


# Displays a version of the in_game page that no longer has the iterative buttons and insted declares the winner of the game in that player's color.
elif st.session_state.game_state == "after_game":
    
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

    # Set player colors for markdown text
    color = '#429EBD' if game_winner == 1 else '#F7AD19'

    # Display the winner of the game in the player's color
    st.markdown(f"<h4 style='text-align:center;font-size:40px;color:{color};'>Player {game_winner} Wins the Game after {rounds_total} Rounds!</h4>", unsafe_allow_html=True)
    # st.markdown(f"<i><h6 style='text-align:center;font-size:20px;'>Check out the Stats Dashboard and the War Data by clicking on the navigation bar to your left.</h6></i>", unsafe_allow_html=True)
    columns1, columns2 = st.columns(2)
    with columns1:
        if st.button("See the Generated Stats Dashboard", key='leave_from_post_game_to_stats_dashboard'):
            st.switch_page("pages/2Stats_Dashboard.py")
    with columns2:
        if st.button("See all of the War Data", key='leave_from_post_game_to_war_data'):
            st.switch_page("pages/3War_Data.py")
    # c1, c2, c3, c4 = st.columns(4)
    # with c2:
    #     game_data_button_placeholder = st.empty()
    # with c3:
    #     stats_dashboard_button_placeholder = st.empty()

    # These placeholders keeps the charts updating in the same spot instead of creating new ones above the old ones for every round of the game.
    co1, co2 = st.columns(2)
    with co1:
        pie_chart_placeholder = st.empty()
    with co2:
        bar_chart_placeholder = st.empty()

    line_chart_placeholder = st.empty()

    # Build the data page using the build_data_page() function
    build_data_page()