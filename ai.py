from flask import Flask, request
from structs import *
import json
import numpy

app = Flask(__name__)

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def create_upgrade_action(upgradetype):
    return create_action("UpgradeAction", upgradetype)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

class StateType():
    SearchMineral, GoToMineral, MiningMineral, GoToHouse = range(4)

actualState = StateType.SearchMineral

xMineral = 0
yMineral = 0

totalResources = 0

lvlMiningSpeed = 0
lvlCarryingCapacity = 0

def distEucl (x1,y1,x2,y2) :
    delta_x = x1 - x2
    delta_y = y1 - y2
    return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))

def canIBuySomething(player):

    global lvlMiningSpeed
    global lvlCarryingCapacity
    global totalResources

    if lvlMiningSpeed <= lvlCarryingCapacity :
        if lvlMiningSpeed == 0 and totalResources >= 15000 :
            lvlMiningSpeed = lvlMiningSpeed + 1
            return [UpgradeType.CollectingSpeed] 
        if lvlMiningSpeed == 1 and totalResources >= 50000 :
            lvlMiningSpeed = lvlMiningSpeed + 1
            return [UpgradeType.CollectingSpeed] 
        if lvlMiningSpeed == 2 and totalResources >= 100000 :
            lvlMiningSpeed = lvlMiningSpeed + 1
            return [UpgradeType.CollectingSpeed] 
        if lvlMiningSpeed == 3 and totalResources >= 250000 :
            lvlMiningSpeed = lvlMiningSpeed + 1
            return [UpgradeType.CollectingSpeed] 
        if lvlMiningSpeed == 4 and totalResources >= 500000 :
            lvlMiningSpeed = lvlMiningSpeed + 1
            return [UpgradeType.CollectingSpeed] 
    else :
        if lvlCarryingCapacity == 0 and totalResources >= 15000 :
            lvlCarryingCapacity = lvlCarryingCapacity + 1
            return [UpgradeType.CarryingCapacity] 
        if lvlCarryingCapacity == 1 and totalResources >= 50000 :
            lvlCarryingCapacity = lvlCarryingCapacity + 1
            return [UpgradeType.CarryingCapacity] 
        if lvlCarryingCapacity == 2 and totalResources >= 100000 :
            lvlCarryingCapacity = lvlCarryingCapacity + 1
            return [UpgradeType.CarryingCapacity] 
        if lvlCarryingCapacity == 3 and totalResources >= 250000 :
            lvlCarryingCapacity = lvlCarryingCapacity + 1
            return [UpgradeType.CarryingCapacity] 
        if lvlCarryingCapacity == 4 and totalResources >= 500000 :
            lvlCarryingCapacity = lvlCarryingCapacity + 1
            return [UpgradeType.CarryingCapacity]


    return None

def determinateActionToDo(currentState, deserialized_map,player, x, y,  gameInformations = 0) :

    global xMineral
    global yMineral
    global actualState

    xH = player.HouseLocation.X
    yH = player.HouseLocation.Y

    if xH == x and yH == y :
        upgrade = canIBuySomething(player)
        currentState = StateType.SearchMineral
        if upgrade != None :
            return create_upgrade_action(upgrade)

    if currentState == StateType.SearchMineral :
        [xMineral,yMineral] = searchClosestMineral(deserialized_map, x, y)
        currentState = StateType.GoToMineral

    if currentState == StateType.GoToMineral:

        if player.CarriedRessources == player.CarryingCapacity :
            currentState = StateType.GoToHouse
            
        else :

            [xM,yM] = [xMineral,yMineral]

            
            ### IF FULL

            ### ELSE
            ### IF MINERAL FOUND
            if distEucl(x,y,xM,yM) > 1 :
                if y<yM :
                    return create_move_action(Point(x,y+1))
                elif x<xM :
                    return create_move_action(Point(x+1,y))
                elif y>yM :
                    return create_move_action(Point(x,y-1))
                elif x>xM :
                    return create_move_action(Point(x-1,y))
            elif distEucl(x,y,xM,yM) == 1 :
                if x==xM-1 :
                    return create_collect_action(Point(x+1,y))
                if x==xM+1 :
                    return create_collect_action(Point(x-1,y))
                if y==yM-1 :
                    return create_collect_action(Point(x,y+1))
                if y==yM+1 :
                    return create_collect_action(Point(x,y-1))
            ### ELIF MINERAL NOT FOUND
        
    if currentState == StateType.GoToHouse :
        distance = distEucl(x,y,xH,yH)
        if distance >= 1 :
                if distance == 1:
                    currentState = StateType.SearchMineral
                if x<xH :
                    return create_move_action(Point(x+1,y))
                elif y<yH :
                    return create_move_action(Point(x,y+1))
                elif x>xH :
                    return create_move_action(Point(x-1,y))
                elif y>yH :
                    return create_move_action(Point(x,y-1))
        
    return create_move_action(Point(x,y))

def searchClosestMineral(deserialized_map,x,y):
    distance = 1000
    xM = 0
    yM = 0
    found = False
    for i in range(len(deserialized_map)):
        for j in range(len(deserialized_map[i])):
            tile = deserialized_map[i][j]
            if tile.Content == TileContent.Resource:
                tempDist = distEucl(xM, yM , x , y)
                if tempDist < distance :
                    distance = tempDist
                    xM = deserialized_map[i][j].X
                    yM = deserialized_map[i][j].Y 
                    found = True

    return [xM,yM] if found else None
        
                    
def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"] ,
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    global totalResources

    totalResources = p["TotalResources"]

    #printMap(deserialized_map)

    otherPlayers = []

    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            if player_info == 'notAPlayer':
                continue
            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info })

    # return decision

    printMap(deserialized_map,x,y)
    print(totalResources)
    global actualState
    print(actualState)

    #print x
    #print y

    

    #if x<28 :
    #    return create_move_action(Point(x+1,y))
    #elif y<34 :
    #    return create_move_action(Point(x,y+1))
    #elif x==28 and y==34 :
    #    return create_collect_action(Point(x,y+1))
    #
    #return create_move_action(Point(x,y-1))

    return determinateActionToDo(actualState,deserialized_map, player,x ,y)

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    print("Action demandee")
    return bot()

def printMap(deserialized_map, playerX, playerY):
    for i in range(len(deserialized_map)):
        line = '['
        for j in range(len(deserialized_map[i])):
            tile = deserialized_map[j][i]
            if tile.Content == TileContent.Empty:
                line += ' '
            elif tile.Content == TileContent.House:
                line += 'H'
            elif tile.Content == TileContent.Lava:
                line += '~'
            elif tile.Content == TileContent.Player:
                line += 'o'
            elif tile.Content == TileContent.Resource:
                line += '^'
            elif tile.Content == TileContent.Shop:
                line += 'S'
            elif tile.Content == TileContent.Wall:
                line += '@'
            else:
                line += 'B'
        line += ']'
        print line


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
