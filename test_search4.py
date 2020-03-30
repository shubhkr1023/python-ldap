from flask import Flask,request,Response,json
from flask_httpauth import HTTPBasicAuth
import ldap

con =ldap.initialize('ldap://10.21.74.44:3060')
#con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)




#curl -i -X GET http://10.21.74.44:5000/search?fullname=test8.testSN8 -H 'Content-Type: application/json'

@app.route('/search', methods=['GET'])

def search2():
    if request.method =='GET':
        fullname=request.args.get('fullname')
        print(fullname)
        #con.simple_bind_s("cn=orcladmin", "Oracle#123")
        con.simple_bind_s(request.authorization["username"],request.authorization["password"])
        filter = "(&(objectClass=*)(cn="+fullname+"))"            
        #filter ="(&(objectClass=person)(cn=?))"
        #attr =['cn']
        #attr = None
        attr =['cn','sn','givenName','mail','mobile','uid']

        #result is of the form
        #  
        #[('dn',
        #{
	#'cn': [bytes encoded fullname in list],
	#'sn': [bytes encoded lastname],
	#'givenname': [bytes encoded firstname]
	#'description': [byte encode description]
	#'mobile': [byte encoded mobile]
	#'mail': [byte encoded mail]
	#'uid': [byte encode uid]
	#'objectclass':[byte encode list]
	#'userpassword': hashed
	#'some other oid passwords':hashed
	#}
        #)]

        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        print(results)
        rDict = results[0][1]
        print(rDict)
        rDictDecoded = {i:j[0].decode('utf-8') for i,j in rDict.items()}
        rDictDecoded.update({'dn':results[0][0]})
        print(rDictDecoded)

       #name_matched=results[0][1]['cn'][0].decode('utf-8') 
       #businessUnit
        if len(results) != 0:
           rValue=json.dumps(rDictDecoded)
        elif len(results) == 0:
           rValue="User Not Found!"
        resp = Response(
          mimetype="application/json",
          response=rValue,
          status=200
        )
        return resp


app.run(host='10.21.74.44', debug=True)



# response=json.dumps(results),
          
