from flask import Flask,request,Response,json
import ldap,jsonify
con =ldap.initialize('ldap://10.131.40.84:389')
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)
#sample curl
#curl -i -X GET http://10.21.74.44:5500/search?username=shubham3.kumar -H 'Content-Type: application/json'

@app.route('/rilsearch', methods=['GET'])
def create():
    if request.method == 'GET':
     try:
      con.set_option(ldap.OPT_REFERRALS, 0)
     # con.simple_bind_s("CN=Anjaneyulu.Dollaa,OU=CONSULTANT,OU=USERS,OU=CORPORATE,OU=RELIANCE HYDROCARBON,DC=in,DC=ril,DC=com","ril@1234")
      con.simple_bind_s("CN=Shubham3.Kumar,OU=TRAINING,OU=USERS,OU=RCP,OU=MH_MUM,DC=in,DC=ril,DC=com","Shubh1023")

      username =request.args.get('username',"")
      filter="(&(objectClass=person)(sAMAccountName=rohan.jain))"
      attr=None
      results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
      rDict = results[0][1]
      #rDictDecoded = {i:j[0].decode('utf-8') for i,j in rDict.items()}
      if len(results) != 0:
           rValue=rDict
           code=200
      elif len(results) == 0:
           rValue="User Not Found!"
           code=404
      resp = Response(
          mimetype="application/json",
          response=json.dumps(rValue),
          status=code
        )
      return resp

     except ldap.LDAPError as e:
        mssg = list(e.args)[0]['desc']
        rValue ="Error while searching for user: " + mssg
        return Response(
          mimetype="application/json",
          response=json.dumps(rValue),
          status=400
        )

app.run(host='10.21.74.44', port=5500,debug=True)
