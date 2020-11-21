# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:41:38 2020

@author: Paul Jouet, Aladin Homsy
"""
from typing import List
import random
import numpy as np

class Tournament():
    """
    The tournament's attributes are a datastructure containing the players, another for the games
    """
    def __init__(self, players:List['Player']):
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
    def __init__(self, players:List['Player']):
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
        
    def __str__(self) -> str:
        res = 'Game ' + str(self.game_number) + '\n\nPlayers :\n\n'
        for player in self.players:
            res += str(player) + '\n'
        res += 'Impostor 1 : ' + self.impostors[0].name
        res += '\nImpostor 2 : ' + self.impostors[1].name
        return res
    
class Player():
    def __init__(self, name:str):
        self.name = name
        self.impostor = False
        self.alive = True
        self.score = 0
    
    def __str__(self) -> str:
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
    
class Has_Seen_Graph():
    def __init__(self, players:List['Player'], impostor_list:List['Player']):
        self.graph = set()
        pick_relations = []
        for player in players:
            for i in range(3):
                pick_relations.append(player)
        
        
def player_has_seen(p:'Player', players:List['Player'], matrice:List[List[bool]]) -> List['Player']:
    #definir a quelle ligne se trouve le player
    ligne_p = 0
    for i in range(10):
        if p==players[i]:ligne_p=i
    list_has_seen=[]
    for index_c in range(len(matrice[0])):
        if matrice[ligne_p,index_c] == 1:
            for index_l in range(10):
                if index_l!=ligne_p and matrice[index_l,index_c] == 1: 
                    list_has_seen.append(players[index_l])
    return list_has_seen 

def Player_has_not_seen(p: 'Player', players: List['Player'], matrice: List[List[bool]]) -> List['Player']:
    list_hasnt_seen = []
    list_has_seen = player_has_seen(p, players, matrice)
    for player in players:
        if player not in list_has_seen and player!=p:
            list_hasnt_seen.append(player)
    return list_hasnt_seen
    
def find_second_impostor(dead_cm:'Player', players:List['Player'], matrice) :
    #list of suspected impostor 1
    print("\nSuspects for impostor 1 :\n")
    first_sus = player_has_seen(dead_cm, players, matrice)
    for sus in first_sus:
        print (sus.name + " 1/" + str(len(first_sus)))
    #list of suspected impostor 2
    second_sus = []
    for sus in first_sus:
        second_sus += Player_has_not_seen(sus,players,matrice)
    list_second_sus = [] #without doubles
    for sus2 in second_sus:
        if sus2 not in list_second_sus:
            list_second_sus.append(sus2)
    #counts how many times a suspect is present in the list of potential impostor 2
    print("\nSuspects for impostor 2 :\n")
    for sus in list_second_sus:
        compteur = 0
        for s in second_sus:
            if s == sus:compteur += 1
        prob = str(compteur) + "/" + str(len(second_sus))
        print(sus.name, prob)
            
def test_has_seen():
    """Method for testing the has-seen algorithm"""
    #the incidence matrix representing the has-seen-graph    
    inc_mat=np.array([[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,1,0,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,1,0,1,1,0,0,0,0,0,0],
                     [0,1,0,0,0,0,0,1,0,1,0,0,0,0,0],
                     [0,0,1,0,0,0,0,0,0,0,1,1,0,0,0],
                     [0,0,0,1,0,0,0,0,0,0,0,0,1,1,0],
                     [0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
                     [0,0,0,0,0,0,0,0,1,0,0,1,1,0,0],
                     [0,0,0,0,0,0,0,0,0,1,0,0,0,1,1]])
    players = [Player('doubleA'), Player('polo'), Player('tomus'), 
               Player('youngsamoo'), Player('jbinks'), Player('nyo'), 
               Player('jojo'), Player('clemter'), Player('paul'), Player('aladin')]
    find_second_impostor(players[0],players,inc_mat)
    
    
test_has_seen()

#changé int des matrices d'incidence en bool car 0 ou 1
#matrice en inc_mat plus explicite a faire
#modif affichage en liste triée du plus probable au moins probable a faire
#ajouter fonc qui définit scores random des joueurs
#implémenter fonc qui donne graph aléatoire