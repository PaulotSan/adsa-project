import math
inf=math.inf

class Room():
    def __init__(self,name,connexions,vent_connexions):
        self.name=name
        self.connexions=connexions
        self.vent_connexions=vent_connexions
    def connexion(self,room2,distance):
        self.connexions.append((room2,distance))
        room2.connexions.append((self,distance))
    def vent_connexion(self,room2):
        self.vent_connexions.append(room2)
        room2.vent_connexions.append(self)
        
cafetaria=Room('cafetaria',[],[])
weapons=Room('weapons',[],[])
O2=Room('O2',[],[])
shield=Room('shield',[],[])
navigation=Room('navigation',[],[])
right_room=Room('right_room',[],[])
mid_room=Room('mid_room',[],[])
storage=Room('storage',[],[])
medbay=Room('medbay',[],[])
electrical=Room('electrical',[],[])
secutity=Room('security',[],[])
reactor=Room('reactor',[],[])
upper_e=Room('upper_e',[],[])
lower_e=Room('lower_r',[],[])
coridor_vent=Room('coridor_vent',[],[])

cafetaria.connexion(weapons,2)
cafetaria.connexion(mid_room,3)
cafetaria.connexion(medbay,2)
cafetaria.connexion(storage,3)
cafetaria.connexion(upper_e,8)
weapons.connexion(navigation,6)
weapons.connexion(O2,2)
weapons.connexion(shield,8)
weapons.connexion(coridor_vent,5)
navigation.connexion(O2,5)
navigation.connexion(shield,7)
navigation.connexion(coridor_vent,4)
shield.connexion(right_room,3)
shield.connexion(storage,5)
shield.connexion(coridor_vent,3)
shield.connexion(O2,6)
O2.connexion(coridor_vent,4)
right_room.connexion(storage,4)
storage.connexion(mid_room,3)
storage.connexion(electrical,3)
storage.connexion(lower_e,8)
electrical.connexion(lower_e,4)
lower_e.connexion(reactor,4)
lower_e.connexion(secutity,4)
lower_e.connexion(upper_e,6)
secutity.connexion(reactor,3)
secutity.connexion(upper_e,3)
upper_e.connexion(reactor,3)
upper_e.connexion(medbay,5)

cafetaria.vent_connexion(coridor_vent)
mid_room.vent_connexion(cafetaria)
coridor_vent.vent_connexion(mid_room)
weapons.vent_connexion(navigation)
navigation.vent_connexion(shield)
secutity.vent_connexion(medbay)
medbay.vent_connexion(electrical)
electrical.vent_connexion(secutity)
lower_e.vent_connexion(reactor)
reactor.vent_connexion(upper_e)

vertexes=[cafetaria,weapons,O2,shield,navigation,right_room,mid_room,storage,medbay,electrical,secutity,reactor,upper_e,lower_e,coridor_vent]

unvisited=[cafetaria,weapons,O2,shield,navigation,right_room,mid_room,storage,medbay,electrical,secutity,reactor,upper_e,lower_e,coridor_vent]
visited=[]

shortest=[]
previous=[]
for i in range(15):
    shortest.append(inf)
    previous.append(None)

tableau=[vertexes,shortest,previous]



def dijkstra(start,bol):
    if bol==True:
        shortest[vertexes.index(start)]=0
        
        
    short=1000
    index=0
    for a in shortest:#on cherche le plus petit dans shortest et qui appartient a unvisited
        if a < short and vertexes[index] in unvisited :
            a=short
            vis=index#index de celui a ajouté dans visited
        index+=1
    visited.append(vertexes[vis])#on l ajoute ds visited
    unvisited.remove(vertexes[vis])
    
    for b in vertexes[vis].connexions:
        if b[0] in unvisited:
            somme=shortest[vis]+b[1]
            if somme<shortest[vertexes.index(b[0])]:
                shortest[vertexes.index(b[0])]=somme
                previous[vertexes.index(b[0])]=vertexes[vis]
    
    if len(unvisited)>1:
        print('\nvertexes:\n')
        for i in range(15):
            print (vertexes[i].name)
        print('\nshortest:\n\n',shortest)
        
        print('\nprevious:\n')
        for i in range(15):
            if previous[i]==None:
                print(previous[i])
            else:print(previous[i].name)
        print('\nshortest:\n')
        for i in range(len(visited)):
            print(visited[i].name)
    
        dijkstra(start,False)
                
                
dijkstra(cafetaria,True )                
                
                
                
                
