from __future__ import print_function
# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from builtins import range
from builtins import object
import util
from game import Agent
from game import Grid
from game import Directions
from keyboardAgents import KeyboardAgent
from wekaI import Weka
import inference
import busters
import os


class NullGraphics(object):
    "Placeholder for graphics"

    def initialize(self, state, isBlue=False):
        pass

    def update(self, state):
        pass

    def pause(self):
        pass

    def draw(self, state):
        pass

    def updateDistributions(self, dist):
        pass

    def finish(self):
        pass


class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__(self, index=0, inference="ExactInference", ghostAgents=None, observeEnable=True,
                 elapseTimeEnable=True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.score_storage = [0]
        self.prev_tick = None
        #COMMENTOUT
        self.weka = Weka()
        self.weka.start_jvm()

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        # for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        # self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

    def printLineData(self, gameState, sendArray=False):
        # Retrieving Pacman's position
        posX = gameState.getPacmanPosition()[0]
        posY = gameState.getPacmanPosition()[1]
        # Retrieving Pacman's direction
        directionPacman = gameState.data.agentStates[0].getDirection()
        # Retrieving Ghost's direction
        directionGhosts = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        directionGhost1, directionGhost2, directionGhost3, directionGhost4 = directionGhosts
        # Retrieving Ghost's distance
        distanceGhosts = gameState.data.ghostDistances
        distanceGhosts1, distanceGhosts2, distanceGhosts3, distanceGhosts4 = distanceGhosts
        if not distanceGhosts1:
            distanceGhosts1 = -1
        if not distanceGhosts2:
            distanceGhosts2 = -1
        if not distanceGhosts3:
            distanceGhosts3 = -1
        if not distanceGhosts4:
            distanceGhosts4 = -1
        # Retrieving Position of Walls
        walls = gameState.getWalls()
        # concatenating all variables into single line

        posGhosts = gameState.getGhostPositions()
        posGhost1X, posGhost1Y, posGhost2X, posGhost2Y, posGhost3X, posGhost3Y, posGhost4X, posGhost4Y = (
        posGhosts[0][0], posGhosts[0][1], posGhosts[1][0], posGhosts[1][1], posGhosts[2][0], posGhosts[2][1],
        posGhosts[3][0], posGhosts[3][1])

        actions = gameState.getLegalActions()
        legalNorth = "North" in actions
        legalSouth = "South" in actions
        legalEast = "East" in actions
        legalWest = "West" in actions
        legalStop = "Stop" in actions

        livingGhosts = gameState.getLivingGhosts()
        livingGhost1, livingGhost2, livingGhost3, livingGhost4 = livingGhosts[1:]

        score = gameState.getScore()

        csv_vals = [posX, posY, score, directionGhost1, directionGhost2, directionGhost3, directionGhost4,
                    distanceGhosts1, distanceGhosts2, distanceGhosts3, distanceGhosts4, posGhost1X, posGhost1Y,
                    posGhost2X, posGhost2Y, posGhost3X, posGhost3Y, posGhost4X, posGhost4Y, legalNorth, legalSouth,
                    legalEast, legalWest, legalStop, livingGhost1, livingGhost2, livingGhost3, livingGhost4,
                    score, directionPacman]

        if sendArray:
            temp_vals = [posX, posY, score, directionGhost1, directionGhost2, directionGhost3, directionGhost4,
                        distanceGhosts1, distanceGhosts2, distanceGhosts3, distanceGhosts4, posGhost1X, posGhost1Y,
                        posGhost2X, posGhost2Y, posGhost3X, posGhost3Y, posGhost4X, posGhost4Y, legalNorth, legalSouth,
                        legalEast, legalWest, legalStop, livingGhost1, livingGhost2, livingGhost3, livingGhost4, score]

            for index, val in enumerate(temp_vals):
                if type(val) == bool or val is None:
                    temp_vals[index] = str(val)
            return temp_vals

        if not self.prev_tick:
            self.prev_tick = csv_vals
        else:
            temp = self.prev_tick
            self.prev_tick = csv_vals
            temp[28] = score
            line = ""
            for val in temp:
                line += str(val) + ","
            return line + "\n"




class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index=0, inference="KeyboardInference", ghostAgents=None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)


from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''


class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    ''' Example of counting something'''

    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if (height == True):
                    food = food + 1
        return food

    ''' Print the layout'''

    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0)  ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if (move_random == 0) and Directions.WEST in legal:  move = Directions.WEST
        if (move_random == 1) and Directions.EAST in legal: move = Directions.EAST
        if (move_random == 2) and Directions.NORTH in legal:   move = Directions.NORTH
        if (move_random == 3) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move


class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i + 1]]
        return Directions.EAST

class MLAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        move = Directions.STOP
        x = self.printLineData(gameState, sendArray=True)
        wantMove = self.weka.predict("./training_tutorial1.model", x, "./training_tutorial1.arff")
        legal = gameState.getLegalActions(0)  ##Legal position from the pacman
        if wantMove in legal: move = wantMove
        #
        # if wantMove == Directions.STOP:
        #     move = legal[1]
        return move


