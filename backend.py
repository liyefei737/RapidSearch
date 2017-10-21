from bottle import get, post, route, run, request
from bottle import static_file
from heapq import *
import collections

'''
The following data structures lives as long as the server
'''
# used to store all counts for each 	 word appeared in the search query
word_count_dict = {}

#min heap of size 20, used to store the top 20 searched words in the form of [(word_count, word)...]
min_heap = []


@route('/')
def search_page():
	inputString = request.query.keywords

	if inputString == "":
		return static_file('frontend.html', root='./static')
	else:
		return search_table(inputString)


@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

def search_table(inputString):
	search_result_title = "<p> Searched for \"" + inputString + "\" </p>"

	inputString = inputString.lower()
	splitInput = inputString.split();


	#The following creates a dictionary that stores the count of the occurences
	#of each word IN THE ORDER in which they appear
	occurence_dict = collections.OrderedDict()
	for word in splitInput:
		if word in occurence_dict:
			occurence_dict[word] += 1
			print occurence_dict
		else:
			occurence_dict[word] = 1
			print occurence_dict


	#construct the query word and its occurance occurence table
	occurence_table = "<table border='1' style='width: 200px' id='search_string_occurence'><caption> Words and Their Occurences in the Search String </caption> <thead><tr><th>Word</th><th>Count</th></tr></thead>"
	for word in occurence_dict:
		occurence_table += "<tr> <td align='center'>" + word + "</td> <td align='center'>" + str(occurence_dict[word]) + "</td> </tr>"
	occurence_table += "</table><br>"

	#increment the count for each word in the word_count_dict
	for word in splitInput:
		if word in word_count_dict:
			word_count_dict[word] += 1
		else:
			word_count_dict[word] = 1
		
		word_in_heap = False

		#check to see if the word is already in the heap, if it's update the count
		for i in range(0, len(min_heap)):
			if min_heap[i][1] == word:
				min_heap[i][0] = min_heap[i][0] + 1
				word_in_heap = True
				heapify(min_heap)
				break

		# when heap is full:
		#  if this word is not in the heap, we compare the count of this word with the word with lowest count
		#  from the heap. we add this word into the heap if its count is larger than the word with minimum count
		#  from the heap.
		# when heap has less than 20 elements: 
	    	#  we add the word and its count into the heap and heapify
		if not word_in_heap:
			if len(min_heap) < 20:
				heappush(min_heap, [word_count_dict[word], word])
				heapify(min_heap)
			elif word_count_dict[word] > min_heap[0][0]: # note [0] element is the min of the min heap!
				heappop(min_heap)
				heappush(min_heap, [word_count_dict[word], word])		
				heapify(min_heap)
	
	#create a sorted copy of the heap for output
	copy_heap = sorted(min_heap)

	#construct html to return
	top_twenty = "<table border='1' style='width: 200px'id='top_twenty'><caption> History Top 20 Search Words </caption> <thead><tr><th>Word</th><th>Count</th></tr><thead>"
	for count, w in reversed(copy_heap):
		top_twenty += "<tr> <td align='center'>" + w + "</td> <td align='center' >" + str(count) + "</td> </tr>"
	top_twenty += "</table>"

			
	return search_result_title + occurence_table + top_twenty

run(host='localhost', port=8080, debug=True)
