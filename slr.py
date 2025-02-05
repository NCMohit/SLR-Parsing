import networkx as nx
import matplotlib.pyplot as plt
import follow

########################          TAKING INPUT FROM TEXT          ############################

def filter_rules(rules):
	newrules = []
	for i in rules:
		rule = []
		for j in i:
			rule.append(j.replace("\n",""))
		newrules.append(rule)
	return newrules

rules = []
inputtext = open("rules.txt", "r")
temprules = []
for i in inputtext:
	temprules.append(i.split(","))
rules = filter_rules(temprules)

#rules = [["S","dA","aB"],["A","bA","c"],["B","bB","c"]]
globalsets = []
#rules = [["S","AA"],["A","aA","b"]]
setcount = 0
dfa_mapping_table = []
set_mapping_table = []

########################          GENERATING AUGMENTED GRAMMAR ( CLOSURE OF INIT RULE )          ############################

def set_is_not_complete(dr_vars,finalrules,rules):
	not_complete = 0
	for drvar in dr_vars:
		if(d_rule(drvar,rules) not in finalrules):
			not_complete = 1
	return not_complete

def d_rule(var,rules):
	drule = []
	for rule in rules:
		if rule[0] == var:
			drule.append(var)
			for j in range(1,len(rule)):
				drule.append("."+rule[j])
	return drule

def get_vars(rules):
	getvars = []
	for i in rules:
		getvars.append(i[0])
	return getvars

def get_dr_vars(finalrules,rules):
	drvars = []
	for rule in finalrules:
		for x in rule[1:]:
			#print(x)
			if(x.index(".")<len(x)-1):
				dr = x[x.index(".")+1]
				if(dr in get_vars(rules)):
					drvars.append(dr)
	return drvars

def gen_aug_grammar(initrules,rules):
	finalrules = []
	for i in initrules:
		finalrules.append(i)
	dr_vars = get_dr_vars(finalrules,rules)
	while(set_is_not_complete(dr_vars,finalrules,rules)):
		for var in dr_vars:
			drule = d_rule(var,rules)
			if(drule not in finalrules):
				finalrules.append(drule)
		dr_vars = get_dr_vars(finalrules,rules)
	return finalrules

########################          FINDING ARROWS FOR AUGMENTED GRAMMAR          ############################

def find_arrows(aug_grammar):
	drvars = []
	for rule in aug_grammar:
		for x in rule[1:]:
			#print(x)
			if(x.index(".")<len(x)-1):
				dr = x[x.index(".")+1]
				drvars.append(dr)
	return drvars	

########################          GENERATING NEW RULES FOR NEXT SET          ############################

def gen_new_initrules(arrow,aug_grammar):
	newinitrules = []
	for rule in aug_grammar:
		for x in rule[1:]:
			if(x.index(".")<len(x)-1):
				dr = x[x.index(".")+1]
				if(dr==arrow):
					g = "."+dr
					right = x.replace(g,g[::-1])
					newinitrules.append([rule[0],right])
	return newinitrules

########################          RECURSIVE SLR GENERATION CODE          ############################

def get_aug_grammar_number(set_mapping_table,initrule):
	number = 100
	for i in set_mapping_table:
		if(i[1][0]==initrule):
			number = i[0]
	return number

def gen_slr(initrules,rules,prevset,prevarrow):
	global setcount
	global globalsets
	sets = []
	setcount += 1
	thisset = setcount
	aug_grammar = gen_aug_grammar(initrules,rules)
	if(prevset!=None):
		dfa_mapping_table.append([prevset,prevarrow,setcount])
	sets.append(aug_grammar)
	globalsets.append(aug_grammar)
	set_mapping_table.append([setcount,aug_grammar])
	arrows = find_arrows(aug_grammar)
	for arrow in arrows:
		#print(thisset,arrow)
		newinitrules = gen_new_initrules(arrow,aug_grammar)
		flag = 0
		for currentset in globalsets:
			if(newinitrules[0] in currentset):
				flag = 1
				# if(newinitrules[0][-1][-1]!="."):
				dfa_mapping_table.append([thisset,arrow,get_aug_grammar_number(set_mapping_table,newinitrules[0])])
		if(flag==0):
			nextsets = gen_slr(newinitrules,rules,prevset= thisset,prevarrow= arrow)
			sets = sets + nextsets[0]
			#dfa_mapping_table.append([get_aug_grammar_number(set_mapping_table,aug_grammar),arrow,get_aug_grammar_number(set_mapping_table,nextsets[0][0])])
	return [sets,setcount]

############          GENERATING DFA GRAPH          ################

def create_graph():
	G = nx.DiGraph() 
	edges = []
	labels = {}
	for i in dfa_mapping_table:
		edges.append([i[0],i[2]])
		G.add_edge(i[0],i[2])
		#labels[(i[0],i[2])] = i[1]
	pos=nx.circular_layout(G)
	nx.draw_networkx(G, with_label = True, node_color ='green') 
	nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
	plt.show()

