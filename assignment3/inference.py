import sys
import pdb

prn_switch = 0
pdb_switch = 0

queries = []
truths = {}
clauses = {}

leaves = []

class Query():
	def __init__(self, predicate, constants):
		self.predicate = predicate
		self.constants = constants

def arrangeClauses(head_constants, rules):
	order = {}
	count = 0
	for each in head_constants:
		order[each] = count
		count += 1
	
	new_rules = {}
	for each in rules:
		new_order = []
		for every in each.constants:
			if every in order:
				new_order.append(order[every])
			else:
				new_order.append(every)
		new_rules[each.predicate] = new_order
	
	return new_rules

def parseClause(string):
	global truths, clauses, variables
	if "=>" in string:
		value = string.split(" => ")
		first = value[1]
		head = parseQuery(first)
		second_list = value[0].split(" ^ ")
		rules = []
		for each in second_list:
			rules.append(parseQuery(each))
		
		key = head.predicate+"-"+str(len(head.constants))
		if key in clauses:
			clauses[head.predicate+"-"+str(len(head.constants))].append(arrangeClauses(head.constants, rules))
		else:
			clauses[head.predicate+"-"+str(len(head.constants))] = [arrangeClauses(head.constants, rules)]
	else:
		head = parseQuery(string)
		key = head.predicate+"-"+str(len(head.constants))
		if key in truths:
			truths[key][tuple(head.constants)] = 1
		else:
			truths[key] = {tuple(head.constants):1}		

def parseQuery(string):
	global queries
	predicate, constant, constants = "", "", []
	found = 0
	for each in string:
		if each == ")":
			constants.append(constant)
			break
		elif each == "(":
			found = 1
		elif not found:
			predicate += each
		else:
			if each == ",":
				constants.append(constant)
				constant = ""
			else:
				constant += each
	node = Query(predicate, constants)
	return node

def fetchNewNodes(constants, path):
	new_list = []
	for each in path:
		variables = path[each]
		new_constants = []
		for every in variables:
			if isinstance(every, int):
				new_constants.append(constants[every])
			else:
				new_constants.append(every)
		new_list.append(Query(each, new_constants))
	return new_list

def printQueue(queue, new_queue):
	print "***"
	print "QUEUE"
	for each in queue:
		for every in each[0]:
			print every.predicate, every.constants,
		print 
	print "NEW QUEUE"
	for each in new_queue:
		for every in each[0]:
			print every.predicate, every.constants,
		print
	print "***"

def printLeaves():
	print "\nLEAVES"
	print "====="
	for each in leaves:
		for each_node in each:
			print each_node.predicate, each_node.constants,
		print "\n-----"
	print "====="

def backwardChaining(node, paths):
	global leaves
	if pdb_switch:
		pdb.set_trace()
	
	prev_queue = []
	queue = [ [ [node], paths] ]
	new_queue = []
	while queue:
		#printQueue(queue, new_queue)
		prev_queue = queue[:]
		top = queue.pop(0)
		node_list = top[0]
		node_paths = top[1]
		wasAdded = False

		for i in range(len(node_list)):
			predicate = node_list[i].predicate
			constants = node_list[i].constants
			key = predicate + "-" + str(len(constants))
			if key in node_paths:
				for j in range(len(node_paths[key])):
					new_node_list = node_list[:i] + fetchNewNodes(constants,node_paths[key][j]) + node_list[i+1:] 
					
					new_paths = node_paths.copy()
					new_paths[key] = new_paths[key][:j] + new_paths[key][j+1:]
					new_queue.append([new_node_list, new_paths])
					wasAdded = True
		if not wasAdded:
			leaves.append(node_list)
		if not queue:
			queue = new_queue[:]
			new_queue = []

def capsMatch(truth, constants):
	for i in range(len(truth)):
		if 65 <= ord(constants[i][0]) <= 90:
			if truth[i] != constants[i]:
				return False
	return True

def newAssignment(new_assignment, truth, constants):
	for i in range(len(truth)):
		if not (65 <= ord(constants[i][0]) <= 90):
			new_assignment[constants[i]] = truth[i]

def evaluateLeaf(node_list, assignment):
	global truths
	if pdb_switch:
		pdb.set_trace()

	if not node_list:
		return True
 
	for each in assignment:
		for every_node in node_list:
			node_constants = every_node.constants
			for i in range(len(node_constants)):	
				if node_constants[i] == each:
					node_constants[i] = assignment[each]
		
	top = node_list.pop(0)
	predicate = top.predicate
	constants = top.constants
	
	key = predicate + "-" + str(len(constants))
	value = False
	if key in truths:
		for each in truths[key]:
			if capsMatch(list(each), constants):
				new_assignment = assignment.copy()
				newAssignment(new_assignment, list(each), constants)
				value = value or evaluateLeaf(node_list, new_assignment)
	return value
	
f = open(sys.argv[2], "r")
fout = open("output.txt", "w")

num_queries = int(f.readline())

for i in range(num_queries):
	queries.append(parseQuery(f.readline()))

num_clauses = int(f.readline())
for i in range(num_clauses):
	parseClause(f.readline())

if prn_switch:
	print "\n-- QUERIES --"
	for each in queries:
		print each.predicate, each.constants

	print "\n-- TRUTHS --"
	for each in truths:
		print each, " - ", truths[each]

	print "\n-- CLAUSES --"
	for each in clauses:
		print each, " - "
		for every in clauses[each]:
			print every

	print "\n\n-- ANSWER --"

for query in queries:
	backwardChaining(query, dict(clauses))
	#printLeaves()
	isValid = False
	for each in leaves:
		isValid = isValid or evaluateLeaf(each, {})
	if prn_switch:
		print isValid
	if isValid:
		fout.write("TRUE\n")
	else:
		fout.write("FALSE\n")
	leaves = []

f.close()
fout.close()
