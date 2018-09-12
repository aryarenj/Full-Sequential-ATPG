fin1 = open("ATPG_pattern.stil" , 'r')
fin2 = open ("62RandomPatterns.txt", 'r')
fin3 = open ("638_patterns.txt", 'r')
fout = open ("Fault_Sim.pattern" , 'w')

patterns = []
for i in fin2:
  patterns.append(i.strip("\n").strip("\r"))

patterns_SI = []
for i in fin3:
  patterns_SI.append(i.strip("\n").strip("\r"))

flag = 0
count = 0


for i in fin1:
  if "Pattern \"_pattern_\" {" in i:
      flag = 1
  if flag == 1 :
    if "\"SI\"=" not in i || "\"_pi\"=0100" not in i :
       fout.write(i)
    else:   
       if "\"SI\"="  in i :
          fout.write("\t"+"\"SI\"="+patterns_SI[count]+"; }\n")
       elif "\"_pi\"=01000" in i :
          fout.write("\t"+"\"_pi\"=01000"+patterns[count]+";\n")
       count += 1
       if count == 187 :
          break


fout.close()
fin1.close()
fin2.close()
fin3.close()
