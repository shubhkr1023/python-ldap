from flask import Flask,request
import ldap

con =ldap.initialize('ldap://10.21.74.44:3060')
#con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)



#create user with JSON entry
#sample curl
#curl -i -X POST http://10.21.74.44:5000/create --data '{"cn":"test8","sn":"testSN8","objectClass":"person","bindDN":"orcladmin","bindPW":"Oracle#123"}' -H {'Content-Type: application/json'}
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':

        data = request.get_json()  #converting to python dictionary
        print(data)
       # bindDN=data['bindPW']
       # bindPW=data['bindPW']
       # con.simple_bind_s(bindDN, bindPW)
       # print('Data Received: "{data}"'.format(data=data))
       # dn="cn="+data['cn']+","+"cn=users,"+ldap_base
       # parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in data.items()]
       # con.add_s(dn,parsed_entry)
       # return "Created user with cn:" + data['cn']+ "\n"
        return(data)




#delete user
##sample curl
#curl -i -X DELETE http://10.21.74.44:5000/delete --data '{"cn":"test8","bindDN":"cn=orcladmin","bindPW":"Oracle#123"}' -H 'Content-Type: application/json'

@app.route('/delete', methods=['DELETE'])
def delete():
    if request.method == 'DELETE':

        data = request.get_json()  #converting to python dictionary
        bindDN=data['bindDN']
        bindPW=data['bindPW']
        con.simple_bind_s(bindDN, bindPW)
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['cn']+","+"cn=users,"+ldap_base
        con.delete_s(dn)
        return "Deleted user with cn:" + data['cn']+ "\n"

#search user with filter and attribute || list all users
#sample curl
#curl -i -X GET http://10.21.74.44:5000/search --data '{"filter":"(objectClass=person)","attribute":"cn"}' -H 'Content-Type: application/json'


     



app.run(host='10.21.74.44',debug=True)








