from flask import Flask,request,Response,json
import ldap,simplejson
con =ldap.initialize('ldap://10.21.74.44:3060')
con.simple_bind_s("cn=orcladmin", "Oracle#123")

ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)


#search users with filter and attribute





#sample curl
#curl -i -X GET http://10.21.74.44:5000/search --data '{"filter":"(&(objectclass=user)(name=test*))","attribute":"None"}' -H 'Content-Type: application/json'




#@app.route('/search',methods=['GET'])
#def search():
# filter="(&(objectclass=user)(name=test*))"
# attr=['cn']
# results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
# json_parse = simplejson.dumps(results)
# return Response(
 #         mimetype="application/json",
  #        response=json.dumps({'Listing all users': json_parse}),
  #        status=200
  #      )




@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':

        data = request.get_json()  #converting to python dictionary
        print('Data Received: "{data}"'.format(data=data))
        filter = data['filter']
        attr = [data['attribute']]
        results = con.search_s(ldap_base, ldap.SCOPE_SUBTREE,filter,attr)
        json_parse = simplejson.dumps(results)
        return Response(
          mimetype="application/json",
          response=json.dumps({'Listing all users': json_parse}),
          status=200
        )






app.run(host='10.21.74.44',debug=True)

