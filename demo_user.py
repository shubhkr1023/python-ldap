from flask import Flask,request,Response,json
import ldap,jsonify
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)



@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':

     try:
        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
        entry ={"cn":data['fullname'],'givenName':data['firstname'],"sn":data['lastname'],"objectClass":"inetOrgPerson","description":data['desc'],"telephoneNumber":data['mobile'],"userPassword":data['password']}
        parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
        con.add_s(dn,parsed_entry)
        #return Response( mimetype="application/json", response=json.dumps(results), status=200  )
        return "Created user : " + data['fullname']+ "\n"

     except ldap.LDAPError as e:
        print(e)
        print(type(e))
        print(str(e))
        print(type(str(e)))
        #print(e[0]['desc'])
        print(e.args)
        print(type(e.args))
        print(list(e.args))
        print(list(e.args)[0]['desc'])
        mssg = list(e.args)[0]['desc']
        return "Error while adding user: " + mssg
       # return ('LDAP Error: {0}'.format(e.message['desc'] if 'desc' in e.message else str(e))
       


app.run(host='10.21.74.44',debug=True)


#create user with JSON entry
#sample curl
#curl -i -X POST http://10.21.74.44:5000/create --data '{"cn":"test8","sn":"testSN8","objectClass":"person"}' -H 'Content-Type: application/json'
#curl -i -X POST http://10.21.74.44:5000/create --data '{"fullname":"test9 testSN9","lastname":"testSN9","mail":"test9@abc.com","password":"123","mobile":"123"}' -H 'Content-Type: application/json'

