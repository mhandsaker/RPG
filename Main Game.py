import time, random, pygame, io, sys, pickle, pygame.mixer
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (120, 0, 255)
YELLOW = (255, 255, 0)

pygame.mixer.music.load("Sounds/theme1.wav")

classes = {"player":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":10, "LCK":0},\
           "ezra":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":5, "LCK":0},\
           "rat":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":5, "LCK":0},\
           "spider":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":5, "LCK":0},\
           "wild dog":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":5, "LCK":0},\
           "moose":{"HP":15, "STR":10, "SKL":10, "DEF":10, "MAG":10, "SPE":10, "LCK":0}}
            
weapons = {"bronze sword":{"pwr":5,"acc":90,"crit":8,"effect":"none","wclass":"SWD","uses":50},\
           "iron sword":{"pwr":8,"acc":90,"crit":10,"effect":"none","wclass":"SWD","uses":35},\
           "bronze spear":{"pwr":4,"acc":100,"crit":5,"effect":"none","wclass":"SPR","uses":50},\
           "bronze axe":{"pwr":7,"acc":75,"crit":5,"effect":"none","wclass":"AXE","uses":50},\
           "basic wind tome":{"pwr":5,"acc":100,"crit":5,"effect":"none","wclass":"MAG","uses":50},\
           "shortbow":{"pwr":200,"acc":85,"crit":10,"effect":"none","wclass":"BOW","uses":50},\
           "bite":{"pwr":3,"acc":95,"crit":2,"effect":"none","wclass":"ANM","uses":-1}}


tileset = {"0":pygame.image.load("Tiles/grass.bmp"),\
           "r":pygame.image.load("Tiles/road.bmp"),\
           " ":pygame.image.load("Tiles/black.bmp"),\
           "2":pygame.image.load("Tiles/water.png"),\
           "s":pygame.image.load("Tiles/sand.png"),\
           "1":pygame.image.load("Tiles/dirtroad.bmp"),\
           "w":pygame.image.load("Tiles/woodfloor.png")\
           }

featureset = {"x":pygame.image.load("Tiles/bush.png"),\
              "0":pygame.image.load("Tiles/blank.png"),\
              "3":pygame.image.load("Tiles/tree1.png"),\
              "4":pygame.image.load("Tiles/tree2.png"),\
              "5":pygame.image.load("Tiles/tree3.png"),\
              "6":pygame.image.load("Tiles/tree4.png"),\
              "I":pygame.image.load("Tiles/Inn1.bmp"),\
              "z":pygame.image.load("Tiles/blank.png"),\
              "b":pygame.image.load("Tiles/bed.png"),\
              "c":pygame.image.load("Tiles/counter.png"),\
              "k":pygame.image.load("Tiles/shopkeeper.png")\
              }

tilepassset = [" ", "2"]

featurepassset = ["x", "I", "z", "c"]

locset = {"grassyarea":["Worlds/grassyarea.txt","Worlds/grassyareafeatures.txt"],\
          "town":["Worlds/town.txt","Worlds/townfeatures.txt"],\
          "grassyarea2":["Worlds/grassyarea2.txt","Worlds/grassyareafeatures2.txt"],\
          "grassyarea3":["Worlds/grassyarea2.txt","Worlds/grassyareafeatures3.txt"],\
          "lake1":["Worlds/lake1.txt","Worlds/lake1features.txt"],\
          "lake2":["Worlds/lake2.txt","Worlds/lake2features.txt"],\
          "lake3":["Worlds/lake3.txt","Worlds/lake3features.txt"],
          "inn1":["Worlds/inn1.txt","Worlds/innfeatures1.txt"],\
          "shop":["Worlds/shop.txt","Worlds/shopfeatures.txt"]\
          }
WORLDMAP = [["grassyarea2","grassyarea3"],\
            ["grassyarea","town"],\
            ["lake1","lake2","lake3"]\
            ]


pdir = {"u":False,\
        "d":False,\
        "l":False,\
        "r":False}




##NOTE: I removed fullscreen for the purposes of right now because it doesn't work on my or jared's computer reliably
##We can add it back in later.
##
window = pygame.display.set_mode((1280, 720))
#window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
pygame.display.set_caption('Tile Based RPG')

