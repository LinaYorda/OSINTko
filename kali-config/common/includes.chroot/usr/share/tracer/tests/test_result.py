from tracer import Result, Website
import unittest


attributes = {
    "website": Website("localhost", "http://localhost/{}", 0),
    "status_code": 200,
    "successfully": True,
    "delay": 4.75,
    "host": "localhost",
    "url": "http://localhost/tracer"
}


class TestResult(unittest.TestCase):
    def testDataRepresentation(self):
        result = Result(**attributes)

        self.assertIs(result.website, attributes["website"])
        self.assertEqual(result.status_code, attributes["status_code"])
        self.assertEqual(result.successfully, attributes["successfully"])
        self.assertEqual(result.delay, attributes["delay"])
        self.assertEqual(result.host, attributes["host"])
        self.assertEqual(result.url, attributes["url"])


if __name__ == "__main__":
    unittest.main()
