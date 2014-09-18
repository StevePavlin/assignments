#!/usr/bin/python
#
#-------------------------------------------------------------------------------
# Name:    Adventure Game
#
# Author:  Steve Pavlin
#
# Created: September 09, 2014
#-------------------------------------------------------------------------------

# Imports
from random import randint


"""Game class, this class constructs a game object that can be reused."""
class Game(object):

    def __init__(self):
        # Different lines of text to be displayed at different points in the game. Accessed using self.text['key']
        self.text = {
         'INTRO': 'Welcome to Arch Linux! You have been placed in your /home directory. \nls returns two directories, one contains a shell script that will rm -rf /.\nthe other contains a wallet.dat file with 1000 Bitcoin, choose wisely!''',
        'CHOOSE_CAVE': 'Choose a directory (1 or 2): ',
        'WIN': 'You chose right and have been awarded with 1000 Bitcoin!',
        'LOSS': 'root@system~# rm -rf / | echo You chose the wrong directory, good luck repairing your system!',
        'PLAY_AGAIN': 'Would you like to play again? (y or n): '
        }

        # The correct choice will be generated everytime the game resets in start().
        self.correctCave = None

    # Called everytime the game resets.
    def start(self):
        # Generate the correct choice.
        self.correctCave = randint(1, 2)
        # Print the introduction paragraph.
        print(self.text['INTRO'])
        self.chooseCave()

    def chooseCave(self):
        # Print the directory choice line, (1 or 2).
        choice = int(input(self.text['CHOOSE_CAVE']))
        if choice == self.correctCave:
            self.winGame()
        else:
            self.loseGame()
        
        # Ask the user to play again.
        self.playAgain()


    def winGame(self):
        # Print the win text.
        print(self.text['WIN'])

    def loseGame(self):
        # Print the loss text.
        print(self.text['LOSS'])

    def playAgain(self):
        # Print out the play again choice line, (y or n).
        choice = input(self.text['PLAY_AGAIN'])

        if (choice == 'y'):
            # Restart
            self.start()

        else:
            # Finished executing
            pass


# Construct a game object.
game = Game()
# Call start() to begin the game.
game.start()
