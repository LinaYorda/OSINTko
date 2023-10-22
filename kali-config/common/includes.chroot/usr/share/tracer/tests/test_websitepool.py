from tracer import WebsitePool, Website
import unittest


pool = WebsitePool()


class TestWebsitePool(unittest.TestCase):
    def testAdding(self):
        site = Website("www.example.com", "", 10)
        pool.add(site)

        self.assertIn(site, pool, "Added website is not in the pool")

        pool.remove(lambda w: w is site)

        self.assertNotIn(site, pool, "Removed website is still in the pool")

    def testIterable(self):
        try:
            for _ in pool:
                ...
            self.assertTrue(True)
        except:
            self.fail("Pool is not iterable")

    def testSetName(self):
        name = "TestName"
        pool.set_name(name)

        self.assertEqual(pool.name, name, "Setting the name for the pool didn't work")

    def testSetUsername(self):
        pool.add(Website("www.example.com", "https://example.com/{}", 0))
        pool.set_username('tracerino')

        for website in pool:
            self.assertEqual(website.username, 'tracerino')

        pool.remove(lambda website: website.username == 'tracerino')


if __name__ == '__main__':
    unittest.main()
