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
you = int(f.readline())
cutoff = int(f.readline())
print "cutoff: ", cutoff
board2= getBoard(f.readline())
board1 = getBoard(f.readline())
mancala2 = int(f.readline())
mancala1 = int(f.readline())

path = []
print task, you, cutoff
print board2
print board1
print mancala2, mancala1

def miniMax(board2, board1, curr_player, level, cutoff, mancala2, mancala1, n):

	if level == cutoff:
		return [mancala1 - mancala2, []]
	
	max_index, min_index = -1, -1
	max_val = -10000000
	min_val = 10000000
	
	if curr_player == 1 and board1.count(0) == len(board1):
		return mancala1 - mancala2 - sum(board2)
	if curr_player == 2 and board2.count(0) == len(board2):
		return mancala1 + sum(board1) - mancala2

	for i in range(len(board1)):
		new_board2 = board2[:]
		new_board1 = board1[:]
		new_mancala2 = mancala2
		new_mancala1 = mancala1
		if curr_player == 1:
			stones = new_board1[i]
			if stones == 0:
				continue
			else:
				print "B" + str(i+1) + "," + str(level) + "," + str(max_val)
			new_board1[i] = 0
		else:
			stones = new_board2[i]
			if stones == 0:
				continue
			else:
				print "A" + str(i+1) + "," + str(level) + "," + str(min_val)
			new_board2[i] = 0

		quo = stones / (2*n + 1)
		rem = stones % (2*n + 1)
		
		# set new player
		new_player = 2 if curr_player == 1 else 1

		for j in range(n):
			new_board2[j] += quo
			new_board1[j] += quo
		
		if curr_player == 1:
			new_mancala1 += quo
		else:
			new_mancala2 += quo
		
		if curr_player == 1:
			j = i+1
			while rem and j < n:
				new_board1[j] += 1
				rem -= 1
				j += 1
				if not rem and new_board1[j-1] == 1:
					#new_player = 1
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
					#new_player = 1
					new_mancala1 += new_board2[j-1]
					new_board2[j-1] = 0
		else:
			j = i-1
			while rem and j >= 0:
				new_board2[j] += 1
				rem -= 1
				j -= 1
				if not rem and new_board2[j+1] == 1:
					#new_player = 2
					new_mancala2 += new_board1[j+1]
					new_board1[j+1] = 0
			if rem:
				new_mancala2 += 1
				rem -= 1
				if not rem:
					new_player = 2

			j = 0
			while rem and j < n:
				new_board1[j] += 1
				j += 1
				rem -= 1
			j = n-1
			while rem and j > i:
				new_board2[j] += 1
				rem -= 1
				j -= 1
				if not rem and new_board2[j+1] == 1:
					#new_player = 2
					new_mancala2 += new_board1[j+1]
					new_board1[j+1] = 0


		if new_player == curr_player:
			new_level = level
		else:
			new_level = level + 1
		
		value = miniMax(new_board2, new_board1, new_player, new_level, cutoff, new_mancala2, new_mancala1, n)
		
		if curr_player == 1:
			if value[0] > max_val:
				print "A" + str(i+1) + "," + str(level) + "," + str(max_val)
				max_val = value[0]
				chain = value[1]
				max_index = i
		else:
			if value[0] < min_val:
				print "B" + str(i+1) + "," + str(level) + "," + str(max_val)
				min_val = value[0]
				chain = value[1]
				min_index = i

	#path.append([curr_player, max_index if curr_player == 1 else min_index])
	new_path = [ [curr_player, max_index if curr_player == 1 else min_index] ] + chain
	return [max_val if curr_player == 1 else min_val, new_path]

def getNextStep(i, new_board2, new_board1, new_mancala2, new_mancala1, n):
	stones = new_board1[i]
	new_board1[i] = 0
	quo = stones / (2*n + 1)
	rem = stones % (2*n + 1)

	for j in range(n):
		new_board2[j] += quo
		new_board1[j] += quo
	new_mancala1 += quo

	j = i+1
	while rem and j < n:
		new_board1[j] += 1
		rem -= 1
		j += 1
		if not rem and new_board1[j-1] == 1:
			new_mancala1 += new_board2[j-1]
			new_board2[j-1] = 0
	if rem:
		new_mancala1 += 1
		rem -= 1

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
			new_mancala1 += new_board2[j-1]
			new_board2[j-1] = 0
	
	return [new_mancala2, new_mancala1]

def printNextSteps(path, value, board2, board1, mancala2, mancala1):
	curr_index = path[0][1]
	[mancala2, mancala1] = getNextStep(curr_index, board2, board1, mancala2, mancala1, len(board2))
	
	path_index = 1
	while path_index < len(path) and path[path_index][0] == 1:
		[mancala2, mancala1] = getNextStep(path[path_index][1], board2, board1, mancala2, mancala1, len(board2))
		path_index += 1
	for each in board2:
		print each,
	print
	for each in board1:
		print each,
	print
	print mancala2
	print mancala1

if task == 1:
	print "greedy"
	value = miniMax(board2, board1, you, 0, 1, mancala2, mancala1, len(board2))
	
elif task == 2:
	print "minimax"
	value = miniMax(board2, board1, you, 0, cutoff, mancala2, mancala1, len(board2))

elif task == 3:
	alphaBeta()

print "Value: ", value[0]
print "Path: ", value[1]
printNextSteps(value[1], value, board2, board1, mancala2, mancala1)
f.close()
fout.close()
