from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from bottle import get, post, route, run, request, redirect, app, template
from bottle import static_file, response
import bottle
from beaker.middleware import SessionMiddleware
from heapq import *
import collections
import httplib2
import Queue
#global data structures
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

user_most_recent_dict = {}
user_history_dict = {}
user_history_heap = {}

user_most_recent_dict = {}

SCOPE = ['https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/userinfo.email']

@route('/')
def search_page():
	s = request.environ.get('beaker.session')
	bottle.TEMPLATES.clear()

	inputString = request.query.keywords
	if 'email' in s: #user logged in
		logged_in = True

		if inputString == "":
			return template('frontend.tpl', loggedin=logged_in, name=s['name'])
		else:
			return search_table(inputString)
	else:
		if inputString == "":
			return template('frontend.tpl', loggedin=False)
		else:
			return search_table(inputString)


@route('/login')
def login_trigger():

	s = request.environ.get('beaker.session')
	if 'email' not in s:
		flow = flow_from_clientsecrets('./client_secret.json', scope=SCOPE, redirect_uri="http://localhost:8081/redirect")
		auth_uri = flow.step1_get_authorize_url()
		redirect(str(auth_uri))
	else:
		redirect(str('/'))

@route('/logout')
def logout_trigger():
	session = request.environ.get('beaker.session')
	session.delete()
	redirect(str("/"))

@route('/redirect')
def redirect_page():
	code = request.query.get('code','')

	flow = OAuth2WebServerFlow(client_id='619195777450-ea3m50l60rlmbo9ro0abiimmb4o9admp.apps.googleusercontent.com',
							client_secret='SBurZL_VZPCjaLLVEKGRyD5v',
							scope=SCOPE,
							redirect_uri="http://localhost:8081/redirect")

	credentials = flow.step2_exchange(code)
	token = credentials.id_token['sub']
	http = httplib2.Http()
	http = credentials.authorize(http)

	users_service = build('oauth2', 'v2', http=http)
	user_document = users_service.userinfo().get().execute()
	user_email = user_document['email']
	print user_document

	session = request.environ.get('beaker.session')
	session['email'] = user_email
	session['name'] = user_document['given_name']
	session['picture'] = user_document['picture']
	session['logged_in'] = True
	session.save()
	redirect(str('/'))

	



@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')

def search_table(inputString):
	bottle.TEMPLATES.clear()
	s = request.environ.get('beaker.session')
	request.response.set_header("Cache-Control", "no-cache, no-stoe, must-revalidate")
	request.response.set_header("Pragma", "no-cache")
	
	
	search_result_title = "<p> Search for \"" + inputString + "\" </p>"

	inputStringLower = inputString.lower()
	splitInput = inputStringLower.split();


	#The following creates a dictionary that stores the count of the occurences
	#of each word IN THE ORDER in which they appear
	occurence_dict = collections.OrderedDict()
	for word in splitInput:
		if word in occurence_dict:
			occurence_dict[word] += 1
		else:
			occurence_dict[word] = 1

		
	if 'logged_in' not in s:
		return template('results.tpl', logged_in=False,inputString=inputStringLower, splitInput=splitInput, occurence_dict=occurence_dict)
	#count the words in a dictionary and put it in the min heap if it's top 20

	name = s['name']
	email = s['email']
	if email not in user_history_dict and email not in user_history_heap and email not in user_most_recent_dict:
		user_history_dict[email] = {}
		user_history_heap[email] = []
		user_most_recent_dict[email] = []

	if len(user_most_recent_dict[email]) < 10:
		user_most_recent_dict[email].append(inputString)
	else:
		user_most_recent_dict[email].pop(0)
		user_most_recent_dict[email].append(inputString)

	user_history_dict[s['email']], user_history_heap[s['email']] = insert_into_dict_and_heap(user_history_dict[s['email']], user_history_heap[s['email']], splitInput)
	copy_heap = sorted(list(user_history_heap[s['email']]))
	reversed_copy_heap = reversed(copy_heap)

	return template('results.tpl', logged_in=True, name=name, inputString=inputStringLower, splitInput=splitInput, occurence_dict=occurence_dict, reversed_copy_heap=reversed_copy_heap, queue=user_most_recent_dict[email])

def insert_into_dict_and_heap(user_dict, min_heap, word_list):
	for word in word_list:
		if word in user_dict:
			user_dict[word] += 1
		else:
			user_dict[word] = 1

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
				heappush(min_heap, [user_dict[word], word])
				heapify(min_heap)
			elif min_heap[0][0] < user_dict[word]:
				heappop(min_heap)
				heappush(min_heap, [user_dict[word], word])		
				heapify(min_heap)
	return user_dict, min_heap

run(host='localhost', port=8081, debug=True, app=app)