from flask import Flask,request,Response,json
import ldap

con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)
@app.route('/search', methods=['GET'])
def search2():
    if request.method =='GET':
        fullname =request.args.get('fullname',"")

        filter = "(&(objectClass=person)(cn="+fullname+"))"            #to list all persons in DIT entry 
        attr =['cn','sn','givenName','mail','mobile','uid']

        #attr = None
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        #exit with 400 if user doesn't exists
        if len(results) == 0:
          return Response(
          mimetype="application/json",
          response=json.dumps("User doesn't exists") ,
          status=404
        )

        rDict = results[0][1]
        rDictDecoded = {i:j[0].decode('utf-8') for i,j in rDict.items()}
        rDictDecoded.update({'dn':results[0][0]})
        responseDict = rDictDecoded
        responseDict['fullname']= rDictDecoded.pop('cn')
        responseDict['firstname']= rDictDecoded.pop('givenname')
        responseDict['lastname']= rDictDecoded.pop('sn')


       #name_matched=results[0][1]['cn'][0].decode('utf-8')
        if len(results) != 0:
           rValue=responseDict
           code=200
        elif len(results) == 0:
           rValue="User Not Found!"
           code=404
        resp = Response(
          mimetype="application/json",
          response=json.dumps(rValue),
          status=code
        )
        return resp


app.run(host='10.21.74.44', debug=True)



# response=json.dumps(results),
          
