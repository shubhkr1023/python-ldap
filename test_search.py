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
       
        filter = "(&(objectClass=person)(cn="+data['Name']+"))"            #to list all persons in DIT entry 
        #filter = None #to list everything in DIT
        #filter = "(&(objectClass=person)(cn=test1 testSN1))"  
        attr =['cn']
        #attr = None
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        print(type(results))
        print(results)
        #print( type(results[0][1]['cn'][0]) )
        #print( (results[0][1]['cn'][0]).decode('utf-8') )
        #json_result = json.dumps(results)
        #resp = Response(          mimetype="application/json",          response=json_result,          status=200        )
        #print(type(json_result))
        #print(json_result)
        #print(json_result[1])
        #print(type(resp))
        #print(resp)
        return str(results)


app.run(host='10.21.74.44', debug=True)



# response=json.dumps(results),
          
