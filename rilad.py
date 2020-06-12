from flask import Flask,request,Response,json
import ldap,jsonify
con =ldap.initialize('ldap://adldap.in.ril.com:389')
ldap_base = "dc=in,dc=ril,dc=com"
#con.simple_bind_s(request.authorization["username"],request.authorization["password"])
#con.simple_bind_s("CN=Shubham3.Kumar,OU=FTE,OU=USERS,OU=CORPORATE,OU=RELIANCE HYDROCARBON,DC=in,DC=ril,DC=com","Shubh102bkb3")
con.set_option(ldap.OPT_REFERRALS, 0)
con.simple_bind_s("CN=Anjaneyulu.Dollaa,OU=CONSULTANT,OU=USERS,OU=CORPORATE,OU=RELIANCE HYDROCARBON,DC=in,DC=ril,DC=com","ril@1234")
user=input("name")
filter="(&(objectClass=person)(sAMAccountName="+ user+"))"
#attr=["sAMAccountName","mail"]
attr=["username","mail"]
results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
print(results)
