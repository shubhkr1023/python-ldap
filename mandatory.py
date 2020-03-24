input={"fullname":"test9.testSN9","firstname":"test9","lastname":"testSN9","description":"developer","mobile":"1234567890","mCode":"91","ou":"IRM","uid":"t9"}
mand=["fullname","lastname","description","mobile","mCode","mail","password"]
input_chk=[i for(i,j) in input.items()]
print("mand",mand)
print("input",input_chk)
temp = [x for x in mand if x in input_chk]
print(temp)
missing_attr=set(mand) - set(temp)
print(missing_attr)

