

text=input()
done=""

for i in text:
  if i not in done:
   print(i,":",text.count(i))
   done=done+i
   

a=input("Enter a string : ")
rev=""
for i in a:
  rev=i+rev

if a==rev: 
  print("palindrome")
else:
  print("not palindrome")  


a=input("Enter a string : ")
b=a

if b==a[::1]:
  print("palindrome")
else:
 print("not palindrome")  