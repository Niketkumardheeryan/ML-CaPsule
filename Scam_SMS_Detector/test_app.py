import unittest
import json
from app import app

class ScamSMSDetectorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Scam SMS Detector', response.data)

    def test_predict_scam(self):
        payload = {
            'message': 'URGENT! Your bank account has been locked. Click http://bit.ly/verify to restore access.'
        }
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['is_scam'])
        self.assertEqual(data['prediction'], 'SCAM')

    def test_predict_safe(self):
        payload = {
            'message': 'Hey are we still meeting for lunch at 1pm today?'
        }
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertFalse(data['is_scam'])
        self.assertEqual(data['prediction'], 'SAFE')

    def test_empty_message(self):
        payload = {'message': ''}
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
