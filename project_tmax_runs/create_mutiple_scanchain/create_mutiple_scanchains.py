file1 = open ("CUT.v" , 'r')
file2 = open ("Q_list.txt" , 'r')
file3 = open("CUT_interim_scan.v" , 'w')

qname = []
qname.append("SI")
for i in file2:
  k = i.strip("\n")
  qname.append(k)

index = 0
for i in file1 :
  if "DFFX1" not in i:
    file3.write(i)
  else:
    if index % 64 == 0:
      file3.write("assign SO = "+qname[index]+" ;\n")
      p = i.split("), .Q(")
      file3.write("S_"+p[0])
      file3.write("), .SE(SE), .SI(")
      file3.write("SI")
      file3.write("), .Q(")
      file3.write(p[1])
      print "added scanchanin at input of FF",index
    else:

      p = i.split("), .Q(")
      file3.write("S_"+p[0])
      file3.write("), .SE(SE), .SI(")
      file3.write(qname[index]) 
      file3.write("), .Q(")
      file3.write(p[1])

    index += 1

print index
file1.close()
file2.close()
file3.close() 