action = False

loc = "grassyarea"
oldloc = loc
basicFont = pygame.font.SysFont(None, 48)

def cube(x):
    return x * x * x

class character:
    lvl = 0
    exp = 0
    name = ""
    stats = {'HP':0,'SKL':0,'STR':0,'DEF':0,'LCK':0,'MAG':0,'SPE':0}
    bonus = {'HP':0,'SKL':0,'STR':0,'DEF':0,'LCK':0,'MAG':0,'SPE':0}
    classname = ''
    inv = []
    equip = []
    status = "none"
    kills = 0
    def __init__(self, name, classname, level):
        self.name = name
        self.classname = classname
        self.lvl = level
        self.stats = {'HP':0,'SKL':0,'STR':0,'DEF':0,'LCK':0,'MAG':0,'SPE':0}
        self.bonus = {'HP':0,'SKL':0,'STR':0,'DEF':0,'LCK':0,'MAG':0,'SPE':0}
        self.inv = []
        self.equip = []
        self.statcalc()
        self.exp = level * level * level
        self.lvl = self.lvl * 1.0

    def statcalc(self):
        for x in self.stats:
            if x == 'HP':
                self.stats[x] = ((self.lvl * classes[self.classname][x]) / 10) + 15
            else:
                self.stats[x] = ((self.lvl * classes[self.classname][x]) / 10) + 5
    def summary(self):
        window.fill((0,0,0))
        println(self.name.upper() + ":", 0, 0)
        println("Level " + str(self.lvl) + " " + self.classname, 0 , 48)
        println( "STATS:",0,96)
        println( "Health: " + str(self.stats["HP"] + self.bonus["HP"]) + "/" + str(self.stats["HP"]), 0 , 142)
        println( "Skill: " + str(self.stats["SKL"] + self.bonus["SKL"]) , 0, 190)
        println( "Strength: " + str(self.stats["STR"] + self.bonus["STR"]), 0 , 238)
        println( "Defense: " + str(self.stats["DEF"] + self.bonus["DEF"]), 0 , 286)
        println( "Magic: " + str(self.stats["MAG"] + self.bonus["MAG"]) , 0 , 334)
        println( "Speed: " + str(self.stats["SPE"] + self.bonus["SPE"]), 0, 382)
        println( "Luck: " + str(self.stats["LCK"] + self.bonus["LCK"]), 0, 430)
        println( "INVENTORY:", 0, 478)
        for i in self.inv:
            println( "- " + i.name.title() + " " + str(i.uses) + "/" + str(weapons[i.name]["uses"]) + ".", 0, 526)

        
    
class weapon:
    wclass = '' #SWD, MAG, BOW, SPR, AXE
    pwr = 0
    acc = 0
    crit = 0
    effect = "none"
    name = ''
    uses = 0 #Number of times you can use a weapon before it breaks. You can repair weapons to make them last longer.
    def __init__(self,name):
        self.name = name
        self.pwr = weapons[self.name]["pwr"]
        self.acc = weapons[self.name]["acc"]
        self.crit = weapons[self.name]["crit"]
        self.effect = weapons[self.name]["effect"]
        self.uses = weapons[self.name]["uses"]
        self.wclass = weapons[self.name]["wclass"]


def mapbuild(loc):
    x = 0
    y = 0
    world = io.open(locset[loc][0], 'r')
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
        x = 0
        y = y + 16
    world.close()
    x = 0
    y = 0
    world = io.open(locset[loc][1], 'r')
    worldlines = []
    iterator = 1
    while iterator <= 45:
        worldlines.append(world.readline())
        iterator = iterator + 1
    for line in worldlines:
        if len(line) > 80:
            line = line[0:80]
        for char in line:
            window.blit(featureset[char], (x, y))
            #Draw Tile at x, y. Aka, put image in.
            x = x + 16 #Assuming sixteen x sixteen pixel tiles currently; maybe scale up to 32?
        x = 0
        y = y + 16
    world.close()




def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def pointInsideRect2(x, y, rect):
    if x > rect[0] and x < (rect[0] + rect[2]) and y > rect[1] and y < (rect[1] + rect[3]):
        return True
    return False
    
