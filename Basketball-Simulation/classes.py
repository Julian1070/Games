import random


class Team:
    def __init__(self, pos, fga, fgm, ffga, ffgm, orb, drb, tg, identity):
        self.pos = pos
        self.fga = (fga-ffga)/tg
        self.fgp = (fgm-ffgm)/(fga-ffga)
        self.ffga = ffga/tg
        self.ffgp = ffgm/ffga
        self.orb = orb/tg
        self.drb = drb/tg
        self.identity = identity


class Game:
    def __init__(self, scorea, scoreb, total_pos, current_pos, team_pos):
        self.scoreA = scorea
        self.scoreB = scoreb
        self.total_pos = total_pos
        self.current_pos = current_pos
        self.team_pos = team_pos

    def tip_off(self):
        if random.random() > 0.5:
            self.team_pos = 1
