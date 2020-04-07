from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/hello', methods=['GET'])
def hello():
 return 'Helloooo World!'
if __name__ == "__main__":
 app.run(host='10.21.74.44')
