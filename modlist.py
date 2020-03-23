import ldap
from ldap import modlist

con=ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
old ={"cn":"test1.testsn1","sn":"testSN1","objectClass":"person","description":"developer","telephoneNumber":"123456796","userPassword":"12345"}
new={"cn":"test1.testsn1","sn":"testSN1","objectClass":"person","description":"developer","telephoneNumber":"123456796","userPassword":"98765"}

dn="cn="+"test11.testsn11" + "," +"cn=users,"+"dc=in,dc=ril,dc=com"
entry ={"cn":"test11.testsn11","sn":"testSN11","objectClass":"person","description":"developer","telephoneNumber":"123456796","userPassword":"12345"}

r=ldap.modlist.modifyModlist(old,new)
a=ldap.modlist.addModlist(entry)
print(r)
print(a)
con.add_s(dn,a)
