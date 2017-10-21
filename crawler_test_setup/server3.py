from bottle import route, run
from bottle import static_file

@route('/')
def home():
    return static_file('p3.html', root='./static')

run(host='localhost', port=8090, debug=True)

