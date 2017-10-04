from bottle import get, post, route, run, request
from bottle import static_file
from heapq import *
import collections
#global data structures

word_count_dict = {}

min_heap = []


#[(5, "apple"), ]
@route('/')
def search_page():
 return static_file('frontend.html', root='./static')

@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

@post('/')
def search_table():
	inputString = request.forms.get("searchBox")

	search_result_title = "<p> Search for \"" + inputString + "\" </p>"

	inputString = inputString.lower()
	splitInput = inputString.split();



	occurence_dict = collections.OrderedDict()
	for word in splitInput:
		if word in occurence_dict:
			occurence_dict[word] += 1
			print occurence_dict
		else:
			occurence_dict[word] = 1
			print occurence_dict


	#Construct the occurence table
	occurence_table = "<table id='search_string_occurence'> <tr><th>Word</th> <th><Count</th></tr>"
	for word in occurence_dict:
		occurence_table += "<tr> <td>" + word + "</td> <td>" + str(occurence_dict[word]) + "<td> </tr>"
	occurence_table += "</table>"

	#count the words in a dictionary and put it in the min heap if it's top 20
	for word in splitInput:
		if word in word_count_dict:
			word_count_dict[word] += 1
		else:
			word_count_dict[word] = 1
		
		word_in_heap = False #flag to see if the word is already in the heap

		#check to see if the word is already in the heap
		for i in range(0, len(min_heap)):
			if min_heap[i][1] == word:
				min_heap[i][0] = min_heap[i][0] + 1
				word_in_heap = True
			
		heapify(min_heap)

		#add the word and its count into the heap if its in the top 20; if heap less than 20 entries, then insert it automatically
		if not word_in_heap:
			if len(min_heap) < 20:
				heappush(min_heap, [word_count_dict[word], word])
				heapify(min_heap)
			elif min_heap[0][0] < word_count_dict[word]:
				heappop(min_heap)
				heappush(min_heap, [word_count_dict[word], word])		
				heapify(min_heap)
	
	#sort the heap from max to min
	copy_heap = sorted(list(min_heap))

	#construct html to return
	top_twenty = "<table id='top_twenty'> <tr><th>Word</th> <th><Count</th></tr>"
	for count, w in reversed(copy_heap):
		top_twenty += "<tr> <td>" + w + "</td> <td>" + str(count) + "<td> </tr>"
	top_twenty += "</table>"

			
	return search_result_title + occurence_table + top_twenty

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