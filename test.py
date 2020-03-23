import ldap
import flask,simplejson, jsonify
from flask import Flask, Response,json
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")

ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)



#listing all entries in DIT

@app.route('/listall', methods=['GET'])
def listall():

 results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,None,None)
 json_parse = simplejson.dumps(results)
 #return json_parse
 return Response(
          mimetype="application/json",
          response=json.dumps({'Listing all entries': json_parse}),
          status=200
        )
  
  





#listing all users

@app.route('/userlist', methods=['GET'])
def userlist():
 filter="(objectClass=person)"
 attr=None
 results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
 json_parse = simplejson.dumps(results)
 return Response(
          mimetype="application/json",
          response=json.dumps({'Listing all users': json_parse}),
          status=200
        )






#list all users with object class=person and attribute=cn

@app.route('/search',methods=['GET'])
def search():
 filter="(objectClass=person)"
 attr=['cn']
 results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
 json_parse = simplejson.dumps(results)
 return Response(
          mimetype="application/json",
          response=json.dumps({'Listing all users': json_parse}),
          status=200
        )
 


#create users

@app.route('/create', methods=['POST'])
def create():
 dn="cn=test7,cn=users,dc=in,dc=ril,dc=com"
 entry=[('cn',[b'test7']),('sn', [b'testSN7']),('objectClass', [b'person'])] 
 con.add_s(dn,entry)
 return Response(
          mimetype="application/json",
          response=json.dumps({'Created User': 'test7'}),
          status=201
        )


 


#deleting user by cn

@app.route('/delete', methods=['DELETE'])
def delete():
  dn="cn=test7,cn=users,dc=in,dc=ril,dc=com"
  con.delete_s(dn)
  return Response(
          mimetype="application/json",
          response=json.dumps({'Deleted User': 'test7'}),
          status=200
        )

if __name__ == "__main__":  
 app.run(host='10.21.74.44',debug=True)

