# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:41:38 2020

@author: Paul Jouet, Aladin Homsy
"""
from typing import List, Tuple
from pandas.io.parsers import read_csv
from pandas import DataFrame
import math
import csv

rooms = ["cafetaria","weapons","O2","navigation","shield","mid_room",
          "right_room","storage","electrical","lower_e","security","reactor","upper_e","medbay"]

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
    
def import_graph(graph_cm:str = "crewmate_mobility_graph.csv", graph_im:str = "impostor_mobility_graph.csv") -> Tuple[List[List[float]], List[List[float]]]:
    """
    This method imports the graphs from the csv files to a matrix

    Parameters
    ----------
    graph_cm : str, optional
        Path to the csv file containing the adjacency matrix of the mobility graph for crewmates
        The default is "crewmate_mobility_graph.csv".
    graph_im : str, optional
        Path to the csv file containing the adjacency matrix of the mobility graph for impostors
        The default is "impostor_mobility_graph.csv".

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
    
#print_all_paths_fw()
#query_path()


def display_fw_pd():
    """
    This method displays all paths using a pandas DataFrame

    Returns
    -------
    None.

    """
    mat_cm = read_csv("crewmate_mobility_graph_pd.csv", delimiter=';', index_col = 0)
    mat_im = read_csv("impostor_mobility_graph_pd.csv", delimiter=';', index_col = 0)
    floyd_warshall_pd(mat_cm)
    floyd_warshall_pd(mat_im)
    print(mat_cm, '\n', mat_im)
    
def floyd_warshall_pd(mat: DataFrame):
    """
    This method modifies the adjacency matrix, replacing the edges with the shortest path for every 
    pair of vertices, using pandas dataframes.

    Parameters
    ----------
    mat : DataFrame
        Adjacency matrix.

    Returns
    -------
    None.

    """
    for k in range(14):
        for i in range(14):
            for j in range(14):
                if mat.iloc[i,j] > mat.iloc[i,k] + mat.iloc[k,j]: 
                    mat.iloc[i,j] = mat.iloc[i,k] + mat.iloc[k,j]
        
print_all_paths_fw()


