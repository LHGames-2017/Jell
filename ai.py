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

def determinateActionToDo(currentState, x, y, gameInformations = 0) :

    if currentState == StateType.SearchMineral or currentState == StateType.GoToMineral:

        ### IF FULL
        ### ELSE
        ### IF MINERAL FOUND
        global actualState
        actualState = StateType.GoToMineral
        if x<28 :
            return create_move_action(Point(x+1,y))
        elif y<34 :
            return create_move_action(Point(x,y+1))
        elif x==28 and y==34 :
            return create_collect_action(Point(x,y+1))
        ### ELIF MINERAL NOT FOUND
        
    return create_move_action(Point(x,y))

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

    #printMap(deserialized_map,x,y)

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

    return determinateActionToDo(actualState,x ,y)

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
            tile = deserialized_map[i][j]
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
