fin1 = open("ATPG_pattern.stil" , 'r')
fin2 = open ("./62bit_700Patterns.txt", 'r')
fin3 = open ("./64bit_7000Patterns.txt", 'r')
fout = open ("Fault_Sim.pattern" , 'w')

patterns = []
for i in fin2:
  patterns.append(i.strip("\n").strip("\r"))

patterns_SI = []
for i in fin3:
  patterns_SI.append(i.strip("\n").strip("\r"))

flag = 0
count = 0
j = 0
s = 1

for i in fin1:
  if count == 186 :
      break
      
  if "Pattern \"_pattern_\" {" in i :
      print i
      flag = 1
  elif flag == 0:
      fout.write(i)
  if flag == 1 :
      if  "      \"SI"  in i :
	  print "hi"
	  fout.write("\t"+"\"SI"+str(s)  +"\"="+patterns_SI[j]+"; \n")
          j += 1
	  s +=1
          if s== 11:
        	fout.write("}\n")
      elif "\"_pi\"=01000" in i :
          fout.write("\t"+"\"_pi\"=01000000000000"+patterns[count]+";\n")
          count += 1
          s=1
      else:
          fout.write(i)

fout.write("}\n}")
print count
fout.close()
fin1.close()
fin2.close()
fin3.close()
