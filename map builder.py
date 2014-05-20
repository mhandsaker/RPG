import time, random, pygame, io, sys, pickle
from pygame.locals import *

tileset = {"0":pygame.image.load("Tiles/grass.bmp"),\
           "1":pygame.image.load("Tiles/road.bmp"),\
           " ":pygame.image.load("Tiles/black.bmp"),\
           "2":pygame.image.load("Tiles/water.png")\
           }

featureset = {"x":pygame.image.load("Tiles/bush.png"),\
              "0":pygame.image.load("Tiles/blank.png"),\
              }


loc = "Worlds/grassyarea.txt"
loc2 ="Worlds/grassyare.txt"
oldloc = loc

window = pygame.display.set_mode((1280, 720))
#window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
pygame.display.set_caption('Tile Based RPG')


def mapbuild(loc, MAP):
    x = 0
    y = 0
    world = io.open(loc, 'r')
    worldlines = []
    iterator = 1
    while iterator <= 45:
        worldlines.append(world.readline())
        iterator = iterator + 1
    for line in worldlines:
        if len(line) > 80:
            line = line[0:80]
        for char in line:
            window.blit(tileset[char], (x, y))
            #Draw Tile at x, y. Aka, put image in.
            x = x + 16 #Assuming sixteen x sixteen pixel tiles currently; maybe scale up to 32?
        MAP.append(line) 
        x = 0
        y = y + 16
    world.close()
MAP = []
editline = []
newtile = 3
x=0
y=0
z=''
worldlines = []
worldline = []
mapbuild(loc, MAP)
char = 5


def mapedit(MAP,x,y):
    line = MAP[y-1]
    for char in line:
        editline.append(int(char))
    print"what new tile"
    newtile = input()
    editline.pop(x-1)
    editline.insert(x-1, newtile)
    z=''
    for i in editline:
        z=z+str(i)
    MAP[y-1] = z
    world = io.open(loc2, 'w')
    pickle.dump(MAP, world)
    world.close()
    print editline
    print z
        
    
mapedit(MAP,3,1)
print MAP
##while 1:
##    for event in pygame.event.get():
##        if event.type == QUIT:
##            pygame.quit()
##            sys.exit()
##        if event.type == MOUSEBUTTONDOWN:
##            world = io.open(loc, 'r')
##            iterator = 1
##            while iterator <= 45:
##                worldlines.append(world.readline())
##                iterator = iterator + 1
##            worldline = worldlines[(event.pos[1]/16)+1]
##            print worldline[(event.pos[0]/16)+1]
    
        
        
##    mapbuild(loc)
##    pygame.display.update()
