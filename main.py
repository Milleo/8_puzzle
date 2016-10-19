# -*- coding: utf-8 -*-
import copy
import heapq
import os
import random
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

	def solveIt(self, verbose = False, passo_a_passo = False):
		start = time.time()
		self.history = set()
		puzzle = Puzzle_Board()
		openset = PriorityQueue()
		puzzle.randomize()

		if(verbose == True):
			print("Estado inicial do quebra-cabeças")
			print(puzzle)

		start_state = State(puzzle.pieces)
		openset.add(start_state)

		while openset:
			current = openset.poll()

			if(current == puzzle.PUZZLE_SOLUTION):
				end = time.time()
				
				if(verbose == True):
					path = self.rebuild_path(current)
					for state in reversed(path):
						print(state)
						if(passo_a_passo == True):
							raw_input()

					print("=" * 30)
					print("Quebra-cabeças solucionado em " + str(current.moves) + " movimentos")
					print("Em um total de: " + str(float(end - start)) + " segundos")
					print("=" * 30 + "\n\n")
				
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


def sair():
	exit()

def resolver_quebra_cabecas():
	sm = SmartBoy()
	sm.solveIt(True)

def media_resolucao():
	qtde_iteracoes = raw_input("Insira a quantidade de iterações para extrair a média [Padrão: 100]: ")
	total_movimentos = 0
	total_tempo = 0.0

	for i in range(1, int(qtde_iteracoes)):
		sm = SmartBoy()
		movimentos, tempo = sm.solveIt()
		total_movimentos += movimentos
		total_tempo += tempo

	media_movimentos = total_movimentos / int(qtde_iteracoes)
	media_tempo = total_tempo / int(qtde_iteracoes)

	print("Média de movimentos para cada solução: " + str(media_movimentos))
	print("Tempo médio para cada solulção: " + str(media_tempo) + " segundos")

def passo_a_passo():
	sm = SmartBoy()
	sm.solveIt(True, True)

while(True):
	opcoes = {
		1: { 'label': "Solucionar Quebra-cabeças", 'function': resolver_quebra_cabecas },
		2: { 'label': "Ver o passo-a-passo da solução do quebra-cabeças", 'function': passo_a_passo },
		3: { 'label': "Extrair média de resolução por movimentos e tempo", 'function': media_resolucao },
		4: { 'label': "Sair", 'function': sair }
	}

	os.system('clear')

	print("=" * 30)
	print(("=" * 10) + " 8 Puzzle " + ("=" * 10))
	print("=" * 30)
	for numero, opcao in opcoes.iteritems():
		print(str(numero) + ' - ' + opcao['label'])

	opcao_input = raw_input("\nOpcao: ")

	opcao_escolhida = opcoes.get(int(opcao_input), lambda: "nothing")
	funcao = opcao_escolhida['function']

	funcao()

	raw_input("Pressione qualquer tecla para continuar...")