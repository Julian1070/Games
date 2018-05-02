from game import *
from classes import Team, Game

try:
    x = int(input("How many games do you want to simulate?\n(Enter a positive integer)\n\n"))
except:
    print("Incorrect input. Simulating for 10 games instead:")
    x = 10
teamAwins = 0
teamBwins = 0
for i in range(x):
    TeamA = Team(100.6, 3655, 1657, 1238, 466, 418, 1338, 43, 0)
    TeamB = Team(97.3, 3760, 1724, 1097, 405, 445, 1542, 45, 1)
    game_pos = int(TeamA.pos+TeamB.pos)
    the_Game = Game(0, 0, game_pos, 0, 0)
    game = play(i+1, the_Game, TeamA, TeamB)
    print(game)
    if the_Game.scoreA > the_Game.scoreB:
        teamAwins += 1
    elif the_Game.scoreB > the_Game.scoreA:
        teamBwins += 1
print("Total result in wins (" + str(x) + " games played): Team A " + str(teamAwins) + ":" + str(teamBwins) + " Team B")
