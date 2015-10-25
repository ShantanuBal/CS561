import sys
import pdb

prn_switch = 0
pdb_switch = 0

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

last_line = ""

lines = 0

def printNode(this_player, level, max_val, min_val, curr_player, Alpha, Beta, isLeaf = False):
	global last_line, lines, you

	if isLeaf:
		last = str(max_val * (-1 if you == 2 else 1))
		print_line = this_player + "," + str(level) + "," + last
	else:
		last = max_val if curr_player == 1 else min_val
		last = str(last * (-1 if you == 2 else 1))
		if last == "1000000":
			last = "-Infinity"
		elif last == "-1000000":
			last = "Infinity"
		print_line = this_player + "," + str(level) + "," + last
	
	if Alpha != None:
		print_line += "," + (str(Alpha) if Alpha != -1000000 else "-Infinity") + "," + (str(Beta) if Beta != 1000000 else "Infinity")
	
	if not (print_line.split(",")[0] == last_line.split(",")[0] and print_line.split(",")[1] == last_line.split(",")[1]):
		fout.write(print_line + '\n')
		print print_line
		last_line = print_line
		lines += 1

def miniMax(board2, board1, curr_player, level, cutoff, mancala2, mancala1, isTopLevel, parent, Alpha = None, Beta = None):
	if pdb_switch:
		pdb.set_trace()
	
	if level > cutoff:
		return [mancala1 - mancala2, []]

	max_index, min_index = -1, -1
	max_val = -1000000
	min_val = 1000000
	
	if isTopLevel:
		printNode(parent[0], parent[1], parent[2], parent[3], parent[4], Alpha, Beta)

	for i in range(len(board1)):
		new_board2 = board2[:]
		new_board1 = board1[:]
		new_mancala2 = mancala2
		new_mancala1 = mancala1

		if (curr_player == 1 and new_board1[i] == 0) or (curr_player == 2 and new_board2[i] == 0):
			continue
		
		this_player = ("B" if curr_player == 1 else "A") + str(i+2)

		if prn_switch: 
			print this_player; print " ", new_board2; print new_mancala2, new_board1, new_mancala1
		
		#printNode(this_player, level, max_val, min_val, curr_player)
		
		[new_mancala2, new_mancala1, new_player] = getNextStep(i, new_board2, new_board1, new_mancala2, new_mancala1, curr_player)
		
		if prn_switch: 
			print this_player; print " ", new_board2; print new_mancala2, new_board1, new_mancala1

		new_level = level if new_player == curr_player else level+1
		
		if new_level <= cutoff:
			#printNode(this_player, level, max_val, min_val, curr_player, Alpha, Beta)
			printNode(this_player, level, -1000000, 1000000, curr_player, Alpha, Beta)
		
		value = miniMax(new_board2, new_board1, new_player, new_level, cutoff, new_mancala2, new_mancala1, False, [this_player, level, max_val, min_val, curr_player], Alpha, Beta)
		
		#printNode(this_player, level, max_val, min_val, curr_player)
		#printNode(parent[0], parent[1], parent[2], parent[3], parent[4], True)

		if curr_player == 1:
			if value[0] > max_val:
				max_val = value[0]
				chain = value[1]
				max_index = i
				if Alpha != None and max_val >= Alpha:
					Alpha = max_val
		else:
			if value[0] < min_val:
				min_val = value[0]
				chain = value[1]
				min_index = i
				if Beta != None and min_val <= Beta:
					Beta = min_val
		
		if value[1] == []:
			printNode(this_player, level, value[0], value[0], curr_player, Alpha, Beta, True)
		else:
			printNode(this_player, level, max_val, min_val, curr_player, Alpha, Beta)
		
		
		parent_player = parent[4]
		if parent_player == curr_player:
			#printNode(parent[0], parent[1], parent[2] if parent[2] > max_val else max_val, parent[3] if parent[3] < min_val else min_val, parent[4], Alpha, Beta)
			printNode(parent[0], parent[1], max_val, min_val, parent[4], Alpha, Beta)
		else:
			#printNode(parent[0], parent[1], parent[2] if parent[2] > min_val else min_val, parent[3] if parent[3] < max_val else max_val, parent[4], Alpha, Beta)
			printNode(parent[0], parent[1], min_val,  max_val, parent[4], Alpha, Beta)
		
		if Alpha != None and Alpha >= Beta:
			break

	new_path = [ [curr_player, max_index if curr_player == 1 else min_index] ] + chain
	return [max_val if curr_player == 1 else min_val, new_path]

def getNextStep(i, new_board2, new_board1, new_mancala2, new_mancala1, player):
	n = len(new_board1)
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
				new_mancala1 += new_board2[j-1] + 1
				new_board2[j-1] = 0
				new_board1[j-1] = 0
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
				new_mancala1 += new_board2[j-1] + 1
				new_board2[j-1] = 0
				new_baard1[j-1] = 0
	else:
		j = i-1
		while rem and j >= 0:
			new_board2[j] += 1
			rem -= 1
			j -= 1
			if not rem and new_board2[j+1] == 1:
				new_mancala2 += new_board1[j+1] + 1
				new_board1[j+1] = 0
				new_board2[j+1] = 0
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
				new_mancala2 += new_board1[j+1] + 1
				new_board1[j+1] = 0
				new_board2[j+1] = 0	

	return [new_mancala2, new_mancala1, new_player]

def printNextSteps(path, value, board2, board1, mancala2, mancala1, you):
	curr_index = path[0][1]
	[mancala2, mancala1, new_player] = getNextStep(curr_index, board2, board1, mancala2, mancala1, you)
	
	path_index = 1
	while path_index < len(path) and path[path_index][0] == you:
		[mancala2, mancala1, new_player] = getNextStep(path[path_index][1], board2, board1, mancala2, mancala1, you)
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
	value = miniMax(board2, board1, you, 1, 1, mancala2, mancala1, True, ["root", 0, -1000000,1000000, you], None, None)
	
elif task == 2:
	print "minimax"
	value = miniMax(board2, board1, you, 1, cutoff, mancala2, mancala1, True, ["root", 0, -1000000,1000000, you], None, None)

elif task == 3:
	print "alphabeta"
	value = miniMax(board2, board1, you, 1, cutoff, mancala2, mancala1, True, ["root", 0, -1000000,1000000, you], -1000000, 1000000)

print "Lines: ", lines
printNextSteps(value[1], value, board2, board1, mancala2, mancala1, you)
f.close()
fout.close()
fnext.close()
