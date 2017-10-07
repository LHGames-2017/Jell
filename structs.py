import math

class ActionTypes():
    DefaultAction, MoveAction, AttackAction, CollectAction, UpgradeAction, StealAction, PurchaseAction, HealAction = range(8)


class UpgradeType():
    CarryingCapacity, AttackPower, Defence, MaximumHealth, CollectingSpeed = range(5)


class TileType():
    Tile, Wall, House, Lava, Resource, Shop = range(6)


class TileContent():
    Empty, Wall, House, Lava, Resource, Shop, Player = range(7)

class State():
    FindResource, GoToResource, GatherResource, ReturnResource = range(4)


class Point(object):

    # Constructor
    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    # Overloaded operators
    def __add__(self, point):
        return Point(self.X + point.X, self.Y + point.Y)

    def __sub__(self, point):
        return Point(self.X - point.X, self.Y - point.Y)

    def __str__(self):
        return "{{{0}, {1}}}".format(self.X, self.Y)

    # Distance between two Points
    def Distance(self, p1, p2):
        delta_x = p1.X - p2.X
        delta_y = p1.Y - p2.Y
        return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


#class GameInfo(object):
#
#    def __init__(self, json_dict):
#        self.__dict__ = json_dict
#        self.HouseLocation = Point(json_dict["HouseLocation"])
#        self.Map = BigMap()
#        self.Players = dict()


class Tile(object):

    def __init__(self, content=None, x=0, y=0):
        self.Content = content
        self.X = x
        self.Y = y


class Player(object):

    def __init__(self, health, maxHealth, position, houseLocation, score, carriedRessources,
                 carryingCapacity=1000):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position
        self.HouseLocation = houseLocation
        self.Score = score
        self.CarriedRessources = carriedRessources
        self.CarryingCapacity = carryingCapacity


class PlayerInfo(object):

    def __init__(self, health, maxHealth, position):
        self.Health = health
        self.MaxHealth = maxHealth
        self.Position = position

class ActionContent(object):

    def __init__(self, action_name, content):
        self.ActionName = action_name
        self.Content = str(content)

    
class BigMap(object):
    initialized = False

    def initMap(self, littleMap):
        
        startX = littleMap[0][0].X
        startY = littleMap[0][0].Y

        self.Map = [[TileContent.Wall for i in range(startX + 30)] for j in range(startY + 30)]

        self.updateMap(littleMap)

    def updateMap(self, littleMap):
        startX = littleMap[0][0].X
        startY = littleMap[0][0].Y

        for i in range (0,len(littleMap)):
            for j in range (0,len(littleMap[i])):
                self.Map[startX + i][startY + j] = littleMap[i][j].Content




