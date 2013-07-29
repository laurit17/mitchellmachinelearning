import itertools

class GameBoard(object):
	"""Representation of TicTacToe board"""

	O, X = 1, 2

	def __init__(self, board=None):
		if not board:
			self.board = [
				[0, 0, 0],
				[0, 0, 0],
				[0, 0, 0]]
		else:
			self.board = board
		self.trace = [self.copyBoard()]

	def hasWon(self, player):
		return self.straightsWithXOfType(player, 3)

	def isDraw(self):
		return ((not self.hasWon(GameBoard.O) and
			not self.hasWon(GameBoard.X)) and
			self.boardFull())

	def gameEnded(self):
		return (self.hasWon(GameBoard.O) or
				self.hasWon(GameBoard.X) or
				self.isDraw())

	def boardFull(self):
		for row in self.board:
			if 0 in row:
				return False
		return True		

	def checkRows(self, player):
		player_row = [player]*3
		for row in self.board:
			if row == player_row:
				return True
		return False

	def checkColumns(self, player):
		player_row = [player]*3
		side = range(3)
		for column_num in side:
			if [self.board[x][column_num] for x in side] == player_row:
				return True
		return False

	def checkDiagonals(self, player):
		player_row = [player]*3
		side = range(3)
		return player_row in ([self.board[x][x] for x in side], 
							  [self.board[x][2 - x] for x in side])


	def possibleMoves(self):
		return [(x, y) for x, y in 
			[inner for outer in 
				[zip([z]*3, range(3)) for z in range(3)] for inner in outer]
					if not self.board[x][y]]

	def chooseMove(self, strategy, player):
		moves = self.possibleMoves()
		evals_of_moves = [(self.evaluateStrategy(move, strategy, player), move) for move in moves]
		return max(evals_of_moves)[1]

	def getFeatures(self, player=None):
		"""factors that go into strategy:
		   - straights containing 1 O and nothing else
		   - straights containing 1 X and nothing else
		   - straights containing 2 O's and nothing else
		   - straights containing 2 X's and nothing else
		   - straights containing 3 O's and nothing else
		   - straights containing 3 X's and nothing else

		   strategy is therefore a 6-tuple of weights

		"""
		if not player:
			player = self.O
		opponent = self.O if player == self.X else self.X

		board_attributes = (
			self.straightsWithXOfType(player, 1),
			self.straightsWithXOfType(opponent, 1),
			self.straightsWithXOfType(player, 2),
			self.straightsWithXOfType(opponent, 2),
			self.straightsWithXOfType(player, 3),
			#self.straightsWithXOfType(opponent, 3),

		)

		return board_attributes

	def evaluateStrategy(self, move, strategy, player):
		x, y = move
		self.addMove(player, x, y)
		board_value = self.evaluateBoard(strategy, player)
		self.board[x][y] = 0
		self.trace.pop()
		return board_value

	def evaluateBoard(self, strategy, player):
		return sum((weight*factor for weight, factor in zip(strategy, self.getFeatures(player=player))))

	def straightsWithXOfType(self, player, num):
		opponent = self.O if player == self.X else self.X
		side = range(3)
		count = sum([1 for row in self.getRows() if opponent not in row and sum(row) == player*num])
		count += sum([1 for column in self.getColumns()
					if opponent not in column and sum(column) == player*num])
		count += sum([1 for diagonal in self.getDiagonals() 
			if opponent not in diagonal and sum(diagonal) == player*num])

		return count

		#return [1 for row in self.getRows() if opponent not in row]  #and sum(row) == player]

	def addMove(self, player, row, col):
		self.board[row][col] = player
		self.trace.append(self.copyBoard())

	def undoMove(self, row, col):
		self.board[row][col] = 0
		self.trace.pop()

	def getRows(self):
		return self.board

	def getColumns(self):
		side = range(3)
		return [[self.board[x][c] for x in side] for c in side]

	def getDiagonals(self):
		side = range(3)
		return [[self.board[x][x] for x in side], [self.board[x][2 - x] for x in side]]

	def copyBoard(self):
		return [list(row) for row in self.board]

	def prettyPrint(self):
		print 
		print '\n'.join(([' '.join([str(entry) for entry in row]) for row in self.board]))
		print



if __name__ == '__main__':
	g = GameBoard()
	print type(g)

	g.prettyPrint()
	g.addMove(GameBoard.O, 1, 1)
	g.addMove(GameBoard.O, 2, 2)
	#g.addMove(GameBoard.X, 0, 1)
	g.addMove(GameBoard.X, 2, 1)
	g.prettyPrint()
	g.chooseMove((1, -1, 1, -1, 1, -1), g.X)
	print g.gameEnded()


