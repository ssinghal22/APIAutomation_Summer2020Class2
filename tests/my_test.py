import json
import unittest
import requests

class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response(self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)

class CareerPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    def test_login(self):
        positions = requests.get(self.base_url + '/positions')
        json_positions = json.loads(positions.text)

        self.assertEqual(5, len(json_positions))

        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        verify_header = {'Authorization': 'Bearer ' + token}
        verify_header.update(self.headers)

        verify_response = requests.post(self.base_url + '/verify', headers=verify_header)
        verify_content = json.loads(verify_response.content)

        auser_id = verify_content['id']
        aemail = verify_content['email']

        self.assertTrue('student@example.com' == aemail)
        self.assertEqual(8, auser_id)

        my_positions = requests.get(self.base_url + '/candidates/' + str(auser_id) + '/positions')
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(3, len(json_my_positions))


if __name__ == '__main__':
    unittest.main()
