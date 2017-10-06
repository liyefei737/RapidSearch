from bottle import route, run
from bottle import static_file

@route('/')
def home():
    return static_file('p4.html', root='./static')

run(host='localhost', port=8089, debug=True)

