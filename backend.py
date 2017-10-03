from bottle import get, post, route, run, request
from bottle import static_file
from heapq import *

#data structures

word_count_dict = {}

min_heap = []


#[(5, "apple"), ]
@get('/search')
def search_page():
 return '''	
 	<body>
		<div class="logo">
			<img src="original_images-Google_Logo.png">
		</div>
		<div class="searchFunction">
			<form action="/search" method="POST">
				<input type="text" name="searchBox"/><br>
				<input type="submit" value="Google Search"/><br>
			</form>
		</div>
	</body>
	'''

@post('/search')
def search_table():
	inputString = request.forms.get('searchBox')
	splitInput = inputString.split();
	for word in splitInput:
		if word in word_count_dict:
			word_count_dict[word] += 1
		else:
			word_count_dict[word] = 1
		
		word_in_heap = False
		for i in range(0, len(min_heap)):
			if min_heap[i][1] == word:
				min_heap[i][0] = min_heap[i][0] + 1
				word_in_heap = True
			
		heapify(min_heap)
		if not word_in_heap:
			if len(min_heap) < 20:
				heappush(min_heap, [word_count_dict[word], word])
				heapify(min_heap)
			elif min_heap[0][0] < word_count_dict[word]:
				heappop(min_heap)
				heappush(min_heap, [word_count_dict[word], word])		
				heapify(min_heap)
	copy_heap = list(min_heap)
	sorted(copy_heap)
	print min_heap
	top_twenty = "<table id='top_twenty'>"
	for count, w in reversed(copy_heap):
		top_twenty += "<tr> <td>" + w + "</td> <td>" + str(count) + "<td> </tr>"
	top_twenty += "</table>"
			
	return top_twenty

@get('/login') # or @route('/login')
def login():
	return '''
		<form action="/login" method="post">
			Username: <input name="username" type="text" />
			Password: <input name="password" type="password" />
			<input value="Login" type="submit" />
		</form>
		
		'''

@post('/login') # or @route('/login', method='POST')
def do_login():
	username = request.forms.get('username')
	password = request.forms.get('password')
	return "<p>" + username + "</p>"

run(host='localhost', port=8080, debug=True)