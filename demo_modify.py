import ldap
from ldap import modlist
con=ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")

dn="cn="+"test1.testsn1" + "," +"cn=users,"+"dc=in,dc=ril,dc=com"
#mod_attr=[ ( ldap.MOD_REPLACE, 'userPassword"', b'12345678' )]
#mod_attr=[ ( ldap.MOD_REPLACE, 'description' ,b'random')]
#mod_attr=[ ( ldap.MOD_REPLACE, 'telephoneNumber' ,b'9876543210')]
#mod_attr=[ ( ldap.MOD_REPLACE, 'sn', b'testSN1modified' )]
#mod_attr=[(ldap.MOD_ADD,'givenName',b'test1')]
mod_attr=[( ldap.MOD_REPLACE, 'description' ,b'randomTEST'), ( ldap.MOD_REPLACE, 'telephoneNumber' ,b'9876543210TEST'),( ldap.MOD_REPLACE, 'sn', b'testSN1modifiedTEST' )]
con.modify_s(dn,mod_attr)
