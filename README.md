# http_requests_clf

Веб-сервис для предсказания опасности HTTP-запросов.

Модель определяет, является ли полученный запрос вредоносным (класс "1") или нормальным (класс "0").

## Запуск

Для запуска веб-сервиса нужно, чтобы порт `5000` был свободен. Запускать можно или из Python, или с помощью Docker.

### Запуск из Python

Для запуска с Python перейти в папку `app` и запустить сервис командой `python request_clf/server.py`. Для остановки использовать `Ctrl-C` (если запущен не в фоновом режиме).

### Docker-образ

Для загрузки и запуска веб-сервиса из DockerHub'а:
`docker run -p 5000:5000 -d asinadskiy/request-clf-server`

Чтобы проверить - перейти на `http://127.0.0.1:5000/` в браузере или использовать `curl http://127.0.0.1:5000/`. В результате должно появиться текстовое сообщение.

Для остановки сервиса использовать `docker stop`.

Для сборки нового Docker-image (при необходимости) - перейти в папку `app` и выполнить команду `docker image build -t yourname/request-clf-server .`. После этого - запустить `docker run -p 5000:5000 -d asinadskiy/request-clf-server`

## Использование

Для того, чтобы сервис предсказал класс запроса, нужно передать ему JSON.

Пример в Python: `data` - сам запрос  
`url = 'http://127.0.0.1:5000/predict'`  
`headers = {'Content-Type': 'application/json'}`  
`label = requests.post(url, headers=headers, data=data).text`  
`print(label)`  

Пример содержания запроса:

`data = json.dumps({"CLIENT_IP": "188.138.92.55",`  
`                   "CLIENT_USERAGENT": "",`  
`                   "REQUEST_SIZE": "166",`  
`                   "RESPONSE_CODE": "404",`  
`                   "MATCHED_VARIABLE_SRC": "REQUEST_URI",`  
`                   "MATCHED_VARIABLE_NAME": "",`  
`                   "MATCHED_VARIABLE_VALUE": "//tmp/20160925122692indo.php.vob",`  
`                   "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu"})`  

При корректных входных данныех в ответе сервис передаст или значение `'0'` (не вредоносный), или значение `'1'` (вредоносный).

В файле `app/request_clf/client.py` описаны функции `predict_one` и `send_all_csv`. Их можно использовать для ускорения начала работы с сервисом.

## Тестирование

Перейти в папку `app` и запустить сервис командой `python request_clf/server.py` (или запустить Docker-контейнер).

Находясь в папке `app`, запустить тесты командой `python -m unittest discover -s tests`.