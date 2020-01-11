# -*- coding: UTF-8 -*-
import unittest
import requests
"""
    tests - just python run_test.py.   these should prolly be flask tests but being basic
    drop and recreate the tables before running this
"""


class TestApp(unittest.TestCase):
    def test_missing_query(self):
        """
        missing parameter #1
        :return:
        """
        r = requests.get('http://localhost:5000/connections?fake=4')
        self.assertEqual(r.status_code, 400)

    def test_missing_value(self):
        """
        missing parameter #2
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=location_name')
        self.assertEqual(r.status_code, 400)

    def test_query_location_name(self):
        """
        test location_name
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=location_name&value=PDX')
        the_result = r.json()
        self.assertEqual(len(the_result["data"]), 2)

    def test_query_location_city(self):
        """
        test location_city
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=location_city&value=Portland')
        the_result = r.json()
        self.assertEqual(len(the_result["data"]), 2)

    def test_query_customer_name(self):
        """
        test customer_name
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=customer_name&value=Dunder%20Mifflin')
        the_result = r.json()
        self.assertEqual(len(the_result["data"]), 2)

    def test_query_connection_speed(self):
        """
        test connection speed
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=connection_speed&value=1G')
        the_result = r.json()
        self.assertEqual(len(the_result["data"]), 2)

    def test_query_connection_status(self):
        """
        test connection status
        :return:
        """
        r = requests.get('http://localhost:5000/connections?query=connection_status&value=active')
        the_result = r.json()
        self.assertEqual(len(the_result["data"]), 4)

    def test_post(self):
        """
        sort of test POST - just check return value
        :return:
        """
        post_data = {
          "description": "Test",
          "customer_id": 1,
          "location_id": 1
        }
        r = requests.post('http://localhost:5000/connection', json=post_data)
        self.assertEqual(r.status_code, 200)

    def test_404(self):
        """
        make sure does something sensible (i.e. - no wildcard handler)
        :return:
        """
        r = requests.get('http://localhost:5000/cats')
        self.assertEqual(r.status_code, 404)


if __name__ == '__main__':
    unittest.main()
