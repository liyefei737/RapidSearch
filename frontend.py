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
	print 'hello1'

	inputString = request.query.keywords
	if inputString == "":
		return static_file('frontend.html', root='./static')
	else:
		return search_table(inputString)


@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

def search_table(inputString):
	search_result_title = "<p> Search for \"" + inputString + "\" </p>"

	inputString = inputString.lower()
	splitInput = inputString.split();


	#The following creates a dictionary that stores the count of the occurences
	#of each word IN THE ORDER in which they appear
	occurence_dict = collections.OrderedDict()
	for word in splitInput:
		if word in occurence_dict:
			occurence_dict[word] += 1
		else:
			occurence_dict[word] = 1


	#Construct the occurence table
	occurence_table = "<table border='1' style='width: 200px' id='search_string_occurence'><caption> Words and Their Occurences in the Search String </caption> <thead><tr><th>Word</th><th>Count</th></tr></thead>"
	for word in occurence_dict:
		occurence_table += "<tr> <td align='center'>" + word + "</td> <td align='center'>" + str(occurence_dict[word]) + "</td> </tr>"
	occurence_table += "</table><br>"

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
	top_twenty = "<table border='1' style='width: 200px'id='top_twenty'><caption> History Top 20 Search Words </caption> <thead><tr><th>Word</th><th>Count</th></tr><thead>"
	for count, w in reversed(copy_heap):
		top_twenty += "<tr> <td align='center'>" + w + "</td> <td align='center' >" + str(count) + "</td> </tr>"
	top_twenty += "</table>"

			
	return search_result_title + occurence_table + top_twenty

run(host='localhost', port=8081, debug=True)