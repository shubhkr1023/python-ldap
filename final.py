from flask import Flask,request,Response,json
import ldap,simplejson

con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)



#create user with JSON entry
#sample curl
#curl -i -X POST http://10.21.74.44:5000/create --data '{"cn":"test8","sn":"testSN8","objectClass":"person"}' -H 'Content-Type: application/json'
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['cn']+","+"cn=users,"+ldap_base
        parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in data.items()]
        con.add_s(dn,parsed_entry)
        return "Created user with cn:" + data['cn']+ "\n"




#delete user
##sample curl
#curl -i -X DELETE http://10.21.74.44:5000/delete --data '{"cn":"test8"}' -H 'Content-Type: application/json'

@app.route('/delete', methods=['DELETE'])
def delete():
    if request.method == 'DELETE':

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['cn']+","+"cn=users,"+ldap_base
        con.delete_s(dn)
        return "Deleted user with cn:" + data['cn']+ "\n"



#listusers
#sample curl
#curl -i -X GET http://10.21.74.44:5000/users --data '{"filter":"(objectClass=person)","attribute":"cn"}' -H 'Content-Type: application/json'



@app.route('/listusers', methods=['GET'])
def listusers():
    if request.method == 'GET':

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        filter = data['filter']
        attr = [data['attribute']]
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        return Response(
          mimetype="application/json",
          response=json.dumps(results),
          status=200
        )

app.run(host='10.21.74.44',debug=True)








