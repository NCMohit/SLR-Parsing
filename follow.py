def print_rules(rules):
	for i in rules:
		print(i[0]," -> ",end=" ")
		for j in range(1,len(i)-1):
			print(i[j],"|",end=" ")
		print(i[len(i)-1])

def eleminate_left_recursion(rules):
	newrules = []
	for i in range(len(rules)):
		lhslength = len(rules[i][0])
		alphas = []
		betas = []
		for j in range(1,len(rules[i])):
			if(rules[i][j][0:len(rules[i][0])]==rules[i][0]):
				alpha = rules[i][j][len(rules[i][0]):]
				alphas.append(alpha)
			else:
				betas.append(rules[i][j])
		if(len(alphas)==0):
			newrules.append(rules[i])
		else:
			lhsdash = rules[i][0]+"'"
			rule1 = [rules[i][0]]
			rule2 = [lhsdash,"@"]
			for i in betas:
				rule1.append(i+lhsdash)
			for i in alphas:
				rule2.append(i+lhsdash)
			newrules.append(rule1)
			newrules.append(rule2)
	return newrules

def find_var_list(rules):
	varlist = []
	for i in rules:
		if(i[0] not in varlist):
			varlist.append(i[0])
	return varlist

def finding_first(rules,init):
	varlist = find_var_list(rules)
	if(init not in varlist):
		return [init]
	results = []
	for i in rules:
		if(i[0]==init):
			for j in range(1,len(i)):
				if(i[j][0] not in varlist):
					results.append(i[j][0])
				else:
					for k in range(len(i[j])):
						if("@" in finding_first(rules,i[j][k])):
							for m in finding_first(rules,i[j][k]):
								if(m != "@"):
									results.append(m)
						else:
							for m in finding_first(rules,i[j][k]):
								results.append(m)
							break							
	return results

def temp_goes_to(rules,init):
	for i in rules:
		if(i[0]==init):
			return i[1:]

def finding_follow(rules,init):
	varlist = find_var_list(rules)
	rightcomponent = ""
	components = []
	follow = []
	if(init==rules[0][0]):
		follow.append("$")
	else:
		for i in rules:
			for j in i[1:]:
				if(init in j):
					if(j[(j.index(init)+1):]!=""):
						rightpart = j[(j.index(init)+1):]
						for k in rightpart:
							if(k not in varlist):
								if(k not in follow):
									follow.append(k)
								break
							else:
								for m in finding_first(eleminate_left_recursion(rules),k):
									if((m not in follow) & (m!="@")):
										follow.append(m)
								if("@" in finding_first(eleminate_left_recursion(rules),k)):
									if(rightpart.index(k)==len(rightpart)-1):
										if(i[0]!=init):
											for k in finding_follow(rules,i[0]):
												if(k not in follow):
													follow.append(k)
									continue
								else:
									break

					else:
						if(i[0]!=init):
							for k in finding_follow(rules,i[0]):
								if(k not in follow):
									follow.append(k)
	return follow
