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

print task, player, cutoff
print board2
print board1
print mancala2, mancala1

def greedy(board2, board1, player, level, cutoff, mancala2, mancala1, n):
	if level == cutoff:
		return [mancala1 - mancala2, None]
	max_index = -1
	max_val = -1000
	for i in range(len(board1)):
		new_board2 = board2[:]
		new_board1 = board1[:]
		new_mancala2 = mancala2
		new_mancala1 = mancala1
		stones = new_board1[i]
		new_board1[i] = 0
		quo = stones / (2*n + 2)
		rem = stones % (2*n + 2)
		# make this dynamic
		new_player = 2

		for j in range(n):
			new_board2[j] += quo
			new_board1[j] += quo
		new_mancala2 += quo
		new_mancala1 += quo

		j = i+1
		while rem and j < n:
			new_board1[j] += 1
			rem -= 1
			j += 1
			if not rem and new_board1[j-1] == 1:
				new_player = 1
				new_mancala1 += new_board2[j-1]
				new_board2[j-1] = 0
		if rem:
			new_mancala1 += 1
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
			if not rem and new_board1[j-1] == 1:
				new_player = 1
				new_mancala1 += new_board2[j-1]
				new_board2[j-1] = 0

		if new_player == player:
			new_level = level
		else:
			new_level = level + 1
		value = greedy(new_board2, new_board1, new_player, new_level, cutoff, new_mancala2, new_mancala1, n)
		if value[0] > max_val:
			max_val = value[0]
			max_index = i
	
	return [max_val, max_index]

if task == 1:
	value = greedy(board2, board1, player, 0, 1, mancala2, mancala1, len(board2))
	print value
elif task == 2:
	miniMax()
elif task == 3:
	alphaBeta()

f.close()
fout.close()
