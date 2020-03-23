from flask import Flask,request,Response
import ldap
import ldap.modlist as modlist


con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"

app = Flask(__name__)

#sample request
#curl -i -X POST http://10.21.74.44:5000/update --data '{"fullname":"test1.testSN1","lastname":"testSN1","description":"developer","mobile":"1234567890"}' -H 'Content-Type: application/json'



@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
     try:
        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
        entry ={"sn":data['lastname'],"description":data['description'],"telephoneNumber":data['mobile']}
        parsed_entry=[(ldap.MOD_REPLACE,i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
        con.modify_s(dn,parsed_entry)
        rValue = "Updated user : " + data['fullname']
        return Response(
          mimetype="application/json",
          response=rValue,
          status=200
        )


     except ldap.LDAPError as e:

        mssg = list(e.args)[0]['desc']
        rValue ="Error while updating user: " + mssg
        return Response(
          mimetype="application/json",
          response=rValue,
          status=400
        )




app.run(host='10.21.74.44',debug=True)

