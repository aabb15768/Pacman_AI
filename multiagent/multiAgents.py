# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):

        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        from util import manhattanDistance
        foods = newFood.asList()
        score = 0

        for food in foods:
            foodDistance = manhattanDistance(newPos, food)
            if foodDistance <= 1:
                score += 3
            elif foodDistance <= 2:
                score += 2
            elif foodDistance <= 3:
                score += 1
            elif foodDistance <= 6:
                score += 0.5
            elif foodDistance <= 12:
                score += 0.25
            else:
                score += 0.15

        for ghostPos in successorGameState.getGhostPositions():
            if ghostPos == newPos and newScaredTimes[0] > 0:
                return 1000000
            elif ghostPos == newPos and newScaredTimes[0] == 0:
                return -1000000
            elif manhattanDistance(ghostPos, newPos) <= 1:
                return -1000
            elif manhattanDistance(ghostPos, newPos) <= 2:
                return -500
            elif manhattanDistance(ghostPos, newPos) <= 3:
                return -250

        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        class Move:
            def __init__(self):
                self.cost = -99999999
                self.action = 0

        def miniMax(gameState, agent, depth):
            move = Move()
            if depth == self.depth or not gameState.getLegalActions(agent):
                move.cost = self.evaluationFunction(gameState)
                return move
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = 0
            else:
                nextAgent = agent + 1

            for action in gameState.getLegalActions(agent):
                if move.cost == -99999999:
                    nextMove = miniMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                    move.action = action
                    move.cost = nextMove.cost
                else:
                    previousCost = move.cost
                    nextMove = miniMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                    if nextMove.cost > previousCost:
                        if agent == 0:
                            move.cost = nextMove.cost
                            move.action = action
                    else:
                        if agent != 0:
                            move.cost = nextMove.cost
                            move.action = action
            return move

        move = miniMax(gameState, 0, 0)
        return move.action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        class Move:
            def __init__(self):
                self.cost = -99999999
                self.action = 0

        def alphaBetaPruning(gameState, agent, depth, alpha, beta):
            move = Move()
            if depth == self.depth or not gameState.getLegalActions(agent):
                move.cost = self.evaluationFunction(gameState)
                return move
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = 0
            else:
                nextAgent = agent + 1
            if agent == 0:
                for action in gameState.getLegalActions(agent):
                    if move.cost == -99999999:
                        nextMove = alphaBetaPruning(gameState.generateSuccessor(agent, action), nextAgent, depth, alpha, beta)
                        move.action = action
                        move.cost = nextMove.cost
                        alpha = max(move.cost, alpha)
                    else:
                        if move.cost > beta:
                            return move
                        nextMove = alphaBetaPruning(gameState.generateSuccessor(agent, action), nextAgent, depth, alpha, beta)
                        if nextMove.cost > move.cost:
                            move.cost = nextMove.cost
                            move.action = action
                            alpha = max(move.cost, alpha)
            else:
                for action in gameState.getLegalActions(agent):
                    if move.cost == -99999999:
                        nextMove = alphaBetaPruning(gameState.generateSuccessor(agent, action), nextAgent, depth, alpha, beta)
                        move.action = action
                        move.cost = nextMove.cost
                        beta = min(move.cost, beta)
                    else:
                        if move.cost < alpha:
                            return move
                        nextMove = alphaBetaPruning(gameState.generateSuccessor(agent, action), nextAgent, depth, alpha, beta)
                        if nextMove.cost < move.cost:
                            move.cost = nextMove.cost
                            move.action = action
                            beta = min(move.cost, beta)
            return move

        move = alphaBetaPruning(gameState, 0, 0, -float("inf"), float("inf"))
        return move.action
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        class Move:
            def __init__(self):
                self.cost = -99999999
                self.action = 0

        def expectiMax(gameState, agent, depth):
            move = Move()
            if depth == self.depth or not gameState.getLegalActions(agent):
                move.cost = self.evaluationFunction(gameState)
                return move
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = 0
            else:
                nextAgent = agent + 1
            if agent == 0:
                for action in gameState.getLegalActions(agent):
                    if move.cost == -99999999:
                        nextMove = expectiMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                        move.action = action
                        move.cost = nextMove.cost
                    else:
                        nextMove = expectiMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                        if nextMove.cost > move.cost:
                            move.cost = nextMove.cost
                            move.action = action
            else:
                for action in gameState.getLegalActions(agent):
                    move.action = action
                    if move.cost == -99999999:
                        nextMove = expectiMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                        move.cost = (1.0/len(gameState.getLegalActions(agent))) * nextMove.cost
                    else:
                        nextMove = expectiMax(gameState.generateSuccessor(agent, action), nextAgent, depth)
                        move.cost += (1.0/len(gameState.getLegalActions(agent))) * nextMove.cost
            return move
            #end def:expectiMax
        move = expectiMax(gameState, 0, 0)
        return move.action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
