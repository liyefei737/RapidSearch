import unittest
from crawler import crawler

class CrawlerTests(unittest.TestCase):

  def setUp(self):
    self.crawler = crawler(None, 'urls.txt')
    self.inverted_index = self.crawler.get_inverted_index()
    self.resolved_inverted_index = self.crawler.get_resolved_inverted_index()

  def test_inverted_is_not_empty(self):
      self.assertNotEqual(self.inverted_index, {})

  def test_word_appeared_in_more_than_one_websites(self):
      self.assertTrue(len(self.resolved_inverted_index['latte'])  > 1)

 
if __name__ == '__main__':   
    unittest.main()