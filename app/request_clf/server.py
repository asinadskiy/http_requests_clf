# -*- coding: utf-8 -*-
"""
Сервис для предсказания вредоносности HTTP-запроса

@author: asinadskiy
"""

from flask import Flask, request
from waitress import serve
import joblib


class ServerApp(Flask):

    count_vect = False
    tfidf_transformer = False
    clf_model = False
    model_path = 'data/'
    
    def load_model(self):
        """
        Загрузка необходимых для предсказания ML-моделей
        """
        self.count_vect = joblib.load(self.model_path + 'requests_count_vect.pkl')
        self.tfidf_transformer = joblib.load(self.model_path + 'requests_tfidf_transformer.pkl')
        self.clf_model = joblib.load(self.model_path + 'requests_model.pkl')
    
    def predict(self, x_data):
        """
        Предскзазание класса входных данных с использованием загруженных ML моделей

        Parameters
        ----------
        x_data : string
            Строка с данными, для которой нужно сделать предсказание.

        Returns
        -------
        y_pred : int
            Предсказанный класс: 0 - неопасный, 1 - опасный.
        """
        x_data_counts = self.count_vect.transform([x_data])
        x_data_tfidf = self.tfidf_transformer.transform(x_data_counts)
        y_pred = self.clf_model.predict(x_data_tfidf)
        return y_pred


app = ServerApp(__name__)


@app.route("/")
def home() :
    advertisement = "Это сервис для предсказания вредоносности HTTP-запросов.\n"
    advertisement += "Для предсказания отправьте на /predict POST-запрос с информацией о HTTP-запросе в формате JSON\n"
    advertisement += "В JSON обязательно должно быть поле MATCHED_VARIABLE_VALUE\n"
    return advertisement


@app.post("/predict")
def predict():
    if not (app.count_vect and app.tfidf_transformer and app.clf_model):
        app.load_model()

    if request.is_json:
        x_data = request.get_json()

        if 'MATCHED_VARIABLE_VALUE' not in x_data.keys():
            {"error": "Request JSON must have MATCHED_VARIABLE_VALUE field"}, 415

        x_data = x_data['MATCHED_VARIABLE_VALUE']
        y_pred = str(app.predict(x_data)[0])
        return y_pred, 201

    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':

    app.load_model()
    # app.count_vect = joblib.load(app.model_path + 'requests_count_vect.pkl')
    # app.tfidf_transformer = joblib.load('../data/requests_tfidf_transformer.pkl')
    # app.clf_model = joblib.load('../data/requests_model.pkl')

    serve(app, host="0.0.0.0", port=5000)
    # app.run(debug=True, port=5000)  # для отладки в при необходимости в будущем
