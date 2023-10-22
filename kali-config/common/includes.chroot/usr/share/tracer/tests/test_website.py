from tracer import Category, Result, Website
from asyncio import iscoroutine
import unittest


site = Website("www.example.com", "https://example.com/{}", Category.PROGRAMMING)


class TestWebsite(unittest.TestCase):
    def testCategory(self):
        self.assertEqual(site.category.as_number, Category.PROGRAMMING)

    def testSetUsername(self):
        site.set_username("idontexistandyouknowthat")
        self.assertEqual(site.username, "idontexistandyouknowthat", "Username didn't get set")

    def testURL(self):
        site.set_username('a')
        self.assertEqual(site.url, "https://example.com/a", "The username should be in the URL")

    def testSetResult(self):
        result = Result(site, 200, True, 5, "", "")
        site.set_result(result)

        self.assertIs(site.result, result, "'set_result' doesn't work")

    def testRequestCoro(self):
        self.assertTrue(iscoroutine(site.send_request(object)), "'send_request' should return a coro")


if __name__ == "__main__":
    unittest.main()
