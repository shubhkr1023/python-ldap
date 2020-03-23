from flask import Flask,request
import ldap
con =ldap.initialize('ldap://10.21.74.44:3060')
ldap_base = "dc=in,dc=ril,dc=com"
app = Flask(__name__)
#sample curl
#curl -i -X POST http://10.21.74.44:5000/create --data '{"cn":"test8","sn":"testSN8","objectClass":"person"}' -H {'Content-Type: application/json','username':'cn=orcladmin','pass':'Oracle#123'}
@app.route('/test', methods=['POST','GET'])
def test():
   data = request.get_json()
   print(data)


app.run(host='10.21.74.44',debug=True)
