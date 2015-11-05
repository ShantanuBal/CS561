import sys
import pdb

prn_switch = 0
pdb_switch = 0

queries = []
clauses = {}

class Query():
	def __init__(self, predicate, constants):
		self.predicate = predicate
		self.constants = constants

def parseClause(string):
	print string

def parseQuery(string):
	global queries
	predicate, constant, constants = "", "", []
	found = 0
	for each in string[:-1]:
		if each == "(":
			found = 1
		elif not found:
			predicate += each
		else:
			if each == ",":
				constants.append(constant)
				constant += ""
			else:
				constant += each
	constants.append(constant)
	queries.append(Query(predicate, constants))
	print queries[-1].predicate, queries[-1].constants

f = open(sys.argv[2], "r")
fout = open("output.txt", "w")

queries = int(f.readline())

for i in range(queries):
	parseQuery(f.readline())

clauses = int(f.readline())
for i in range(clauses):
	parseClause(f.readline())

fout.close()
fnext.close()
