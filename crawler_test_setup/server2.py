from bottle import route, run
from bottle import static_file

@route('/')
def home():
    return static_file('coffee.html', root='./static')

run(host='localhost', port=8089, debug=True)

