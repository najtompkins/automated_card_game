import pydealer as pyd # For card/stack/deck classes
from time import sleep # For optional delay between rounds
# from IPython.display import clear_output # To Clear Jupyter cell outputs
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Raises error when player's hand is empty
class NoCards(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

        # Declare Global Variables for data generation after each round/war-end condition

# Game Data
## Round Data
import streamlit as st

def create_global_variables():
    # Initialize variables if they don't already exist in the session state
    variables = {
        'Data_Round_Number': 0,
        'Data_Round_Winner': 0,
        'Data_War_Number': 0,  # Might not be needed
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
        'Result_Value': None, ######################################
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
        # # Dataframe variables
        'Game_Statistics': None,
        'Player_1_Statistics': None,
        'Player_2_Statistics': None,
        # Other variables needed
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

    for key, initial_value in variables.items():
        if key not in st.session_state:
            st.session_state[key] = initial_value

# Deals card(s) to specified player's war_stack from the top (index -1) of the player's hand
# Returns error code 10 if player's hand is empty. None if deal was successful.

def deal(player_hand, player_war_stack, number_of_cards):
    # Deal the top cards from the player's hand and place them into the war stack
    # print(f"--Dealing Cards to {player_hand.name}--")
    # print(f"Before dealing, The Player's war_stack size: {len(player_war_stack)}")

    try:
        if len(player_hand) == 0:
            raise NoCards("Player's hand is empty")
        elif len(player_hand) > 0:
            temp_card = player_hand.deal(number_of_cards)
            player_war_stack.add(temp_card)
            # print(f"--[{temp_card}]-- Card Dealt Successfully to {player_hand.name}--")
            
            # global Data_War_Happened
            # Pulls in and updates global variables based on which player_hand was passed through
            if player_hand.name == "Player 1's Hand":
                # global Data_Player_1_Card
                st.session_state.Data_Player_1_Card = st.session_state.player_1_war[-1]
                # global Data_Player_1_Card_Face
                st.session_state.Data_Player_1_Card_Face = st.session_state.player_1_war[-1].value
                # global Data_Player_1_Card_Suit
                st.session_state.Data_Player_1_Card_Suit = st.session_state.player_1_war[-1].suit
                # global Data_Player_1_Card_Value
                st.session_state.Data_Player_1_Card_Value = get_face_value(st.session_state.player_1_war[-1])

                # global Data_War_Happened
                # Data_War_Happened = Data_War_Happened
                if st.session_state.Data_War_Happened == True:
                    # global Data_Total_Player_1_War_Cards_Dealt_In_Game # Increase total for player 1 for game
                    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game += 1
                    # global Data_Total_Player_1_War_Cards_Dealt_In_Round # Increase total for player 1 for round
                    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round += 1
                elif st.session_state.Data_War_Happened == False:
                    # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Game # Increase total for player 1 for game
                    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game += 1
                    # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Round # Increase total for player 1 for round
                    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round += 1

            elif player_hand.name == "Player 2's Hand":
                # global Data_Player_2_Card
                st.session_state.Data_Player_2_Card = st.session_state.player_2_war[-1]
                # global Data_Player_2_Card_Face
                st.session_state.Data_Player_2_Card_Face =  st.session_state.player_2_war[-1].value
                # global Data_Player_2_Card_Suit
                st.session_state.Data_Player_2_Card_Suit = st.session_state.player_2_war[-1].suit
                # global Data_Player_2_Card_Value
                st.session_state.Data_Player_2_Card_Value = get_face_value(st.session_state.player_2_war[-1])

                # global Data_War_Happened
                # Data_War_Happened = Data_War_Happened
                if st.session_state.Data_War_Happened == True:
                    # global Data_Total_Player_2_War_Cards_Dealt_In_Game # Increase total for player 2 for game
                    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game += 1
                    # global Data_Total_Player_2_War_Cards_Dealt_In_Round # Increase total for player 2 for round
                    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round += 1
                elif st.session_state.Data_War_Happened == False:
                    # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Game # Increase total for player 2 for game
                    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game += 1
                    # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Round # Increase total for player 2 for round
                    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round += 1

    except NoCards as e:
        # print(e)
        return 10
    # print(f"After dealing, the Player's war_stack  size: {len(player_war_stack)}")
    
# Function to get the numerical value of a card
def get_face_value(card):
    card_face_values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "Jack": 11, "Queen": 12, "King": 13, "Ace": 14
    }
    return card_face_values[card.value]

# Compares the top cards in the player's war_stacks.
# Returns error code 10 if player's hand is empty
    # Returns code 0 if there is a war
    # Returns code 1 if player 1 wins
    # Returns code 2 if player 2 wins

def compare():
    # print(f"--Comparing the player cards. ({len(st.session_state.player_1_war)} in 1's war stack, {len(st.session_state.player_2_war)} in 2's war stack)--")
    # assign the top cards in the war stack to variables.
    top_card_1 = st.session_state.player_1_war[-1]
    top_card_2 = st.session_state.player_2_war[-1]

    # print(f"Player 1's card --> {top_card_1} / {top_card_2} <-- Player 2's card")

    if get_face_value(top_card_1) > get_face_value(top_card_2):
        # print(f"Player 1 wins the round with the {top_card_1}!")
        return 1
    elif get_face_value(top_card_1) < get_face_value(top_card_2):
        # print(f"Player 2 wins the round with the {top_card_2}!")
        return 2
    elif get_face_value(top_card_1) == get_face_value(top_card_2):
        # print(f"Neither player wins! It's a war!")
        return 0
    else: # if something went wrong
        # print("Something went wrong!")
        return 10

# Moves all cards from the both player's war stack into the their respective discard hands
# Based on result value (0, 1, or 2) which is passed into function after comparison function returns a verdict.

def reset_war_stacks(result):
    # print(f"--Resetting the war stacks from 1's {len(st.session_state.player_1_war)} and 2's {len(st.session_state.player_2_war)} to Zero (0)--")
    # reset the war stacks

    # global Data_Round_Winner

    if st.session_state.result == 1:
        # print(f"Player 1 won the round, so all cards go to {st.session_state.player_1_discard.name}")
        st.session_state.Data_Round_Winner = 1
        # global Data_Player_1_Rounds_Won
        st.session_state.Data_Player_1_Rounds_Won += 1
        # reset player 1's war stack into st.session_state.player_1_discard
        for i in range(len(st.session_state.player_1_war)):
            temp_card = st.session_state.player_1_war.deal(1)
            st.session_state.player_1_discard.add(temp_card)

        # reset player 2's war stack into st.session_state.player_1_discard
        for i in range(len(st.session_state.player_2_war)):
            temp_card = st.session_state.player_2_war.deal(1)
            st.session_state.player_1_discard.add(temp_card)
    
    elif st.session_state.result == 2:

        # print(f"Player 2 won the round, so all cards go to {st.session_state.player_2_discard.name}")
        st.session_state.Data_Round_Winner = 2
        # global Data_Player_2_Rounds_Won
        st.session_state.Data_Player_2_Rounds_Won += 1
        # reset player 1's war stack into st.session_state.player_2_discard
        for i in range(len(st.session_state.player_1_war)):
            temp_card = st.session_state.player_1_war.deal(1)
            st.session_state.player_2_discard.add(temp_card)

        # reset player 2's war stack into st.session_state.player_2_discard
        for i in range(len(st.session_state.player_2_war)):
            temp_card = st.session_state.player_2_war.deal(1)
            st.session_state.player_2_discard.add(temp_card)

    # Further else statements only show when something went wrong. They should never print in a functioning game.
    elif st.session_state.result == 10:
        print("Cannot reset stacks when comparison errors (value 10) are passed into reset function")
    
    elif st.session_state.result == 0:
        print("Hey there's a war going on! Cannot reset the stacks right now!")

    else: print("Something went wrong when resetting the stacks.")

# Empties discard pile of specified player into hand of specified player.
    # Returns error code 10 if player's discard pile is empty
    # Returns None if discard pile is successfully emptied into the player's hand

def empty_discard_pile(player_hand, player_discard_pile):
    # print(f"--Attempting to empty the discard pile for {player_hand.name}--")

    # Check if the discard pile is empty, returning error code 10 if so
    if len(player_discard_pile) == 0:
        # print(f"{player_hand.name} is empty, returning error code 10")
        return 10
    
    # Empty discard pile into player hand
    elif len(player_discard_pile) > 0:
        # print(f"{player_discard_pile.name} is not empty: There are {len(player_discard_pile)} cards in it. Emptying into {player_hand.name}")
        for card in player_discard_pile:
            temp_card = player_discard_pile.deal(1)
            player_hand.add(temp_card)
            if player_discard_pile.name == "Player 1's Discard Pile":
                # global Data_Player_1_Ran_Out_of_Cards
                st.session_state.Data_Player_1_Ran_Out_of_Cards = True
                # global Data_Cards_Dealt_Back_to_Player_1
                st.session_state.Data_Cards_Dealt_Back_to_Player_1 += 1
            elif player_discard_pile.name == "Player 2's Discard Pile":
                # global Data_Player_2_Ran_Out_of_Cards
                st.session_state.Data_Player_2_Ran_Out_of_Cards = True
                # global Data_Cards_Dealt_Back_to_Player_2
                st.session_state.Data_Cards_Dealt_Back_to_Player_2 += 1

    # shuffle the player hand
    # print(f"Shuffling {player_hand.name}")
    player_hand.shuffle()

# Performs final check for winner (all player stacks are empty), returning Boolean value.

def check_for_winner(player_hand, player_war_stack, player_discard):
    if ((len(player_hand)) + (len(player_war_stack)) + (len(player_discard))) == 0:
        return True
    else:
        return False

# Create an empty dataframe that contains the game statistics as they are generated

def create_game_dataframes():
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
        "Result Value"]

    Column_Names_Player_1_Data = [
        "Round Number",
        "Player 1 Card",
        "Player 1 Card Face",
        "Player 1 Card Suit",
        "Player 1 Card Value",
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

    Column_Names_Player_2_Data = [
        "Round Number",
        "Player 2 Card",
        "Player 2 Card Face",
        "Player 2 Card Suit",
        "Player 2 Card Value",
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

# Create dataframs that are globally available, and have one row of starting data per column

    # global Game_Statistics
    st.session_state.Game_Statistics = pd.DataFrame(columns=Column_Names_Game_Data,)
    # Game_Statistics['War Happened'] = Game_Statistics["War Happened"].astype('boolean')

    # global Player_1_Statistics
    st.session_state.Player_1_Statistics = pd.DataFrame(columns=Column_Names_Player_1_Data)
    # Player_1_Statistics['Player 1 Ran Out of Cards'] = Player_1_Statistics["Player 1 Ran Out of Cards"].astype('boolean')

    # global Player_2_Statistics
    st.session_state.Player_2_Statistics = pd.DataFrame(columns=Column_Names_Player_2_Data)
    # Player_2_Statistics['Player 2 Ran Out of Cards'] = Player_2_Statistics["Player 2 Ran Out of Cards"].astype('boolean')

# Creates Function for reporting the round data and adding that to a dataframe
def report_round_data(Data_DF):
    
    # global Local_War_Count
    # Local_War_Count = Local_War_Count
    # global Data_Total_Wars_In_Round
    # Data_Total_Wars_In_Round = Data_Total_Wars_In_Round
    # global Data_War_Happened
    # Data_War_Happened = Data_War_Happened
    # global Is_Dealing_In_War
    # Is_Dealing_In_War = Is_Dealing_In_War

    # global player_1_hand
    # global player_1_discard
    # global player_1_war
    # global player_2_hand
    # global player_2_discard
    # global player_2_war

    # player_1_hand = player_1_hand
    # player_1_discard = player_1_discard
    # player_1_war = player_1_war
    # player_2_hand = player_2_hand
    # player_2_discard = player_2_discard
    # player_2_war = player_2_war
    
    global Data_Total_Cards_In_Play
    # global Data_Player_1_Hand_Size
    # global Data_Player_1_Discard_Pile_Size
    # global Data_Player_1_War_Stack_Size
    # global Data_Player_2_Hand_Size
    # global Data_Player_2_Discard_Pile_Size
    # global Data_Player_2_War_Stack_Size

    st.session_state.Data_Player_1_Hand_Size = len(st.session_state.player_1_hand)
    st.session_state.Data_Player_1_Discard_Pile_Size = len(st.session_state.player_1_discard)
    st.session_state.Data_Player_1_War_Stack_Size = len(st.session_state.player_1_war)
    st.session_state.Data_Player_2_Hand_Size = len(st.session_state.player_2_hand)
    st.session_state.Data_Player_2_Discard_Pile_Size = len(st.session_state.player_2_discard)
    st.session_state.Data_Player_2_War_Stack_Size = len(st.session_state.player_2_war)
    Data_Total_Cards_In_Play = len(st.session_state.player_1_hand) + len(st.session_state.player_1_war) + len(st.session_state.player_1_discard) + len(st.session_state.player_2_hand) + len(st.session_state.player_2_war) + len(st.session_state.player_2_discard)
    st.session_state.Data_Total_Player_1_Cards = len(st.session_state.player_1_hand) + len(st.session_state.player_1_war) + len(st.session_state.player_1_discard)
    st.session_state.Data_Total_Player_2_Cards = len(st.session_state.player_2_hand) + len(st.session_state.player_2_war) + len(st.session_state.player_2_discard)

    # global Data_Total_Player_1_War_Cards_Dealt_In_Round
    # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
    global Data_Total_Player_1_Cards_Dealt_In_Round
    # global Data_Total_Player_1_War_Cards_Dealt_In_Game
    # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
    global Data_Total_Player_1_Cards_Dealt_In_Game
    # global Data_Total_Player_2_War_Cards_Dealt_In_Round
    # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
    global Data_Total_Player_2_Cards_Dealt_In_Round
    # global Data_Total_Player_2_War_Cards_Dealt_In_Game
    # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
    global Data_Total_Player_2_Cards_Dealt_In_Game

    # Data_Total_Player_1_War_Cards_Dealt_In_Round = Data_Total_Player_1_War_Cards_Dealt_In_Round
    # Data_Total_Player_1_NonWar_Cards_Dealt_In_Round = Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
    Data_Total_Player_1_Cards_Dealt_In_Round = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
    # Data_Total_Player_1_War_Cards_Dealt_In_Game = Data_Total_Player_1_War_Cards_Dealt_In_Game
    # Data_Total_Player_1_NonWar_Cards_Dealt_In_Game = Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
    Data_Total_Player_1_Cards_Dealt_In_Game = st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Game
    # Data_Total_Player_2_War_Cards_Dealt_In_Round = Data_Total_Player_2_War_Cards_Dealt_In_Round
    # Data_Total_Player_2_NonWar_Cards_Dealt_In_Round = Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
    Data_Total_Player_2_Cards_Dealt_In_Round = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
    # Data_Total_Player_2_War_Cards_Dealt_In_Game = Data_Total_Player_2_War_Cards_Dealt_In_Game
    # Data_Total_Player_2_NonWar_Cards_Dealt_In_Game = Data_Total_Player_2_NonWar_Cards_Dealt_In_Game
    Data_Total_Player_2_Cards_Dealt_In_Game = st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Game + st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Game

    # global Data_Player_1_Ran_Out_of_Cards
    # global Data_Cards_Dealt_Back_to_Player_1
    # global Data_Player_2_Ran_Out_of_Cards
    # global Data_Cards_Dealt_Back_to_Player_2

    # Data_Player_1_Ran_Out_of_Cards = Data_Player_1_Ran_Out_of_Cards
    # Data_Cards_Dealt_Back_to_Player_1 = Data_Cards_Dealt_Back_to_Player_1
    # Data_Player_2_Ran_Out_of_Cards = Data_Player_2_Ran_Out_of_Cards
    # Data_Cards_Dealt_Back_to_Player_2 = Data_Cards_Dealt_Back_to_Player_2

    # global Data_Player_1_Rounds_Won
    # global Data_Player_1_Wars_Won
    # global Data_Player_2_Rounds_Won
    # global Data_Player_2_Wars_Won

    # Data_Player_1_Rounds_Won = Data_Player_1_Rounds_Won
    # Data_Player_1_Wars_Won = Data_Player_1_Wars_Won
    # Data_Player_2_Rounds_Won = Data_Player_2_Rounds_Won
    # Data_Player_2_Wars_Won = Data_Player_2_Wars_Won

    # global Game_Statistics
    # global Player_1_Statistics
    # global Player_2_Statistics


    if Data_DF is st.session_state.Game_Statistics:
        df = st.session_state.Game_Statistics

        new_row_index = len(df)
        # Generate an empty row of data at that index
        df.loc[new_row_index] = pd.NA

        if st.session_state.Is_Dealing_In_War == False: # The default end-of-the-round reporting
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

        elif st.session_state.Is_Dealing_In_War == True: # The Special report-during-each-deal-to-war-stack reporting
            df.at[new_row_index, "Round Number"] = st.session_state.Data_Round_Number
            # df.at[new_row_index, "Round Winner"] = st.session_state.Data_Round_Winner
            # if st.session_state.Local_War_Count > 0:
            df.at[new_row_index, "War Number"] = st.session_state.Data_War_Number + 1
            # else:
                # df.at[new_row_index, "War Number"] = None
            # df.at[new_row_index, "War Winner"] = st.session_state.Data_War_Winner
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

    elif Data_DF is st.session_state.Player_1_Statistics:
        df = st.session_state.Player_1_Statistics

        new_row_index = len(df)
        # Generate an empty row of data at that index
        df.loc[new_row_index] = pd.NA

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
        
    
    elif Data_DF is st.session_state.Player_2_Statistics:
        df = st.session_state.Player_2_Statistics

        new_row_index = len(df)
        # Generate an empty row of data at that index
        df.loc[new_row_index] = pd.NA

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

def set_up_game_environment():
    # Set up the game environment using global variables

    # Assign the global variables and their starting values
    create_global_variables()
    # create the game dataframes as global variables (based on the global variables)
    create_game_dataframes()

    # Create the stacks and give them names
    # build the starting deck
    # global starting_deck
    starting_deck = pyd.Deck()
    # shuffle the deck
    starting_deck.shuffle()

    # deal the cards to player variables
    player_1_cards = starting_deck.deal(26)
    player_2_cards = starting_deck.deal(26)

    # build player 1's starting hand
    st.session_state.player_1_hand = pyd.Stack()
    st.session_state.player_1_hand.add(player_1_cards)
    # build player 2's starting hand
    st.session_state.player_2_hand = pyd.Stack()
    st.session_state.player_2_hand.add(player_2_cards)

    # build player 1's discard pile
    st.session_state.player_1_discard = pyd.Stack()
    # build player 2's discard pile
    st.session_state.player_2_discard = pyd.Stack()

    # build player 1's war stack
    st.session_state.player_1_war = pyd.Stack()
    # build player 2's war stack
    st.session_state.player_2_war = pyd.Stack()

    # Naming the Stacks for better output readability of print statements
    st.session_state.player_1_hand.name = "Player 1's Hand"
    st.session_state.player_1_discard.name = "Player 1's Discard Pile"
    st.session_state.player_1_war.name = "Player 1's War Stack"

    st.session_state.player_2_hand.name = "Player 2's Hand"
    st.session_state.player_2_discard.name = "Player 2's Discard Pile"
    st.session_state.player_2_war.name = "Player 2's War Stack"

def reset_non_aggregate_global_variables():
    # global Data_War_Number
    # Data_War_Number = 0
    # global Data_War_Winner
    st.session_state.Data_War_Winner = None

    # global Data_Round_Winner
    st.session_state.Data_Round_Winner = None

    # global Local_War_Count
    st.session_state.Local_War_Count = 0

    # global Data_War_Happened
    st.session_state.Data_War_Happened = False

    # global Data_Total_Player_1_War_Cards_Dealt_In_Round
    st.session_state.Data_Total_Player_1_War_Cards_Dealt_In_Round = 0
    # global Data_Total_Player_1_NonWar_Cards_Dealt_In_Round
    st.session_state.Data_Total_Player_1_NonWar_Cards_Dealt_In_Round = 0
    global Data_Total_Player_1_Cards_Dealt_In_Round
    Data_Total_Player_1_Cards_Dealt_In_Round = 0
    
    # global Data_Total_Player_2_War_Cards_Dealt_In_Round
    st.session_state.Data_Total_Player_2_War_Cards_Dealt_In_Round = 0
    # global Data_Total_Player_2_NonWar_Cards_Dealt_In_Round
    st.session_state.Data_Total_Player_2_NonWar_Cards_Dealt_In_Round = 0
    global Data_Total_Player_2_Cards_Dealt_In_Round
    Data_Total_Player_2_Cards_Dealt_In_Round = 0

    # global Data_Player_1_Ran_Out_of_Cards
    st.session_state.Data_Player_1_Ran_Out_of_Cards = False
    # global Data_Cards_Dealt_Back_to_Player_1
    st.session_state.Data_Cards_Dealt_Back_to_Player_1 = 0
    # global Data_Player_2_Ran_Out_of_Cards
    st.session_state.Data_Player_2_Ran_Out_of_Cards = False
    # global Data_Cards_Dealt_Back_to_Player_2
    st.session_state.Data_Cards_Dealt_Back_to_Player_2 = 0

    # global Data_Total_Wars_In_Round
    st.session_state.Data_Total_Wars_In_Round = 0

    # global result
    st.session_state.result = None


if "first_game" not in st.session_state:
    st.session_state.first_game = True

if st.session_state.first_game == True:
    set_up_game_environment()
    st.session_state.first_game = False

def play_war(sleepy_time = 0.2):
    # result = None
    # print(f"At the beginning of found {st.session_state.Data_Round_Number}, result is: ({st.session_state.result}) ")
    # st.session_state.playing_game_increment = 1
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

def play_with_increments(rounds, sleepy_time):
    st.session_state.playing_game_increment = rounds
    play_war(sleepy_time=sleepy_time)

# Initialize 'game_state' in session state if not already present
if 'game_state' not in st.session_state:
    st.session_state.game_state = "before_game"

# Function to handle the "Play Game?" button action
def handle_play_game():
    # Update session state to indicate the game has started
    st.session_state.game_state = "in_game"

def build_data_page():

    # st Game_Statistics
    Game_Statistics = st.session_state.Game_Statistics
    # global Player_1_Statistics
    Player_1_Statistics = st.session_state.Player_1_Statistics
    # global Player_2_Statistics
    Player_2_Statistics = st.session_state.Player_2_Statistics

    # For the Line graph
    Card_Distributions = pd.DataFrame(columns=['Round Number', 'Total Player 1 Cards', 'Total Player 2 Cards'])
    Card_Distributions['Round Number'] = st.session_state.Game_Statistics['Round Number'].astype(float)
    Card_Distributions['Total Player 1 Cards'] = st.session_state.Player_1_Statistics['Total Player 1 Cards'].astype(int)
    Card_Distributions['Total Player 2 Cards'] = st.session_state.Player_2_Statistics['Total Player 2 Cards'].astype(int)
    Card_Distributions.drop_duplicates(subset=['Round Number'], keep='last')

    # For the line chart
    # Get the last value in the Player_1_Statistics['Total Player 1 Cards'] column
    try:
        Player_1_Card_Count = Player_1_Statistics['Total Player 1 Cards'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_1_Card_Count = 0
    try:
        Player_2_Card_Count = Player_2_Statistics['Total Player 2 Cards'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_2_Card_Count = 0

    players = ['Player 1', 'Player 2']
    values = [Player_1_Card_Count, Player_2_Card_Count]  # Example values indicating the proportion of cards
    # Create a bar chart using streamlit
    line_chart_placeholder.line_chart(Card_Distributions, x='Round Number', y=['Total Player 1 Cards', 'Total Player 2 Cards'], color=["#429EBD","#F7AD19"])

    # For the pie chart
    # Get the last values in the player total rounds won columns
    try:
        Player_1_Rounds_Won_Chart = Player_1_Statistics['Player 1 Rounds Won'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_1_Rounds_Won_Chart = 0
    try:
        Player_2_Rounds_Won_Chart = Player_2_Statistics['Player 2 Rounds Won'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        Player_2_Rounds_Won_Chart = 0

    players = ['Player 1', 'Player 2']
    fig_pie = go.Figure(data=[
        go.Pie(labels=players, values=values, marker=dict(colors=['#429EBD','#F7AD19']), sort=False, direction="clockwise")])
    fig_pie.update_layout(width=300, height=400, showlegend=False)
    pie_chart_placeholder.plotly_chart(fig_pie)

    # Data for bar chart
    # rounds_won = [Player_1_Rounds_Won_Chart, Player_2_Rounds_Won_Chart]
    # bar_dict = pd.DataFrame({"Players": players, "Player 1 Rounds Won": Player_1_Rounds_Won_Chart, "Player 2 Rounds Won": Player_2_Rounds_Won_Chart})
    # bar_chart_placeholder.bar_chart(bar_dict, width=300, height=400, x="Players", y=["Player 1 Rounds Won", "Player 2 Rounds Won"], use_container_width=True, color=["#429EBD","#F7AD19"], )


    fig_bar = go.Figure(data=[
        go.Bar(name='Player 1 Rounds Won', x=['Player 1'], y=[Player_1_Rounds_Won_Chart], marker_color='#429EBD', text=[Player_1_Rounds_Won_Chart], textposition=['outside']),
        go.Bar(name='Player 2 Rounds Won', x=['Player 2'], y=[Player_2_Rounds_Won_Chart], marker_color='#F7AD19', text=[Player_2_Rounds_Won_Chart], textposition=['outside'])
    ])
    fig_bar.update_layout(barmode='group', showlegend=False)
    bar_chart_placeholder.plotly_chart(fig_bar, use_container_width=True)





st.markdown("<h1 style='text-align:center;font-size:50px;'>The War Room</h1>", unsafe_allow_html=True)

col1, col2, col3, col4= st.columns(4)

# Display the "Play Game?" button only if it's the first run
if st.session_state.game_state == "before_game":
    column1, column2 = st.columns(2)
    with column1:
        # create empty placeholder
        st.markdown("<h3 style='text-align:left;font-size:42px;'>Play the Game?</h3>", unsafe_allow_html=True)
        # st.write("# The War Room")
        if st.button('Let\'s Go', on_click=handle_play_game):
            pass

elif st.session_state.game_state == "in_game":
    column1, column2 = st.columns(2)
    color1 = '#429EBD' 
    color2 = '#F7AD19'

    with column1:
        st.markdown(f"<h4 style='text-align:left;font-size:40px;color:{color1};'>Player 1</h4>", unsafe_allow_html=True)
    with column2:
        st.markdown(f"<h4 style='text-align:Right;font-size:40px;color:{color2};'>Player 2</h4>", unsafe_allow_html=True)


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

    co1, co2 = st.columns(2)
    with co1:
        pie_chart_placeholder = st.empty()
    with co2:
        bar_chart_placeholder = st.empty()
    

    line_chart_placeholder = st.empty()

    build_data_page()
elif st.session_state.game_state == "after_game":
    
    try:
        game_winner = st.session_state.Game_Statistics['Round Winner'].iloc[-1]
    except IndexError:  # Catching the case where the DataFrame is empty
        game_winner = 0
    try:
        rounds_total = int(st.session_state.Game_Statistics['Round Number'].iloc[-1])
    except IndexError:  # Catching the case where the DataFrame is empty
        rounds_total = 0

    # with col2:
        # st.write("The Game Ended")
    color = '#429EBD' if game_winner == 1 else '#F7AD19'
    # st.markdown(f"<h4 style='text-align:center;font-size:40px;color:{color};>Player " + str(game_winner) + " Won the Game!</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:center;font-size:40px;color:{color};'>Player {game_winner} Wins the Game after {rounds_total} Rounds!</h4>", unsafe_allow_html=True)
    st.markdown(f"<i><h6 style='text-align:center;font-size:20px;'>Check out the Stats Dashboard and the War Data by clicking on the navigation bar to your left.</h6></i>", unsafe_allow_html=True)

    co1, co2 = st.columns(2)
    with co1:
        pie_chart_placeholder = st.empty()
    with co2:
        bar_chart_placeholder = st.empty()

    line_chart_placeholder = st.empty()

    build_data_page()