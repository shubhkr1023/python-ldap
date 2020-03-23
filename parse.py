a={"cn":"test8","sn":"testSN8","objectClass":"person"}
b=[('cn',[b'test8']),('sn', [b'testSN8']),('objectClass', [b'person'])]
#[('cn', 'test8'), ('sn', 'testSN8'), ('objectClass', 'person')]

c=[]
d=[(i,bytes(j,encoding='utf-8'))for i,j in a.items()]
#c.append(m,"[b"+n+"]" for(m,n) in a.items())
#c.append((m,x) for(m,n) in a.items() where x="[b"+(n)+"]")

print(a)
print(b)
print(d)
#print(list)