############          GENERATING SLR PARSING TABLE          ################

def get_all_elems(rules):
	elems = ["$"]
	for rule in rules:
		for i in rule:
			for j in i:
				if(j not in elems):
					elems.append(j)
	elems.sort()
	return elems

def gen_matrix(elems):
	matrix = []
	matrix.append([" "]+elems)
	for i in set_mapping_table:
		matrix.append([i[0]]+["-"]*len(elems))
	return matrix

def gen_numbered_rules(rules):
	num_rules = []
	counter = 0
	for rule in rules:
		for j in rule[1:]:
			counter+=1
			num_rules.append([counter,[rule[0],j]])
	return num_rules

def insert_matrix(matrix,setnum,arrow,value):
	for i in range(len(matrix)):
		if(matrix[i][0]==setnum):
			matrix[i][matrix[0].index(arrow)] = value
	return matrix

def get_matrix(matrix,setnum,arrow):
	for i in range(len(matrix)):
		if(matrix[i][0]==setnum):
			return matrix[i][matrix[0].index(arrow)]

def get_SR_value(setnum,arrow,num_rules,rules,temp=0):
	nextset = None
	for i in set_mapping_table:
		if(i[0]==setnum):
			if(i[1][0][1].index(".")==len(i[1][0][1])-1):
				undottedrule = [i[1][0][0],i[1][0][1].replace(".","")]
				for num_rule in num_rules:
					if(temp==1):
						if((num_rule[1]==undottedrule)):
							return "R"+str(num_rule[0])						
					if((num_rule[1]==undottedrule) & (arrow in follow.finding_follow(rules,undottedrule[0]))):
						return "R"+str(num_rule[0])
			if((i[1][0][1]==rules[0][0]+".") & (arrow=="$")):
				return "Accept"
	for i in dfa_mapping_table:
		if((i[0]==setnum) & (i[1]==arrow)):
			nextset = i[2]
	if((arrow.isupper()) & (nextset!=None)):
		return nextset
	if(nextset!=None):
		return "S"+str(nextset)
	return nextset

def gen_temp(matrix,num_rules,rules):
	for i in range(1,len(matrix)):
		for j in range(1,len(matrix[i])):
			matrix[i][j] = get_SR_value(matrix[i][0],matrix[0][j],num_rules,rules,temp=1)
	return matrix

def gen_parsing_table(matrix,num_rules,rules):
	for i in range(1,len(matrix)):
		for j in range(1,len(matrix[i])):
			matrix[i][j] = get_SR_value(matrix[i][0],matrix[0][j],num_rules,rules)
	return matrix

def get_num_rule(num_rules,num):
	for rule in num_rules:
		if(rule[0]==num):
			return rule[1]

############          PARSING INPUT STRING USING PARSING TABLE         ################

def parse_input(inputstring,pars_table,num_rules):
	inputpointer = 0
	stack = ["1"]
	accepted = 0
	while(inputpointer<len(inputstring)):
		if(inputstring[inputpointer] not in pars_table[0]):
			break
		srval = get_matrix(pars_table,int(stack[len(stack)-1]),inputstring[inputpointer])
		if((len(stack)==0) | (srval == None)):
			break
		if(srval=="Accept"):
			accepted = 1
			break
		elif(srval[0]=="S"):
			stack.append(inputstring[inputpointer])
			inputpointer += 1
			stack.append(srval[1:])
		elif(srval[0]=="R"):
			lengthreduce = len(get_num_rule(num_rules,int(srval[1:]))[1])
			for i in range(lengthreduce):
				stack = stack[0:len(stack)-1]
				stack = stack[0:len(stack)-1]
			stack.append(get_num_rule(num_rules,int(srval[1:]))[0])
			stack.append(str(get_matrix(pars_table,int(stack[len(stack)-2]),stack[len(stack)-1])))
		print("Stack: ",stack)
		print("Input string pointer: ",inputpointer)
	if(accepted==1):
		return 1
	else:
		return 0

############          MAIN CODE EXECUTION         ################

sets = gen_slr([[rules[0][0]+"'","."+rules[0][0]]],rules,prevset=None,prevarrow=None)[0]
print("Sets mapping table (Mapping of numbers to set): ")
for i in set_mapping_table:
	print(i)

print("\nDFA mapping table: ")
print("Here left element represents initial set number, middle represents arrow and right represents goto set number")
for i in dfa_mapping_table:
	print(i)

elems = get_all_elems(rules)
num_rules = gen_numbered_rules(rules)
matrix = gen_matrix(elems)
pars_table = gen_parsing_table(matrix,num_rules,rules)

print("\nParsing Table: \n")
for i in pars_table:
	for j in i:
		print(" "*(6-len(str(j)))+str(j),end=" ")
	print()

inputstring = input("Enter a string you want to parse: ")

accepted = parse_input(inputstring+"$",gen_temp(matrix,num_rules,rules),num_rules)
if(accepted==1):
	print("String accepted")
else:
	print("String rejected")

create_graph()
