from gameboard import GameBoard
from random import choice

DEFAULT_STRATEGY = (0.5, 0.5, 0.5, 0.5, 0.5)
ETA = 0.1



def performanceSystem(first_strategy, board=None, 
                      second_strategy=DEFAULT_STRATEGY):
  if not board:
		board = GameBoard()
  i = len(board.trace)
	while not board.gameEnded():
		player, strategy = GameBoard.X, second_strategy
		if i % 2:
			player, strategy = GameBoard.O, first_strategy
		x, y = board.chooseMove(strategy, player)
		board.addMove(player, x, y)
		i += 1
  return board.trace


def experimentGenerator():
	"""returns random board with 2 pieces already on it"""
	board = GameBoard()
	x, y = choice(board.possibleMoves())
	board.addMove(GameBoard.O, x, y)
	x, y = choice(board.possibleMoves())
	board.addMove(GameBoard.X, x, y)
	return board
	

def critic(trace, strategy):
	"""produces training examples by successor rule"""
	training_examples = []
	for index in range(2, len(trace)):
		if index == len(trace) - 1:
			if GameBoard(trace[index]).isDraw():
				training_examples.append((GameBoard(trace[index]).getFeatures(), 0))
			elif GameBoard(trace[index]).hasWon(GameBoard.O):
				#print "We have won!"
				training_examples.append((GameBoard(trace[index]).getFeatures(), 10))
			else:
				# means we have lost
				#print "We have lost!"
				training_examples.append((GameBoard(trace[index - 1]).getFeatures(), -10))
		elif index % 2 == 0:
			training_examples.append((GameBoard(trace[index - 2]).getFeatures(), GameBoard(trace[index]).evaluateBoard(strategy, GameBoard.O)))
	return training_examples

def dotProduct(first_vector, second_vector):
	"""computes dot product of two tuples of numbers"""
	return sum((first*second for first, second in zip(first_vector, second_vector)))

def generalizer(training_examples, strategy):
	"""creates new hypothesis based on LMS algorithm"""
	for features, score in training_examples:
		v_hat_score = dotProduct(features, strategy)
		strategy = [w + ETA*(score - v_hat_score)*x for w, x in 
                zip(strategy, features)]
	return strategy






if __name__ == '__main__':


	strategy = DEFAULT_STRATEGY


	# board = GameBoard()
	# trace = performanceSystem(strategy)



	for _ in range(50):
		wins, draws, losses = 0, 0, 0
		board = GameBoard()
		for _ in range(50):
			trace = performanceSystem(strategy, experimentGenerator())
			if GameBoard(trace[-1]).hasWon(GameBoard.O):
				wins += 1
			elif GameBoard(trace[-1]).hasWon(GameBoard.X):
				losses += 1
			else:
				draws += 1
        print ("Player won %d, drew %d, lost %d out of %d games using "
               "strategy %s" % (wins, draws, losses, 50, str(strategy)))
        training_examples = critic(performanceSystem(strategy, experimentGenerator()), strategy)
        strategy = generalizer(training_examples, strategy)
		#for _ in range(10:)
		#	board = experimentGenerator()
		#	trace = performanceSystem(strategy, board)
		#	#trace = performanceSystem(strategy)
		#	training_examples = critic(trace, strategy)
		#	strategy = generalizer(training_examples, strategy)


