
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s</h1>' % name

@app.route('/ga')
def useragent():
    print dir(Response)
    # print dir(request.headers)
    print dir(request)
    return request.headers.get('Cookie')

if __name__ == "__main__":
    app.run(debug=True)
