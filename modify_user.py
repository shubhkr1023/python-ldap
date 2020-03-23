from flask import Flask,request
import ldap
import ldap.modlist as modlist

con =ldap.initialize('ldap://10.21.74.44:3060')
#con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)


#create user with JSON entry
#sample curl
#curl -i -X PATCH http://10.21.74.44:5000/upadte --data '{"old":{"cn":"test8","sn":"testSN8","objectClass":"person"}, "new":{"cn":"test9","sn":"testSN8","objectClass":"person}}' -H 'Content-Type: application/json'
@app.route('/update', methods=['PATCH'])
def update():
    if request.method == 'PATCH':

        data = request.get_json()  #converting to python dictionary
        con.simple_bind_s("cn=orcladmin", "Oracle#123")
        print('Data Received: "{data}"'.format(data=data))
        old_data=data['old']
        new_data=data['new']
        dn="cn="+old_data['cn']+","+"cn=users,"+ldap_base
        #ldif = modlist.modifyModlist(old_data,new_data)
        #con.modify_s(dn,ldif)
        



        return "Updated user with cn:" + old_data['cn']+ "\n"


app.run(host='10.21.74.44', debug=True)
