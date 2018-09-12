import sys
import os
all_eq_classes = []

def identify_faults( level_fault , each_gate_dict , i) :
	per_level_fault = level_fault
	
	if each_gate_dict["gate_type"] == 'NAND2X1' or each_gate_dict["gate_type"] == 'AND2X1':
		del per_level_fault[each_gate_dict["input"][i]][0]
	elif each_gate_dict["gate_type"] == 'NOR2X1' or each_gate_dict["gate_type"] == 'OR2X1':
		del per_level_fault[each_gate_dict["input"][i]][1]
	elif each_gate_dict["gate_type"] == 'INVX1' or each_gate_dict["gate_type"] == 'BUFX1':
		del per_level_fault[each_gate_dict["input"]][0]
		del per_level_fault[each_gate_dict["input"]][0]
		
	return per_level_fault


	
def check (all_eq_classes , eq_classes):
	found = 0
	for i in range(len(all_eq_classes)):	
		for m in eq_classes:
			k = all_eq_classes[i]
			if m in k:
				new = list(set(eq_classes + k))
				all_eq_classes[i] = new
				found =1
				break
	if found != 1 :
		all_eq_classes.append(eq_classes)
				
				
def create_eq_faults(all_eq_classes , each_gate_dict ) :
	
	gatename = each_gate_dict["gate_type"] 
	eq_classes = []
	lookup = {}
	lookup["AND2X1"] = ["sa0 " , "sa0 ", "sa0 " , "sa1 ", "sa1 ", "sa1 "]
	lookup["OR2X1"] = ["sa1 " , "sa1 ", "sa1 " , "sa0 ", "sa0 ", "sa0 "]
	lookup["NAND2X1"] = ["sa0 " , "sa0 ", "sa1 " , "sa1 ", "sa1 ", "sa0 "]
	lookup["NOR2X1"] = ["sa1 " , "sa1 ", "sa0 " , "sa0 ", "sa0 ", "sa1 "]
	lookup["INVX1"] = ["sa0 " , "sa1 ", "sa1 " , "sa0 "]
	lookup["BUFX1"] = ["sa0 " , "sa0 ", "sa1 " , "sa1 "]
	lookup["XOR2X1"] = ["sa0 " , "sa0 ", "sa0 " , "sa1 ", "sa1 ", "sa1 "]
	lookup["fanout"] = ["sa0 " , "sa1 "]
	
	if gatename in inp_2_gates_list:
		
		if gatename != "XOR2X1" :
			eq_classes.append(lookup[gatename][0] + each_gate_dict["input"][0] )
			eq_classes.append(lookup[gatename][1] + each_gate_dict["input"][1] )
			eq_classes.append(lookup[gatename][2] + each_gate_dict["output"] )
			
			try:
				check (all_eq_classes , eq_classes)
			except:
				all_eq_classes.append(eq_classes)
			
			all_eq_classes.append([lookup[gatename][3] + each_gate_dict["input"][0] ])		
			all_eq_classes.append([lookup[gatename][4] + each_gate_dict["input"][1] ])		
			all_eq_classes.append([lookup[gatename][5] + each_gate_dict["output"] ])
		
		else:
			
			all_eq_classes.append([lookup[gatename][0] + each_gate_dict["input"][0] ])		
			all_eq_classes.append([lookup[gatename][1] + each_gate_dict["input"][1] ])		
			all_eq_classes.append([lookup[gatename][2] + each_gate_dict["output"] ])
			all_eq_classes.append([lookup[gatename][3] + each_gate_dict["input"][0] ])		
			all_eq_classes.append([lookup[gatename][4] + each_gate_dict["input"][1] ])		
			all_eq_classes.append([lookup[gatename][5] + each_gate_dict["output"] ])
		

	elif gatename in inp_1_gates_list:
		
		eq_classes.append(lookup[gatename][0] + each_gate_dict["input"] )
		eq_classes.append(lookup[gatename][1] + each_gate_dict["output"] )
		check (all_eq_classes , eq_classes)
		
		eq_classes = []
		eq_classes.append(lookup[gatename][2] + each_gate_dict["input"] )
		eq_classes.append(lookup[gatename][3] + each_gate_dict["output"] )
		check (all_eq_classes , eq_classes)
		
	elif "fanout" in gatename:
		all_eq_classes.append([lookup["fanout"][0] + each_gate_dict["input"] ])		
		all_eq_classes.append([lookup["fanout"][1] + each_gate_dict["input"] ])		
			
		
print "\nEnter input filename : ",
filename = raw_input()	
file_in = open(filename , 'r')

filename_reqd = filename.strip(".v")


fileout_BF = open ( filename_reqd+"_BF.txt" , 'w')
fileout_AF = open ( filename_reqd+"_AF.txt" , 'w')

levels = []
gates = []

inp_2_gates_list = [ 'AND2X1' , 'OR2X1' , 'NAND2X1' , 'NOR2X1' , 'XOR2X1' ]
inp_1_gates_list = [ 'INVX1' ,  'BUFX1' ]

gate_count = 0
fanout_count = 0
fanout_branches = 0
all_gates = []
flag = 0


print "\nData written into output files "+ filename_reqd +"_BF.txt and "+ filename_reqd +"_AF.txt\n"


##### File parsing begins


