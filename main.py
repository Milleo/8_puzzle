import copy
import random
import os
import time
import heapq

class Puzzle_Board():
	PUZZLE_SOLUTION = [['1','2','3'],['4','5','6'],['7','8',' ']]
	pieces = copy.deepcopy(PUZZLE_SOLUTION)
	emptySpaceRow = 2
	emptySpaceColumn = 2
	lastMove = ''
	moves = 0

	def __init__(self, pieces_set = ''):
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

	def __hash__(self):
		return hash(str(self.pieces))

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

	def get_score(self):
		if(self.pieces == self.PUZZLE_SOLUTION):
			return 0

		incorrect_pieces = 0
		piece_distances = 0
		for row_i, row in enumerate(self.pieces):
			for piece_i, piece in enumerate(row):
				if(self.pieces[row_i][piece_i] != self.PUZZLE_SOLUTION[row_i][piece_i]):
					(g_row, g_column) = self.get_piece_correct_position(piece)
					piece_distances += self.get_heuristic_distance((row_i, piece_i), (g_row, g_column))
					incorrect_pieces += 1

		return incorrect_pieces + piece_distances + self.moves

	def get_piece_correct_position(self, piece_value = ''):
		for row_i, row in enumerate(self.PUZZLE_SOLUTION):
			if(piece_value in row):
				index = row.index(piece_value)
				break

		return (row_i, index)

	def get_heuristic_distance(self, piece_coord, goal_coord):
		return (abs(piece_coord[0] - goal_coord[0]) + (abs(piece_coord[1] - goal_coord[1])))


	def __lt__(self, other):
		return self.get_score() < other.get_score()

	def __cmp__(self, other):
		return self.pieces == other

	def __eq__(self, other):
		return self.__cmp__(other)

class SmartBoy():
	history = set()

	def solveIt(self, verbose = True):
		puzzle = Puzzle_Board()
		puzzle.randomize()
		openset = PriorityQueue()
		openset.add(puzzle)

		if(verbose == True):
			print(puzzle)

		while openset:
			current = openset.poll()

			if(self.is_solved(current)):
				puzzle = current
				break

			possibilities = self.get_possible_moves(current)

			for possible_move, puzzle in possibilities.iteritems():
				if hash(puzzle) not in self.history:
					openset.add(puzzle)

			self.history.add(hash(current))
			puzzle.moves = puzzle.moves + 1


			if(verbose == True):
				time.sleep(0.1)
				print(chr(27) + "[2J")
				print(puzzle.moves)
				print(current)

			

		if(verbose == True):
			print("DONE IN " + str(puzzle.moves) + " MOVES")

	def is_solved(self, puzzle):
		if(puzzle == puzzle.PUZZLE_SOLUTION):
			return True
		return False

	def get_possible_moves(self, puzzle):
		if(puzzle == puzzle.PUZZLE_SOLUTION):
			return False

		possibilities = {}
		moves = ['up', 'down', 'left', 'right']

		for move in moves:
			aux = Puzzle_Board(copy.deepcopy(puzzle.pieces))
			aux.moves = puzzle.moves
			possible = getattr(aux, 'move_%s' % move)()

			if (possible == True):
				possibilities[move] = aux
			aux = None

		return possibilities

	
		
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

iterations_avg = 0
sb = SmartBoy()
sb.solveIt()
#for i in range(0, 100):
#	iterations_avg += sb.solveIt(False)
#
#print(iterations_avg / 100)
