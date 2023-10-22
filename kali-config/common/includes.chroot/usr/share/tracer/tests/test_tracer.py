from tracer import Tracer
import unittest


data = [
    {
        "domain": "example.org",
        "url": "https://example.org/{}",
        "category": 1
    },
    {
        "domain": "example.com",
        "url": "http://example.com/user/{}",
        "category": 2
    },
    {
        "domain": "example.net",
        "url": "http://example.net/user/{}",
        "category": 2
    }
]


class TestTracer(unittest.TestCase):
    def testFiltering(self):
        tracer = Tracer("example", data, exclude=["example.org"])

        self.assertEqual(len(tracer.pool), 2)
        self.assertEqual(tracer.pool.sites[0].domain, "example.com")

        tracer = Tracer("example", data, only=["example.org"])

        self.assertEqual(len(tracer.pool), 1)
        self.assertEqual(tracer.pool.sites[0].domain, "example.org")


if __name__ == "__main__":
    unittest.main()
