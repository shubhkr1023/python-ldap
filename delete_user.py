from flask import Flask,request
import ldap
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")

ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)

@app.route('/delete', methods=['DELETE'])
def delete():
    if request.method == 'DELETE':

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['cn']+","+"cn=users,"+ldap_base
        con.delete_s(dn)
        return "Deleted user with cn:" + data['cn']+ "\n"

app.run(host='10.21.74.44',debug=True)



#sample curl
#curl -i -X DELETE http://10.21.74.44:5000/delete --data '{"cn":"test8"}' -H 'Content-Type: application/json'



