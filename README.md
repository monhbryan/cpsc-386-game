
The README is the first document someone sees when they clone the repository or view the repository on a git hosting service.

At a minimum, describe the game, the game's audience, and the sytem requirements. Include images and hyperlinks as needed to help the reader understand what the games is about.

You may wish to describe the game rules in this file or in an additional file of your choosing. If it is in an additional file, make it clear to the reader where game play instructions can be found.

Hello! This is my single-player game that is based off of the Monty Hall Problem (video at the end)

The objective of this game is to win $1,000,000 by picking the correct door out of three doors.


Once you pick a door, one of the incorrect doors will be revealed and you may choose to switch your pick. Alternatively, you may also choose to change your initial bet, although be warned that you may not bet more than you currently have.

If you are correct, you are given the option to "double down" and this is an exponential modifier that can stack infinitely. However, note that if you fail a modifier, you will lose your initial bet and the modifier.

If you are false, you will lose your bet and will be forced to start at a 1x modifier.

The double down calculation is done with: Bet * (2^(doubleDown Amount))

Once you reach $1,000,000 - you win and you may either quit or play again from $10,000.

If you fall at or under $0, you lose and you may either quit or play again.

System Requirements:
Python 3.8
cocos2d python library


Monty Hall Video:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=9vRUxbzJZ9Y
" target="_blank"><img src="http://img.youtube.com/vi/9vRUxbzJZ9Y/0.jpg" 
alt="Monty Hall Problem" width="240" height="180" border="10" /></a>