import unittest

from lib.post import Post
from lib.post import PostLoader

class BasicPostTestCases(unittest.TestCase):

    def setUp(self):
        self.post = Post("This is a post", "http://google.com", 123)

    def testTitle(self):
        self.assertEqual(self.post.title, "This is a post") 

    def testUrl(self):
        self.assertEqual(self.post.url, "http://google.com")

    def testId(self):
        self.assertEqual(self.post.id, 123)


class PostTitleTests(unittest.TestCase):

    def testCapitalize(self):
        post = Post("TIL this is a Title", "http://google.com", 123)
        self.assertEqual(post.title, "This is a Title")

        post = Post("TIL this is a title", "http://google.com", 123)
        self.assertEqual(post.title, "This is a title")

    def testTILremoved(self):
        post = Post("TIL world is green", "http://google.com", 123)
        self.assertEqual(post.title, "World is green")

    def testTILcolonRemoved(self):
        post = Post("TIL: world is green", "http://google.com", 123)
        self.assertEqual(post.title, "World is green")

    def testThatRemoved(self):
        post = Post("TIL that The world is red", "http://google.com", 123)
        self.assertEqual(post.title, "The world is red")

    def testRemoveHypenFromTitle(self):
        post = Post("TIL - emperor hiron", "http://abc.def", 1)
        self.assertEqual(post.title, "Emperor hiron") 
        
    def testRemoveHypenFromTitleSpace(self):
        post = Post("TIL- emperor hiron", "http://abc.def", 1)
        self.assertEqual(post.title, "Emperor hiron")

    def testRemoveHypenFromTitleNoSpaces(self):
        post = Post("TIL-emperor hiron", "http://abc.def", 1)
        self.assertEqual(post.title, "Emperor hiron")         

class PostLoaderTestCases(unittest.TestCase):

    def setUp(self):
        self.loader = PostLoader("til")

    def testSubreditSet(self):
    	self.assertEqual(self.loader.url[-6:], "/r/til")

