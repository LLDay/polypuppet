from flask import Flask, jsonify, request
from polypuppet.server.authentication import authenticate

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    person = authenticate(username, password)
    if person.valid():
        return jsonify(certname=person.certname())
    return str()


if __name__ == '__main__':
    # app.run(ssl_context=('ssl/server.crt', 'ssl/server.key'))
    app.run()
