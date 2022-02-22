# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Directions
from game import GameStateData
import random


##Isa
import sys


class KeyboardAgent(Agent):
   # NOTE: Arrow keys also work.
    WEST_KEY  = 'a'
    EAST_KEY  = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []

    def getAction( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

    def printLineData(self, gameState):
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
        walls_flattened = str(walls).replace("\n", "")
        # concatenating all variables into single line
        wallDimensionsX = walls.width
        wallDimensionsY = walls.height

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
        food = gameState.getFood()

        foodFlattened = str(food).replace("\n", "")

        score = gameState.getScore()

        csv_vals = [posX, posY, directionPacman, directionGhost1, directionGhost2, directionGhost3, directionGhost4,
                    distanceGhosts1,
                    distanceGhosts2, distanceGhosts3, distanceGhosts4, walls_flattened, wallDimensionsX,
                    wallDimensionsY,
                    posGhost1X, posGhost1Y, posGhost2X, posGhost2Y, posGhost3X, posGhost3Y, posGhost4X, posGhost4Y,
                    legalNorth, legalSouth, legalEast, legalWest, legalStop, livingGhost1, livingGhost2, livingGhost3,
                    livingGhost4,
                    foodFlattened, score]

        line = ""
        for val in csv_vals:
            line += str(val) + ","
        return line + "\n"

        
