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