class BasicAgentAA(BustersAgent):

    path = None

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    ''' Example of counting something'''

    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if (height == True):
                    food = food + 1
        return food

    ''' Print the layout'''

    def printGrid(self, gameState):
        table = ""
        # print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ",
              [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances)
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood())
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood())
        # Map walls
        print("Map:")
        print(gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())

    def isValid(self, visited, walls, x, y):
        if (x < 0 or y < 0 or x >= visited.width or y >= visited.height):
            return False
        if visited[x][y]:
            return False
        if walls[x][y]:
            return False
        return True

    def findPathBFS(self, posX, posY, walls, posGhostX, posGhostY):
        # BFS
        wallDimensionsX = walls.width
        wallDimensionsY = walls.height

        xQueue, yQueue = [], []

        dX = [-1, 1, 0, 0]
        dY = [0, 0, 1, -1]

        ghosts = Grid(wallDimensionsX, wallDimensionsY, False)
        ghosts[posGhostX][posGhostY] = True
        visited = Grid(wallDimensionsX, wallDimensionsY, False)

        found = False
        parent_mapping = {}
        path = []
        parent_mapping[(posX, posY)] = None

        xQueue.append(posX)
        yQueue.append(posY)
        visited[posX][posY] = True
        while xQueue:
            x = xQueue.pop(0)
            y = yQueue.pop(0)

            for i in range(4):
                xDir = x + dX[i]
                yDir = y + dY[i]
                if ghosts[x][y]:
                    found = True
                if self.isValid(visited, walls, xDir, yDir):
                    xQueue.append(xDir)
                    yQueue.append(yDir)
                    visited[xDir][yDir] = True
                    parent_mapping[(xDir, yDir)] = (x, y)
            if found:
                curr = (x, y)
                while curr:
                    path.append(curr)
                    curr = parent_mapping.get(curr)
                return path
        return None

    def convertToMove(self, xy, x2y2):
        x, y = xy
        x2, y2 = x2y2
        dx = x2-x
        dy = y2-y
        if dx == -1:
            return Directions.WEST
        if dx == 1:
            return Directions.EAST
        if dy == -1:
            return Directions.SOUTH
        if dy == 1:
            return Directions.NORTH
        return Directions.STOP

    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP

        walls = gameState.getWalls()

        posX = gameState.getPacmanPosition()[0]
        posY = gameState.getPacmanPosition()[1]

        posGhosts = gameState.getGhostPositions()
        posGhost1X, posGhost1Y, posGhost2X, posGhost2Y, posGhost3X, posGhost3Y, posGhost4X, posGhost4Y = (
        posGhosts[0][0], posGhosts[0][1], posGhosts[1][0], posGhosts[1][1], posGhosts[2][0], posGhosts[2][1],
        posGhosts[3][0], posGhosts[3][1])

        livGhosts = gameState.getLivingGhosts()
        livGhost1, livGhost2, livGhost3, livGhost4 = (livGhosts[1], livGhosts[2], livGhosts[3], livGhosts[4])

        # Checks status of ghosts
        if livGhost1:
            if not self.path or self.lastGhostPos != (posGhost1X, posGhost1Y):
                self.path = self.findPathBFS(posX, posY, walls, posGhost1X, posGhost1Y)
                self.lastGhostPos = (posGhost1X, posGhost1Y)
                self.path.pop(-1)
                return self.convertToMove((posX, posY), self.path.pop(-1))
            else:
                return self.convertToMove((posX, posY), self.path.pop(-1))
        elif livGhost3:
            if not self.path or self.lastGhostPos != (posGhost3X, posGhost3Y):
                self.path = self.findPathBFS(posX, posY, walls, posGhost3X, posGhost3Y)
                self.lastGhostPos = (posGhost3X, posGhost3Y)
                self.path.pop(-1)
                return self.convertToMove((posX, posY), self.path.pop(-1))
            else:
                return self.convertToMove((posX, posY), self.path.pop(-1))
        elif livGhost4:
            if not self.path or self.lastGhostPos != (posGhost4X, posGhost4Y):
                self.path = self.findPathBFS(posX, posY, walls, posGhost4X, posGhost4Y)
                self.lastGhostPos = (posGhost4X, posGhost4Y)
                self.path.pop(-1)
                return self.convertToMove((posX, posY), self.path.pop(-1))
            else:
                return self.convertToMove((posX, posY), self.path.pop(-1))
        elif livGhost2:
            if not self.path or self.lastGhostPos != (posGhost2X, posGhost2Y):
                self.path = self.findPathBFS(posX, posY, walls, posGhost2X, posGhost2Y)
                self.lastGhostPos = (posGhost2X, posGhost2Y)
                self.path.pop(-1)
                return self.convertToMove((posX, posY), self.path.pop(-1))
            else:
                return self.convertToMove((posX, posY), self.path.pop(-1))
        return move