def println(text, x, y, color=(0,0,0)):
    label = basicFont.render(str(text), 1, color)
    window.blit(label, (x,y))

class item:
    name = ""

    def __init__(self, name):
        self.name = name

def passtest(a,b,loc):
    x=0
    y=0
    world = io.open(locset[loc][0], 'r')
    worldlines = []
    iterator = 1
    while iterator <= 45:
        worldlines.append(world.readline())
        iterator = iterator + 1
    for line in worldlines:
        if len(line) > 80:
            line = line[0:80]
        for char in line:
            if a == x and b == y:
                if char in tilepassset:
                    return False
            x = x + 16
        x = 0
        y = y + 16
    x=0
    y=0
    world = io.open(locset[loc][1], 'r')
    worldlines = []
    iterator = 1
    while iterator <= 45:
        worldlines.append(world.readline())
        iterator = iterator + 1
    for line in worldlines:
        if len(line) > 80:
            line = line[0:80]
        for char in line:
            if a == x and b == y:
                if char in featurepassset:
                    return False
            x = x + 16
        x = 0
        y = y + 16
    else:
        return True    


def status(player, loc, locx, locy, playerx, playery, inbuilding):
    inventory = []
    equip = []
    menu = "status"
    while 1:
        while menu == "status":
            window.fill((0, 0, 0))
            pygame.draw.rect(window, WHITE, (0, 0, 1280, 50))
            pygame.draw.rect(window, BLACK, (0, 0, 300, 50))
            println("STATUS", 10, 10, WHITE)
            println("EQUIP", 310, 10)
            println("STATS:", 10, 60, WHITE)
            println("LEVEL: " + str(player.lvl), 10, 100, WHITE)
            println("HP: " + str(player.stats["HP"] + player.bonus["HP"]) + "/" + str(player.stats["HP"]), 10, 140, WHITE)
            println("SKILL: " + str(player.stats["SKL"] + player.bonus["SKL"]), 10, 180, WHITE)
            println("STRENGTH: " + str(player.stats["STR"] + player.bonus["STR"]), 10, 220, WHITE)
            println("DEFENSE: " + str(player.stats["DEF"] + player.bonus["DEF"]), 10, 260, WHITE)
            println("MAGIC: " + str(player.stats["MAG"] + player.bonus["MAG"]), 10, 300, WHITE)
            println("SPEED: " + str(player.stats["SPE"] + player.bonus["SPE"]), 10, 340, WHITE)
            println("LUCK: " + str(player.stats["LCK"] + player.bonus["LCK"]), 10, 380, WHITE)
            println("KILLS: " + str(player.kills), 10, 420, WHITE)
            pygame.draw.rect(window, WHITE, (10, 540, 620, 80))
            pygame.draw.rect(window, WHITE, (650, 540, 620, 80))
            println("SAVE", 20, 570, BLACK)
            println("LOAD", 660, 570, BLACK)
            pygame.draw.rect(window, WHITE, (10, 630, 1260, 80))
            println("RETURN TO GAME", 20, 660)
        
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if pointInsideRect2(event.pos[0], event.pos[1], (10, 540, 620, 80)):
                        picklelist = [player, loc, locx, locy, playerx, playery, inbuilding]
                        savefile = open("Slots/" + slot + ".txt", 'w')
                        pickle.dump(picklelist, savefile)
                        savefile.close()
                        print "Saved"
