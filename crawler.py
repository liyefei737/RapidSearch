import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
import re
import numpy as np
import pprint
from pymongo import *

def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""

WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')

class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.

    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    def __init__(self, db_conn, url_file):
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing."""
        
        # list of urls
        self._url_queue = [ ]   
        
        # doc to docID map
        self._url_to_doc_id = { } 
        
        # word to wordID map
        self.lexicon = { }

        # map a doc_id to a url 
        self._doc_id_to_url = {}
        
        # map a word id to a word
        self._word_id_to_word = {}

        #set of tuples (doc_id_from, doc_id_dst)
        self._links = set()

        """
            DOCUMENT INDEX
            contains information about each document and sorted by document ID.
            each document is stored as a dict in the following form:
            {
                "id": 89,
                "url": "www.foo.com",
                "title": "kkkkk",
            }
        """
        self._doc_index = []

        """
            INVERTED INDEX that stores mappings of word_id to set of documents it appears in
            e.g.
                {
                    word_id1: set([docId1, docID3]) 
                }
        """
        self._inverted_index = {}

        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(7)(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-7)

        # never go in and parse these tags
        self._ignored_tags = set([
            'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame', 
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset', 
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        # TODO remove me in real version
        self._mock_next_doc_id = 1
        self._mock_next_word_id = 1

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 0
        self._curr_words = None

        # get all urls into the queue
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    self._url_queue.append((self._fix_url(line.strip(), ""), 0))
        except IOError:
            pass
        
        # make the crawler automatically craw when we create an instance
        self.crawl(depth=1)
        self.save_to_db()
    
    # TODO remove me in real version
    def _mock_insert_document(self, url):
        """A function that pretends to insert a url into a document db table
        and then returns that newly inserted document's id."""
        ret_id = self._mock_next_doc_id
        self._mock_next_doc_id += 1
        return ret_id
    
    # TODO remove me in real version
    def _mock_insert_word(self, word):
        """A function that pretends to inster a word into the lexicon db table
        and then returns that newly inserted word's id."""
        ret_id = self._mock_next_word_id
        self._mock_next_word_id += 1
        return ret_id
    
    def word_id(self, word):
        """Get the word id of some specific word."""
        if word in self.lexicon:
            return self.lexicon[word]
        
        # TODO: 1) add the word to the lexicon, if that fails, then the
        #          word is in the lexicon
        #       2) query the lexicon for the id assigned to this word, 
        #          store it in the word id cache, and return the id.

        word_id = self._mock_insert_word(word)
        self.lexicon[word] = word_id
        return word_id
    
    def document_id(self, url):
        """Get the document id for some url."""
        if url in self._url_to_doc_id:
            return self._url_to_doc_id[url]
        
        # TODO: just like word id cache, but for documents. if the document
        #       doesn't exist in the db then only insert the url and leave
        #       the rest to their defaults.
        
        doc_id = self._mock_insert_document(url)
        self._url_to_doc_id[url] = doc_id
        self._doc_id_to_url[doc_id] = url
        return doc_id
    
    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""
            
        # compute the new url based on import 
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        return urlparse.urljoin(parsed_url.geturl(), rel)

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database, or increase the number of links between
        two pages in the database."""
        # TODO

    def _visit_title(self, elem):
        """Called when visiting the <title> tag."""
        title_text = self._text_of(elem).strip()
        #print "document title="+ repr(title_text)

        # TODO update document title for document id self._curr_doc_id
    
    def _visit_a(self, elem):
        """Called when visiting <a> tags."""

        dest_url = self._fix_url(self._curr_url, attr(elem,"href"))

        #print "href="+repr(dest_url), \
        #      "title="+repr(attr(elem,"title")), \
        #      "alt="+repr(attr(elem,"alt")), \
        #      "text="+repr(self._text_of(elem))

        # add the just found URL to the url queue
        self._url_queue.append((dest_url, self._curr_depth))
        
        # add a link entry into the database from the current document to the
        # other document
        self._links.add((self._curr_doc_id, self.document_id(dest_url)))
        self.add_link(self._curr_doc_id, self.document_id(dest_url))

        # TODO add title/alt/text to index for destination url
    
    def _add_words_to_document(self):
        # TODO: knowing self._curr_doc_id and the list of all words and their
        #       font sizes (in self._curr_words), add all the words into the
        #       database for this document
        #print "    num words="+ str(len(self._curr_words))
        pass

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""
        def increase_it(elem):
            self._font_size += factor
        return increase_it
    
    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""
        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            
            # create a word_id for word
            word_id = self.word_id(word)
            
            self._word_id_to_word[word_id] = word
            self._curr_words.append((word_id, self._font_size))
            
            # add word_id to inverted index and add the doc_id to the set
            if word_id not in self._inverted_index:
                self._inverted_index[word_id] = set()
            self._inverted_index[word_id].add(self._doc_index[-1]["id"])
                 
        
    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = [ ]
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))
            
            return " ".join(text)
        else:
            return elem.string

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when entering
        and leaving tags. When we come accross some text, add it into the index. This
        handles ignoring tags that we have no business looking at."""
        class DummyTag(object):
            next = False
            name = ''
        
        class NextTag(object):
            def __init__(self, obj):
                self.next = obj
        
        tag = soup.html
        stack = [DummyTag(), soup.html]

        while tag and tag.next:
            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)
                    
                    continue
                
                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

            # text (text, cdata, comments, etc.)

            else:
                self._add_text(tag)

    def crawl(self, depth=1, timeout=3):
        """Crawl the web!"""
        seen = set()

        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            #get or create a doc_id for the next url in the queue
            doc_id = self.document_id(url)

            # we've already seen this document, so we skip to the next url
            if doc_id in seen:
                continue

            # mark this document as haven't been visited        
            seen.add(doc_id)
   
            #if this document has not been visited, add it to the document index with its doc_id and url
            self._doc_index.append({
                "id": doc_id,
                "url": url
            })
            
            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())
                
                # get the tile of the page and store it as title in document index
                self._doc_index[-1]["title"] =  soup.title.string
                
                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 0
                self._curr_words = [ ]
                self._index_document(soup)
                self._add_words_to_document()
                #print "    url="+repr(self._curr_url)
                #here

            except Exception as e:
                print e
                pass
            finally:
                if socket:
                    socket.close()
    
    def get_inverted_index(self):
        return self._inverted_index

    def get_resolved_inverted_index(self):
        resolved_inverted_index = dict()
        
        for word_id in self._inverted_index:
            # get word using word_id from word_id_to_word map
            word = self._word_id_to_word[word_id]
            # create an empty set to hold the resolved urls
            resolved_inverted_index[word] = set()
            # get a list of doc_ids for this word_id
            doc_ids = self._inverted_index[word_id]
            
            for doc_id in doc_ids:
               #resolve doc_id to doc/url and add it to the resolved set 
               resolved_inverted_index[word].add(self._doc_id_to_url[doc_id])

        return resolved_inverted_index
    
    def save_to_db(self):
        # TODO clarify what lexicon is
        '''
            Things we persist to DB:
            inverted index, lexicon, document index, PageRank scores to persistent storage
        '''
        client = MongoClient("localhost", 27017)
        db = client["crawler"] #call the db crawler
        # we save all the above items in one collection and we name this collection crawler
        # we can think of this collection like a python dictionary where we have a field called 'type'
        # useful type is 1 of these values ["doc_index", "inverted_index", "pg_score", "lexicon"]
        collection = db["crawler"]

        if collection.find_one({"type":"doc_index"}) is None:
            collection.insert_one({"type":"doc_index", "value": self._doc_index})
        else:
            collection.replace_one({"type":"doc_index"}, {"type":"doc_index", "value": self._doc_index})
        
        if collection.find_one({"type":"lexicon"}) is None:
                collection.insert_one({"type":"lexicon", "value": self.lexicon})
        else:
            collection.replace_one({"type":"lexicon"}, {"type":"lexicon", "value": self.lexicon})
        
        bson_formated_inverted_index = self.bson_format_inverted_index(self._inverted_index)
        
        if collection.find_one({"type":"inverted_index"}) is None:
            collection.insert_one({"type":"inverted_index", "value": bson_formated_inverted_index})
        else:
            collection.replace_one({"type":"inverted_index"}, {"type":"doc_index", "value": bson_formated_inverted_index})
        
        bson_formatted_pg_score = self.bson_key_to_str(self.compute_page_rank(self._links))
        
        if collection.find_one({"type":"pg_score"}) is None:
            collection.insert_one({"type":"pg_score", "value": bson_formatted_pg_score})
        else:
            collection.replace_one({"type":"pg_score"}, {"type":"doc_index", "value": bson_formatted_pg_score})
        
        bson_formatted_doc_id_to_url = self.bson_key_to_str(self._doc_id_to_url)

        if collection.find_one({"type":"doc_id_to_url"}) is None:
                collection.insert_one({"type":"doc_id_to_url", "value": bson_formatted_doc_id_to_url})
        else:
            collection.replace_one({"type":"doc_id_to_url"}, {"type":"doc_id_to_url", "value": bson_formatted_doc_id_to_url})
        
    def compute_page_rank(self,links, num_iterations=20, initial_pr=1.0):
        page_rank = defaultdict(lambda: float(initial_pr))
        num_outgoing_links = defaultdict(float)
        incoming_link_sets = defaultdict(set)
        incoming_links = defaultdict(lambda: np.array([]))
        damping_factor = 0.85

        # collect the number of outbound links and the set of all incoming documents
        # for every document
        for (from_id,to_id) in links:
            num_outgoing_links[int(from_id)] += 1.0
            incoming_link_sets[to_id].add(int(from_id))
    
        # convert each set of incoming links into a numpy array
        for doc_id in incoming_link_sets:
            incoming_links[doc_id] = np.array([from_doc_id for from_doc_id in incoming_link_sets[doc_id]])

        num_documents = float(len(num_outgoing_links))
        lead = (1.0 - damping_factor) / num_documents
        partial_PR = np.vectorize(lambda doc_id: page_rank[doc_id] / num_outgoing_links[doc_id])
        for _ in xrange(num_iterations):
            for doc_id in num_outgoing_links:
                tail = 0.0
                if len(incoming_links[doc_id]):
                    tail = damping_factor * partial_PR(incoming_links[doc_id]).sum()
                page_rank[doc_id] = lead + tail
    
        return page_rank

    def bson_format_inverted_index(self, inverted_index):
        formatted = {}
        for key in inverted_index:
            formatted[str(key)] = list(inverted_index[key])
        return formatted    

    def bson_key_to_str(self, d):
        formatted = defaultdict()
        for key in d:
           formatted[str(key)] =  d[key]
        return formatted


if __name__ == "__main__":
    c = crawler(None, 'urls.txt')
    #pp = pprint.PrettyPrinter()
    #pp.pprint(c.compute_page_rank(c._links))
