from structs import *
import sys

class Pathfinder():

    def __init__(self):
         pass

    def heuristic(self,t1,t2):
        return abs(t1["X"] - t2["X"]) + abs(t1["Y"] - t2["Y"])

    def distance(self, start, end, tiles):
        closedSet = set([])
        openSet = set([start])
        cameFrom = dict()
        gScore = dict()
        fScore = dict()
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                point = Point(i,j)
                gScore[point] = sys.maxint
                fScore[point] = sys.maxint
        gScore[start] = 0
        fScore[start] = self.heuristic(start, end)

        while openSet:
            # Finding the node with the lowest fScore
            bestScore = sys.maxint
            for node in openSet:
                if fScore[node] <= bestScore:
                    currentNode = node
                    bestScore = fScore[node]
            
        if currentNode == end:
            return self.reconstructPath(cameFrom, currentNode)

        openSet.remove(currentNode)
        closedSet.add(currentNode)

        x = currentNode["X"]
        y = currentNode["Y"]
        neighbours = []
        if x > 0:
            neighbours.append(Point(tiles[x-1][y].X,tiles[x-1][y].Y))
        if x < len(tiles) - 1:
            neighbours.append(Point(tiles[x+1][y].X,tiles[x+1][y].Y))
        if y > 0:
            neighbours.append(Point(tiles[x][y-1].X,tiles[x][y-1].Y))
        if y < len(tiles[x]) - 1:
            neighbours.append(Point(tiles[x][y+1].X,tiles[x][y+1].Y))

        for neighbour in neighbours:
            tile = tiles[neighbour["X"]][neighbour["Y"]]
            if tile.Content == TileContent.Lava or tile.Content == TileContent.Wall or tile.Content == TileContent.Player or tile.Content == TileContent.Resource:
                continue

            if neighbour in closedSet:
                continue

            if neighbour not in openSet:
                openSet.add(neighbour)

            currentgScore = gScore[currentNode] + 1
            if currentgScore >= gScore[neighbour]:
                continue
            cameFrom[neighbour] = currentNode
            gScore[neighbour] = currentgScore
            fScore[neighbour] = currentgScore + self.heuristic(neighbour, end)

        return None

    def reconstructPath(self,cameFrom, current):
        path = [current]
        while current in cameFrom.keys:
            current = cameFrom[current]
            path.append(current)
        return path
