import random


def play(i, the_Game, TeamA, TeamB):
    game_total_pos = the_Game.total_pos
    the_Game.tip_off()
    while the_Game.current_pos < game_total_pos:
        if the_Game.team_pos:
            if random.random() < (TeamB.fga+TeamB.ffga)/TeamB.pos:
                if random.random() < TeamB.fga/(TeamB.fga+TeamB.ffga):
                    if random.random() < TeamB.fgp:
                        the_Game.scoreB += 2
                        the_Game.current_pos += 1
                        the_Game.team_pos = 0
                        pass
                    else:
                        if random.random() < TeamB.orb/(TeamB.orb+TeamA.drb):
                            the_Game.current_pos += 1
                            pass
                        else:
                            the_Game.current_pos += 1
                            the_Game.team_pos = 0
                            pass
                else:
                    if random.random() < TeamB.ffgp:
                        the_Game.scoreB += 3
                        the_Game.current_pos += 1
                        the_Game.team_pos = 0
                        pass
                    else:
                        if random.random() < TeamB.orb/(TeamB.orb+TeamA.drb):
                            the_Game.current_pos += 1
                            pass
                        else:
                            the_Game.current_pos += 1
                            the_Game.team_pos = 0
                            pass
            else:
                the_Game.current_pos += 1
                the_Game.team_pos = 0
                pass
        else:
            if random.random() < (TeamA.fga+TeamA.ffga)/TeamA.pos:
                if random.random() < TeamA.fga/(TeamA.fga+TeamA.ffga):
                    if random.random() < TeamA.fgp:
                        the_Game.scoreA += 2
                        the_Game.current_pos += 1
                        the_Game.team_pos = 1
                        pass
                    else:
                        if random.random() < TeamA.orb/(TeamA.orb+TeamB.drb):
                            the_Game.current_pos += 1
                            pass
                        else:
                            the_Game.current_pos += 1
                            the_Game.team_pos = 1
                            pass
                else:
                    if random.random() < TeamA.ffgp:
                        the_Game.scoreA += 3
                        the_Game.current_pos += 1
                        the_Game.team_pos = 1
                        pass
                    else:
                        if random.random() < TeamA.orb/(TeamA.orb+TeamB.drb):
                            the_Game.current_pos += 1
                            pass
                        else:
                            the_Game.current_pos += 1
                            the_Game.team_pos = 1
                            pass
            else:
                the_Game.current_pos += 1
                the_Game.team_pos = 1
                pass
    if the_Game.scoreA == the_Game.scoreB:
        the_Game.current_pos = 0
        the_Game.total_pos = the_Game.total_pos/(48/5)
        play(i, the_Game, TeamA, TeamB)
    return "Game " + str(i) + " ends: Team A " + str(the_Game.scoreA) + ":" + str(the_Game.scoreB) + " Team B"
