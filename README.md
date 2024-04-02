# automated_card_game
Building the card game 'War' in python. Practice in Python development.

### The Purpose:
This project is an exercise in logic flow, function construction, coding with a definitive end-product in mind. I aim to develop a single script that will simulate the 'war' card game between two players using the PyDealer library for card and deck classes. This script uses custom functions for dealing, simulating a war, and once one player has run out of cards, declaring/outputing a winner.


## 3-1-24
* Added first attempt/version. (Program runs infinitely)

## 3-5-24
* Added second attempt/version.

## 3-12-24
* Added third attempt/version. Program still contains broken winning conditions.

## 3-15-24
* Added fourth version. Program is finally functional when running final cell (Simulating the game.)
    - Win conditions fixed. Greatly utilized 'break' feature of all logic loops to avoid running uneccesary and conflicting code.
    - Cards have permenenace, i.e., they exist in one of six stacks and nowhere else, accounting for each at the end of every round by totalling all cards in both players' posession.
    - Added missing discard-to-hand function absent in prior versions, refilling the players hand when they are out of cards.
    - Numerous print statments accross all functions added for debugging ease.

* Bugs
    - Comparing cards does not operate as expected. PyDeck library's methods are returning results such as the Jack of Clubs winning against the Ace of Hearts (Round 81 in last cell output.) Will utilize custom card rankings or other method of comparisons inn future versions.

## 4-2-24
* Added Sixth version. (fifth discarded) Program is much more functional when running the newly-functionized set_up_game_environment() and play_game() cells.
    - Comparison bug solved by using a dictionary to get card value based on the returned Card.value property of the Card object.
    - Running the set_up_game_environment() function generates 3 Pandas dataframes that are populated thorughout the runtime of the play_game() function
    - Utilized global variables to access and modify data points thoughout the numerous functions involved in game logic, but more importantly it was for the purpose of Game and Player Statistics data generation.
    - Over 40+ data points are generated per round.

* Bugs
    - Some values in rows of data (particularly around War rounds) don't match up to the expected values. Data is not eggregiously compromised but some metrics as iron-clad as they should be. 

