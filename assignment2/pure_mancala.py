import sys
import pdb

switch = 0

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
fout = open("traverse_log.txt", "w")
fnext = open("next_state.txt", "w")	

task = int(f.readline())
you = int(f.readline())
cutoff = int(f.readline())
board2= getBoard(f.readline())
board1 = getBoard(f.readline())
mancala2 = int(f.readline())
mancala1 = int(f.readline())

print board2
print board1

def printNode(this_player, level, max_val, min_val, curr_player):
	last = str(max_val) if curr_player == 1 else str(min_val)
	if last == "1000000":
		last = "-Infinity"
	elif last == "-1000000":
		last = "Infinity"
	print_line = this_player + "," + str(level) + "," + last
	fout.write(print_line + '\n')
	print print_line

def miniMax(board2, board1, curr_player, level, cutoff, mancala2, mancala1, n, isTopLevel, Alpha = None, Beta = None):
	if level > cutoff:
		return [mancala1 - mancala2, []]

	max_index, min_index = -1, -1
	max_val = -1000000
	min_val = 1000000
	
	if isTopLevel:
		if curr_player == 1: print_line = "root,0,-Infinity"
		else: print_line = "root,0,Infinity"; 
		fout.write(print_line + '\n');
		print print_line

	for i in range(len(board1)):
		new_board2 = board2[:]
		new_board1 = board1[:]
		new_mancala2 = mancala2
		new_mancala1 = mancala1

		if (curr_player == 1 and new_board1[i] == 0) or (curr_player == 2 and new_board2[i] == 0):
			continue
		
		this_player = ("B" if curr_player == 1 else "A") + str(i+2)

		if switch:
			#checker
			print this_player; print " ", new_board2; print new_mancala2, new_board1, new_mancala1
		
		printNode(this_player, level, max_val, min_val, curr_player)
		
		[new_mancala2, new_mancala1, new_player] = getNextStep(i, new_board2, new_board1, new_mancala2, new_mancala1, n, curr_player)
		
		if switch:
			#checker
			print this_player; print " ", new_board2; print new_mancala2, new_board1, new_mancala1

		new_level = level if new_player == curr_player else level+1
		
		value = miniMax(new_board2, new_board1, new_player, new_level, cutoff, new_mancala2, new_mancala1, n, False, Alpha if Alpha else None, Beta if Beta else None)

		if curr_player == 1:
			if value[0] > max_val:
				max_val = value[0]
				chain = value[1]
				max_index = i
				if Alpha and max_val > Alpha:
					Alpha = max_val
				if Beta and Alpha > Beta:
					break
		else:
			if value[0] < min_val:
				min_val = value[0]
				chain = value[1]
				min_index = i
				if Beta and min_val < Beta:
					Beta = min_val
				if Alpha and  Beta < Alpha:
					break
		
		printNode(this_player, level, max_val, min_val, curr_player)
			
		if isTopLevel:
			if curr_player == 1:
				print_line = "root,0," + str(max_val)
			else:
				print_line = "root,0," + str(min_val)
			fout.write(print_line + '\n')
			print print_line

	new_path = [ [curr_player, max_index if curr_player == 1 else min_index] ] + chain
	return [max_val if curr_player == 1 else min_val, new_path]

def getNextStep(i, new_board2, new_board1, new_mancala2, new_mancala1, n, player):
	new_player = 1 if player == 2 else 2

	if player == 1:
		stones = new_board1[i]
		new_board1[i] = 0
	else:
		stones = new_board2[i]
		new_board2[i] = 0

	quo = stones / (2*n + 1)
	rem = stones % (2*n + 1)

	for j in range(n):
		new_board2[j] += quo
		new_board1[j] += quo
	
	if player == 1:
		new_mancala1 += quo
	else:
		new_mancala2 += quo
	
	if player == 1:
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
				new_mancala1 += new_board2[j-1]
				new_board2[j-1] = 0
	else:
		j = i-1
		while rem and j >= 0:
			new_board2[j] += 1
			rem -= 1
			j -= 1
			if not rem and new_board2[j+1] == 1:
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
				new_mancala2 += new_board1[j+1]
				new_board1[j+1] = 0			

	return [new_mancala2, new_mancala1, new_player]

def printNextSteps(path, value, board2, board1, mancala2, mancala1, you):
	curr_index = path[0][1]
	[mancala2, mancala1, new_player] = getNextStep(curr_index, board2, board1, mancala2, mancala1, len(board2), you)
	
	path_index = 1
	while path_index < len(path) and path[path_index][0] == you:
		[mancala2, mancala1, new_player] = getNextStep(path[path_index][1], board2, board1, mancala2, mancala1, len(board2), you)
		path_index += 1
	line = ""
	for each in board2:
		line += str(each) + " "
	line = line[:-1]
	print line
	fnext.write(line + '\n')

	line = ""
	for each in board1:
		line += str(each) + " "
	line = line[:-1]
	print line
	fnext.write(line + '\n')

	print mancala2
	fnext.write(str(mancala2) + '\n')

	print mancala1
	fnext.write(str(mancala1) + '\n')

fout.write("Node,Depth,Value\n")
if task == 1:
	print "greedy"
	value = miniMax(board2, board1, you, 1, 1, mancala2, mancala1, len(board2), True, None, None)
	
elif task == 2:
	print "minimax"
	value = miniMax(board2, board1, you, 1, cutoff, mancala2, mancala1, len(board2), True, None, None)

elif task == 3:
	print "alphabeta"
	value = miniMax(board2, board1, you, 1, cutoff, mancala2, mancala1, len(board2), True, -1000000, 1000000)

printNextSteps(value[1], value, board2, board1, mancala2, mancala1, you)
f.close()
fout.close()
fnext.close()
