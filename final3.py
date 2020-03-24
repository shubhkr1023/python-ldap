from flask import Flask,request,Response,json
import ldap,jsonify
from emailverify import everify
from phoneverify import pverify
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)

#create user
#sample request
#curl -i -X POST http://10.21.74.44:5000/create --data '{"fullname":"test9.testSN9","firstname":"test9","lastname":"testSN9","description":"developer","mobile":"1234567890","mCode":"91","mail":"test9.testSN9@ril.com","password":"12345","ou":"IRM","uid":"t9"}' -H 'Content-Type: application/json'

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
     try:

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        user_input=[i for(i,j) in data.items()] #key of all user input

        #verifying correct email format

        if('mail' in user_input):

          #verify mail format only if it exists in body of user request 
          if(everify(data['mail'])==0 ):
            rValue="Incorrect email format!"
            return Response(
            mimetype="application/json",
            response=rValue,
            status=400)




        #verifying correct mobile number format

        if('mobile' in user_input):

          #verify mail format only if it exists in body of user request
          if(pverify(data['mobile'])==0 ):
            rValue="Incorrect mobile number format!"
            return Response(
            mimetype="application/json",
            response=rValue,
            status=400)


        #verifying mandatory inputs from user

        mandatory=["fullname","lastname","description","mobile","mCode","mail","password"]
        temp = [x for x in mandatory if x in user_input]
        missing_attr=set(mandatory) - set(temp)
        if(len(missing_attr)==0): #i.e all mandatory fields are present in user input request body

                #adding user data to LDAP DIT
                dn="cn="+data['fullname']+","+"cn=users,"+ldap_base
                entry ={"cn":data['fullname'],"sn":data['lastname'],"givenName":data['firstname'],"objectClass":"inetOrgPerson","description":data['description'],"mobile":'+'+data['mCode']+data['mobile'],"mail":data['mail'],"userPassword":data['password']}
                parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
                con.add_s(dn,parsed_entry)
                rValue = "Created user : " + data['fullname']+"\n"
                return Response(
                mimetype="application/json",
                response=rValue,
                status=200
                     )
        else:
                #missing mandatory fields! Exit with 400
                rValue="Missing mandatory user attributes " + str(missing_attr)+ "\n"
                return Response(
                mimetype="application/json",
                response=rValue,
                status=400)






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
#curl -i -X POST http://10.21.74.44:5000/delete --data '{"fullname":"test9.testSN9"}' -H 'Content-Type: application/json'

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





#User search
#sample curl
#curl -i -X GET http://10.21.74.44:5000/search --data '{"fullname":"test1.testSN1"}' -H 'Content-Type: application/json'

@app.route('/search', methods=['GET'])
def search():
    if request.method =='GET':
        data = request.get_json()                   #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        filter = "(&(objectClass=inetOrgPerson)(cn="+data['fullname']+"))"
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
        user_input=[i for(i,j) in data.items()] #key of all user input

        #verifying correct email format

        if('mail' in user_input):

          if(everify(data['mail'])==0 ):
            rValue="Incorrect email format!"
            return Response(
            mimetype="application/json",
            response=rValue,
            status=400)

        #verifying correct mobile number format

        if('mobile' in user_input):

          if(pverify(data['mobile'])==0 ):
            rValue="Incorrect mobile number format!"
            return Response(
            mimetype="application/json",
            response=rValue,
            status=400)

       # entry ={"sn":data['lastname'],"description":data['description'],"telephoneNumber":data['mobile']}
        entry ={"sn":data['lastname'],"description":data['description'],"mobile":data['mobile'],"userPassword":data['password']}
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

