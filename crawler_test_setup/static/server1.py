from bottle import route, run
from bottle import static_file

@route('/')
def home():
    return static_file('home.html', root='./static')

run(host='localhost', port=8088, debug=True)

