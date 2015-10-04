import sys
import pdb
#pdb.set_trace()

def getBoard(string):
	board = []
	value = ""
	for each in string:
		if each == " ":
			board.append(int(value))
			value = ""
		else:
			value += each
	return board + [int(value)]
	
f = open(sys.argv[2], "r")
fout = open("next_state.txt", "w")
	
task = int(f.readline())
player = int(f.readline())
cutoff = int(f.readline())
board2= getBoard(f.readline())
board1 = getBoard(f.readline())
mancala2 = int(f.readline())
mancala1 = int(f.readline())

def greedy(board2, board1, player, level, cutoff, mancala2, mancala1, n):
	if level > cutoff:
		return mancala1 - mancala2
	max_index = -1
	max_val = -1000
	for i in range(board1):
		new_board2 = board2
		new_board1 = board1
		stones = new_board1[i]
		new_board1[i] = 0
		quo = stone / (2*n + 2)
		rem = stone % (2*n + 2)
		# make this dynamic
		new_player = 2

		for j in range(n):
			new_board2[j] += quo
			new_board1[j] += quo
		j = i+1
		while rem and j < n:
			new_board1[j] += 1
			rem -= 1
			j += 1
			if not rem and new_board1[j-1] == 1:
				new_player = 1
		if rem:
			mancala1 += 1
			rem -= 1
			if not rem:
				new_player = 1

		j = n-1
		while rem and j >= 0:
			new_board2[j] += 1
			j -= 1
			rem -= 1
		j = 0
		while rem and j < i:
			new_board1[j] += 1
			rem -= 1
			j += 1
			

if task == 1:
	greedy(board2, board1, player, 0, cutoff, mancala2, mancala1, len(board2))
elif task == 2:
	miniMax()
elif task == 3:
	alphaBeta()

f.close()
fout.close()
