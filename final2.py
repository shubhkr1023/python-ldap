from flask import Flask,request,Response,json
import ldap,jsonify
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)



#create user 
#sample request
#curl -i -X POST http://10.21.74.44:5000/create --data '{"fullname":"test9.testSN9","lastname":"testSN9","desc":"developer","mobile":"1234567890","password":"12345"}' -H 'Content-Type: application/json'



@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
     try:

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
        entry ={"cn":data['fullname'],"sn":data['lastname'],"objectClass":"person","description":data['desc'],"telephoneNumber":data['mobile'],"userPassword":data['password']}
        parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
        con.add_s(dn,parsed_entry)
        rValue = "Created user : " + data['fullname']+"\n"
        return Response(
          mimetype="application/json",
          response=rValue,
          status=200
        )

  
     except ldap.LDAPError as e:
          
        mssg = list(e.args)[0]['desc']
        rValue ="Error while adding user: " + mssg+"\n"
        return Response(
          mimetype="application/json",
          response=rValue,
          status=400
        )





#delete user
#sample curl
#curl -i -X DELETE http://10.21.74.44:5000/delete --data '{"fullname":"test9.testSN9"}' -H 'Content-Type: application/json'

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':

     try:

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
        con.delete_s(dn)
        rValue= "Deleted user : " + data['fullname']+"\n"
        return Response(
          mimetype="application/json",
          response=rValue,
          status=200
        )


     except ldap.LDAPError as e:

        mssg = list(e.args)[0]['desc']
        rValue= "Error while deleting user " + "'"+ data['fullname'] + "': " + mssg+"\n"
        return Response(
          mimetype="application/json",
          response=rValue,
          status=400
        )


#List all users in domain
@app.route('/userlist', methods=['GET'])
def userlist():
    if request.method =='GET':
        filter = "(objectClass=person)" #to list all persons in DIT entry
        attr =["cn=test999999999"]
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        return Response(
          mimetype="application/json",
          response=json.dumps(results),
          status=200
        )





#User search
#sample curl
#curl -i -X GET http://10.21.74.44:5000/search --data '{"fullname":"test1.testSN1"}' -H 'Content-Type: application/json'

@app.route('/search', methods=['GET'])
def search():
    if request.method =='GET':
        data = request.get_json()                   #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        filter = "(&(objectClass=person)(cn="+data['fullname']+"))"
        attr =['cn']
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        #name_matched=results[0][1]['cn'][0].decode('utf-8')
        if len(results) != 0:
           rValue="User Found!"+"\n"
           code=200
        elif len(results) == 0:
           rValue="User Not Found!"+"\n"
           code=404
        resp = Response(
          mimetype="application/json",
          response=rValue,
          status=code
        )
        return resp


#user modify
#sample request
#curl -i -X POST http://10.21.74.44:5000/update --data '{"fullname":"test1.testSN1","lastname":"testSN1","description":"developer","mobile":"1234567890"}' -H 'Content-Type: application/json'



@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
     try:
        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
       # entry ={"sn":data['lastname'],"description":data['description'],"telephoneNumber":data['mobile']}
        entry ={"sn":data['lastname'],"description":data['description'],"telephoneNumber":data['mobile'],"userPassword":data['password']}
        parsed_entry=[(ldap.MOD_REPLACE,i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
        con.modify_s(dn,parsed_entry)
        rValue = "Updated user : " + data['fullname']+"\n"
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


