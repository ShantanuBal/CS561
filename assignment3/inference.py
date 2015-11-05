import sys
import pdb

prn_switch = 0
pdb_switch = 0

queries = []
truths = {}
clauses = {}

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
	global truths, clauses
	if "=>" in string:
		value = string.split(" => ")
		first = value[1]
		head = parseQuery(first)
		second_list = value[0].split(" ^ ")
		rules = []
		for each in second_list:
			rules.append(parseQuery(each))
		
		if prn_switch:
			print head.predicate, head.constants
			for each in rules:
				print each.predicate, each.constants,
			print
		key = head.predicate+"-"+str(len(head.constants))
		if key in clauses:
			clauses[head.predicate+"-"+str(len(head.constants))].append(arrangeClauses(head.constants, rules))
		else:
			clauses[head.predicate+"-"+str(len(head.constants))] = [arrangeClauses(head.constants, rules)]
	else:
		head = parseQuery(string)
		if prn_switch: print head.predicate, head.constants
		truths[head.predicate+"-"+str(head.constants)] = 1

def parseQuery(string):
	global queries
	predicate, constant, constants = "", "", []
	found = 0
	for each in string:
		if each == ")":
			constants.append(constant)
			break
		if each == "(":
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

f = open(sys.argv[2], "r")
fout = open("output.txt", "w")

num_queries = int(f.readline())

for i in range(num_queries):
	queries.append(parseQuery(f.readline()))

num_clauses = int(f.readline())
for i in range(num_clauses):
	parseClause(f.readline())

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

f.close()
fout.close()
