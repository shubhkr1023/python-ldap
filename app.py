import ldap, json, simplejson, jsonify
import ldap.modlist as modlist
import flask 
from flask import Flask, jsonify
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")

ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)


#search user


results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,"cn=test5")
#print(type(results))
#print(results)
#json_parse = simplejson.dumps(results)
#print(type(json_parse))
#print(json_parse)
#print(type(jsonify(json_parse)))


#add new user

dn="cn=test6,cn=users,dc=in,dc=ril,dc=com" 
entry=[('cn',[b'test6']),('sn', [b'testSN6']),('objectClass', [b'person'])]
#attrs = {}
#attrs['objectclass']='person'
#attrs['cn'] = 'test2'
#ldif = modlist.addModlist(attrs)
#con.add_s(dn,entry)
#print("new added")




#delete user

delDN="cn=test5,cn=users, dc=in,dc=ril,dc=com"
#con.delete_s(delDN)
#print("deleted!!")



#modify users

#mod_attrs = [( ldap.MOD_ADD, 'cn','updated6' )]
#mod_attrs = [( ldap.MOD_REPLACE, 'sn','updated6' )]
#con.modify_s('cn=tesi6,ou=users,dc=in,dc=ril,dc=com', mod_attrs)

dn="cn=test6modified,cn=users,dc=in,dc=ril,dc=com"
attrs = {}
attrs['objectclass'] = b'person'
attrs['cn'] = b'test6modified'
attrs['sn'] = b'testSN6modified'
ldif = modlist.addModlist(attrs)
con.add_s(dn,ldif)
print("modified")
