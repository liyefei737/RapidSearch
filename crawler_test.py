import unittest
from crawler import crawler

class CrawlerTests(unittest.TestCase):

  def setUp(self):
    self.crawler = crawler(None, 'urls.txt')
    self.inverted_index = self.crawler.get_inverted_index()
    self.resolved_inverted_index = self.crawler.get_resolved_inverted_index()

  def test_inverted_is_not_empty(self):
      self.assertNotEqual(self.inverted_index, {})
      print "Inverted is not empty"

  def test_document_index_not_empty(self):
      self.assertNotEqual(self.crawler._doc_index, {})
      print "Document index is not empty"

  def test_resolved_inverted_is_not_empty(self):
      self.assertNotEqual(self.resolved_inverted_index, {})
      print "Resolved inverted index is not empty"

  def test_word_appeared_in_more_than_one_websites(self):
      self.assertTrue(len(self.resolved_inverted_index['latte'])  > 1)
      print "Word appeared in more than one websites contains more than 1 documents in its inverted index"

 
if __name__ == '__main__':   
    unittest.main()