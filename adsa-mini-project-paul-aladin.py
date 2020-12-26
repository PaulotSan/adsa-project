# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:41:38 2020

@authors: Paul Jouet, Aladin Homsy
"""
from typing import List, Set, Tuple, Dict
import random
import numpy as np
import math
import csv

# this list represents the rooms of the mobility graph, helps printing in a more readable way (not indexes)
rooms = ["cafetaria","weapons","O2","navigation","shield","mid_room",
          "right_room","storage","electrical","lower_e","security","reactor","upper_e","medbay"]

class Tournament():
    """
    The tournament's attributes are a datastructure containing the players, another for the games
    """
    def __init__(self, players: List['Player']):
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
     

    def dico(self, score) -> str:
        """
        Apply a dichotomic search for a score in the database, complexity is O(log(n))

        Parameters
        ----------
        score : int
            The score of the player we wish to find.

        Returns
        -------
        str 
            The name of the first player found, False if none.

        """
        d = 0
        f = len(self.players)-1 # This is O(1) complexity, because the len value is stored in the data structure in Python !
        while (f >= d):
            m = (f+d)//2
            if self.players[m].score == score : # accessing any index from a list is O(1) complexity
                return self.players[m].name 
            elif self.players[m].score < score : 
                f = m-1
            else:
                d = m+1
        return False

    def randomgames(self):
        """
        Launches a round of random games (10 games with random players, this has to be done 3 times)

        Returns
        -------
        None.

        """
        random.shuffle(self.players)
        for ten in range(10):
            game = Game(self.players[ten*10:ten*10+10])
            game.Points()
            self.games.append(game)
        fusion(self.players) #O(nlog(n)) sort (so we can still access any player with O(log(n)) complexity) 
                
    def eliminatorygames(self):
        """
        Launches a round of eliminatory games

        Returns
        -------
        None.

        """
        for i in range(1,10):
            for ten in range(10-(i-1)):
                game = Game(self.players[ten*10:ten*10+10])
                game.Points()
                self.games.append(game)
            fusion(self.players)
            for i in range(10):
                self.players.pop()
        
    
    def finals(self):
        for player in self.players : player.score = 0 # reset scores
        for i in range(5):
            game = Game(self.players)
            game.Points()
            self.games.append(game)
        fusion(self.players)
            
        
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
            
        self.crewmates = [] #list of crewmates which can be easier to manipulate in some cases
        for player in players:
            if not player.impostor: self.crewmates.append(player)
            
        Game.total_game_number += 1 #increase the total number of games static class attribute
        self.game_number = Game.total_game_number
        
    def __str__(self) -> str:
        res = '\nGame ' + str(self.game_number) + '\n\nPlayers :\n\n'
        for player in self.players:
            res += str(player) + '\n'
        res += 'Impostor 1 : ' + self.impostors[0].name
        res += '\nImpostor 2 : ' + self.impostors[1].name
        return res
    
    def Tasks_Vote_point(self,nb_done,multipl):
        """
        This method adds the points for votes and tasks to the crewmates

        """
        liste = []
        while(nb_done!=0):
            for crewmate in self.crewmates:
                ran = random.randint(1, 3)
                if ran == 1 and nb_done != 0: #means crewmate has done all tasks
                    if crewmate not in liste:
                        crewmate.score += 1 * multipl
                        liste.append(crewmate)
                        nb_done -= 1
 
    
    def Kill_cm(self, nb_dead: int):
        """
        

        Parameters
        ----------
        nb_dead : int

        Returns
        -------
        None.

        """
        liste = []
        while(nb_dead != 0):
            for crewmate in self.crewmates:
                ran = random.randint(1,3)
                if ran == 1 and nb_dead != 0: #means the crewmate has done all of his tasks
                    if crewmate not in liste:
                        crewmate.alive = False
                        liste.append(crewmate)
                        nb_dead -= 1
            
    
    
    def Points(self):
        """
        This functions attributes a score to each player of the game according to the random events in the game

        Returns
        -------
        None.

        """
        victory = random.randint(1,2)
        
        if victory == 1: #impostors win
            """print("\nImpostors Win\n")"""
            
            #then all crewmates are dead
            for crewmate in self.crewmates:
                crewmate.alive = False
                
            #impostors won : 10 points
            for impostor in self.impostors:
                impostor.score += 10
            im_alive = random.randint(1,3)
            
            if im_alive == 2: #both impostors are alive at the end of the game
            
                #simple kills
                nb_murdered = random.randint(4,7)
                max_kill_im1 = nb_murdered-1
                nb_kills_im1 = random.randint(1,max_kill_im1)
                nb_kills_im2 = nb_murdered-nb_kills_im1
                
                #undiscovered murders 
                undiscovered_murders = random.randint(0,4)#mettre moins de chance sur le 4??
                nb_spe_kills_im1 = random.randint(0,undiscovered_murders)
                if nb_spe_kills_im1 > nb_kills_im1: 
                    nb_spe_kills_im1 = nb_kills_im1
                nb_spe_kills_im2 = undiscovered_murders - nb_spe_kills_im1
                
                #attribution of points for the impostors
                points_im1 = nb_kills_im1 - nb_spe_kills_im1 + (3 * nb_spe_kills_im1)
                points_im2 = nb_kills_im2 - nb_spe_kills_im2 + (3 * nb_spe_kills_im2)
                self.impostors[0].score += points_im1
                self.impostors[1].score += points_im2
                
                #tasks fully done
                tasks = random.randint(0,7) 
                self.Tasks_Vote_point(tasks,1)
                
            else:
                #case where one impostor is dead, we decide whom
                im_dead = random.randint(0,1)
                self.impostors[im_dead].alive = False
                
                #simple kills
                nb_murdered = random.randint(4, 7)
                nb_kill_im_alive = random.randint(nb_murdered - 2, nb_murdered)
                nb_kill_im_dead = nb_murdered-nb_kill_im_alive
                
                #undiscovered murders
                undiscovered_murders=random.randint(0,3)
                
                #undiscovered murdered crewmates
                if undiscovered_murders == 3 and nb_kill_im_alive == 2:
                    nb_spe_kill_im_alive = 2
                    
                else:
                    nb_spe_kill_im_alive = 3
                    
                #attribution of the points for the impostors
                points_im_alive = nb_spe_kill_im_alive * 3 - (nb_kill_im_alive - nb_spe_kill_im_alive)
                points_im_dead = nb_kill_im_dead #no special kill for dead impostor
                self.impostors[im_dead].score += points_im_dead
                im_alive = 1 - im_dead
                self.impostors[im_alive].score += points_im_alive
                
                #tasks fully done
                tasks = random.randint(2, 7) #more possible tasks done because one impostor is dead
                self.Tasks_Vote_point(tasks,1)
                
                #vote points
                vote = random.randint(3, 8)
                self.Tasks_Vote_point(vote, 3)
                
        else: #crewmates win
            """print("\nCrewmates Win")"""
            for crewmate in self.crewmates:
                crewmate.score += 5
            win_crewmates = random.randint(0,10)
            
            if win_crewmates <= 7:
                """print("by killing all Impostors\n")"""
                
                #2 impostors are dead
                self.impostors[0].alive = False
                self.impostors[1].alive = False
                
                #simple_kills points impostors
                dead_crewmates = random.randint(1,5)
                nb_kills_im1 = random.randint(0,dead_crewmates)
                self.impostors[0].score += nb_kills_im1
                self.impostors[1].score += dead_crewmates-nb_kills_im1
                
                #dead cm
                self.Kill_cm(dead_crewmates)
                
                #first vote to kill impostor
                dead_cm_first_time = random.randint(0, dead_crewmates)
                vote = random.randint(3, 8 - dead_cm_first_time)
                self.Tasks_Vote_point(vote, 3)
                
                #second vote to kill impostor
                vote = random.randint(3, 8 - dead_crewmates)
                self.Tasks_Vote_point(vote, 3)
                
                #tasks point
                tasks = random.randint(1, 6) 
                self.Tasks_Vote_point(tasks, 1)
                
            else:
                """print("by doing all tasks\n")"""
                #all tasks done
                self.Tasks_Vote_point(8, 1)
                
                #dead cm
                dead_crewmates = random.randint(0, 4)
                self.Kill_cm(dead_crewmates)
                
                #one impostor dead
                im_is_dead = random.randint(1, 2)
                if im_is_dead == 1:
                    deadim = random.randint(0, 1)
                    self.impostors[deadim].alive = False
                    
                    #points for voting impostor
                    cm_vote_im = random.randint(5, 7)
                    self.Tasks_Vote_point(cm_vote_im, 3)
    
    def graph_has_seen(self) -> Set[Tuple['Player','Player']]:
        """

        Returns a set of tuples each containing 2 Player objects
        -------
        This method uses the list of players to define random connexions between each player. 
        It returns a graph in the form of a set containing tuples for each 'have seen' relation between players

        """
        
        def list_players_seen(players: List['Player']) -> List['Player']:
            """
            This function defines the number of occurences of each player in the graph

            Parameters
            ----------
            players : List['Player']
                List of players in the game

            Returns
            -------
            l : list(Player)
                Returns a list of players, in which they appear as often as they have seen another player

            """
            l = []
            for i in range(10):
                r = random.randint(2,5)
                for a in range(r):
                    l.append(players[i])
            if len(l) % 2 != 0:
                l.append(players[0])
            return l
    
        occ = list_players_seen(self.players)
        seen_graph = set()
        cpt = 0 #this counter will help in case we have a never ending loop
        #for example, if the last 2 players in the occurrences list are already linked in the graph
        #the algorithm will try at most 100 times to put them into the set, and then move on
        
        while(len(occ) != 0 and cpt < 100): #we stop either when the list of occurrences is empty, or the counter reaches 100
            a = random.randint(0,len(occ)-1)
            b = random.randint(0,len(occ)-1) #we pick 2 random players from the list
            if occ[a] != occ[b] and not (occ[a] in self.impostors and occ[b] in self.impostors): 
                #since each player appears multiple times in the occurrences list, 
                #we have to check whether the 2 players picked are different
                #we also have to check if the 2 players are both impostors as they cannot meet
                relation = (occ[a], occ[b])
                rev_relation = (occ[b], occ[a]) #since (a,b) != (b,a) we have to check for both relations to avoid redondoncies
                if (relation not in seen_graph) and (rev_relation not in seen_graph):
                    seen_graph.add(relation)
                    occ.remove(occ[a])
                    if b > a: occ.remove(occ[b-1])
                    else: occ.remove(occ[b])
                else: cpt += 1
            else: cpt += 1
            
        #for relation in seen_graph:
        #    print (relation[0].name, relation[1].name)  ### FOR TESTING ###
            
        return seen_graph
    
    def mat_has_seen(self) -> List[List[bool]]:
        """
        

        Returns
        -------
        List[List[bool]]
            The incidence matrix for the graph 'has seen'

        """
        seen_graph = self.graph_has_seen()
        inc_mat = np.zeros((10, len(seen_graph)))
        nb_j = 0
        for relation in seen_graph:
            inc_mat[self.players.index(relation[0]), nb_j] = 1
            inc_mat[self.players.index(relation[1]), nb_j] = 1
            nb_j += 1
        return inc_mat
    
    def player_has_seen(self, p: 'Player', inc_mat: List[List[bool]]) -> Tuple[List['Player'], List['Player']]:
        """
        This method returns the list of players one has seen according to the incidence matrix, along
        with the list of players he has not seen.
    
        Parameters
        ----------
        p : 'Player'
            The player whom we want to know who he saw.
        players : List['Player']
            The list of players in the game.
        inc_mat : List[List[bool]]
            The incidence matrix representing the 'has seen' graph.
    
        Returns
        -------
        list_has_seen : List['Player']
            The list of players seen by p.
        list_not_seen : List['Player']
            The list of players not seen by p.
    
        """
        #define on which line of the incidence matrix the player is
        line_p = 0
        for i in range(10):
            if p == self.players[i]: line_p = i
            
        list_has_seen = []
        for index_c in range(len(inc_mat[0])): #the incidence matrix has dimension 0 of length 10 but variable dimension 1 (number of relations)
            if inc_mat[line_p, index_c] == 1:
                for index_l in range(10):
                    if index_l != line_p and inc_mat[index_l, index_c] == 1: 
                        list_has_seen.append(self.players[index_l])
             
        list_not_seen = []
        for player in self.players:
            if player not in list_has_seen and player != p:
                list_not_seen.append(player)
        return list_has_seen, list_not_seen
    
    def probable_impostors(self, dead_cm: 'Player', inc_mat: List[List[bool]]) -> Dict['Player', float]:
        """
        

        Parameters
        ----------
        dead_cm : 'Player'
            The dead crewmate.
        inc_mat : List[List[bool]]
            The incidence matrix.

        Returns
        -------
        probs : Dict['Player', float]
            A dictionnary with player as key and its probability of being impostor as value
        """
        probs = {player:0 for player in self.players}
        
        first_suspects = self.player_has_seen(dead_cm, inc_mat)[0] #list of players having seen the dead cm, therefore potential first impostor
        second_suspects_occ = [] #list of suspects for impostor 2
        for suspect in first_suspects:
            probs[suspect] += 1/len(first_suspects)
            for suspect2 in self.player_has_seen(suspect, inc_mat)[1]: 
                second_suspects_occ.append(suspect2) #we add each player not seen by the current suspect to the second_suspect_occ list
            #each player will appear as much times as there are suspects he has not seen
            
        for suspect2 in second_suspects_occ: 
            probs[suspect2] += 1/len(second_suspects_occ)
            
        impostor_probabilities = {player: probs[player] for player in sorted(probs, key=probs.get, reverse=True)}
        
        print("\nThe first crewmate who died in our scenario is", dead_cm.name, "who had seen :\n")
        for s in first_suspects:
            print (s.name)
            
        print("\nThe most probable impostors are therefore (with their probabilities) :\n")
        
        for p in impostor_probabilities.keys():
            print (p.name, impostor_probabilities[p])
            
        return impostor_probabilities
    
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
        res += ", current score : " + str(self.score)
        return res
    
def fusion(l: List['Player']):
    """
    A divide and conquer algorithm for sorting our player list

    Parameters
    ----------
    l : List[Player]
        The list of players.

    Returns
    -------
    None.

    """
    n = len(l) # O(1)

    # stop condition
    if n > 1:
        # split into 2 sub lists
        milieu = n // 2
        liste_gauche = l[0:milieu]
        liste_droite = l[milieu:n]
        # sort sub lists
        fusion(liste_gauche)
        fusion(liste_droite)

        # merge lists
        indice_liste = indice_gauche = indice_droite = 0

        while indice_gauche < len(liste_gauche) and indice_droite < len(liste_droite):
            if liste_gauche[indice_gauche].score > liste_droite[indice_droite].score:
                l[indice_liste] = liste_gauche[indice_gauche]
                indice_gauche += 1
            else:
                l[indice_liste] = liste_droite[indice_droite]
                indice_droite += 1
            indice_liste +=1

        while indice_gauche < len(liste_gauche):
            l[indice_liste] = liste_gauche[indice_gauche]
            indice_gauche +=1
            indice_liste += 1

        while indice_droite < len(liste_droite):
            l[indice_liste] = liste_droite[indice_droite]
            indice_droite += 1
            indice_liste += 1
        
### STEP 3 ###

def Floyd_warshall(mat: List[List[float]]):
    """
    This method modifies the adjacency matrix, replacing the edges with the shortest path for every 
    pair of vertices.

    Parameters
    ----------
    mat : List[List[float]]
        Adjacency matrix.

    Returns
    -------
    None.

    """
    for k in range(14):
        for i in range(14):
            for j in range(14):
                if mat[i][j] > mat[i][k] + mat[k][j]: 
                    mat[i][j] = mat[i][k] + mat[k][j]
    
def import_graph(graph_cm:str = "graphs/crewmate_mobility_graph.csv", graph_im:str = "graphs/impostor_mobility_graph.csv") -> Tuple[List[List[float]], List[List[float]]]:
    """
    This method imports the graphs from the csv files to a matrix

    Parameters
    ----------
    graph_cm : str, optional
        Path to the csv file containing the adjacency matrix of the mobility graph for crewmates
        The default is "graphs/crewmate_mobility_graph.csv".
    graph_im : str, optional
        Path to the csv file containing the adjacency matrix of the mobility graph for impostors
        The default is "graphs/impostor_mobility_graph.csv".

    Returns
    -------
    Tuple[List[List[float]], List[List[float]]]
        Returns the matrixes as a list of lists of float values.

    """
    mat_cm = []
    mat_im = []
    
    with open(graph_cm, newline='') as cm_csv:
        reader = csv.reader(cm_csv, delimiter=';')
        for row in reader:
            mat_cm.append(row)
            for element in range(len(row)):
                if row[element] == 'inf':
                    row[element] = math.inf
                else:
                    row[element] = float(row[element])
                
    with open(graph_im, newline='') as im_csv:
        reader = csv.reader(im_csv, delimiter=';')
        for row in reader:
            mat_im.append(row)
            for element in range(len(row)):
                row[element] = float(row[element])
                
                
    return (mat_cm, mat_im)


def print_all_paths_fw():
    
    
    mat_cm, mat_im = import_graph()
    Floyd_warshall(mat_cm) 
    Floyd_warshall(mat_im)
    
    for i in range(14):
        for j in range(14):
            print(rooms[i],rooms[j],'\nfor crewmates :', 
                  mat_cm[i][j],'seconds\nfor impostors :', mat_im[i][j],'seconds\n')

def query_path():
    """
    Asks the user for 2 rooms and displays the shortest time between those rooms
    """
    mat_cm, mat_im = import_graph()
    Floyd_warshall(mat_cm) 
    Floyd_warshall(mat_im)
    
    print("Type index of first room, then second")
    for i in range(14):
        print(i, ":", rooms[i])
    a = int(input("From : "))
    b = int(input("To : "))
    
    print("For a crewmate it takes", mat_cm[a][b], "seconds")
    print("For an impostor it takes", mat_im[a][b], "seconds")
    
### END STEP 3 ###

### STEP 4 ###

def hamilton_path() -> List[List[int]]:
    """
    This method returns the list of all Hamilton paths, using a recursive depth first search with backtracking

    Returns
    -------
    hamilton_paths : List[List[int]]
        The list of all hamilton paths

    """
    adj_mat = import_graph()[0] # we use the crewmate mobility matrix
    stack = [] # the list (used as a stack) which will contain the path
    hamilton_paths = []
    
    def recursion_hamilton(start: int):
        """
        The recursive part of the method, for each node we explore all adjacent nodes which have not yet been
        explored, adding them to a stack, when the stack is full (it has n elements, the number of nodes), we 
        add the path to hamilton_paths.

        Parameters
        ----------
        start : int
            the current node.

        Returns
        -------
        None.

        """
        if len(stack) == len(adj_mat):
            hamilton_paths.append(stack[:])
            stack.pop()
            
        else:
            for j in range(len(adj_mat[start])):
                if adj_mat[start][j] > 0 and adj_mat[start][j] < math.inf and j not in stack:
                    stack.append(j)
                    recursion_hamilton(j)
            stack.pop()
            
    for i in range(len(adj_mat)):
        stack.append(i)
        recursion_hamilton(i)
    return hamilton_paths
 
      
def shortest_hamilton(paths: List[List[int]], adj_mat: List[List[float]]) -> Tuple[List[int], float, int]:
    """
    This method uses the list of all hamiltonian paths, with the adjacence matrix used to compute them, and 
    returns the first shortest path, its length, and the number of paths having the same length (other shortest)

    Parameters
    ----------
    paths : List[List[int]]
        Rooms are denoted by their corresponding integer.
    adj_mat : List[List[float]]
        Adjacence matrix of the mobility graph.

    Returns
    -------
    Tuple[List[int], float, int]
        Tuple containing a shortest hamiltonian path, its length and the number of paths of equal length

    """
    shortest_time = math.inf
    shortest_path = None
    cpt=1
    
    def path_length(path: List[int]) -> float:
        """
        Sub-function which returns the length of a path

        Parameters
        ----------
        path : List[int]
            the path described as a list of integers (representing the rooms).

        Returns
        -------
        float
            length in seconds/centimeters.

        """
        length = 0
        for i in range(len(path)-1):
            length += adj_mat[path[i]][path[i+1]]
        return length
    
    for path in paths:
        path_len = path_length(path)
        if path_len < shortest_time:
            shortest_time = path_len
            shortest_path = path
            cpt=1
        if path_len == shortest_time:
            cpt+=1
            
    return shortest_path, shortest_time, cpt

### END STEP 4 ###

def Main():
    """
    Main method for demonstrating the features of our program.

    Returns
    -------
    None.

    """
    again = True
    while (again):
    
        # Menu
        print("\nWhich feature should we try ?")
        print(" 1 : Tournament")
        print(" 2 : Set of probable impostors")
        print(" 3 : Time to travel between any pair of room")
        print(" 4 : How to secure last tasks")  
        
        """
        #notes
        #dans 1 mettre l option de voir tt ce qui s est passé
        
        """
        choice = int(input())
        
        # Tournament
        if choice == 1:
            print("\nThe Among Us tournament has officially started !!!")
            players = []
            for i in range(100):
                player_name = 'player' + str(i+1)
                players.append(Player(player_name))
            tournament = Tournament(players)
            
            tournament.randomgames()
            print(tournament)
            print("\nHere we simply created a tournament, and launched the first 10 random games to get a first leaderboard.")
            print("We printed the details for all games. As there will be more and more games, we will not continue doing "+
                  "so, but they are available in the 'games' attribute of the tournament. We did not optimize "+
                  "this part of the tournament object as it was not required, but helps visualize what is happening")
            
            print("\nLet us now play the 2 next random games to see our leaderboard before eliminatory games !")
            
            tournament.randomgames()
            tournament.randomgames()
            
            print("\nDone !\n\nWould you like to see the leaderboard now ?\n1 for yes, 2 for no")
            if int(input()) == 1:
                for player in players : print(player.name,"has scored",player.score,"points")
                
                print("\nWould you like trying to find a player using his score ?")
                print("\n1 for yes, 2 for no")
                if int(input()) == 1:
                    print("\nEnter the score of the player you want to check")
                    x = int(input())
                    playername = tournament.dico(x)
                    if playername == False : playername = "... not in this list because no one has this score"
                    print("\nA player with a score of",x,"is",playername)
            
            tournament.eliminatorygames()
            print("\nNow the eliminatory games have been played, do you want to see the 10 remaining players?")
            print("\n1 for yes, 2 for no")
            if int(input()) == 1:
                for player in players : 
                    print(player.name,"score :", str(player.score))
                
            print("\n\nLet us now play the finals, we reset the scores and play 5 last games with our 10 remaining players !")
            tournament.finals()
            
            print("\nGame details :\n\n")
            for i in range(5):
                print(tournament.games[-5+i])
            
            # winners
            print("\n\nHere are the winners !\n")
            for i in range(3):
                print("n°",i+1,players[i].name,"with a score of",str(players[i].score))
            
            print("\nWould you like to try another part of the project ?")
            print("\n1 : Yes , 2 : No")
            if int(input()) == 2 : again = False
            
        
        # Set of probable impostors
        if choice == 2:
            print("Let's create a game between our most famous ESILV teachers ! (this list is non-exhaustive)")
            bestTeachers = [Player('M.Peretti'), Player('Mme.Thai'), Player('M.Chendeb'), 
                   Player('M.Gossard'), Player('M.Clain'), Player('M.Bertin'), 
                   Player('M.Sart'), Player('M.Ghassany'), Player('M.He'), Player('M.Courbin')]
            print("The players are :\n")
            for teacher in bestTeachers:
                print(teacher.name)
            game = Game(bestTeachers)
            random_dead_idx = random.randint(0,7) # we choose a random crewmate to die
            
            dead_cm = game.crewmates[random_dead_idx]
            inc_mat = game.mat_has_seen()
            
            print("\nThe following incidence matrix represents the relation of seeing each other for players (rows in the order they were presented)\n")
            print(inc_mat)
            
            game.probable_impostors(dead_cm, inc_mat)
            
            
            print("\nWould you like to try another part of the project ?")
            print("\n1 : Yes , 2 : No")
            if int(input()) == 2 : again = False
        
        # Time to travel any pair of rooms
        if choice == 3:
            query_path()
            
            print("Would you like to print the adjacency matrixes for crewmates and impostors ?")
            print("\n1 : Yes , 2 : No")
            if int(input()) == 1 :
                mat_cm, mat_im = import_graph()
                print("\nThis is the original graph (as an adjacency matrix) for crewmate mobility :\n\n" + str(mat_cm))
                print("\nThis is the original graph (as an adjacency matrix) for impostor mobility :\n\n" + str(mat_im))
                
                Floyd_warshall(mat_cm)
                Floyd_warshall(mat_im)
                
                print("\nThis is the new graph (as a matrix representing the time to travel between any pair of rooms) for crewmates :\n\n" + str(mat_cm))
                print("\nThis is the new graph (as a matrix representing the time to travel between any pair of rooms) for impostors :\n\n" + str(mat_im))
            
            print("\nWould you like to try another part of the project ?")
            print("\n1 : Yes , 2 : No")
            if int(input()) == 2 : again = False
        
        #last tasks
        if choice == 4:
            
            paths = hamilton_path()
            print("There are " + str(len(paths)) + " Hamiltonian paths in the crewmates' mobility graph..." +
                  "\nWe will not print them all but let's try to find the shortest !\n")
            
            """
            for path in paths:
                print(path)
                for room in path:
                    print(rooms[room])
            """
            
            short_path = shortest_hamilton(paths, import_graph()[0])
            
            print("We have computed the shortest path, in room number it looks like :\n" + str(short_path[0]) +
                  ",\nthe corresponding room names however are :\n\n")
            
            for room in short_path[0]:
                print(rooms[room])
                
            print("\nIts length is " + str(short_path[1]) + ", but there are actually " + str(short_path[2]) + " paths that short !")
            
            print("\nWould you like to try another part of the project ?")
            print("\n1 : Yes , 2 : No")
            if int(input()) == 2 : again = False  
       
"""
Some test functions we used throughout the project
The test_has_seen function uses the example provided in the subject of the project ! We obtain the same
results as in our theoretical approach provided in the report
"""
def test_game():
    players = [Player('doubleA'), Player('polo'), Player('tomus'), 
               Player('youngsamoo'), Player('jbinks'), Player('nyo'), 
               Player('jojo'), Player('clemter'), Player('paul'), Player('aladin')]
    game1 = Game(players)
    game2 = Game(players)
    print(game1) #la partie est bien crée, et 2 imposteurs sont choisis aléatoirement
    print(game2)
    
def test_points():
    """
    Method for testing the points attribution between players in a game

    Returns
    -------
    None.

    """
    players = [Player('doubleA'), Player('polo'), Player('tomus'), 
               Player('youngsamoo'), Player('jbinks'), Player('nyo'), 
               Player('jojo'), Player('clemter'), Player('paul'), Player('aladin')]
    game = Game(players)
    
    game.Points()
    for player in game.players:
        print("Impostor :", player.impostor, player.name, player.score)
    
def test_tournament():
    players = []
    for i in range(100):
        player_name = 'player' + str(i+1)
        players.append(Player(player_name))
    tournament = Tournament(players)
    tournament.Start()
    print(tournament)
    

# test function for computing the probability for each player of being an impostor in the example given
def test_has_seen():
    """
    Method for testing the has-seen algorithm
    """
    
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
    game = Game(players)
    game.probable_impostors(players[0], inc_mat)
  

def test_random_has_seen():
    """
    Test function for generating a random first kill and random connexions between the players, 
    and then computing players' probability of being impostor
    """
    players = [Player('doubleA'), Player('polo'), Player('tomus'), 
               Player('youngsamoo'), Player('jbinks'), Player('nyo'), 
               Player('jojo'), Player('clemter'), Player('paul'), Player('aladin')]
    game = Game(players)
    inc_mat = game.mat_has_seen()
    print(inc_mat,"\n")
    random_dead_idx = random.randint(0,7) # we choose a random crewmate to die
    dead_cm = game.crewmates[random_dead_idx]
    
    game.probable_impostors(dead_cm, game.mat_has_seen())
    
def test_tournament2():
    players = []
    for i in range(100):
        player_name = 'player' + str(i+1)
        players.append(Player(player_name))
    tournament = Tournament(players)
    #3random games
    tournament.randomgames()
    #organise players
    fusion(players)
    #eliminative games
    tournament.eliminatorygames()
    #finals
    tournament.finals()
    #winners
    fusion(players)
    print("Here are the winners!!!")
    for i in range(3):
        print(players[i].name,"with a score of:",players[i].score)
    

    
Main() 