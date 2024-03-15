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


