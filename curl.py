from flask import Flask,request

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':

        data = request.get_json()
        print(data)
        print(type(data))
        print(type(('Data Received: "{data}"'.format(data=data))))
        print('Data Received: "{data}"'.format(data=data))
        return "Request Processed.\n"

app.run(host='10.21.74.44',debug=True)




#curl call
#curl 10.21.74.44:5000/post -d '{"foo": "bar"}' -H 'Content-Type: application/json'
