# -*- coding: utf-8 -*-
"""
Тесты для клиента

@author: asinadskiy
"""

from request_clf import client
import unittest, json


url = 'http://127.0.0.1:5000/predict'
small_csv_file_path = 'data/part_10_small.csv'
big_csv_file_path = 'data/part_10.csv'


class TestClient(unittest.TestCase):

    def test_predict_one(self):
        """
        Проверяет работу предсказания для одной записи от клиента
        """
        data_json = json.dumps({"CLIENT_IP": "188.138.92.55",
                                "CLIENT_USERAGENT": "",
                                "REQUEST_SIZE": "166",
                                "RESPONSE_CODE": "404",
                                "MATCHED_VARIABLE_SRC": "REQUEST_URI",
                                "MATCHED_VARIABLE_NAME": "",
                                "MATCHED_VARIABLE_VALUE": "//tmp/20160925122692indo.php.vob",
                                "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu"})
        result = client.predict_one(url=url, data=data_json)
        self.assertEqual(result, '0')

    def test_predict_empty(self):
        """
        Проверяет работу предсказания для пустого JSON'а от клиента
        """
        data_json = json.dumps({"CLIENT_IP": "",
                                "CLIENT_USERAGENT": "",
                                "REQUEST_SIZE": "",
                                "RESPONSE_CODE": "",
                                "MATCHED_VARIABLE_SRC": "",
                                "MATCHED_VARIABLE_NAME": "",
                                "MATCHED_VARIABLE_VALUE": "",
                                "EVENT_ID": ""})
        result = client.predict_one(url=url, data=data_json)
        self.assertEqual(result, '0')

    def test_send_all_csv(self):
        """
        Проверяет работу предсказания для всех записей из файла для клиента
        """
        result = client.send_all_csv(url=url, csv_file_path=small_csv_file_path)
        self.assertEqual(result, ['0', '0'])

        
if __name__ == '__main__':
    unittest.main()



