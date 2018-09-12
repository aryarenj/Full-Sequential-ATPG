file1= open ("CUT.v" , 'r')
file2 = open ("Q_list.txt" ,'w')


count = 0
for i in file1:
  if "DFFX1" in i:
    k= i.split("), .Q(")
    l = k[1].split("));") 
    file2.write(l[0]+"\n")
    count += 1

print count

file1.close()
file2.close()