##                    if pointInsideRect2(event.pos[0], event.pos[1], (650, 540, 620, 80)):
##                        check = True
##                        while check:
##                            window.fill((0,0,0))
##                            println("Which slot would you like to load?", 25, 25, (255, 255, 255))
##                            pygame.draw.rect(window, (180, 180, 180), (25, 320, 1230, 80))
##                            pygame.draw.rect(window, (180, 180, 180), (25, 420, 1230, 80))
##                            pygame.draw.rect(window, (180, 180, 180), (25, 520, 1230, 80))
##                            println("SLOT 1", 45, 350)
##                            println("SLOT 2", 45, 450)
##                            println("SLOT 3", 45, 550)
##                            for event in pygame.event.get():
##                                if event.type == QUIT:
##                                    pygame.quit()
##                                    sys.exit()
##                                if event.type == MOUSEBUTTONDOWN:
##                                    if pointInsideRect2(event.pos[0], event.pos[1], (25, 320, 1230, 80)):
##                                        saveslot = "slot1"
##                                    if pointInsideRect2(event.pos[0], event.pos[1], (25, 420, 1230, 80)):
##                                        saveslot = "slot3"
##                                    if pointInsideRect2(event.pos[0], event.pos[1], (25, 520, 1230, 80)):
##                                        saveslot = "slot3"
##                                    if clicked:
##                                        savefile = open("Slots/" + saveslot + ".txt")
##                                        (player, locx, locy, playerx, playery) = pickle.load(savefile)
##                                        savefile.close()
##                                        check = False
##                            pygame.display.update()
##                            clock.tick(30)
                    if pointInsideRect2(event.pos[0], event.pos[1], (10, 630, 1260, 80)):
                        return player, locx, locy, playerx, playery
                    if pointInsideRect2(event.pos[0], event.pos[1], (300, 0, 300, 50)):
                        menu = "equip"
        
        
        while menu == "equip":
            items = []
            items2 = []
            window.fill((0, 0, 0))
            pygame.draw.rect(window, WHITE, (0, 0, 1280, 50))
            pygame.draw.rect(window, BLACK, (300, 0, 300, 50))
            println("STATUS", 10, 10)
            println("EQUIP", 310, 10, (255, 255, 255))
            pygame.draw.rect(window, WHITE, (10, 630, 1260, 80))
            println("RETURN TO GAME", 20, 660)
            println("INVENTORY:", 10, 60, (200, 200, 200))
            println("EQUIPPED:", 640, 60, (200, 200, 200))
            y = 100
            x = 0
            
            for i in player.inv:
                pygame.draw.rect(window, (100, 100, 100), (10, y, 350, 35))
                println(i.name.title(), 10, y)
                items.append([x,(10, y, 350, 35)])
                y = y + 40
                x = x + 1

            y = 100
            x = 0
            for i in player.equip:
                pygame.draw.rect(window, (100, 100, 100), (640, y, 350, 35))
                println(i.name.title(), 640, y)
                items2.append([x,(640, y, 350, 35)])
                y = y + 40
                x = x + 1
                
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if pointInsideRect2(event.pos[0], event.pos[1], (10, 630, 1260, 80)):
                        return player, locx, locy, playerx, playery
                    if pointInsideRect2(event.pos[0], event.pos[1], (0, 0, 300, 50)):
                        menu = "status"
                    for i in items:
                        if pointInsideRect2(event.pos[0], event.pos[1], i[1]):
                            z = 0
                            for w in player.equip:
                                if w.wclass == player.inv[i[0]].wclass or (w.wclass == ('SWD' or 'AXE' or 'SPR') and player.inv[i[0]].wclass == ('SWD' or 'AXE' or 'SPR')):
                                    player.inv.append(player.equip.pop(z))
                                z = z + 1
                            player.equip.append(player.inv.pop(i[0]))
                    for i in items2:
                        if pointInsideRect2(event.pos[0], event.pos[1], i[1]):
                            player.inv.append(player.equip.pop(i[0]))
            
            
            
            
def check(player, opp):
    if player.stats["HP"] + player.bonus["HP"] <= 0:
        pygame.quit()
        sys.exit()
    if opp.stats["HP"] + opp.bonus["HP"] <= 0:
        player.kills = player.kills + 1
        return True
    

