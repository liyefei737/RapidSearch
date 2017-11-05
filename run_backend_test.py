from crawler import *
from pprint import *

c = crawler(None, 'urls.txt')
pp = PrettyPrinter()
page_rank_scores = [ kv[1] for kv in c.compute_page_rank(c._links).items()]
page_rank_scores.sort(reverse=True)
pp.pprint(page_rank_scores)