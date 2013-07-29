import gameboard
from random import choice

ETA = 0.1

'''
class PerformanceSystem(object):

    
    def __init__(self, board, first_strategy, second_strategy):
        if not board:
            self.board = gameboard.GameBoard()
        else:
            self.board = board
        self.first_strategy = first_strategy
        self.second_strategy = second_strategy

    def playGame(self):
        i = len(self.board.trace)
        while not self.board.gameEnded():
            if i % 2:
                player, strategy = gameboard.GameBoard.O, self.first_strategy
            else:
                player, strategy = gameboard.GameBoard.X, self.second_strategy
            x, y = self.board.chooseMove(strategy, player)
            self.board.addMove(player, x, y)
            i += 1
        return self.board.trace
'''

def playGame(board, first_strategy, second_strategy):
    i = len(board.trace)
    while not board.gameEnded():
        if i % 2:
            player, strategy = gameboard.GameBoard.O, first_strategy
        else:
            player, strategy = gameboard.GameBoard.X, second_strategy
        x, y = board.chooseMove(strategy, player)
        board.addMove(player, x, y)
        i += 1
    return board.trace

def produceTrainingExamples(trace, strategy, player):
    training_examples = []
        
    for i in xrange(len(trace)):
        if i == len(trace) - 1:
            training_examples.append(_doEndOfGame(trace, strategy))
        elif i < len(trace) - 2:
            training_examples.append(_successorRule(trace, player, strategy, i))

    return training_examples

def _successorRule(trace, player, strategy, i):
    successor_board = gameboard.GameBoard(trace[i + 2])
    return (gameboard.GameBoard(trace[i]).getFeatures(player), 
            successor_board.evaluateBoard(strategy, player))

def _doEndOfGame(trace, player):
    final_board = gameboard.GameBoard(trace[-1])
    features = final_board.getFeatures(player)
    if final_board.isDraw():
        return (features, 0)
    elif final_board.hasWon(player):
        return (features, 100)
    return (features, -100)

def evaluateStrategy(features, strategy):
    return sum([first*second for first, second in 
                zip(strategy, (1,) + features)])

def computeNewStrategy(training_examples, strategy):
    """creates new hypothesis based on LMS algorithm."""
    for features, score in training_examples:
        v_hat_score = evaluateStrategy(features, strategy)
        strategy = [w + ETA*(score - v_hat_score)*x for w, x in
                    zip(strategy, (1,) + features)]
    return strategy

def generateRandomBoard(moves = 2):
    board = gameboard.GameBoard()
    for i in xrange(moves):
        x, y = choice(board.possibleMoves())
        player = gameboard.GameBoard.O if i % 2 else gameboard.GameBoard.X
        board.addMove(player, x, y)
    return board

def O_won(board):
    return gameboard.GameBoard(board).hasWon(gameboard.GameBoard.O)
def X_won(board):
    return gameboard.GameBoard(board).hasWon(gameboard.GameBoard.X)

if __name__ == '__main__':

    DEFAULT_STRATEGY = (0.5, 1, -1, 2, -2, 3)
    strategy = DEFAULT_STRATEGY

    for _ in xrange(50):
        wins, losses, draws = 0, 0, 0
        for _ in xrange(20):
            initial_board = generateRandomBoard()
            #trace = PerformanceSystem(
            #    initial_board, strategy, DEFAULT_STRATEGY).playGame()
            trace = playGame(initial_board, strategy, DEFAULT_STRATEGY)
            if O_won(trace[-1]):
                wins += 1
            elif X_won(trace[-1]):
                losses += 1
            else:
                draws += 1

        print ("With strategy %s, machine won %d games, lost %d, drew %d" % 
               (str(strategy), wins, losses, draws))
        empty_board = gameboard.GameBoard()
        #trace = PerformanceSystem(
        #    initial_board, strategy, DEFAULT_STRATEGY).
        trace = playGame(initial_board, strategy, DEFAULT_STRATEGY)
        training_examples = produceTrainingExamples(trace,
                                                    strategy,
                                                    gameboard.GameBoard.O)
        strategy = computeNewStrategy(training_examples, strategy)
        
        

                
            
        
    
            