def damage(o, d, move, opp):
    #background = pygame.image.load('Tiles/battlebackground.png')
    background = pygame.image.load('Tiles/ezra_battle_background2.png')
    choice = False
    while not(choice):
        window.blit(background, (0, 0))
        pygame.draw.rect(window, WHITE, (0, 620, 1280, 100))
        pygame.draw.rect(window, BLACK, (998,78,154,14))
        pygame.draw.rect(window, BLACK, (198,78,154,14))
        pygame.draw.rect(window, RED, (200, 80, (150 * (player.stats["HP"] + player.bonus["HP"]) / player.stats["HP"]), 10))
        pygame.draw.rect(window, RED, (1000, 80, (150 * (opp.stats["HP"] + ezra.bonus["HP"]) / opp.stats["HP"]), 10))
        println(o.name.upper() + " attacked using " + move.name.upper(), 440, 586)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                choice = True
        pygame.display.update()
        clock.tick(30)
    if move.wclass != "MAG":
        damage = int(((1.5 * (o.stats["STR"] + o.bonus["STR"]) * (move.pwr - 1))/(d.stats["DEF"] + d.bonus["DEF"])) * random.randint(85, 115) / 100)
    else:
        damage = int(((1.1 * (o.stats["MAG"] + o.bonus["MAG"]) * (move.pwr - 1))/(d.stats["MAG"] + d.bonus["MAG"])) * random.randint(75, 125) / 100)
    accuracy = move.acc + 3 * (o.stats["SKL"] + o.bonus["SKL"] - d.stats["LCK"] + d.bonus["LCK"])
    choice = False
    hpcurrent = d.stats["HP"] + d.bonus["HP"]
    while not(choice):
        window.blit(background, (0, 0))
        pygame.draw.rect(window, WHITE, (0, 620, 1280, 100))
        pygame.draw.rect(window, BLACK, (998,78,154,14))
        pygame.draw.rect(window, BLACK, (198,78,154,14))
        pygame.draw.rect(window, RED, (200, 80, (150 * (player.stats["HP"] + player.bonus["HP"]) / player.stats["HP"]), 10))
        pygame.draw.rect(window, RED, (1000, 80, (150 * (opp.stats["HP"] + opp.bonus["HP"]) / opp.stats["HP"]), 10))
        if accuracy < random.randint(1,100):
            println("But it missed!", 440, 586)
            damage = 0
        else:
            while (hpcurrent - damage) < (d.stats["HP"] + d.bonus["HP"]):
                d.bonus["HP"] = d.bonus["HP"] - 1
                pygame.display.update()
            if abs(d.bonus["HP"]) > d.stats["HP"]:
                d.bonus["HP"] = d.stats["HP"] * -1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                choice = True
        pygame.display.update()
        clock.tick(30)

def battlestart(player, opp):
    if battle(player, opp):
        print player.stats
        expgain = int((opp.lvl / player.lvl) * (opp.stats["HP"] + random.randint(1,5)))
        player.exp = player.exp + expgain
        if player.exp >= cube(player.lvl + 1):
            player.lvl = player.lvl + 1
            player.statcalc()
            print "LEVEL UP!"
            print player.stats
    else:
        pass #"You Fled" code
    pygame.mixer.music.load("Sounds/theme1.wav")
    pygame.mixer.music.play(-1)
    return player


