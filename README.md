# Automated Card Game

Building the card game 'War' in Python. Practice in Python development.

## The Purpose

This project is an exercise in logic flow, function construction, coding with a definitive end-product in mind. I aim to develop a single script that will simulate the 'war' card game between two players using the PyDealer library for card and deck classes. This script uses custom functions for dealing, simulating a war, and once one player has run out of cards, declaring/outputting a winner.

---

### Updates

#### 3-1-24
- Added first attempt/version. (Program runs infinitely)

#### 3-5-24
- Added second attempt/version.

#### 3-12-24
- Added third attempt/version. Program still contains broken winning conditions.

#### 3-15-24
- Added fourth version. Program is finally functional when running final cell (Simulating the game.)
  - Win conditions fixed. Greatly utilized 'break' feature of all logic loops to avoid running unnecessary and conflicting code.
  - Cards have permanence, i.e., they exist in one of six stacks and nowhere else, accounting for each at the end of every round by totaling all cards in both players' possession.
  - Added missing discard-to-hand function absent in prior versions, refilling the players' hand when they are out of cards.
  - Numerous print statements across all functions added for debugging ease.

##### Bugs
- Comparing cards does not operate as expected. PyDeck library's methods are returning results such as the Jack of Clubs winning against the Ace of Hearts (Round 81 in last cell output.) Will utilize custom card rankings or other methods of comparison in future versions.

#### 4-2-24
- Added Sixth version. (fifth discarded) Program is much more functional when running the newly-functionized `set_up_game_environment()` and `play_game()` cells.
  - Comparison bug solved by using a dictionary to get card value based on the returned `Card.value` property of the Card object.
  - Running the `set_up_game_environment()` function generates 3 Pandas dataframes that are populated throughout the runtime of the `play_game()` function.
  - Utilized global variables to access and modify data points throughout the numerous functions involved in game logic, but more importantly, it was for the purpose of Game and Player Statistics data generation.
  - Over 40+ data points are generated per round and populated on the GameData worksheet.

##### Bugs
- Some values in rows of data (particularly around War rounds) don't match up to the expected values. Data is not egregiously compromised, but some metrics are not as iron-clad as they should be.

#### 4-5-24
- Added Excel Version 1. For the purpose of learning programmatic development within the Visual Basic for Applications (VBA) programming language, I took some time to develop this same Python War simulator in Excel. The added visual elements of the worksheets help the end-user visualize game statistics and, depending on how fast your machine is (I developed a lot of game logic on a laptop running Windows 10 that was bought in 2007!), you can also see the shuffling/dealing/round processing as it happens. *Macros must be enabled to run this file.*
  - Comparison operations are performed using Index/Match functions within the VBA IDE, using BackEnd arrays as reference for card values.
  - Program operates on back-end/hidden worksheets and then displays results on the front-end/accessible worksheets.
  - Utilized global variables to access and modify data points throughout the numerous functions involved in game logic, but more importantly, it was for the purpose of Game and Player Statistics data generation.
  - Nearly 40 data points are generated per round.

##### Bugs
- This version of the program was developed on the Windows 10/11 operating systems running Microsoft Office/Excel 365. Due to this, when running on MacOS Sonoma 14.4, a bug halts execution when initializing a variable. Experimentation proves that when the offending line is found in debug mode in the IDE, simply continuing the application will not result in any more issues.
- This version of the program is simply a proof-of-concept. While it is a fully functioning program, it still encounters errors if the expected sequence of events is not followed properly. Error handling, to some extent, is implemented, but is not comprehensive.
