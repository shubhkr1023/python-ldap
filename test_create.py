from flask import Flask,request,Response,json
import ldap,jsonify
from emailverify import everify
from phoneverify import pverify
con =ldap.initialize('ldap://10.21.74.44:3060')
#con.simple_bind_s("cn=orcladmin", "Oracle#123")
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)
bVerticals=['irm','retail','grca']


#create user
#sample request
#curl -i -X POST http://10.21.74.44:5000/create --data '{"fullname":"test1.testSN1","firstname":"test1","lastname":"testSN1","businessUnit":"irm","description":"developer","mobile":"1234567890","mCode":"91","mail":"test1.testSN1@ril.com","password":"12345","uid":"t1"}' -H 'Content-Type: application/json'

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
     try:
        
        con.simple_bind_s(request.authorization["username"],request.authorization["password"])  
        data = request.get_json()  #converting to python dictionary
        
        #exit if Business Unit doesn't exist
        buFilter = "(&(objectClass=organizationalUnit)(ou=" + data['businessUnit']+ "))"
        buAttr = None 
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,buFilter,buAttr) 
        print(results)
        if(len(results) == 0):
            return Response(
            mimetype="application/json",
            response=json.dumps("Business Unit doesn't exist ") ,
            status=400)

        user_input=[i for(i,j) in data.items()] #key of all user input

        #verifying correct email format

        if('mail' in user_input):

          #verify mail format only if it exists in body of user request 
          if(everify(data['mail'])==0 ):
            rValue="Incorrect email format!"
            return Response(
            mimetype="application/json",
            response=json.dumps(rValue),
            status=400)


        #verifying correct mobile number format

        if('mobile' in user_input):

          #verify mail format only if it exists in body of user request
          if(pverify(data['mobile'])==0 ):
            rValue="Incorrect mobile number format!"
            return Response(
            mimetype="application/json",
            response=json.dumps(rValue),
            status=400)


        #verifying mandatory inputs from user

        mandatory=["fullname","lastname","description","mobile","mCode","mail","password","businessUnit"]
        temp = [x for x in mandatory if x in user_input]
        missing_attr=set(mandatory) - set(temp)
        if(len(missing_attr)==0): #i.e all mandatory fields are present in user input request body

                #adding user data to LDAP DIT

                dn="cn=" + data['fullname'] + ",ou=" + data['businessUnit']+ ",cn=users," + ldap_base
                entry ={"cn":data['fullname'],"sn":data['lastname'],"givenName":data['firstname'],"objectClass":"inetOrgPerson","description":data['description'],"mobile":'+'+data['mCode']+data['mobile'],"mail":data['mail'],"userPassword":data['password'],"uid":data['uid']}
                parsed_entry=[(i,bytes(j,encoding='utf-8'))for i,j in entry.items()]
                con.add_s(dn,parsed_entry)
                rValue = "Created user : " + data['fullname']
                return Response(
                mimetype="application/json",
                response=json.dumps(rValue),
                status=200
                     )
        else:
                #missing mandatory fields! Exit with 400
                rValue="Missing mandatory user attributes " + str(missing_attr)
                return Response(
                mimetype="application/json",
                response=json.dumps(rValue),
                status=400)



     except ldap.LDAPError as e:

        mssg = list(e.args)[0]['desc']
        rValue ="Error while adding user: " + mssg
        return Response(
          mimetype="application/json",
          response=json.dumps(rValue),
          status=400
        )


app.run(host='10.21.74.44',debug=True)

