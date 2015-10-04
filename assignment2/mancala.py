import sys
import pdb
#pdb.set_trace()
current = 0

def find_nodes(line):
	node_list = []
	node = ""
	for i in range(len(line)):
		if line[i] == " ":
			node_list.append(node)
			node = ""
		elif line[i] not in ['\n','\r']:
			node += line[i]
	node_list.append(node)
	return node_list

def find_off(line):
	time_list = []
	for each in line:
		time = []
		for every in each.split("-"):
			time.append(int(every)%24)
		time_list.append(time)
	return time_list

# insert node in the right position of the open queue
def insert_node(queue, node, time):
	"""
	for i in range(len(queue)):
		if node == queue[i][0]:
			if time < queue[i][1]:
				queue.pop(i)
				break
			else:
				return queue
	"""
	for i in range(len(queue)):
		if time < queue[i][1] or (time == queue[i][1] and node < queue[i][0]):
			queue = queue[:i] + [[node, time]] + queue[i:]
			break
	else:
		queue.append([node, time])
	return queue

# check if pipe is usable at this point of time
def isPipeActive(time, timeOffList):
	time = time%24
	for each in timeOffList:
		if each[0] <= time <= each[1] or (each[1] < each[0] and (each[0] <= time or time <= each[1])):
			return False
	return True

def UCS(src, des, mid, edg, stt):
	if current == 18:
		pdb.set_trace()
	open_queue = [[src, stt]]
	visited = {}
	while open_queue:
		top = open_queue.pop(0)
		node, time = top[0], top[1]
		if node in des:
			return str(node) + " " + str(time%24)
		if node in visited:
			continue
		visited[node] = True
		if node in edg:
			for edge in edg[node]:
				if isPipeActive(time, edge['off']):
					open_queue = insert_node(open_queue, edge['to'], time+edge['len'])
				else:
					del visited[node]
	return "None"

def DFS(src, des, mid, edg, stt):
	stack = [[src, stt]]
	visited = {}
	while stack:
		top = stack.pop()
		node, time = top[0], top[1]
		if node in des:
			return str(node) + " " + str(time%24)
		if node in visited:
			continue
		visited[node] = True
		if node in edg:
			for edge in edg[node][::-1]:
				stack.append([edge['to'], (time+1)])

	return "None"	


def BFS(src, des, mid, edg, stt):
	queue = [[src, stt]]
	visited = {}
	while queue:
		top = queue.pop(0)
		node, time = top[0], top[1]
		if node in des:
			return str(node) + " " + str(time%24)
		if node in visited:
			continue
		visited[node] = True
		if node in edg:
			for edge in edg[node]:
				queue.append([edge['to'], (time+1)])

	return "None"

f = open(sys.argv[2], "r")
fout = open("output.txt", "w")
cases = int(f.readline())
while current < cases:
	alg = f.readline()[:3]
	line = f.readline()
	src = ""
	for each in line:
		if each in ['\n','\r']:
			break
		else:
			src += each
	des = find_nodes(f.readline())
	mid = find_nodes(f.readline())
	pip = int(f.readline())
	edg = {}
	for i in range(pip):
		pip_info = find_nodes(f.readline())
		off = find_off(pip_info[4:])
		if pip_info[0] not in edg:
			edg[pip_info[0]] = []
		new_edge = {'to':pip_info[1], 'len':int(pip_info[2]), 'off':off}
		edg[pip_info[0]].append(new_edge)
	
	for each in edg:
		edg[each].sort(key=lambda node:node['to'])
	
	stt = int(f.readline())
	empty = f.readline()
	
	if alg == "BFS":
		result = BFS(src, des, mid, edg, stt)
	elif alg == "DFS":
		result = DFS(src, des, mid, edg, stt)
	else:
		result = UCS(src, des, mid, edg, stt)
	fout.write(result + "\n")
	current += 1
f.close()
fout.close()
