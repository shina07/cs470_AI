# searchAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
from game import Actions
import random, util

from game import Agent
import inspect

##this is example agents 
class LeftTurnAgent(Agent):
  "An agent that turns left at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
        
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)

class BFSAgent(Agent):
  """
    Your BFS agent (question 1)
  """
  def __init__(self):
    self.f = open('result.txt', 'w')
    self.current = Node (False, (0, 0))
    
    self.future = []
    self.history = set ()
    self.f.write (str (self.current.position) + '\n')
    setf.history.add (self.current)

    self.visited = False
    self.queue = util.Queue()

  def getAction(self, gameState):

    """
      Returns the BFS seracing action using gamestae.getLegalActions()
      
      legal moves can be accessed like below 
      legalMoves = gameState.getLegalActions()
      this method returns current legal moves that pac-man can have in curruent state
      returned results are list, combination of "North","South","West","East","Stop"
      we will not use stop action for this project
     
      Please write code that Pacman traverse map in BFS order. 
      Because Pac-man does not have any information of map, it should move around in order to get 
      information that is needed to reach to the goal.

      Also please print order of x,y cordinate of location that Pac-man first visit in result.txt file with format
      (x,y)
      (x1,y1)
      (x2,y2)
      .
      .
      . 
      (xn,yn)
      note that position that Pac-man starts is considered to be (0,0)
      
      this method is called until Pac-man reaches to goal
      return value should be one of the direction Pac-man can move ('North','South'....)
    """
    "*** YOUR CODE HERE ***"

    # visited = set() #non-iterable set 

    # # position = gameState.getPacmanPosition()
    # # print (position)

    # state = gameState.getPacmanState()
    # print (state)

    # print (gameState, type (gameState))
    # legal = gameState.getLegalPacmanActions()
    # print (legal)

    # if Directions.STOP in legal: 
    #   legal.remove(Directions.STOP)

    # successors = [(gameState.generateSuccessor(0, action), action) for action in legal] 
    # for s in successors:
    #   print ("SUCCESSORS:\n", s[0], s[1])

    # scored = [(self.evaluationFunction(state), action) for state, action in successors]
    # for sc in scored:
    #   print ("SCORED:\n", sc)

    # bestScore = max(scored)[0]
    # print ("BESTSCORE: \n", bestScore)

    # bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    # for b in bestActions:
    #   print ("BESTS: \n", b)
    # #return random.choice(bestActions)

    # First seen Node
    if not visited:
      legals = gameState.getLegalPacmanActions()

    for legal in legals:
      dx, dy = Actions._directions[legal]
      x, y = self.current.position
      node = Node (False, (x + dx, y + dy))

      if node in self.history or node in self.future:
        continue
      node.parent = self.current
      self.future.append (node)

    dst = self.tovisit[0]
    

class AstarAgent(Agent):
  """
    Your astar agent (question 2)

    An astar agent chooses actions via an a* function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.

  """
  def __init__(self):
    self.path = None
    self.isCallAstar = False

  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses the best movement according to the a* function.

    The return value of a* function is paths made up of Stack. The top
    is the starting point, and the bottom is goal point.

    """

    if self.isCallAstar is False:
        layout = gameState.getWalls()

        # print(layout)

        maps = [[0 for col in range(layout.width)] for row in range(layout.height)]

        for raw in range(layout.height):
            for col in range(layout.width):
                maps[raw][col] = Node(layout[col][layout.height-1 - raw], (col, layout.height-1 - raw))
        
        # the position of pac-man
        start = gameState.getPacmanPosition()

        # the position of food
        goal = gameState.getFood().asList()[0]

        # print(grid[layout.height-1 - start[1]][start[0]].position)
        # print(grid[layout.height-1 - goal[1]][goal[0]].position)
        
        self.path = aStar(maps[layout.height-1 - start[1]][start[0]], maps[layout.height-1 - goal[1]][goal[0]], maps)

        self.isCallAstar = True
    
    if len(self.path.list) < 2:
        self.isCallAstar = False
        return 'Stop'
    else:
        move = self.whatMove(self.path)
        self.path.pop()

    "Add more of your code here if you want to"

    return move

  def whatMove(self, path):
    current = path.pop()
    next = path.pop()
    path.push(next)
    path.push(current)

    if(current.position[0] == next.position[0]):
        if current.position[1] < next.position[1]: return 'North'
        else: return 'South'
    else:
        if current.position[0] < next.position[0]: return 'East'
        else: return 'West'

class Node:
    """
    The value is presence of wall, so it is True or False.
    The parent is previous position. The point is the position of Node.
    It is different from raw and column of matrix.

    """
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.parent = None
        self.H = 0
        self.G = 0

    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.parent = None
        self.H = 0
        self.G = 0

    def __eq__(self, other):
        return self.position == other.position

    # For Node Comparison
    def __gt__(self, other):
        return self.position > other.position

    def __lt__(self, other):
        return self.position < other.position

    def __ge__(self, other):
        return self.position >= other.position

    def __le__(self, other):
        return self.position <= other.position

    # For Set Hash value
    def __hash__(self):
        return hash (self.position)

    def move_cost(self):
        return 1

def getChildren(position, maps):
    """
    Return the children that can move legally

    """
    x, y = position.position
    links = [maps[len(maps)-1 - d[1]][d[0]] for d in [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]]
    return [link for link in links if link.value != True]

def aStar(start, goal, maps):
    """
    The a* function consists of three parameters. The first is the starting
    point of pac-man, the second is the point of food, the last is the presence
    of wall in the map. The map consists of nodes.
    
    Return the coordinates on the Stack where top is the starting point and bottom is
    the goal point.

    For example, if the starting point is (9, 1) and the goal point is (1, 8), you
    return the path like this.

    
    (9, 1) <- top
    (8, 1)

    ...

    (1, 7)
    (1, 8) <- bottom
    """
    path = util.Stack()

    "*** YOUR CODE HERE ***"

    priorityQueue = util.PriorityQueueWithFunction (lambda priority : priority.H + priority.G)
    
    # Heuristic Function
    start.H = util.manhattanDistance (start.position, goal.position)
    # Estimation Function
    start.G = 0

    priorityQueue.push (start)
    history = set ()
    depth = 1

    while True:
      if priorityQueue.isEmpty():
        break

      current = priorityQueue.pop()
      if current == goal:
        break

      history.add (current)

      for node in getChildren (current, maps):

        if node in history: 
          continue
            
        node.parent = current
        node.H = util.manhattanDistance (node.position, goal.position)
        node.G = depth
        priorityQueue.push (node)

      depth += 1

    while True:
      path.push (current)

      if current.parent is None:
        break

      current = current.parent


    return path


