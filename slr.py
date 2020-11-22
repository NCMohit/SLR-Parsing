#rules = [["S","dA","aB"],["A","bA","c"],["B","bB","c"]]
globalsets = []
rules = [["S","AA"],["A","aA","b"]]
setcount = 0
dfa_mapping_table = []
set_mapping_table = []

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

def find_arrows(aug_grammar):
	drvars = []
	for rule in aug_grammar:
		for x in rule[1:]:
			#print(x)
			if(x.index(".")<len(x)-1):
				dr = x[x.index(".")+1]
				drvars.append(dr)
	return drvars	

def gen_new_initrules(arrow,aug_grammar):
	newinitrules = []
	for rule in aug_grammar:
		for x in rule[1:]:
			dr = x[x.index(".")+1]
			if(dr==arrow):
				g = "."+dr
				right = x.replace(g,g[::-1])
				newinitrules.append([rule[0],right])
	return newinitrules

# aug_grammar = gen_aug_grammar([["S'",".S"]],rules)
# print(aug_grammar)
# arrows = find_arrows(aug_grammar)
# print(arrows)
# for arrow in arrows:
# 	newinitrules = gen_new_initrules(arrow,aug_grammar)
# 	print(newinitrules)

def get_aug_grammar_number(set_mapping_table,aug_grammar):
	number = 100
	for i in set_mapping_table:
		if(i[1]==aug_grammar):
			number = i[0]
	return number

def gen_slr(initrules,rules):
	global setcount
	global globalsets
	sets = []
	setcount += 1
	aug_grammar = gen_aug_grammar(initrules,rules)
	#print(aug_grammar)
	sets.append(aug_grammar)
	globalsets.append(aug_grammar)
	set_mapping_table.append([setcount,aug_grammar])
	arrows = find_arrows(aug_grammar)
	for arrow in arrows:
		newinitrules = gen_new_initrules(arrow,aug_grammar)
		flag = 0
		for currentset in globalsets:
			if(newinitrules[0] in currentset):
				flag = 1
				if(newinitrules[0][-1][-1]!="."):
					dfa_mapping_table.append([get_aug_grammar_number(set_mapping_table,aug_grammar),arrow,get_aug_grammar_number(set_mapping_table,aug_grammar)])
		if(flag==0):
			nextsets = gen_slr(newinitrules,rules)
			sets = sets + nextsets[0]
			dfa_mapping_table.append([get_aug_grammar_number(set_mapping_table,aug_grammar),arrow,get_aug_grammar_number(set_mapping_table,nextsets[0][0])])
	return [sets,setcount]

sets = gen_slr([["S'",".S"]],rules)[0]
print("Sets mapping table (Mapping of numbers to set): ")
for i in set_mapping_table:
	print(i)
print("DFA mapping table: ")
print("Here left element represents initial set number, middle represents arrow and right represents goto set number")
for i in dfa_mapping_table:
	print(i)