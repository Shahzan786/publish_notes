a=[[1,2],3,4,5,6,[7,8]]
new=[]

for i in a:
    if type(i)==list:
        new=new+i
    else:
        new.append(i)

print(new)         


a=input("Enter a string")
done=""
for i in a:
    if i not in done:
        print(i,":",a.count(i))
        done=done+i    


lst=[1,1,3,5,9,9]
a=[]

for i in lst:
    if i not in a:
      a.append(i)

print(a)      
 