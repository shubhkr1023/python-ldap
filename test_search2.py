from flask import Flask,request,Response,json
import ldap

con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)
@app.route('/search', methods=['GET'])
def search2():
    if request.method =='GET':
        data = request.get_json()                   #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
       
        filter = "(&(objectClass=person)(cn="+data['Name']+"))"            
        attr =['cn']
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        #name_matched=results[0][1]['cn'][0].decode('utf-8') 
        if len(results) != 0:
           value="User Found!"
        elif len(results) == 0:
           value="User Not Found!"
        resp = Response(
          mimetype="application/json",
          response=value,
          status=200
        )
        return resp


app.run(host='10.21.74.44', debug=True)



# response=json.dumps(results),
          
