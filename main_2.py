import copy
import random
import heapq
import time

class Puzzle_Board(object):

	def __init__(self, pieces_set = '', moves = 0):
		self.PUZZLE_SOLUTION = [['1','2','3'],['4','5','6'],['7','8',' ']]
		self.pieces = copy.deepcopy(self.PUZZLE_SOLUTION)
		self.emptySpaceRow = 2
		self.emptySpaceColumn = 2
		self.lastMove = ''
		self.moves = moves

		if(pieces_set != ''):
			self.pieces = pieces_set
			self.emptySpaceRow, self.emptySpaceColumn = self.get_empty_piece_pos()
		return	

	def __str__(self):
		output = ''
		for row in self.pieces:
			row_str = ""
			for piece in row:
				row_str += "[" + str(piece) + "]"
			output += row_str + "\n"

		return output

	def move_up(self):
		if(self.emptySpaceRow > 0):
			value = self.pieces[self.emptySpaceRow - 1][self.emptySpaceColumn]
			self.pieces[self.emptySpaceRow - 1][self.emptySpaceColumn] = ' '
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn] = value
			self.emptySpaceRow -= 1

			return True
		return False

	def move_down(self):
		if(self.emptySpaceRow < 2):
			value = self.pieces[self.emptySpaceRow + 1][self.emptySpaceColumn]
			self.pieces[self.emptySpaceRow + 1][self.emptySpaceColumn] = ' '
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn] = value
			self.emptySpaceRow += 1

			return True
		return False
		
	def move_left(self):
		if(self.emptySpaceColumn > 0):
			value = self.pieces[self.emptySpaceRow][self.emptySpaceColumn - 1]
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn - 1] = ' '
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn] = value
			self.emptySpaceColumn -= 1

			return True
		return False

	def move_right(self):
		if(self.emptySpaceColumn < 2):
			value = self.pieces[self.emptySpaceRow][self.emptySpaceColumn + 1]
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn + 1] = ' '
			self.pieces[self.emptySpaceRow][self.emptySpaceColumn] = value
			self.emptySpaceColumn += 1

			return True
		return False

	def randomize(self, turns=9999):
		moves = ['up', 'right', 'down', 'left']

		for turn in range(1,turns):
			random_move = random.choice(moves)
			getattr(self, 'move_%s' % random_move)()

	def get_empty_piece_pos(self):
		for row_i, row in enumerate(self.pieces):
			if(' ' in row):
				index = (row_i, row.index(' '))
				break

		return index

	def is_solved(self):
		if(self.pieces == self.PUZZLE_SOLUTION):
			return True
		return False

class State(Puzzle_Board):

	def __init__(self, pieces_set = '', moves = 0, parent = None):
		super(State, self).__init__(pieces_set, moves)
		self.parent = parent

	def get_score(self):
		if(self == self.PUZZLE_SOLUTION):
			return 0

		incorrect_pieces = 0
		piece_distances = 0
		for row_i, row in enumerate(self.pieces):
			for piece_i, piece in enumerate(row):
				if(self.pieces[row_i][piece_i] != self.PUZZLE_SOLUTION[row_i][piece_i]):
					(g_row, g_column) = self.get_piece_correct_position(piece)
					piece_distances += self.get_heuristic_distance((row_i, piece_i), (g_row, g_column))
					incorrect_pieces += 1

		return piece_distances + self.moves

	def get_piece_correct_position(self, piece_value = ''):
		for row_i, row in enumerate(self.PUZZLE_SOLUTION):
			if(piece_value in row):
				index = row.index(piece_value)
				break

		return (row_i, index)

	def get_heuristic_distance(self, piece_coord, goal_coord):
		return (abs(piece_coord[0] - goal_coord[0]) + (abs(piece_coord[1] - goal_coord[1])))

	def __hash__(self):
		return hash(str(self.pieces))

	def __lt__(self, other):
		return self.get_score() < other.get_score()

	def __cmp__(self, other):
		return self.pieces == other

	def __eq__(self, other):
		return self.__cmp__(other)

class PriorityQueue:
	pq = []

	def add(self, item):
		heapq.heappush(self.pq, item)

	def poll(self):
		return heapq.heappop(self.pq)

	def remove(self, item):
		value = self.pq.remove(item)
		heapq.heapify(self.pq)
		return value is not None

	def __len__(self):
		return len(self.pq)

class SmartBoy():

	def solveIt(self):
		start = time.time()
		self.history = set()
		puzzle = Puzzle_Board()
		openset = PriorityQueue()
		puzzle.randomize()

		start_state = State(puzzle.pieces)
		openset.add(start_state)

		while openset:
			current = openset.poll()

			if(current == puzzle.PUZZLE_SOLUTION):
				end = time.time()
				return current.moves, float(end - start)

			possibilities = self.get_possible_moves(current)
			for move, state in possibilities.iteritems():
				if hash(state) not in self.history:
					openset.add(state)

			self.history.add(hash(current))

	def get_possible_moves(self, puzzle):
		possibilities = {}
		moves = ['up', 'down', 'left', 'right']

		moves_count = puzzle.moves + 1
		for move in moves:
			state = State(copy.deepcopy(puzzle.pieces), moves_count, puzzle)
			possible = getattr(state, 'move_%s' % move)()

			if (possible == True):
				possibilities[move] = state
			state = None

		return possibilities

	def rebuild_path(self, end):
		path = [end]
		state = end.parent
		while state.parent:
			path.append(state)
			state = state.parent

		return path

total = 0
total_time = 0.0

for i in range(1, 100):
	sm = SmartBoy()
	count, time_taken = sm.solveIt()
	total += count
	total_time += time_taken
	sm = None

print(total/100)
print(total_time/100)