for j in file_in:

	if "//" in j:
		k = j.split("//")
		i =  k[0]
	elif "/*" in j:
		k = j.split("/*")
		i =  k[0]
		multi_line_com = 1
	elif "*/" in j:
		k = j.split("*/")
		i =  k[1]
		multi_line_com = 0
		flag = 0
	else :
		i = j

	if flag == 0:		
		if "input" in i:
			m1 = i.split(";")
			m = m1[0].split(" ")
			prim_input = m[1].split(",")
			prim_input_count = len(prim_input)				

		if "output" in i:			
			m1 = i.split(";")
			m = m1[0].split(" ")
			prim_output = m[1].split(",")
			
		eachline = i.strip('\n').split(" ")
		firstword =  eachline[0]
		gates = {}
		try:
			if firstword in inp_2_gates_list:
				gate_input = []
				gates["gate_type"] = firstword
				gates["gate_name"] = eachline[1]
				m1 = eachline[2].strip("));").split("),.B(")
				gate_input.append(m1[1])
				m2 = m1[0].split("),.A(")
				gate_input.append(m2[1])
				gates["input"] = gate_input
				m3 = m2[0].split(".Y(")
				gates["output"] = m3[1]
				gate_count += 1
				all_gates.append(gates)
				
			if firstword in inp_1_gates_list:
				gates["gate_type"] = firstword
				gates["gate_name"] = eachline[1]
				m1 = eachline[2].strip("));").split("),.A(")
				gates["input"] = m1[1]
				m2 = m1[0].split(".Y(")
				gates["output"] = m2[1]
				gate_count += 1
				all_gates.append(gates)
				
			elif "fanout" in firstword:
				fanout_out = []
				k = eachline[0].split("fanout")		#k[1] will give number of branches
				m1 = eachline[2].strip("));").split("Y")				
				m0 = m1[0].split("(.A(")
				m00 = m0[1].split("),.")
				for j in range(int(k[1])):
					m2 = m1[j+1].split("(")
					m3 = m2[1].split(")")
					fanout_out.append(m3[0])
			
				fanout_branches += int(k[1])
				gates["gate_type"] = firstword
				gates["gate_name"] = eachline[1]
				gates["input"] = m00[0]
				gates["output"] = fanout_out
				fanout_count += 1 
				all_gates.append(gates)
				
			if multi_line_com == 1 :
				flag = 0
		except:
			continue	
		
		
		
##### File parsing ends 
	
fault_locations_count = prim_input_count + gate_count + fanout_branches

levels.insert(0, prim_input)
removed_faults_per_level = {}

all_faults_list = []
checked_wires = prim_input
levels_faults = []
faults_after_removal = []


i = 0

while levels[i] != [] :
	level_faults_dict = {}
	if i != 0:
		for m in range(len(levels[i])):
			checked_wires.append(levels[i][m])


	for m in range(len(levels[i])):		
		level_faults_dict[levels[i][m]] = [ "sa0"  , "sa1"]
		all_faults_list.append("sa0" + " " + levels[i][m])			# Faults before collapsing
		all_faults_list.append("sa1" + " " + levels[i][m])
		
	levels_faults.append(level_faults_dict)
	
	
	removed_faults_per_level = level_faults_dict

	for j in levels[i]:
		levels.append([])
		for k in range(fanout_count + gate_count):			
			if j == all_gates[k]["input"][0]:			#to consider if a wire goes to 2 i/p gate's input
				create_eq_faults( all_eq_classes, all_gates[k] )
				removed_faults_per_level = identify_faults(level_faults_dict, all_gates[k] , 0)
				if all_gates[k]["input"][1] in checked_wires:
					levels[i+1].append(all_gates[k]["output"])
									
			elif j == all_gates[k]["input"][1]:
				create_eq_faults(all_eq_classes, all_gates[k] )
				removed_faults_per_level = identify_faults(level_faults_dict, all_gates[k] , 1)
				if all_gates[k]["input"][0] in checked_wires:
					levels[i+1].append(all_gates[k]["output"])
				
				
			if j == all_gates[k]["input"]:	
				if "fanout" in all_gates[k]["gate_type"]:		#to consider if a wire goes to fanout
					create_eq_faults(all_eq_classes, all_gates[k] )
					for p in range(len(all_gates[k]["output"]))	:			
						levels[i+1].append(all_gates[k]["output"][p])
				else :									#to consider if a wire goes to INV of BUF
					levels[i+1].append(all_gates[k]["output"])
					create_eq_faults(all_eq_classes, all_gates[k] )
					removed_faults_per_level = identify_faults(level_faults_dict, all_gates[k] , 0)
		
	myset = set(levels[i+1])
	levels[i+1] = list(myset)
	i += 1
	for j in levels[i-1]:
		try: 
			faults_after_removal.append(removed_faults_per_level[j][0] + " " + j)
			faults_after_removal.append(removed_faults_per_level[j][1] + " " + j)
		except:
			continue
			
	
	
fault_locations_count = prim_input_count + gate_count + fanout_branches
total_faults_count = fault_locations_count * 2	


new_list = []
for p in all_eq_classes:
	if p not in new_list:
		new_list.append(p)
all_eq_classes = new_list

for i in  all_eq_classes:
	j = all_eq_classes.index(i) + 1
	while j < len(all_eq_classes):
		if set(i).intersection(set(all_eq_classes[j])) != set([]):
			all_eq_classes.remove(all_eq_classes[j])
			j -= 1			
		j += 1

for i in range(len(all_faults_list)):
	fileout_BF.write( all_faults_list[i] + "\n")
fileout_BF.write( "\nTotal Faults_BF = " + str(len(all_faults_list) ))

for i in range(len(faults_after_removal)):
	fileout_AF.write( faults_after_removal[i] + "\n")
fileout_AF.write( "\nTotal Faults_AF = " + str(len(faults_after_removal) ))
fileout_AF.write( "\nCollapse_ratio = " + str(float(len(faults_after_removal))/len(all_faults_list)) )

fileout_AF.write( "\n\nEquivalent Classes : \n")
for i in all_eq_classes:
	for j in i:
		fileout_AF.write( j )
		if i.index(j) != len(i)-1:
			fileout_AF.write(  ", ")
	fileout_AF.write("\n")	

