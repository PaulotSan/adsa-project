# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:41:38 2020

@author: Paul Jouet, Aladin Homsy
"""

import random

class Tournament():
    """
    The tournament's attributes are a datastructure containing the players, another for the games
    """
    def __init__(self, players):
        self.players = players
        self.games = []
        
    def __str__(self):
        res = 'Players :\n\n'
        for player in self.players:
            res += player.name + ' : ' + str(player.score) + ' points\n'
        res += '\nGame detail :\n\n'
        for game in self.games:
            res += str(game) + '\n\n'
        return res
        
    def Start(self):
        shuffled_players = random.sample(self.players, k=len(self.players))
        for i in range(10):
            game_players = shuffled_players[10*i:10*(i+1)]
            self.games.append(Game(game_players))
        
        
class Game():
    """
    players : list of players for this game (10)
    impostors : list of players who are impostors (2)
    """
    total_game_number=0
    def __init__(self, players):
        if len(players) == 10:
            for player in players: #reset players' attributes
                player.alive = True
                player.impostor = False
            self.players = players 
        else:
            self.players = None
            
        self.impostors = random.sample(players, k=2) #set 2 random impostors
        for player in self.impostors:
            player.impostor = True
            
        Game.total_game_number += 1 #increase the total number of games static class attribute
        self.game_number = Game.total_game_number
        
    def __str__(self):
        res = 'Game ' + str(self.game_number) + '\n\nPlayers :\n\n'
        for player in self.players:
            res += str(player) + '\n'
        res += 'Impostor 1 : ' + self.impostors[0].name
        res += '\nImpostor 2 : ' + self.impostors[1].name
        return res
    
class Player():
    def __init__(self, name):
        self.name = name
        self.impostor = False
        self.alive = True
        self.score = 0
    
    def __str__(self):
        res = self.name + ' is '
        if self.alive:
            res += 'alive, and he is '
        else:
            res += 'dead, and he was '
        if self.impostor:
            res += 'an impostor'
        else:
            res += 'a crewmate'
        return res
        
def test_game():
    players = [Player('doubleA'), Player('polo'), Player('tomus'), 
               Player('youngsamoo'), Player('jbinks'), Player('nyo'), 
               Player('jojo'), Player('clemter'), Player('paul'), Player('aladin')]
    game1 = Game(players)
    game2 = Game(players)
    print(game1) #la partie est bien crée, et 2 imposteurs sont choisis aléatoirement
    print(game2)
    
def test_tournament():
    players = []
    for i in range(100):
        player_name = 'player' + str(i+1)
        players.append(Player(player_name))
    tournament = Tournament(players)
    tournament.Start()
    print(tournament)
    
test_tournament()