def battle(player, opp):
    pygame.mixer.music.play(-1)
    pdir["u"] = False
    pdir["d"] = False
    pdir["l"] = False      
    pdir["r"] = False
    #background = pygame.image.load('Tiles/battlebackground.png')
    background = pygame.image.load('Tiles/ezra_battle_background2.png')
    melee = False
    ranged = False
    magic = False
    defend = False

    choice = False
    wexist = True
    choice2 = False
    while wexist:
        while not(choice):
            window.blit(background, (0, 0))
            pygame.draw.rect(window, WHITE, (0, 620, 1280, 100))
            pygame.draw.rect(window, BLACK, (998,78,154,14))
            pygame.draw.rect(window, BLACK, (198,78,154,14))
            pygame.draw.rect(window, RED, (200, 80, (150 * (player.stats["HP"] + player.bonus["HP"]) / player.stats["HP"]), 10))
            pygame.draw.rect(window, RED, (1000, 80, (150 * (opp.stats["HP"] + opp.bonus["HP"]) / opp.stats["HP"]), 10))
            pygame.draw.rect(window, RED, (0, 620, 640, 100))
            pygame.draw.rect(window, BLUE, (640, 620, 640, 100))
            println("A WILD " + opp.name.upper() + " ATTACKS!", 440, 586)
            println("FLEE!", 900, 655)
            println("FIGHT!", 260, 655)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if pointInsideRect2(event.pos[0], event.pos[1], (640, 620, 640, 100)):
                        return False
                    if pointInsideRect2(event.pos[0], event.pos[1], (0, 620, 640, 100)):
                        choice = True
                        wexist = False
                        priority = 0
                        opriority = 0
                        if player.equip == []:
                            choice2 = True
                            wexist = True
            pygame.display.update()
            clock.tick(30)
            
        choice = False
        while choice2:
            window.blit(background, (0, 0))
            pygame.draw.rect(window, WHITE, (0, 620, 1280, 100))
            pygame.draw.rect(window, BLACK, (998,78,154,14))
            pygame.draw.rect(window, BLACK, (198,78,154,14))
            pygame.draw.rect(window, RED, (200, 80, (150 * (player.stats["HP"] + player.bonus["HP"]) / player.stats["HP"]), 10))
            pygame.draw.rect(window, RED, (1000, 80, (150 * (opp.stats["HP"] + opp.bonus["HP"]) / opp.stats["HP"]), 10))
            pygame.draw.rect(window, RED, (0, 620, 640, 100))
            pygame.draw.rect(window, BLUE, (640, 620, 640, 100))
            println("YOU CANNOT FIGHT WITHOUT A WEAPON EQUIPPED.", 200, 586)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    choice2 = False        
            pygame.display.update()
            clock.tick(30)
            
    while 1:
        choice = False
        while not(choice):
            window.blit(background, (0, 0))
            pygame.draw.rect(window, WHITE, (0, 620, 1280, 100))
            pygame.draw.rect(window, BLACK, (998,78,154,14))
            pygame.draw.rect(window, BLACK, (198,78,154,14))
            pygame.draw.rect(window, RED, (200, 80, (150 * (player.stats["HP"] + player.bonus["HP"]) / player.stats["HP"]), 10))
            pygame.draw.rect(window, RED, (1000, 80, (150 * (opp.stats["HP"] + opp.bonus["HP"]) / opp.stats["HP"]), 10))
            pygame.draw.rect(window, GREY, (0, 620, 320, 100))
            pygame.draw.rect(window, GREEN, (320, 620, 320, 100))
            pygame.draw.rect(window, PURPLE, (640, 620, 320, 100))
            pygame.draw.rect(window, YELLOW, (960, 620, 320, 100))
            println("What would you like to do?", 440, 586)
            for w in player.equip:
                if w.wclass == "MAG":
                    magic = True
                if w.wclass == ("SWD" or "AXE" or "SPR"):
                    melee = True
                if w.wclass == "BOW":
                    ranged = True
                if w.wclass == "DFN":
                    defend = True
            if magic:
                println("MAGIC", 650, 655)
            if ranged:
                println("RANGED", 330, 655)
            if melee:
                println("MELEE", 10, 655)
            if defend:
                println("DEFEND", 970, 655)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if pointInsideRect2(event.pos[0], event.pos[1], (0, 620, 320, 100)) and melee:
                        for m in player.equip:
                            if m.wclass == ("SWD" or "AXE" or "SPR"):
                                mu = m
                        choice = True
                    elif pointInsideRect2(event.pos[0], event.pos[1], (320, 620, 320, 100)) and ranged:
                        for m in player.equip:
                            if m.wclass == "BOW":
                                mu = m
                                priority = 1
                        choice = True
                    elif pointInsideRect2(event.pos[0], event.pos[1], (640, 620, 320, 100)) and magic:
                        for m in player.equip:
                            if m.wclass == "MAG":
                                mu = m
                        choice = True
                    elif pointInsideRect2(event.pos[0], event.pos[1], (960, 620, 320, 100)) and defend:
                        for m in player.equip:
                            if m.wclass == "DFN":
                                mu = m
                        choice = True
                    
            pygame.display.update()
            clock.tick(30)
        oppmu = random.randint(1,len(opp.inv))
        oppmu = opp.inv[oppmu - 1]

        if priority > opriority:
            damage(player, opp, mu, opp)
            if check(player, opp):
                return True
            damage(opp, player, oppmu, opp)
            if check(player, opp):
                return True
        elif priority < opriority:
            damage(opp, player, oppmu, opp)
            if check(player, opp):
                return True
            damage(player, opp, mu, opp)
            if check(player, opp):
                return True
        elif priority == opriority:
            if (player.stats['SPE'] + player.bonus['SPE']) > (opp.stats['SPE'] + opp.bonus['SPE']):
                damage(player, opp, mu, opp)
                if check(player, opp):
                    return True
                damage(opp, player, oppmu, opp)
                if check(player, opp):
                    return True
            if (player.stats['SPE'] + player.bonus['SPE']) < (opp.stats['SPE'] + opp.bonus['SPE']):
                damage(opp, player, oppmu, opp)
                if check(player, opp):
                    return True
                damage(player, opp, mu, opp)
                if check(player, opp):
                    return True
            if (player.stats['SPE'] + player.bonus['SPE']) == (opp.stats['SPE'] + opp.bonus['SPE']):
                if random.randint(1,2) == 1:
                    damage(player, opp, mu, opp)
                    if check(player, opp):
                        return True
                    damage(opp, player, oppmu, opp)
                    if check(player, opp):
                        return True
                else:
                    damage(opp, player, oppmu, opp)
                    if check(player, opp):
                        return True
                    damage(player, opp, mu, opp)
                    if check(player, opp):
                        return True
        
        
