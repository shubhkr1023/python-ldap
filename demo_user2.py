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
        

        #verifying mandatory input from user
 
        mandatory=["fullname","lastname","description","mobile","mCode","mail","password"]
        temp = [x for x in mandatory if x in user_input]
        missing_attr=set(mandatory) - set(temp)
        if(len(missing_attr)==0):
                #adding user data to LDAP DIT
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
                rValue="Missing mandatory user attributes" + str(missing_attr)+ "\n"
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

app.run(host='10.21.74.44',debug=True)
