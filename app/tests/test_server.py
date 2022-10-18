# -*- coding: utf-8 -*-
"""
Тесты для сервера

@author: asinadskiy
"""

from request_clf import server
import unittest, json


class TestServer(unittest.TestCase):

    def setUp(self):
        server.app.testing = True
        self.app = server.app.test_client()
        server.app.model_path = 'data/'

    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_predict_correct_data(self):
        """
        Проверяет корректность предсказания для конкретного запроса
        """
        data_json = json.dumps({"CLIENT_IP": "188.138.92.55",
                                "CLIENT_USERAGENT": "",
                                "REQUEST_SIZE": "166",
                                "RESPONSE_CODE": "404",
                                "MATCHED_VARIABLE_SRC": "REQUEST_URI",
                                "MATCHED_VARIABLE_NAME": "",
                                "MATCHED_VARIABLE_VALUE": "//tmp/20160925122692indo.php.vob",
                                "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu"})
        result = self.app.post('/predict',
                               headers={'Content-Type': 'application/json'},
                               data=data_json)
        self.assertEqual(result.text, '0')

    def test_predict_incorrect_data(self):
        """
        Проверяет, как сервер отвечает на данные в некорректном формате
        """
        data = '123'
        result = self.app.post('/predict', data=data)
        self.assertEqual(result.status_code, 415)

        
if __name__ == '__main__':
    unittest.main()