def Talking(quest):
    pygame.draw.rect(window, (180,180,180), (0,640,1280,720))
    println(quest,25,650)


mapbuild(loc)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (119, 119, 119,)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREEN = (0, 175, 0)
#starting player location
x = 15
y = 352
z=0
#Starting world location
locx = 0
locy = 1
questing = False
questcomplete = False

ezra = character("ezra", "ezra",5)
ezra.inv.append(weapon("bite"))
ezra.inv.append(weapon("bronze sword"))
rat = character("rat", "rat", 3)
rat.inv.append(weapon("bite"))
spider = character("spider", "spider", 4)
spider.inv.append(weapon("bite"))
wilddog = character("wild dog", "wild dog", 5)
wilddog.inv.append(weapon("bite"))





pygame.mixer.music.play(-1)

menu = True
while menu:
    window.fill((0,0,0))
    pygame.draw.rect(window, (180, 180, 180), (25, 320, 1230, 80))
    pygame.draw.rect(window, (180, 180, 180), (25, 420, 1230, 80))
    println("NEW GAME", 45, 350)
    println("LOAD GAME", 45, 450)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if pointInsideRect2(event.pos[0], event.pos[1], (25, 320, 1230, 80)):
                mode = 'n'
                menu = False
            if pointInsideRect2(event.pos[0], event.pos[1], (25, 420, 1230, 80)):
                mode = 'l'
                menu = False
    pygame.display.update()
    clock.tick(30)

menu = True
while menu:
    clicked = False
    println("Which slot would you like to save to?", 25, 25, (255, 255, 255))
    pygame.draw.rect(window, (180, 180, 180), (25, 320, 1230, 80))
    pygame.draw.rect(window, (180, 180, 180), (25, 420, 1230, 80))
    pygame.draw.rect(window, (180, 180, 180), (25, 520, 1230, 80))
    println("SLOT 1", 45, 350)
    println("SLOT 2", 45, 450)
    println("SLOT 3", 45, 550)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if pointInsideRect2(event.pos[0], event.pos[1], (25, 320, 1230, 80)):
                slot = "slot1"
                clicked = True
            if pointInsideRect2(event.pos[0], event.pos[1], (25, 420, 1230, 80)):
                slot = "slot3"
                clicked = True
            if pointInsideRect2(event.pos[0], event.pos[1], (25, 520, 1230, 80)):
                slot = "slot3"
                clicked = True
            if clicked:
                if mode == 'l':
                    savefile = open("Slots/" + slot + ".txt")
                    (player, loc, locx, locy, x, y, inbuilding) = pickle.load(savefile)
                    savefile.close()
                if mode == 'n':
                    player = character("player","player",5)
                    player.inv.append(weapon("bronze sword"))
                    player.inv.append(weapon("basic wind tome"))
                    player.inv.append(weapon("shortbow"))
                    inbuilding = False
                menu = False
    pygame.display.update()
    clock.tick(30)

party = [player]




while True:
    if not(inbuilding):
        loc = WORLDMAP[locy][locx] 
    mapbuild(loc)
    pygame.draw.rect(window, (0,0,0), (x, y, 16, 16))
    oldx = x
    oldy = y
    ezrachance = 0
    #player keystrokes to movement
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                pdir["u"] = True
            if event.key == K_DOWN:
                pdir["d"] = True
            if event.key == K_LEFT:
                pdir["l"] = True
            if event.key == K_RIGHT:
                pdir["r"] = True
            if event.key == K_ESCAPE:
                (player, locx, locy, x, y) = status(player, loc, locx, locy, x, y, inbuilding)
            if event.key == ord('f'):
                ezrachance = 1
            if event.key == K_SPACE:
                action = True
        if event.type == KEYUP:
            if event.key == K_UP:
                pdir["u"] = False
            if event.key == K_DOWN:
                pdir["d"] = False
            if event.key == K_LEFT:
                pdir["l"] = False
            if event.key == K_RIGHT:
                pdir["r"] = False
            if event.key == K_SPACE:
                action = False
    #move player cordinents
    if pdir["u"]:
        y = y - 16
    elif pdir["d"]:
        y = y + 16
    elif pdir["l"]:
        x = x - 16
    elif pdir["r"]:
        x = x + 16
    #check if player can go there
    if passtest(x,y,loc) == False:
        x = oldx
        y = oldy
        z=1
        pdir["u"] = False
        pdir["d"] = False
        pdir["r"] = False
        pdir["l"] = False
    #change map
    if not(inbuilding):
        if x > 1280:
            x=0
            locx = locx + 1
        elif x < 0:
            x = 1264
            locx = locx - 1
        elif y < 0:
            y = 704
            locy = locy - 1
        elif y > 720:
            y = 0
            locy = locy + 1
    
        
    if loc ==  "town" and y == 304 and x == 512:
        worldx = x
        worldy = y
        oldloc = loc
        loc = "inn1"
        x = 560
        y = 400
        inbuilding = True
    if loc ==  "town" and y == 304 and x == 720:
        worldx = x
        worldy = y
        oldloc = loc
        loc = "shop"
        x = 560
        y = 400
        inbuilding = True
    
    if (loc == "inn1" or loc == "shop") and (x == 560 or x == 544) and y == 416 and pdir['d']:
        y = worldy
        x = worldx
        loc = oldloc
        inbuilding = False
    if loc == "inn1" and (x == 656 or x == 672) and (y == 320) and action == True:
        action = False
        player.bonus["HP"] = 0
        println("You have been healed", 340, 586)
        pygame.display.update()
        time.sleep(1)
    if loc == "town":
        pygame.draw.rect(window, (0,0,0), (336,592, 16, 16))
        
    if loc == "town" and (x == 336 or x == 320 or x == 352) and (y == 592 or y == 576 or y == 608) and action == True:
        if questcomplete == False:
            if questing == True and player.kills < 5:
                Talking("You need to kill more Ezras")
                pygame.display.update()
                action = False
                time.sleep(1)
            elif questing == True and player.kills >= 5:
                Talking("Thank You, here is an iron sword")
                player.inv.append(weapon("iron sword"))
                questcomplete = True
                pygame.display.update()
                action = False
                time.sleep(1)
            if questing == False:
                Talking("You need to go and kill 5 wild Ezras for me and than I will give you a Sword.")
                pygame.display.update()
                questing = True
                action = False
                time.sleep(2)
        else:
            Talking("Thanks for killing the Ezras, ur a bro. Pound it")
            pygame.display.update()
            time.sleep(1.5)
            
            
    if ezrachance == 1 and loc == "grassyarea":
        ezra = character('ezra','ezra',random.randint(4,7))
        ezra.statcalc()
        ezra.inv.append(weapon("bite"))
        pygame.mixer.music.load("Sounds/ezra_battle_theme.wav")
        player = battlestart(player, ezra)
    if ezrachance == 1 and loc == "grassyarea3":
        moose = character('moose','moose',random.randint(5,9))
        moose.statcalc()
        moose.inv.append(weapon("bite"))
        if battle(party[0], moose):
            nopress = True
            while nopress:
                mapbuild(loc)
                pygame.draw.rect(window, (0,0,0), (x, y, 16, 16))
                println("You beat the wild Moose!", 440, 586)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        nopress = False
                    if event.type == MOUSEBUTTONDOWN:
                        nopress = False
    pygame.display.update()
    clock.tick(30)
